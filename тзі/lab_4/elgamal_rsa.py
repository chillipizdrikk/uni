"""
elgamal_rsa.py
Реалізація Ель-Гамаля (генерація ключів, шифрування, розшифрування)
та RSA-підпису (генерація ключів, підпис, перевірка).
Підтримує CLI.
"""

import argparse
import secrets
import hashlib
import json
import math
import sys
from typing import List, Tuple

# ----------------------------
# Утиліти: великий простий, MR тест, інверсія
# ----------------------------

def is_probable_prime(n: int, k: int = 8) -> bool:
    """Miller-Rabin probabilistic primality test."""
    if n < 2:
        return False
    small_primes = [2,3,5,7,11,13,17,19,23,29]
    for p in small_primes:
        if n % p == 0:
            return n == p
    # write n-1 as d*2^s
    s = 0
    d = n - 1
    while d % 2 == 0:
        d //= 2
        s += 1
    for _ in range(k):
        a = secrets.randbelow(n - 3) + 2  # [2, n-2]
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(s - 1):
            x = (x * x) % n
            if x == n - 1:
                break
        else:
            return False
    return True

def generate_prime(bits: int) -> int:
    """Генерує просте число заданого розміру в бітах."""
    while True:
        # гарантуємо, що старший біт 1 і непарне
        p = secrets.randbits(bits) | (1 << (bits - 1)) | 1
        if is_probable_prime(p):
            return p

