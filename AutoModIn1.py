import os
import re
import sys
import getopt
import random
import pyzstd
import zipfile
from itertools import permutations
import shutil
from colorama import Fore
with open("ZSTD_DICT.xml", 'rb') as f:
    ZSTD_DICT = f.read()
ZSTD_LEVEL = 1

def giai(a):
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hcd", ["help", "compress", "decompress"])
    except getopt.GetoptError:
        sys.exit(1)

    for opt, arg in opts:
        if opt in ("-h", "--help"):
            sys.exit()

    if not args:
        args = [a]

    for path in args:
        if os.path.isdir(path):
            # Nếu là thư mục, duyệt tất cả các file bên trong (đệ quy nếu cần)
            for root, dirs, files in os.walk(path):
                for file in files:
                    file_path = os.path.join(root, file)
                    _giaima_file(file_path, opts)
        else:
            # Nếu là file đơn
            _giaima_file(path, opts)

def _giaima_file(filepath, opts):
    try:
        with open(filepath, "rb") as f:
            if b'"Jg' in f.read():
                return

        with open(filepath, "rb") as f:
            input_blob = f.read()

        if opts:
            opt, _ = opts[0]
        else:
            pos = input_blob.find(b"\x28\xb5\x2f\xfd")
            if pos != -1:
                opt = "-d"
                input_blob = input_blob[pos:]
            else:
                opt = "-c"

        zstd_mode = None
        anti = b''

        if opt in ("-c", "--compress"):
            zstd_mode = "compress"
            output_blob = bytearray(pyzstd.compress(input_blob, ZSTD_LEVEL, pyzstd.ZstdDict(ZSTD_DICT, True)))
            output_blob[0:0] = len(input_blob).to_bytes(4, byteorder="little", signed=False)
            output_blob[0:0] = b"\x22\x4a\x00\xef"
            anti += random.randbytes(0)
        elif opt in ("-d", "--decompress"):
            pos = input_blob.find(b"\x28\xb5\x2f\xfd")
            if pos == -1:
                return
            input_blob = input_blob[pos:]
            zstd_mode = "decompress"
            output_blob = pyzstd.decompress(input_blob, pyzstd.ZstdDict(ZSTD_DICT, True))

        with open(filepath, "wb") as output_file:
            output_file.write(output_blob)
        with open(filepath, "ab") as output_file:
            output_file.write(anti)
    except Exception as e:
        print(f"Lỗi giải file: {filepath} - {e}")
#-----------------------------------------------
SkinId = input(Fore.GREEN + "ID Bị Đè: ").split()
shutil.copy(f'Resources/1.58.1/Ages/Prefab_Characters/Prefab_Hero/Actor_{SkinId[0][:3]}_Actions.pkg.bytes',f'Actor_{SkinId[0][:3]}_Actions.pkg.bytes')
f = 'Actor_' + SkinId[0][:3] + '_Actions.pkg.bytes'
unique_dirs = set()

with zipfile.ZipFile(f, 'r') as zip_ref:
    zip_ref.extractall()
    for name in zip_ref.namelist():
        if 'imprint' in name.lower():
            continue
        relative_path = name.replace('root/', '', 1) if name.startswith('root/') else name
        dir_path = os.path.dirname(relative_path)
        if dir_path:
            unique_dirs.add(dir_path)
selected_dir = next(iter(unique_dirs)) if unique_dirs else None
if selected_dir:
    pass
folder_in1=selected_dir
giai(folder_in1)
folder = folder_in1
def store_folder(folder_in1, output_zip):
    with zipfile.ZipFile(output_zip, 'w', compression=zipfile.ZIP_STORED) as zipf:
        for root, _, files in os.walk(folder_in1):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, folder_in1)
                zipf.write(file_path, arcname)
