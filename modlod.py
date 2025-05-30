import os, glob

print('Tools Auto Infor by lluevty mod™')

MAX_SIZE = 10 * 1024 * 1024  # Giới hạn tối đa 10MB khi đọc

def _Mod_Infos(file1, file2, sau):
    # Đọc file nguồn chứa skin cần lấy
    with open(file2, "rb") as f:
        GT1 = f.read(92)[-4:]
        SkinPrefab = None
        for _ in range(int.from_bytes(GT1, 'little')):
            kb = f.read(4)
            size = int.from_bytes(kb, 'little')
            if size < 4 or size > MAX_SIZE:
                f.seek(size - 4, 1)
                continue
            Code = kb + f.read(size - 4)
            if b'SkinPrefab' in Code:
                SkinPrefab = Code

    if SkinPrefab is None:
        print(f"[!] Không tìm thấy 'SkinPrefab' trong {file2}")
        return

    Skin = b""
    with open('.kb', 'wb') as f1:
        f1.write(SkinPrefab)

    with open('.kb', 'rb') as f1:
        f1.read(8)
        f1.read(89)
        SL = int.from_bytes(f1.read(4), 'little')
        for _ in range(SL):
            kb = f1.read(4)
            size = int.from_bytes(kb, 'little')
            if size < 4 or size > MAX_SIZE:
                f1.seek(size - 4, 1)
                continue
            Code = kb + f1.read(size - 4)
            if (sau + "_").encode() in Code:
                Skin = Code
                break

    if not Skin:
        print(f"[!] Không tìm thấy ID Skin '{sau}' trong {file2}")
        return

    # Đọc file đích và thay skin
    with open(file1, "rb") as f:
        DauG = f.read(88)
        GT1 = f.read(4)
        CodeMD, CodeCuoi = b'', b''
        C, NameActor = 1, b''
        for i in range(int.from_bytes(GT1, 'little')):
            kb = f.read(4)
            size = int.from_bytes(kb, 'little')
            if size < 4 or size > MAX_SIZE:
                f.seek(size - 4, 1)
                continue
            Code = kb + f.read(size - 4)

            if C == 2:
                CodeCuoi += Code
            if b'SkinPrefab' in Code:
                SkinPrefab = Code
                C = 2
            if C == 0:
                CodeMD += Code
            if i == 0:
                NameActor = Code
                C = 0

    with open('.kb', 'wb') as f1:
        f1.write(SkinPrefab)

    with open('.kb', 'rb') as f1:
        GTC1 = f1.read(4)
        Dau = f1.read(89)
        GTC2 = f1.read(4)
        SL = f1.read(4)

    SkinMulti = Skin * int.from_bytes(SL, 'little')
    newSkinPrefab = (
        len(Dau[4:] + len(SL + SkinMulti).to_bytes(4, 'little') + SL + SkinMulti) + 8
    ).to_bytes(4, 'little') + Dau + (len(SL + SkinMulti) + 4).to_bytes(4, 'little') + SL + SkinMulti

    # Tạo Code mặc định
    CodeMD = b""
    with open('.kb', 'rb') as f1:
        f1.read(92)
        SL = int.from_bytes(f1.read(4), 'little')
        for _ in range(SL):
            kb = f1.read(4)
            size = int.from_bytes(kb, 'little')
            if size < 4 or size > MAX_SIZE:
                f1.seek(size - 4, 1)
                continue
            Code = kb + f1.read(size - 4)
            if b"LOD0" in Code or b"LODE\x780" in Code:
                Code = Code.replace(b"Skin", b"")
                Code = len(Code).to_bytes(4, 'little') + Code[4:]
                ii = (len(Code) - 4).to_bytes(4, 'little')
                Code = Code[:4] + ii + Code[8:]
            CodeMD += Code
            if Code[8:30].hex() == "5072656c6f6164416e696d61746f7245666665637473":
                break

    # Gộp lại thành file hoàn chỉnh
    new_total = DauG + GT1 + NameActor + CodeMD + newSkinPrefab + CodeCuoi
    SLN = 0
    dl2 = new_total[92:]

    while dl2:
        VT = dl2[:4]
        size = int.from_bytes(dl2[4:8], 'little')
        dl2 = dl2[int.from_bytes(VT, 'little'):]
        SLN += 1

    new_total = DauG + SLN.to_bytes(4, 'little') + NameActor + CodeMD + newSkinPrefab + CodeCuoi

    with open(file1, 'wb') as f:
        f.write(new_total)
    print(f"[+] Đã gắn skin {sau} vào {file1}")

# ===================== CHẠY =====================
k = input('\n1. Chế\n2. Thường\n________\nNhập: ')
skin_ids = input('\nNhập danh sách ID Skin: ').split()
hero_ids = input('Nhập ID Hero tương ứng (cách nhau bằng khoảng trắng): ').split()

if len(skin_ids) != len(hero_ids):
    print("Số lượng ID Skin và Hero không khớp.")
    exit()

for sau, truoc in zip(skin_ids, hero_ids):
    id1, id2 = truoc[:3], sau[:3]
    file1 = next((f for f in glob.glob(id1 + '*_actorinfo.bytes') if 'Tutorail' not in f), None)
    file2 = next((f for f in glob.glob(id2 + '*_actorinfo.bytes') if 'Tutorail' not in f), None)

    if not file1 or not file2:
        print(f"[!] Không tìm thấy file phù hợp cho Skin {sau} hoặc Hero {truoc}")
        continue

    _Mod_Infos(file1, file2, sau)
