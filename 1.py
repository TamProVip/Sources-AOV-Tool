import re
import os
from colorama import init, Fore

init(autoreset=True)

def get_block(payload, skin_id):
    id_bytes = skin_id.to_bytes(2, 'little')
    startAddr = payload.find(id_bytes)
    if startAddr == -1:
        return None, None, None

    endAddr = startAddr + 1
    for offset in range(skin_id + 1, skin_id + 100):
        next_id = offset.to_bytes(2, 'little')
        endAddr = payload.find(next_id, startAddr + 2)
        if endAddr != -1:
            break

    if endAddr == -1:
        endAddr = startAddr + 1

    start_block = max(startAddr - 4, 0)
    end_block = max(endAddr - 4, 0)
    return start_block, end_block, payload[start_block:end_block]

def patch_block(block, id1, id2, replace_30id=True):
    id1_bytes = id1.to_bytes(2, 'little')
    id2_bytes = id2.to_bytes(2, 'little')
    block = block.replace(id1_bytes, id2_bytes)

    if replace_30id:
        def clean_id(ID):
            ID = str(ID)
            last2 = int(ID[-2:])
            if 0 <= last2 <= 9:
                ID = ID[:-1]  # bỏ 1 số 0 nếu hai số cuối là 00–09
            return ID

        pattern = re.search(rb'30\d{4,7}', block)
        if pattern:
            id1_str_real = pattern.group(0)
            id2_str_clean = f"30{clean_id(id2)}".encode()
            block = block.replace(id1_str_real, id2_str_clean, 1)

    # Thay byte sau _##
    match = re.search(rb'_##.{2}', block)
    if match:
        last2 = int(str(id2)[-2:])
        patch_bytes = bytes([0, last2])
        block = block[:match.start()] + match.group(0)[:-2] + patch_bytes + block[match.end():]

    return block

# -------------------- MAIN --------------------

dataPath = 'Actor/heroSkin.bytes'
output_path = "Actor/heroSkin_patched.bytes"

if not os.path.exists(dataPath):
    print(f"{Fore.RED}[LỖI] Không tìm thấy file heroSkin.bytes{Fore.RESET}")
    exit()

with open(dataPath, "rb") as f:
    payload = bytearray(f.read())

already_patched_30id = False  # Chỉ patch 30xxxx lần đầu

while True:
    print(f"\n{Fore.CYAN}Nhập ID Skin GỐC (ID1) (Enter để thoát):{Fore.RESET}", end=' ')
    id1_input = input().strip()
    if not id1_input:
        break

    print(f"{Fore.CYAN}Nhập ID Skin ĐÍCH (ID2):{Fore.RESET}", end=' ')
    id2_input = input().strip()
    if not id2_input:
        break

    try:
        id1 = int(id1_input)
        id2 = int(id2_input)
    except ValueError:
        print(f"{Fore.RED}[!] ID không hợp lệ!{Fore.RESET}")
        continue

    start1, end1, block1 = get_block(payload, id1)
    start2, end2, block2 = get_block(payload, id2)

    if block1 is None or block2 is None:
        print(f"{Fore.RED}[!] Không tìm thấy block của ID1 hoặc ID2{Fore.RESET}")
        continue

    patched_block = patch_block(block1, id1, id2, replace_30id=not already_patched_30id)
    already_patched_30id = True  # Sau lần đầu thì không thay "30xxx" nữa

    payload[start2:end2] = patched_block

    print(f"{Fore.GREEN}[✓] Đã thay block ID {id2} bằng block từ ID {id1} và patch thành công!")

# Ghi file sau khi hoàn tất
with open(output_path, "wb") as f:
    f.write(payload)

print(f"{Fore.YELLOW}[→] File ghi ra: {output_path}{Fore.RESET}")