def extract_namehero_from_file(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except UnicodeDecodeError:
        return None
    except Exception as e:
        print(f"Lỗi khi đọc file {filepath}: {e}")
        return None
    match = re.search(r'value="(?:[Pp]refab|prefab)_[Ss]kill_[Ee]ffects/[Hh]ero_[Ss]kill_[Ee]ffects/([^/"]+)', content)
    if match:
        return match.group(1)
    else:
        return None

def process_directory(directory):
    results = {}
    for filename in os.listdir(directory):
        filepath = os.path.join(directory, filename)
        if os.path.isfile(filepath):
            namehero = extract_namehero_from_file(filepath)
            if namehero:
                results[filename] = namehero
    return results
results = process_directory(folder)
for filename, namehero in results.items():
    pass
checkname=namehero
def Function_Track_Guid(folder):
    for file in os.listdir(folder):
        file_path = os.path.join(folder, file)
        with open(file_path, "rb") as r0:
            context = r0.read()
            Tracks = re.findall(rb'<Track trackName="(.*?)</Track>', context, re.DOTALL)
            if Tracks:
                for i in range(len(Tracks)):
                    trackName = Tracks[i]
                    guid_track = (re.findall(rb'guid="(.+?)" enabled', trackName)[0]).decode()
                    guid_true = str.encode(f'id="{i}" guid="{guid_track}"')
                    IdGuidFalse = re.findall(str.encode(rf'id="(.+?)" guid="{guid_track}"'), context)
                    if IdGuidFalse:
                        for j in range(len(IdGuidFalse)):
                            j = IdGuidFalse[j].decode()
                            guid_false = str.encode(f'id="{j}" guid="{guid_track}"')
                            context = context.replace(guid_false, guid_true)
        with open(file_path, "wb") as w0:
            w0.write(context)

def process_file(file_path, SkinId):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            text = f.read()
    except UnicodeDecodeError:
        return

    # ---Thêm SkinAvatarFilterType="11"---
    def add_skinavatar_attr(match):
        tag = match.group(0)
        if 'SkinAvatarFilterType=' not in tag:
            return tag[:-1] + ' SkinAvatarFilterType="11">'
        return tag

    text = re.sub(
        r'<Track[^>]*?(trackName="(PlayHero[^"]*|TriggerParticleTick[^"]*)"|eventType="TriggerParticle")[^>]*?>',
        add_skinavatar_attr,
        text
    )

    # ---Thêm SkinOrAvatarList---
    def insert_skin_list(match):
        block = match.group(0)
        indent = re.search(r'(\n[ \t]*)</Event>', block)
        indent = indent.group(1) if indent else '\n    '
        skin_lines = ''.join(f'{indent}<SkinOrAvatarList id="{i}" />' for i in SkinId)
        return re.sub(r'(</Event>)', r'\1' + skin_lines.rstrip(), block)

    text = re.sub(
        r'<Track[^>]*?(trackName="(PlayHero[^"]*|TriggerParticleTick[^"]*)"|eventType="TriggerParticle")[^>]*>.*?</Track>',
        insert_skin_list,
        text,
        flags=re.DOTALL
    )

    # --- B3: Xoá extraSkinId trong Event PlayHeroSoundTick ---
    lines = text.splitlines()
    processed_lines = []
    inside_event = False
    in_extraskin_block = False

    for line in lines:
        stripped = line.strip()
        if '<Event eventName="PlayHeroSoundTick"' in stripped:
            inside_event = True
        if '</Event>' in stripped and inside_event:
            inside_event = False
        if inside_event and '<Array name="extraSkinId"' in stripped and '/>' in stripped:
            continue
        if inside_event and '<Array name="extraSkinId"' in stripped and '/>' not in stripped:
            in_extraskin_block = True
            continue  
        if in_extraskin_block:
            if '</Array>' in stripped:
                in_extraskin_block = False
            continue

        processed_lines.append(line)
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(processed_lines))

def process_folder(folder_path, SkinId):
    for filename in os.listdir(folder_path):
        if filename.lower().endswith(".xml"):
            file_path = os.path.join(folder_path, filename)
            if not os.path.isfile(file_path):
                continue
            process_file(file_path, SkinId)
process_folder(folder, SkinId)
#-----------------------------------------------
id_skins = input('ID Skin:').split()
#id_heros = SkinId
namehero = checkname
if len(id_skins) != len(SkinId):
    print("Số lượng ID Skin và ID Hero không khớp.")
    exit()

path = folder

