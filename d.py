import re, shutil

def tach_doan_giu_thut_le(xml_text):
    doan_1 = []
    for match in re.finditer(
        r'<Element var="Com" type="Assets\.Scripts\.GameLogic\.SkinElement">.*?</LookAt>',
        xml_text, re.DOTALL
    ):
        doan_1.append(xml_text[match.start():match.end()])

    doan_2 = []
    for match in re.finditer(
        r'<ArtPrefabLOD.*?<ArtSkinLobbyShowCamera.*?>',
        xml_text, re.DOTALL
    ):
        doan_2.append(xml_text[match.start():match.end()])

    return doan_1, doan_2
def loc_dong_rong(content):
    lines = content.splitlines(keepends=True)
    lines = [line for line in lines if line.strip() != ""]
    return "".join(lines)
def lay_doan(index_str, doan1, doan2):
    try:
        phan, idx = index_str.strip().split('[')
        idx = int(idx.replace(']', '')) - 1
        if phan == '1':
            return doan1[idx] if 0 <= idx < len(doan1) else None
        elif phan == '2':
            return doan2[idx] if 0 <= idx < len(doan2) else None
    except Exception:
        return None
    return None



# --- Bắt đầu chạy script ---

with open("Prefab_Hero/150_HanXin/150_HanXin_actorinfo1.xml", "r", encoding="utf-8") as f:
    content = f.read()

doan1, doan2 = tach_doan_giu_thut_le(content)

print("=== Đoạn 1 ===")
for i, d1 in enumerate(doan1):
    print(f"\n--- Đoạn 1 [{i+1}] ---\n{d1}")

print("\n=== Đoạn 2 ===")
for i, d2 in enumerate(doan2):
    print(f"\n--- Đoạn 2 [{i+1}] ---\n{d2}")

chuoi_bi_thay_list = input("\nNhập các đoạn bị thay : ").split()
chuoi_thay_the_list = input("Nhập các đoạn thay thế tương ứng: ").split()

if len(chuoi_bi_thay_list) != len(chuoi_thay_the_list):
    print("Lỗi: Số đoạn bị thay và đoạn thay thế không khớp.")
    exit()

content_thay_the = content

for bi_thay, thay_the in zip(chuoi_bi_thay_list, chuoi_thay_the_list):
    doan_bi_thay = lay_doan(bi_thay, doan1, doan2)
    doan_thay_the = lay_doan(thay_the, doan1, doan2)
    if doan_bi_thay is None:
        print(f"Lỗi: Không tìm thấy đoạn bị thay {bi_thay}")
        exit()
    if doan_thay_the is None:
        print(f"Lỗi: Không tìm thấy đoạn thay thế {thay_the}")
        exit()

    content_thay_the = content_thay_the.replace(doan_bi_thay, doan_thay_the)

# Thay thế thêm
thay_the_bytes = [
    ('<Element var="Com" type="Assets.Scripts.GameLogic.SkinElement">', ''),
    ('<ArtSkinPrefabLOD var="Array" type="System.String[]">', '<ArtPrefabLOD var="Array" type="System.String[]">'),
    ('</ArtSkinPrefabLOD>', '</ArtPrefabLOD>'),
    ('<ArtSkinPrefabLODEx var="Array" type="System.String[]">', '<ArtPrefabLODEx var="Array" type="System.String[]">'),
    ('</ArtSkinPrefabLODEx>', '</ArtPrefabLODEx>'),
    ('<ArtSkinLobbyShowLOD var="Array" type="System.String[]">', '<ArtLobbyShowLOD var="Array" type="System.String[]">'),
    ('</ArtSkinLobbyShowLOD>', '</ArtLobbyShowLOD>'),
    ('<ArtSkinLobbyIdleShowLOD var="Array" type="System.String[]">', '<ArtLobbyIdleShowLOD var="Array" type="System.String[]">'),
    ('</ArtSkinLobbyIdleShowLOD>', '</ArtLobbyIdleShowLOD>'),
]

for old, new in thay_the_bytes:
    content_thay_the = content_thay_the.replace(old, new, 1)
    content_thay_the = loc_dong_rong(content_thay_the)
with open("Prefab_Hero/150_HanXin/150_HanXin_actorinfo2.xml", "w", encoding="utf-8") as f:
    f.write(content_thay_the)

print("\n> Đã lưu nội dung mới vào: 150_HanXin/150_HanXin_actorinfo_sua.xml")