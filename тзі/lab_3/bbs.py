import secrets
import math

# ---------- Утиліти перетворення текст <-> біти ----------
def text_to_bits(s):
    # LSB-first у байті: біт j має вагу 2^j
    return [(ord(c) >> i) & 1 for c in s for i in range(8)]

def bits_to_text(bits):
    out = []
    for i in range(0, len(bits), 8):
        byte = 0
        for j in range(8):
            if i + j < len(bits):
                byte |= (bits[i + j] << j)
        out.append(chr(byte))
    return ''.join(out)

def xor_bits(a, b):
    return [x ^ y for x, y in zip(a, b)]

# ---------- Завдання 1: Генератор BBS і потоковий шифр ----------
def is_probable_prime(n, k=40):
    if n < 2:
        return False
    # Сита малих простих
    small_primes = [2,3,5,7,11,13,17,19,23,29]
    for p in small_primes:
        if n == p:
            return True
        if n % p == 0:
            return n == p
    # Міллера-Рабіна
    d, r = n - 1, 0
    while d % 2 == 0:
        d //= 2; r += 1
    for _ in range(k):
        a = secrets.randbelow(n - 3) + 2
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True

def generate_blum_prime(bits=256):
    while True:
        candidate = secrets.randbits(bits) | 1
        candidate += (3 - candidate) % 4  # зробити ≡ 3 (mod 4)
        if is_probable_prime(candidate):
            return candidate

def bbs_init(bits=256):
    p = generate_blum_prime(bits)
    q = generate_blum_prime(bits)
    n = p * q
    # seed x0, взаємно простий з n
    while True:
        x0 = secrets.randbelow(n - 2) + 2
        if math.gcd(x0, n) == 1:
            return (p, q, n, x0)

def bbs_stream(n, x0, nbits, bit_mode="lsb"):
    """
    bit_mode: "lsb" -> x & 1; "byte" -> x & 0xFF повертає 8 біт за такт
    """
    x = x0
    if bit_mode == "lsb":
        for _ in range(nbits):
            x = pow(x, 2, n)
            yield x & 1
    elif bit_mode == "byte":
        for _ in range(nbits // 8 + (nbits % 8 != 0)):
            x = pow(x, 2, n)
            byte = x & 0xFF
            for i in range(8):
                yield (byte >> i) & 1
    else:
        raise ValueError("Unknown bit_mode")

# ---------- Завдання 2: LFSR для x^8 + x^6 + x^2 + 1 ----------
# Конвенція стану: [b7, b6, b5, b4, b3, b2, b1, b0], вихідний біт = b0, правий зсув
# Тапи (без старшого ступеня 8): 6, 2, 0 -> feedback = b6 ^ b2 ^ b0
def lfsr_step(state):
    b7,b6,b5,b4,b3,b2,b1,b0 = state
    feedback = b6 ^ b2 ^ b0
    output = b0
    new_state = [feedback, b7, b6, b5, b4, b3, b2, b1]
    return new_state, feedback, output

def lfsr_run(initial_state, steps):
    state = list(initial_state)
    rows = []
    for i in range(steps):
        new_state, f, out = lfsr_step(state)
        rows.append({
            "state_no": i,
            "state": state.copy(),
            "feedback": f,
            "output": out
        })
        state = new_state
    return rows

def print_lfsr_table(rows):
    print("Номер\tb7 b6 b5 b4 b3 b2 b1 b0\tf\tВихідний біт")
    for r in rows:
        bits = ' '.join(str(b) for b in r["state"])
        print(f'{r["state_no"]:>5}\t{bits}\t{r["feedback"]}\t{r["output"]}')

def lfsr_key_bits(initial_state, nbits):
    state = list(initial_state)
    stream = []
    for _ in range(nbits):
        state, f, out = lfsr_step(state)
        stream.append(out)
    return stream

def lfsr_period(initial_state):
    seen = {}
    state = tuple(initial_state)
    t = 0
    while state not in seen:
        seen[state] = t
        ns, _, _ = lfsr_step(list(state))
        state = tuple(ns)
        t += 1
    return t

# ---------- Демонстрація обох завдань ----------
if __name__ == "__main__":
    # ===== Завдання 1: BBS =====
    print("=== Завдання 1: BBS потоковий шифр ===")
    p, q, n, x0 = bbs_init(bits=128)  # можна 256 для реальності; 128 швидше для демо
    message = "HELLO"
    msg_bits = text_to_bits(message)
    key_bits = list(bbs_stream(n, x0, len(msg_bits), bit_mode="lsb"))
    cipher_bits = xor_bits(msg_bits, key_bits)
    # Дешифрування
    key_bits2 = list(bbs_stream(n, x0, len(msg_bits), bit_mode="lsb"))
    plain_bits = xor_bits(cipher_bits, key_bits2)
    print("Message:", message)
    print("Recovered:", bits_to_text(plain_bits))

    # ===== Завдання 2: LFSR =====
    print("\n=== Завдання 2: LFSR x^8 + x^6 + x^2 + 1 ===")
    initial = [1,0,0,1,0,1,0,1]  # будь-який не-нульовий стан [b7..b0]
    rows = lfsr_run(initial, steps=12)  # друк 12 станів як у фото
    print_lfsr_table(rows)
    print("Period (з цього стану, до повтору):", lfsr_period(initial))

    # Шифрування в Z2 ключем LFSR
    msg2 = "CRYPTO"
    msg2_bits = text_to_bits(msg2)
    lfsr_key = lfsr_key_bits(initial, len(msg2_bits))
    ct2 = xor_bits(msg2_bits, lfsr_key)
    # Дешифрування тим самим початковим станом
    lfsr_key2 = lfsr_key_bits(initial, len(msg2_bits))
    pt2 = xor_bits(ct2, lfsr_key2)
    print("Message2:", msg2)
    print("Recovered2:", bits_to_text(pt2))