for filename in os.listdir(path):
    filepath = os.path.join(path, filename)
    if not os.path.isfile(filepath):
        continue

    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except UnicodeDecodeError:
        print(f"Bỏ qua file không đọc được utf-8: {filename}")
        continue

    tracks = re.findall(r'(^[ \t]*<Track trackName=".*?</Track>)', content, re.MULTILINE | re.DOTALL)
    new_tracks = []
    updated_content = content

    for track in tracks:
        track = re.sub(r'^[ \t]*<SkinOrAvatarList id="\d+"(?: heroId="\d+")? ?/>\n?', '', track, flags=re.MULTILINE)
        if 'SkinAvatarFilterType="11"' in track:
            track = track.replace('SkinAvatarFilterType="11"', 'SkinAvatarFilterType="9"')
        else:
            track = re.sub(
                r'(<Track\b[^>]*)(>)',
                lambda m: m.group(1) + ' SkinAvatarFilterType="9"' + m.group(2)
                if 'SkinAvatarFilterType=' not in m.group(1) else m.group(0),
                track,
                count=1
            )
        is_prefab = ('<String name="resourceName"' in track or '<String name="prefabName"' in track) \
                    and re.search(r'(?i)prefab_s', track) \
                    and re.search(r'(?i)kill_effects', track) \
                    and 'ui_fx' not in track \
                    and '<String name="resourceName" value=""' not in track \
                    and 'Indicator/AutoY"' not in track

        is_sound = ('<String name="eventName"' in track or '<String name="endEventName"' in track) \
                   and 'eventName" value=""' not in track

        if is_prefab or is_sound:
            indent_match = re.match(r'^([ \t]*)<Track', track)
            indent_track = indent_match.group(1) if indent_match else ''

            event_indent_match = re.search(r'^([ \t]*)</Event>', track, re.MULTILINE)
            indent_event = event_indent_match.group(1) if event_indent_match else indent_track + '  '

            for skin_id, hero_id in zip(id_skins, SkinId):
                mod_track = track
                if is_sound:
                    mod_track = re.sub(
                        r'(eventName" value="[^"]+?)(")',
                        lambda m: m.group(1) + f"_Skin{int(skin_id[-2:])}" + m.group(2),
                        mod_track
                    )
                if is_prefab:
                    def replace_resource_path(match):
                        full_tail = match.group(2)
                        return f'{match.group(1)}prefab_skill_effects/hero_skill_effects/{namehero}/{skin_id}/{full_tail}{match.group(3)}'

                    mod_track = re.sub(
                        r'(name="(?:resourceName|prefab)" value=")prefab_skill_effects/hero_skill_effects/[^/]+/([^"]+)(")',
                        replace_resource_path,
                        mod_track
                    )
                mod_track = re.sub(
                    r'(</Event>)',
                    r'\1\n' + indent_event + f'<SkinOrAvatarList id="{hero_id}" />',
                    mod_track
                )

                new_tracks.append(mod_track)

    if new_tracks:
        print(f"----- Xử lý file: {filename} -----")
        insert_block = '\n'.join(new_tracks) + '\n'
        print(insert_block)

        if '</Action>' in updated_content:
            action_indent_match = re.search(r'^([ \t]*)</Action>', updated_content, re.MULTILINE)
            action_indent = action_indent_match.group(1) if action_indent_match else ''
            updated_content = re.sub(r'^([ \t]*)</Action>', insert_block + action_indent + '</Action>', updated_content, flags=re.MULTILINE)
        elif '</Project>' in updated_content:
            project_indent_match = re.search(r'^([ \t]*)</Project>', updated_content, re.MULTILINE)
            project_indent = project_indent_match.group(1) if project_indent_match else ''
            updated_content = re.sub(r'^([ \t]*)</Project>', insert_block + project_indent + '</Project>', updated_content, flags=re.MULTILINE)
        else:
            updated_content += '\n' + insert_block

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(updated_content)

        print(f"Đã thêm các track mod vào file {filename}")
    
for filename in os.listdir(path):
    filepath = os.path.join(path, filename)
    if not os.path.isfile(filepath):
        continue
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            lines = [line for line in f if line.strip()]
        with open(filepath, 'w', encoding='utf-8') as f:
            f.writelines(lines)
    except UnicodeDecodeError:
        pass
    except PermissionError:
        print(f"Không có quyền xử lý file: {filename}")
    #giai(path)
    output_zip = 'Actor_'+SkinId[0][:3]+'_Actions.pkg.bytes'
    store_folder(folder_in1, output_zip)

# Danh sách màu sắc để tô màu kết quả
color_codes = [
    "#FF0000", "#00FF00", "#0000FF", "#FFD700", "#FFA500",
    "#800080", "#00FFFF", "#FFC0CB", "#8B4513", "#4B0082",
    "#7FFF00", "#DC143C", "#00CED1", "#FF69B4", "#ADFF2F", "#40E0D0"
]

