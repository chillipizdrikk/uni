def f(r, k):
    """Спрощена функція f: XOR + циклічний зсув на 1 біт"""
    xor = r ^ k
    shifted = ((xor << 1) | (xor >> 7)) & 0xFF
    return shifted

def feistel_round(l, r, k):
    """Один раунд мережі Фейстеля"""
    new_l = r
    new_r = l ^ f(r, k)
    return new_l, new_r

def visualize_speed_encrypt(block, keys, rounds=4):
    """Шифрування з покроковою візуалізацією"""
    l = (block >> 8) & 0xFF
    r = block & 0xFF

    print("Початкові дані:")
    print(f"Відкритий текст (M): {bin(block)[2:].zfill(16)}")
    print(f"L0: {bin(l)[2:].zfill(8)}")
    print(f"R0: {bin(r)[2:].zfill(8)}")
    print("\nРаунди шифрування:")

    print(f"{'Раунд':<6} {'Ключ':<10} {'L (до)':<10} {'R (до)':<10} {'f(R,K)':<10} {'R ⊕ f':<10} {'L (після)':<12} {'R (після)':<12}")
    print("-" * 80)

    for i in range(rounds):
        key = keys[i % len(keys)]
        l_before, r_before = l, r
        f_val = f(r_before, key)
        r_xor_f = l_before ^ f_val
        l, r = feistel_round(l_before, r_before, key)
        print(f"{i+1:<6} {bin(key)[2:].zfill(8):<10} {bin(l_before)[2:].zfill(8):<10} {bin(r_before)[2:].zfill(8):<10} {bin(f_val)[2:].zfill(8):<10} {bin(r_xor_f)[2:].zfill(8):<10} {bin(l)[2:].zfill(8):<12} {bin(r)[2:].zfill(8):<12}")

    final_block = (l << 8) | r
    print("\nЗашифрований блок (C):", bin(final_block)[2:].zfill(16))
    return final_block

# 🔧 Вхідні дані
plaintext = 0b1010101011110000  # 16-бітний блок
keys = [0b11001100, 0b00110011, 0b11110000, 0b00001111]  # 4 підключі

# 🚀 Запуск з візуалізацією
ciphertext = visualize_speed_encrypt(plaintext, keys)
