import re
import os
from colorama import init, Fore

# Khởi tạo colorama để hỗ trợ màu sắc trên Windows
init(autoreset=True)

def hexDump(raw):
    return ''.join(f"\\x{byte:02x}" for byte in raw)

def textDump(raw, max_lines=10):
    output = ""
    line_count = 0
    for i, byte in enumerate(raw):
        if i % 64 == 0:
            if line_count >= max_lines:
                output += "\n[...]"
                break
            if i > 0:
                output += "\n"
            line_count += 1
        output += chr(byte) if 32 <= byte <= 126 else '.'
    return output

def analyzeSkin(data, skin_id):
    """Phân tích dữ liệu skin chi tiết"""
    print(f"\n{Fore.MAGENTA}[PHÂN TÍCH SKIN ID {skin_id}]{Fore.RESET}")

    # 1. Thông tin cơ bản
    print(f"\n{Fore.YELLOW}[1] Thông tin vị trí:{Fore.RESET}")
    print(f"- Kích thước: {len(data)} bytes")

    # 2. Hex dump dạng \x

    # 3. Các hash _##
    hashes = re.findall(rb'([A-Za-z0-9]{8,}_##)', data)
    if hashes:
        print(f"\n{Fore.GREEN}[3] Các hash _##:{Fore.RESET}")
        for h in set(hashes):
            print(f"- {h.decode('ascii', errors='ignore')}")

    # 4. Đường dẫn BG
    bg_paths = re.findall(rb'(BG_[^\x00]+)', data)
    if bg_paths:
        print(f"\n{Fore.CYAN}[4] Đường dẫn BG:{Fore.RESET}")
        for bg in set(bg_paths):
            print(f"- {bg.decode('ascii', errors='ignore')}")

    # 5. Ảnh Share
    share_imgs = re.findall(rb'(Share_[^\x00]+\.(?:jpg|png))', data)
    if share_imgs:
        print(f"\n{Fore.BLUE}[5] Ảnh Share:{Fore.RESET}")
        for img in set(share_imgs):
            print(f"- {img.decode('ascii', errors='ignore')}")

    # 6. Ảnh Skin
    skin_imgs = re.findall(rb'(Skin_[^\x00]+\.(?:jpg|png))', data)
    if skin_imgs:
        print(f"\n{Fore.BLUE}[6] Ảnh Skin:{Fore.RESET}")
        for img in set(skin_imgs):
            print(f"- {img.decode('ascii', errors='ignore')}")

    # 7. Model/Skill
    model_skill = re.findall(rb'(Skin_[A-Za-z]+_[^\x00]+)', data)
    if model_skill:
        print(f"\n{Fore.LIGHTBLUE_EX}[7] Model/Skill:{Fore.RESET}")
        for item in set(model_skill):
            decoded = item.decode('ascii', errors='ignore')
            if not decoded.endswith('.png') and not decoded.endswith('.jpg'):
                print(f"- {decoded}")

    # 8. Text dump
    print(f"\n{Fore.YELLOW}[8] Dạng text (rút gọn):{Fore.RESET}")
    # 8. Text dump (rút gọn) dạng readable + hex
    print(f"\n{Fore.YELLOW}[8] Dạng text (readable + hex):{Fore.RESET}")
    text = textDump(data)
    result = ''
    for byte in data:
        if 32 <= byte <= 126:
            result += chr(byte)
        else:
            result += f'\\x{byte:02x}'
    print(result)




# Đường dẫn file
dataPath = 'Actor/heroSkin.bytes'

# Kiểm tra file tồn tại
if not os.path.exists(dataPath):
    print(f"{Fore.RED}[LỖI] Không tìm thấy file heroSkin.bytes{Fore.RESET}")
    exit()

# Đọc file
try:
    with open(dataPath, "rb") as f:
        payload = f.read()
except Exception as e:
    print(f"{Fore.RED}[LỖI] Đọc file thất bại: {e}{Fore.RESET}")
    exit()

# Nhập ID skin
print(f"\n{Fore.CYAN}Nhập ID Skin :{Fore.RESET}", end=' ')
targetID = input().strip()

while targetID:
    try:
        targetInt = int(targetID)
    except:
        print(f"{Fore.RED}[!] ID không hợp lệ{Fore.RESET}")
        break

    # Tìm vị trí ID trong file
    id_bytes = targetInt.to_bytes(2, 'little')
    startAddr = payload.find(id_bytes)

    if startAddr == -1:
        print(f"{Fore.RED}[!] Không tìm thấy skin ID {targetID}{Fore.RESET}")
        break

    # Tìm điểm kết thúc
    endAddr = startAddr + 1
    for offset in range(targetInt + 1, targetInt + 100):
        next_id = offset.to_bytes(2, 'little')
        endAddr = payload.find(next_id, startAddr + 2)
        if endAddr != -1:
            break

    if endAddr == -1:
        endAddr = startAddr + 1  # fallback giới hạn

    scanZone = payload[max(startAddr - 4, 0):max(endAddr - 4, 0)]

    analyzeSkin(scanZone, targetID)

    # Tiếp tục vòng lặp
    print(f"\n{Fore.CYAN}Nhập ID Skin :{Fore.RESET}", end=' ')
    targetID = input().strip()