def int_to_little_endian_bytes(value: int) -> bytes:
    return value.to_bytes(2, byteorder='little')

def bytes_to_hex_str(b: bytes) -> str:
    return b.hex().upper()

def read_bytes_file(path: str) -> bytes:
    with open(path, 'rb') as f:
        return f.read()

def read_text_file_lines(path: str) -> list:
    with open(path, 'r', encoding='utf-8') as f:
        return f.readlines()

# Sửa tên biến trong hàm này
def extract_skin_name(key: str, lang_files: list) -> str:
    for lang_file in lang_files:
        try:
            with open(lang_file, 'r', encoding='utf-8') as f:
                for line in f:
                    if key in line and '=' in line:
                        return line.split('=')[1].strip().title()
        except FileNotFoundError:
            print(f"[!] File {lang_file} không tồn tại.")
    return "Không Tìm Thấy"

def find_key_by_id(file_bytes: bytes, id_value: int) -> str:
    id_bytes = int_to_little_endian_bytes(id_value)
    offset = file_bytes.find(id_bytes)
    if offset == -1:
        return None
    hex_40 = file_bytes[offset + 40 : offset + 59]
    try:
        decoded_key = hex_40.decode('utf-8', errors='ignore').strip().replace('\x00', '')
        return decoded_key
    except:
        return None

def extract_ascii_before_id(filehero, target_id):
    sig = f"10{str(target_id)[:3]}".encode()
    with open(filehero, 'rb') as f:
        data = f.read()
    offset = data.find(sig)
    if offset == -1:
        print("[x] ID không tồn tại trong file.")
        return None
    else:
        extract = data[max(0, offset - 24):offset - 5].decode('utf-8', errors='replace')
        print("[*] ASCII Output:\n" + extract)
        return extract

def replace_line_content_with_mapping(filename, keyword, mappings):
    def colorize(mod, skin, color1, color2):
        return f"<color={color1}>{mod}</color> --> <color={color2}>{skin}</color>"

    color_pairs = list(permutations(color_codes, 2))
    random.shuffle(color_pairs)

    if len(mappings) > len(color_pairs):
        print("[!] Cảnh báo: Số cặp màu không đủ cho tất cả dòng, một số màu có thể bị trùng.")

    new_lines = []
    for i, (mod, skin) in enumerate(mappings):
        color1, color2 = color_pairs[i % len(color_pairs)]
        new_lines.append(colorize(mod, skin, color1, color2))

    new_text = "\\n".join(new_lines)

    with open(filename, 'r', encoding='utf-8', errors='replace') as f:
        lines = f.readlines()
    
    with open(filename, 'w', encoding='utf-8') as f:
        for line in lines:
            if line.startswith(keyword + " ="):
                line = f"{keyword} = {new_text}\n"
            f.write(line)

# ======== CHẠY CHƯƠNG TRÌNH ========
id_mods = SkinId

id_mods = [int(i.strip()) for i in id_mods]
id_skins = [int(i.strip()) for i in id_skins]
shutil.copy('Resources/1.58.1/Languages/VN_Garena_VN/languageMap_Xls.txt','VN_Garena_VN/languageMap_Xls.txt')
shutil.copy('Resources/1.58.1/Languages/VN_Garena_VN/languageMap_Newbie.txt', 'VN_Garena_VN/languageMap_Newbie.txt')
hero_bytes = giai(read_bytes_file('Resources/1.58.1/Databin/Client/Actor/heroSkin.bytes'))
lang_files = ['./VN_Garena_VN/languageMap_Xls.txt', './VN_Garena_VN/languageMap_Newbie.txt']  # <-- Sửa tên biến đúng
giai(lang_files)

mod_names, skin_names = [], []

for mod_id in id_mods:
    key = find_key_by_id(hero_bytes, mod_id)
    name = extract_skin_name(key, lang_files) if key else "Không Tìm Thấy"
    mod_names.append(name)

for skin_id in id_skins:
    key = find_key_by_id(hero_bytes, skin_id)
    name = extract_skin_name(key, lang_files) if key else "Không Tìm Thấy"
    print(f"Skin ID: {skin_id} -> Little Endian Hex: {bytes_to_hex_str(int_to_little_endian_bytes(skin_id))}")
    skin_names.append(name)