def egcd(a: int, b: int):
    if b == 0:
        return (a, 1, 0)
    g, x1, y1 = egcd(b, a % b)
    x = y1
    y = x1 - (a // b) * y1
    return (g, x, y)

def modinv(a: int, m: int) -> int:
    g, x, _ = egcd(a, m)
    if g != 1:
        raise ValueError("modular inverse does not exist")
    return x % m

def prime_factors(n: int) -> List[int]:
    """Досить просте розкладання на прості множники (для p-1, де p великий,
       досить шукати фактори малого розміру). Тут використовується простий підхід."""
    i = 2
    factors = set()
    while i * i <= n:
        if n % i == 0:
            factors.add(i)
            while n % i == 0:
                n //= i
        i += 1 if i == 2 else 2
    if n > 1:
        factors.add(n)
    return list(factors)

def find_primitive_root(p: int) -> int:
    """Знаходить примітивний корінь modulo p (p має бути простим)."""
    if p == 2:
        return 1
    phi = p - 1
    factors = prime_factors(phi)
    for g in range(2, p):
        ok = True
        for q in factors:
            if pow(g, phi // q, p) == 1:
                ok = False
                break
        if ok:
            return g
    raise RuntimeError("Не знайдено примітивного кореня")

# ----------------------------
# ElGamal: ключі, шифрування, розшифрування
# ----------------------------

def elgamal_keygen(p_bits: int = 2048):
    p = generate_prime(p_bits)
    g = find_primitive_root(p)
    a = secrets.randbelow(p - 2) + 1  # приватний ключ 1..p-2
    h = pow(g, a, p)
    return {"p": p, "g": g, "h": h, "a": a}

def _block_size_for_p(p: int) -> int:
    # знайдемо максимальний k: 256**k < p  => k * 8 < log2(p)
    k = (p.bit_length() - 1) // 8
    return max(1, k)

def bytes_to_int_blocks(b: bytes, block_size: int) -> List[int]:
    blocks = []
    for i in range(0, len(b), block_size):
        chunk = b[i:i+block_size]
        blocks.append(int.from_bytes(chunk, byteorder="big"))
    return blocks

def int_blocks_to_bytes(blocks: List[int], block_size: int) -> bytes:
    out = bytearray()
    for x in blocks:
        chunk = x.to_bytes(block_size, byteorder="big")
        out.extend(chunk)
    # strip possible leading zeros from last block?
    return bytes(out).rstrip(b'\x00')

def elgamal_encrypt_file(pub: dict, in_path: str, out_path: str):
    p = int(pub["p"])
    g = int(pub["g"])
    h = int(pub["h"])
    with open(in_path, "rb") as f:
        data = f.read()
    block_size = _block_size_for_p(p)
    blocks = bytes_to_int_blocks(data, block_size)
    ciphertext = []
    for m in blocks:
        if m >= p:
            raise ValueError("Блок >= p; збільшіть p або зменшіть розмір блоку")
        k = secrets.randbelow(p - 2) + 1
        c1 = pow(g, k, p)
        c2 = (m * pow(h, k, p)) % p
        ciphertext.append((str(c1), str(c2)))
    out = {"p": str(p), "g": str(g), "h": str(h), "block_size": block_size, "ciphertext": ciphertext}
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(out, f)
    print(f"Зашифровано {len(blocks)} блоків, записано у {out_path}")

def elgamal_decrypt_file(priv: dict, ciphertext_path: str) -> bytes:
    a = int(priv["a"])
    with open(ciphertext_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    p = int(data["p"])
    block_size = int(data.get("block_size", _block_size_for_p(p)))
    blocks = []
    for c1s, c2s in data["ciphertext"]:
        c1 = int(c1s); c2 = int(c2s)
        s = pow(c1, a, p)
        inv_s = modinv(s, p)
        m = (c2 * inv_s) % p
        blocks.append(m)
    plaintext = int_blocks_to_bytes(blocks, block_size)
    return plaintext

# ----------------------------
# RSA: ключі, підпис, перевірка
# ----------------------------

def rsa_keygen(p_bits: int = 1024, q_bits: int = 1024):
    p = generate_prime(p_bits)
    q = generate_prime(q_bits)
    while q == p:
        q = generate_prime(q_bits)
    n = p * q
    phi = (p - 1) * (q - 1)
    e = 65537
    if math.gcd(e, phi) != 1:
        # знайдемо інше e
        e = 3
        while math.gcd(e, phi) != 1:
            e += 2
    d = modinv(e, phi)
    return {"p": p, "q": q, "n": n, "e": e, "d": d}

def sha256_int_of_bytes(b: bytes) -> int:
    h = hashlib.sha256(b).digest()
    return int.from_bytes(h, byteorder="big")

def rsa_sign_file(priv: dict, in_path: str, out_path: str):
    d = int(priv["d"])
    n = int(priv["n"])
    with open(in_path, "rb") as f:
        data = f.read()
    h_int = sha256_int_of_bytes(data)
    # підпис — модульна степінь хешу
    sig = pow(h_int % n, d, n)
    out = {"n": str(n), "e": str(int(priv.get("e") or (int(priv.get('pub_e')) if 'pub_e' in priv else 65537))), "signature": str(sig)}
    # Замість очікування e в priv — краще згенерувати разом і зберегти e у pub/priv
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(out, f)
    print(f"Підпис збережено у {out_path}")

def rsa_verify_signature_file(signature_path: str, in_bytes: bytes) -> Tuple[bool, dict]:
    with open(signature_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    n = int(data["n"])
    e = int(data["e"])
    sig = int(data["signature"])
    h_int = sha256_int_of_bytes(in_bytes)
    verified = pow(sig, e, n) == (h_int % n)
    return verified, {"hash": str(h_int), "n": str(n), "e": str(e), "signature": str(sig)}

# ----------------------------
# Порожній main: CLI команди
# ----------------------------

def save_json_bigints(path: str, d: dict):
    # Перетворюємо всі int у str
    out = {}
    for k, v in d.items():
        if isinstance(v, int):
            out[k] = str(v)
        else:
            out[k] = v
    with open(path, "w", encoding="utf-8") as f:
        json.dump(out, f)

def load_json_bigints(path: str) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        raw = json.load(f)
    out = {}
    for k, v in raw.items():
        # якщо рядок складається тільки з цифр — розпарсимо
        if isinstance(v, str) and v.isdigit():
            out[k] = int(v)
        else:
            out[k] = v
    return out

def cmd_elgamal_gen_keys(args):
    keys = elgamal_keygen(p_bits=args.p_bits)
    pub = {"p": keys["p"], "g": keys["g"], "h": keys["h"]}
    priv = {"a": keys["a"]}
    save_json_bigints(f"{args.out_prefix}_pub.json", pub)
    save_json_bigints(f"{args.out_prefix}_priv.json", priv)
    print(f"ElGamal keys збережено: {args.out_prefix}_pub.json, {args.out_prefix}_priv.json")

def cmd_elgamal_encrypt(args):
    pub = load_json_bigints(args.pub)
    elgamal_encrypt_file(pub, args.infile, args.out)

def cmd_elgamal_decrypt(args):
    priv = load_json_bigints(args.priv)
    plaintext = elgamal_decrypt_file(priv, args.cipher)
    # напишемо у файл або виведемо
    if args.out:
        with open(args.out, "wb") as f:
            f.write(plaintext)
        print(f"Розшифрований текст збережено у {args.out}")
    else:
        sys.stdout.buffer.write(plaintext)

def cmd_rsa_gen_keys(args):
    keys = rsa_keygen(p_bits=args.p_bits, q_bits=args.q_bits)
    pub = {"n": keys["n"], "e": keys["e"]}
    priv = {"d": keys["d"], "n": keys["n"], "e": keys["e"]}
    save_json_bigints(f"{args.out_prefix}_pub.json", pub)
    save_json_bigints(f"{args.out_prefix}_priv.json", priv)
    print(f"RSA keys збережено: {args.out_prefix}_pub.json, {args.out_prefix}_priv.json")

def cmd_rsa_sign(args):
    priv = load_json_bigints(args.priv)
    rsa_sign_file(priv, args.infile, args.out)

def cmd_verify(args):
    # Зчитати зашифроване повідомлення та підпис
    elg_priv = load_json_bigints(args.elgamal_priv)
    # розшифрувати
    plaintext = elgamal_decrypt_file(elg_priv, args.ciphertext)
    # перевірити підпис
    verified, info = rsa_verify_signature_file(args.signature, plaintext)
    print("-----RESULT-----")
    if verified:
        print("Підпис вірний ✅")
    else:
        print("Підпис НЕВІРНИЙ ❌")
    print("Розшифроване повідомлення (utf-8):")
    try:
        print(plaintext.decode("utf-8"))
    except:
        print("<не UTF-8 байти> (виведено у шістнадцятковому вигляді):")
        print(plaintext.hex())

def build_parser():
    p = argparse.ArgumentParser(description="ElGamal + RSA-sign utilities")
    sub = p.add_subparsers(dest="cmd")

    # ElGamal gen keys
    g1 = sub.add_parser("elgamal-gen-keys", help="Generate ElGamal keypair")
    g1.add_argument("--p-bits", type=int, default=2048)
    g1.add_argument("--out-prefix", type=str, default="elgamal")
    g1.set_defaults(func=cmd_elgamal_gen_keys)

    # ElGamal encrypt
    g2 = sub.add_parser("elgamal-encrypt", help="Encrypt a file with ElGamal public key")
    g2.add_argument("--pub", required=True, help="ElGamal public JSON")
    g2.add_argument("--in", dest="infile", required=True, help="Input plaintext file")
    g2.add_argument("--out", required=True, help="Output ciphertext JSON")
    g2.set_defaults(func=cmd_elgamal_encrypt)

    # ElGamal decrypt
    g3 = sub.add_parser("elgamal-decrypt", help="Decrypt ElGamal ciphertext")
    g3.add_argument("--priv", required=True, help="ElGamal private JSON")
    g3.add_argument("--cipher", required=True, help="Ciphertext JSON")
    g3.add_argument("--out", required=False, help="Output plaintext file (if omitted -> stdout)")
    g3.set_defaults(func=cmd_elgamal_decrypt)

    # RSA gen keys
    g4 = sub.add_parser("rsa-gen-keys", help="Generate RSA keypair")
    g4.add_argument("--p-bits", type=int, default=1024)
    g4.add_argument("--q-bits", type=int, default=1024)
    g4.add_argument("--out-prefix", type=str, default="rsa")
    g4.set_defaults(func=cmd_rsa_gen_keys)

    # RSA sign
    g5 = sub.add_parser("rsa-sign", help="Sign a file using RSA private key")
    g5.add_argument("--priv", required=True, help="RSA private JSON")
    g5.add_argument("--in", dest="infile", required=True, help="Input file to sign")
    g5.add_argument("--out", required=True, help="Output signature JSON")
    g5.set_defaults(func=cmd_rsa_sign)

    # Verify (decrypt ElGamal + verify RSA signature)
    g6 = sub.add_parser("verify", help="Decrypt ElGamal ciphertext and verify RSA signature")
    g6.add_argument("--ciphertext", required=True, help="ElGamal ciphertext JSON")
    g6.add_argument("--elgamal-priv", required=True, help="ElGamal private JSON")
    g6.add_argument("--signature", required=True, help="Signature JSON (contains n,e,signature)")
    g6.set_defaults(func=cmd_verify)

    return p

def main():
    parser = build_parser()
    args = parser.parse_args()
    if not hasattr(args, "func"):
        parser.print_help()
        return
    args.func(args)

if __name__ == "__main__":
    main()