import re
import os
from colorama import init, Fore

init(autoreset=True)

def hexDump(raw):
    return ''.join(f"\\x{byte:02x}" for byte in raw)

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

def patch_block(block, id1, id2):
    id1_bytes = id1.to_bytes(2, 'little')
    id2_bytes = id2.to_bytes(2, 'little')
    block = block.replace(id1_bytes, id2_bytes)

    # 🔧 Lấy 2 số cuối của ID2 dạng thập phân
    last2 = int(str(id2)[-2:])  # vd: 15009 → 09 → int(9)

    # 🔍 Tìm _## và sửa 2 byte sau nó
    match = re.search(rb'_##.{2}', block)
    if match:
        patch_bytes = bytes([0, last2])  # \x00 + số cuối ID2
        block = block[:match.start()] + match.group(0)[:-2] + patch_bytes + block[match.end():]

    return block


# Đường dẫn file
dataPath = 'Actor/heroSkin.bytes'

if not os.path.exists(dataPath):
    print(f"{Fore.RED}[LỖI] Không tìm thấy file heroSkin.bytes{Fore.RESET}")
    exit()

with open(dataPath, "rb") as f:
    payload = bytearray(f.read())  # dùng bytearray để cho sửa được

print(f"{Fore.CYAN}Nhập ID Skin GỐC (ID1):{Fore.RESET}", end=' ')
id1 = int(input().strip())

print(f"{Fore.CYAN}Nhập ID Skin ĐÍCH (ID2):{Fore.RESET}", end=' ')
id2 = int(input().strip())

# Lấy block ID1 và ID2
start1, end1, block1 = get_block(payload, id1)
start2, end2, block2 = get_block(payload, id2)

if block1 is None or block2 is None:
    print(f"{Fore.RED}[!] Không tìm được block của ID1 hoặc ID2")
    exit()

# Patch block1 thành phù hợp với ID2
patched_block = patch_block(block1, id1, id2)

# Thay block2 bằng block đã sửa từ ID1
payload[start2:end2] = patched_block

# Ghi lại file mới
with open("Actor/heroSkin_patched.bytes", "wb") as f:
    f.write(payload)

print(f"{Fore.GREEN}[✓] Đã thay block ID {id2} bằng block từ ID {id1} và patch thành công!")