print("-" * 60)
mappings = []
for i in range(min(len(mod_names), len(skin_names))):
    print(f"{mod_names[i]} --> {skin_names[i]}")
    mappings.append((mod_names[i], skin_names[i]))

target_id = id_mods[0]
filehero = 'Resources/1.58.1/Languages/Databin/Client/Actor/hero.bytes'
ascii_key = extract_ascii_before_id(filehero, target_id)

if ascii_key:
    replace_line_content_with_mapping("languageMap_Xls.txt", ascii_key, mappings)
    print("[✓] Đã cập nhật nội dung thành công.")
giai(hero_bytes)
#-----------------------------------------------
'''H = SkinId[0:1]  # Chỉ lấy 1 ID đầu tiên
S = id_skins

if len(H) != 1 or len(S) == 0: exit("Lỗi: Phải nhập 1 HeroID và ≥1 SkinID")

M = dict(zip(S, H * len(S)))
D = 'Sound'

for F in os.listdir(D):
    P = os.path.join(D, F)
    try:
        T = open(P, 'rb').read().decode()
    except: continue

    for s, h in M.items():
        o = f'<Track SkinId="{s}"'
        n = f'<Track SkinId="{h}"'
        if o in T: print(f"[{F}] {s} → {h}")
        T = T.replace(o, n)

    open(P, 'wb').write(T.encode())

print("Done.")'''
files = ['ChatSound', 'BattleBank', 'HeroSound', 'LobbyBank', 'LobbySound']
os.makedirs('Sound', exist_ok=True)
[shutil.copy(f'Resources/1.58.1/Databin/Client/Sound/{f}.bytes', f'Sound/{f}.bytes') for f in files] 

giai('Sound')

H = SkinId[0]
S = id_skins
if not H or not S: exit("Thiếu ID")

def tohex(i): return int(i).to_bytes(2, 'little')
h = tohex(H)
D = 'Sound'

for F in os.listdir(D):
    P = os.path.join(D, F)
    try:
        d = open(P, 'rb').read()
    except: continue

    for s in S:
        s_hex = tohex(s)
        if s_hex in d:
            print(f"[{F}] {s_hex.hex()} → {h.hex()}")
            d = d.replace(s_hex, h)

    open(P, 'wb').write(d)

