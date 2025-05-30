import re
import time
import os

def hexDump(raw):
    output = ""
    for byte in raw:
        output += chr(byte) if 32 <= byte <= 126 else f"\\x{byte:02x}"
    return output

def deepScan():
    dataPath = 'a/heroSkin2.bytes'
    if not os.path.exists(dataPath):
        printSlow("\033[91m[ERROR] Tệp heroSkin.bytes không tồn tại tại: ./a/\033[0m")
        return

    try:
        with open(dataPath, "rb") as bin:
            payload = bin.read()
    except Exception as err:
        printSlow(f"\033[91m[CRITICAL] Lỗi truy cập dữ liệu: {err}\033[0m")
        return

    targetID = input("\033[96m\n[INPUT] ID Skin : \033[0m").strip()
    try:
        targetInt = int(targetID)
    except:
        printSlow("\033[91m[!] ID không hợp lệ.\033[0m")
        return

    sigScan = targetInt.to_bytes(2, 'little')
    startAddr = payload.find(sigScan)

    if startAddr == -1:
        printSlow(f"\033[91m[!] Không tìm thấy ID {targetID} trong dữ liệu.\033[0m")
        return

    # Dò ID kế tiếp (tối đa +100 ID)
    for offset in range(targetInt + 1, targetInt + 100):
        nextSig = offset.to_bytes(2, 'little')
        endAddr = payload.find(nextSig, startAddr + 2)
        if endAddr != -1:
            break
    else:
        endAddr = len(payload)

    scanZone = payload[startAddr:endAddr]
    print(f"\n\033[93m[+] HEX DUMP: Segment của ID {targetID}\033[0m\n")
    print("\033[90m" + hexDump(scanZone) + "\033[0m")

    # Tìm pattern _##
    print("\n\033[95m[~] Pattern _## được phát hiện:\033[0m\n")
    patterns = list(re.finditer(rb'([A-Za-z0-9]{4,}_##)', scanZone))
    if patterns:
        for i, p in enumerate(patterns[:2]):
            pos = p.start()
            preview = scanZone[max(0, pos - 4):pos]
            rawMatch = p.group(1)
            print(f"\033[94m[+] ShowName:\033[0m {hexDump(preview)}\033[92m{rawMatch.decode(errors='ignore')}\033[0m")
    else:
        print("\033[91m[!] Không tìm thấy chuỗi _##\033[0m")

    # Tìm BG_
    print("\n\033[95m[~] Tìm pattern chứa 'BG_':\033[0m\n")
    bg_matches = list(re.finditer(rb'(BG_[^\x00]{2,})', scanZone))
    if bg_matches:
        for bg in bg_matches:
            idx = bg.start()
            before = scanZone[max(0, idx - 4):idx]
            after = scanZone[bg.end():bg.end()+1]
            full = before + bg.group(1) + after
            print(f"\033[96m[BG]:\033[0m {hexDump(full)}")
    else:
        print("\033[91m[!] Không tìm thấy chuỗi BG_\033[0m")

    # Tìm Share_SkinId.jpg
    print("\n\033[95m[~] Tìm pattern 'Share_SkinId.jpg':\033[0m\n")
    share_pattern = b'Share_' + targetID.encode('utf-8') + b'.jpg'
    share_matches = list(re.finditer(share_pattern, scanZone))
    if share_matches:
        for sm in share_matches:
            idx = sm.start()
            before = scanZone[max(0, idx - 4):idx]
            match = sm.group()
            after = scanZone[sm.end():sm.end()+1]
            full = before + match + after
            print(f"\033[93m[ShareImg]:\033[0m {hexDump(full)}")
    else:
        print("\033[91m[!] Không tìm thấy chuỗi 'Share_SkinId.jpg'\033[0m")

# Gọi hàm chính luôn
deepScan()