print(D+"Xong!")
#-----------------------------------------------
"""DS_ID1 = SkinId #input("Nhập các ID skin gốc (cách nhau bằng dấu cách): ").split()
DS_ID2 = S #input("Nhập các ID mod tương ứng (cách nhau bằng dấu cách): ").split()

if len(DS_ID1) != len(DS_ID2):
    print("Số lượng ID gốc và ID mod không khớp!")
    exit()

for i in range(len(DS_ID1)):
    ID_1, ID_2 = DS_ID2[i], DS_ID1[i]

    for file1 in FILES:
        if not os.path.exists(file1):
            print(f"File không tồn tại: {file1}")
            continue
        with open(file1, "rb") as f:
            data = f.read()


        DINH_DANG_1 = str(hex(int(ID_1)))[2:].zfill(4)
        #print(f"ID_1: {ID_1}, DINH_DANG_1 before slicing: {DINH_DANG_1}")
        DINH_DANG_1 = DINH_DANG_1[2:4] + DINH_DANG_1[0:2]
        #print(f"DINH_DANG_1 after slicing: {DINH_DANG_1}")
        DINH_DANG_1 = bytes.fromhex(DINH_DANG_1)

        DINH_DANG1 = str(hex(int(ID_1[:3])))[2:].zfill(4)
        #print(f"ID_1[:3]: {ID_1[:3]}, DINH_DANG1 before slicing: {DINH_DANG1}")
        DINH_DANG1 = DINH_DANG1[2:4] + DINH_DANG1[0:2]
        #print(f"DINH_DANG1 after slicing: {DINH_DANG1}")
        DINH_DANG1 = bytes.fromhex(DINH_DANG1)

        tt1 = ID_1[-2:]
        tt1 = int(tt1)
        hex_str = format(tt1, '02x')
        THU_TU_SKIN1 = bytes.fromhex(hex_str)

        DINH_DANG_1 = b'\x00\x00' + DINH_DANG_1 + b'\x00\x00' + DINH_DANG1

        code_SS = data.find(DINH_DANG_1)

        if code_SS != -1:
            start_index = max(0, code_SS - 2)
            end_index = code_SS
            CODE_TONG_1 = data[start_index:end_index]

            codetong1 = hex(int.from_bytes(CODE_TONG_1, byteorder='big'))[2:].zfill(4)
            if len(codetong1) == 5:
                codetong1 = codetong1[3:5] + "0" + codetong1[2:3]
            else:
                codetong1 = codetong1[2:4] + codetong1[0:2]
            codetong1 = int(codetong1, 16)

            BAT_DAU = code_SS
            KET_THUC = min(len(data), code_SS + codetong1 + 2)
            CODE_SKIN = data[BAT_DAU:KET_THUC]
            CODE_SKIN_1 = CODE_TONG_1 + CODE_SKIN
        else:
            print("ERROR")

        DINH_DANG_2 = str(hex(int(ID_2)))[2:].zfill(4)
        #print(f"ID_2: {ID_2}, DINH_DANG_2 before slicing: {DINH_DANG_2}")
        DINH_DANG_2 = DINH_DANG_2[2:4] + DINH_DANG_2[0:2]
        #print(f"DINH_DANG_2 after slicing: {DINH_DANG_2}")
        DINH_DANG_2 = bytes.fromhex(DINH_DANG_2)

        DINH_DANG2 = str(hex(int(ID_2[:3])))[2:].zfill(4)
        #print(f"ID_2[:3]: {ID_2[:3]}, DINH_DANG2 before slicing: {DINH_DANG2}")
        DINH_DANG2 = DINH_DANG2[2:4] + DINH_DANG2[0:2]
        #print(f"DINH_DANG2 after slicing: {DINH_DANG2}")
        DINH_DANG2 = bytes.fromhex(DINH_DANG2)

        tt1 = ID_2[-2:]
        tt1 = int(tt1)
        hex_str = format(tt1, '02x')
        THU_TU_SKIN2 = bytes.fromhex(hex_str)

        DINH_DANG_2 = b'\x00\x00' + DINH_DANG_2 + b'\x00\x00' + DINH_DANG2
        code_SS = data.find(DINH_DANG_2)

        if code_SS != -1:
            start_index = max(0, code_SS - 2)
            end_index = code_SS
            CODE_TONG_2 = data[start_index:end_index]

            codetong2 = hex(int.from_bytes(CODE_TONG_2, byteorder='big'))[2:].zfill(4)
            if len(codetong2) == 5:
                codetong2 = codetong2[3:5] + "0" + codetong2[2:3]
            else:
                codetong2 = codetong2[2:4] + codetong2[0:2]
            codetong2 = int(codetong2, 16)

            BAT_DAU = code_SS
            KET_THUC = min(len(data), code_SS + codetong2 + 2)
            CODE_SKIN = data[BAT_DAU:KET_THUC]
            CODE_SKIN_2 = CODE_TONG_2 + CODE_SKIN
        else:
            print("ERROR")

        Code_Full = CODE_SKIN_1.replace(DINH_DANG_1, DINH_DANG_2).replace(
            b'_##\x00' + THU_TU_SKIN1 + b'\x00\x00\x00\x14', b'_##\x00' + THU_TU_SKIN2 + b'\x00\x00\x00\x14')
        if ID_2[-2:] == "00":
            ID_1_S = int(ID_1[-2:])
            if ID_1_S < 10:
                ID_S1 = ID_1[:-2] + ID_1[-1]
                ID1 = '_##\x00\x07\x00\x00\x00' + '30' + ID_S1
            elif ID_1_S >= 10:
                ID1 = '_##\x00\x08\x00\x00\x00' + '30' + ID_1
            ID_2_S = int(ID_2[-2:])
            if ID_2_S < 10:
                ID_S2 = ID_2[:-2] + ID_2[-1]
                ID2 = '_##\x00\x07\x00\x00\x00' + '30' + ID_S2
            elif ID_2_S >= 10:
                ID2 = '_##\x00\x08\x00\x00\x00' + '30' + ID_2

            Code_Full = Code_Full.replace(ID1.encode(), ID2.encode()).replace(
                b'_##\x00\x01\x00\x00\x00' + b'\x00\x00', ID2.encode() + b'\x00\x00')

        codetong3 = hex(len(Code_Full) - 4)[2:].zfill(4)
        if len(codetong3) == 5:
            codetong3 = codetong3[3:5] + "0" + codetong3[2:3]
        else:
            codetong3 = codetong3[2:4] + codetong3[0:2]
        codetong3 = bytes.fromhex(codetong3)

        Code_Full = Code_Full.replace(CODE_TONG_1, codetong3)

        Code_Full1 = data.replace(CODE_SKIN_2, Code_Full)

        with open(file1, "wb") as file:
            file.write(Code_Full1)
        print(Code_Full1)"""
#-----------------------------------------------
for src, dst in [("Resources/1.58.1/Databin/Client/Actor/heroSkin.bytes", "Actor/heroSkin.bytes"),("Resources/1.58.1/Databin/Client/Shop/HeroSkinShop.bytes", "Shop/HeroSkinShop.bytes")]:
    os.makedirs(os.path.dirname(dst), exist_ok=True) 
    shutil.copy(src, dst)
giai("Actor/heroSkin.bytes")
giai("Shop/HeroSkinShop.bytes")
def mod_skin(ID, ID_1):
    if ID_1 == ID[0:3] + "00":
        Show = input("\n \033[1;36mShow name? (y/n): ")
    else:
        Show = "n"
    IDB = hex(int(ID))[2:6]
    IDB = bytes.fromhex(IDB[2:4] + IDB[0:2])
    IDC = hex(int(ID_1))[2:6]
    IDC = bytes.fromhex(IDC[2:4] + IDC[0:2])
    Files = ["Actor/heroSkin.bytes", "Shop/HeroSkinShop.bytes"]
    print("\033[1;36m\n" + "-" * 60)
    for File in Files:
        All = []
        All_S = []
        Skin = ""
        S = []
        with open(File, "rb") as file:
            Code = file.read(140)
            while True:
                Num = file.read(2)
                if Num == b"":
                    break
                Number = Num[0] + Num[1] * 256 + 2
                ND = file.read(Number)
                IDH = ND[6:8]
                IDH = IDH[0] + IDH[1] * 256
                Code += Num + ND
                S.append(Num + ND)
                if IDH == int(ID[0:3]):
                    if ND[2:4] == IDB:
                        Skin = Num + ND
                    All.append(Num + ND)
        if Skin == "":
            print("\n \033[1;31m The id couldn't be found in " + File + " file!")
            IDNew = input("\n\033[1;36m  Enter an alternate skin ID: ")
            IDK = hex(int(IDNew))[2:6]
            IDK = bytes.fromhex(IDK[2:4] + IDK[0:2])
            for i in S:
                if i.find(IDK) != -1:
                    Skin = i
                    break
        for id in All:
            if IDC in id:
                All_S.append(id)
        for Id in All_S:
            Cache = Skin.replace(Skin[4:6], Id[4:6], 1)
            Cache = Cache.replace(Cache[35:44], Id[35:44], 1)
            if Show == "y":
                if Id == Skin:
                    Cache = Cache.replace(Skin[35:44], b"\x00" * 5 + b"\x14" + b"\x00" * 3, 1)
                if Id == All[0]:
                    Cache = Cache.replace(Id[35:44], Skin[35:44], 1)
            if File == Files[0]:
                if Id == All[0]:
                    ID30 = b"\x07\x00\x00\x0030" + bytes(ID[0:3] + "0", "utf8") + b"\x00"
                    XYZ = Cache[64]
                    ID0 = Cache[64: 68 + XYZ]
                    Cache = Cache.replace(ID0, ID30, 1)
                    VT = Id.find(b"Hero_")
                    NumHero = Id[VT - 4]
                    Hero = Id[VT - 4: VT + NumHero]
                    Cache = Cache.replace(b"jpg\x00\x01\x00\x00\x00\x00", b"jpg\x00" + Hero)
                    Full = Cache.count(Hero)
                    if Full > 1:
                        Cache = Cache.replace(b"jpg\x00" + Hero, b"jpg\x00\x01\x00\x00\x00\x00", Full - 1)
                    EndTheCode = hex(len(Cache) - 4)
                    if len(EndTheCode) == 5:
                        EndTheCode = EndTheCode[3:5] + "0" + EndTheCode[2:3]
                    else:
                        EndTheCode = EndTheCode[4:6] + EndTheCode[2:4]
                    EndTheCode = bytes.fromhex(EndTheCode)
                    Cache = Cache.replace(Cache[0:2], EndTheCode)
            Code = Code.replace(Id, Cache)
        with open(File, "wb") as file:
            file.write(Code)
        print(Files)
ID_Skin = S #input("\033[1;32mEnter Skin: ").strip().split()
ID_Mod = SkinId #input("\033[1;32mEnter Id: ").strip().split()

if len(ID_Skin) != len(ID_Mod):
    print("Number of skin ids and replace ids must be the same!")
else:
    for ID, ID_1 in zip(ID_Skin, ID_Mod):
        mod_skin(ID, ID_1)

#-----------------------------------------------
def extract_two_unique_blocks(xml_content):
    result = []
    seen_resource_lines = set()
    lines = xml_content.splitlines()
    inside_track = False
    block = []
    current_resource_line = ""

    for line in lines:
        if not inside_track and '<Track trackName="TriggerParticle' in line:
            inside_track = True
            block = [line]
            current_resource_line = ""
        elif inside_track:
            if 'SkinOrAvatarList' in line:
                continue
            block.append(line)
            if '<String name="resourceName"' in line:
                current_resource_line = line.strip()
            if '</Track>' in line:
                if current_resource_line and current_resource_line not in seen_resource_lines:
                    result.append('\n'.join(block))
                    seen_resource_lines.add(current_resource_line)
                inside_track = False
                if len(result) == 2:
                    break
    return result

def remove_unwanted_lines(text):
    lines = text.splitlines()
    filtered_lines = []
    for line in lines:
        if ('<String name="parentResourceName"' in line or
            '<Enum name="ReplacementUsage"' in line or
            '<Enum name="ReplacementSubUsage"' in line):
            continue
        filtered_lines.append(line)
    return '\n'.join(filtered_lines)

def replace_resource_lines(text, namehero, skin_id, id_hero):
    text = text.replace(
        '<String name="resourceName" value="" refParamName="strReturnCityFall" useRefParam="true" />',
        f'<String name="resourceName" value="prefab_skill_effects/hero_skill_effects/{namehero}/{skin_id}/huijidi_01" refParamName="" useRefParam="false" />'
    )
    text = text.replace(
        '<String name="resourceName" value="" refParamName="strReturnCityEffectPath" useRefParam="true" />',
        f'<String name="resourceName" value="prefab_skill_effects/hero_skill_effects/{namehero}/{skin_id}/huicheng_tongyong_01" refParamName="" useRefParam="false" />'
    )

    # Thêm dòng <SkinOrAvatarList id="..." /> trước </Track>
    lines = text.splitlines()
    new_lines = []
    for line in lines:
        if line.strip() == '</Track>':
            new_lines.append(f'      <SkinOrAvatarList id="{id_hero}" />')
        new_lines.append(line)
    return '\n'.join(new_lines)

def insert_blocks_before_action_close(xml_content, blocks):
    lines = xml_content.splitlines()
    output = []
    inserted = False
    for line in lines:
        if not inserted and line.strip() == '</Action>':
            for block in blocks:
                output.extend(block.splitlines())
            inserted = True
        output.append(line)
    return '\n'.join(output)

id_heroes = SkinId#input("ID Hero : ").split()
skin_ids = id_skins#input("ID Skin: ").split()

if len(id_heroes) != len(skin_ids):
    print("Số lượng ID Hero và Skin không khớp!")
    exit()
with zipfile.ZipFile('Resources/1.58.1/Ages/Prefab_Characters/Prefab_Hero/CommonActions.pkg.bytes', 'r') as zipfileback:
    zipfileback.extractall('mod')
giai('mod/commonresource/Back.xml')
with open("mod/commonresource/Back.xml", "r", encoding="utf-8") as f:
    content = f.read()
base_blocks = extract_two_unique_blocks(content)

if len(base_blocks) < 2:
    print("Không tìm thấy đủ 2 block phù hợp để nhân bản.")
    exit()
final_blocks = []
for id_hero, skin_id in zip(id_heroes, skin_ids):
    for block in base_blocks:
        clean = remove_unwanted_lines(block)
        replaced = replace_resource_lines(clean, namehero, skin_id, id_hero)
        replaced = replaced.replace('SkinAvatarFilterType="11"', 'SkinAvatarFilterType="9"')
        final_blocks.append(replaced)
new_content = insert_blocks_before_action_close(content, final_blocks)
with open("mod/commonresource/Back.xml", "w", encoding="utf-8") as f:
    f.write(new_content)
print(new_content)
