import os; import re; import getopt; import random; import pyzstd; import xml.dom.minidom; from colorama import Fore; import sys; import shutil; import zipfile; import uuid

with open("ZSTD_DICT.xml", 'rb') as f:
    ZSTD_DICT = f.read()
ZSTD_LEVEL = 1

def giai(a):
    if os.path.isdir(a):
        for root, dirs, files in os.walk(a):
            for file in files:
                file_path = os.path.join(root, file)
                _giaima_file(file_path)
    else:
        _giaima_file(a)

def _giaima_file(filepath):
    try:
        if not os.path.isfile(filepath):
            return

        with open(filepath, "rb") as f:
            input_blob = f.read()

        # Nếu đã giải mã (ví dụ có XML), thì bỏ qua
        if b'"Jg' in input_blob or b"<?xml" in input_blob:
            return

        # Nếu là file nén ZSTD
        pos = input_blob.find(b"\x28\xb5\x2f\xfd")
        if pos != -1:
            anti_pos = input_blob.rfind(b'ANTI_DECOMP__')
            if anti_pos != -1:
                input_blob = input_blob[:anti_pos]

            if input_blob.startswith(b"\x22\x4a\x00\xef"):
                input_blob = input_blob[8:]

            input_blob = input_blob[input_blob.find(b"\x28\xb5\x2f\xfd"):]
            output_blob = pyzstd.decompress(input_blob, pyzstd.ZstdDict(ZSTD_DICT, True))

            with open(filepath, "wb") as f:
                f.write(output_blob)
        else:
            print(f"❌ Không phải file ZSTD: {filepath}")

    except Exception as e:
        print(f"⚠️ Lỗi giải file: {filepath} - {e}")

def process_input_numbers(numbers):
    results = []
    for number in numbers:
        number_str = str(number)
        if len(number_str) == 5:
            results.append(number - 1)
        elif len(number_str) == 4:
            results.append(int(number_str[:-1] + "0" + number_str[-1]) - 1)
        else:
            print(f"Số {number} không hợp lệ. Vui lòng nhập số có 4 hoặc 5 chữ số.")
            return None
    return results

input_numbers = input('\n\t' + "ID: ")
AABBCC = input('\n\t Nhập Nguồn :')
numbers = [int(num) for num in input_numbers.split()]
results = process_input_numbers(numbers)

if results is None:
    sys.exit()
result_str = ' '.join(map(str, results))
IDD = result_str
IDMODSKIN = IDD.split()
IDMODSKIN1 = IDD.split()
print(IDMODSKIN1)

if len(IDMODSKIN1) == 1:
    print(Fore.RED + "Chỉ 1 ID được nhập vào. Tool sẽ thoát." + Fore.RESET)
    sys.exit()

DANHSACH = IDD.split()

with open(f'Resources/1.58.1/Databin/Client/Actor/heroSkin.bytes', 'rb') as f:
    a = f.read()
if b'"J\x00' in a:
    giai(f'Resources/1.58.1/Databin/Client/Actor/heroSkin.bytes')

FILES_MAP = [
    f'Resources/1.58.1/Languages/VN_Garena_VN/languageMap.txt',
    f'Resources/1.58.1/Languages/VN_Garena_VN/languageMap_Newbie.txt',
    f'Resources/1.58.1/Languages/VN_Garena_VN/languageMap_WorldConcept.txt',
    f'Resources/1.58.1/Languages/VN_Garena_VN/languageMap_Xls.txt',
    f'Resources/1.58.1/Languages/VN_Garena_VN/lanMapIncremental.txt'
]

for mapp in FILES_MAP:
    with open(mapp, 'rb') as f:
        a = f.read()
    if b'"J\x00' in a:
        giai(mapp)

TENSKIN = []
for mapp in FILES_MAP:
    for i in DANHSACH:
        with open(mapp, 'rb') as f:
            rpl = f.read()
        with open(f'Resources/1.58.1/Databin/Client/Actor/heroSkin.bytes', 'rb') as f:
            RPL = f.read()

        i = int(i)
        IDFIND = RPL.find(i.to_bytes(4, 'little') + int(str(i)[:3]).to_bytes(4, 'little'))
        if IDFIND != -1:
            try:
                VT = RPL[IDFIND + 12:IDFIND + 31]
                VT1 = rpl.find(VT)
                VT2 = rpl.find(b'\r', VT1)
                VTR = rpl[VT1:VT2]

                VT = RPL[IDFIND + 40:IDFIND + 59]
                VT1 = rpl.find(VT)
                VT2 = rpl.find(b'\r', VT1)
                VTR_SKIN = rpl[VT1:VT2]

                A = VTR[22:]
                B = VTR_SKIN[22:]
                pack_name = ((A + b' ' + B).decode(errors='ignore'))
                pack_name = ''.join(char for char in pack_name if char not in ['/', '\\', ':', '*', '?', '"', '<', '>', '|'])

                if pack_name.strip() != '' and '[ex]' not in pack_name:
                    TENSKIN.append(pack_name)
            except:
                continue 
aaabbbcccnnn = ''
for pack_name in TENSKIN:
    #print(pack_name)
    aaabbbcccnnn = pack_name
    ten_final = pack_name

print(Fore.YELLOW + '-' * 50 + Fore.RESET)
if len(DANHSACH) > 1:
    pack_name = input("Nhập Tên Pack Skin: ")
    os.mkdir(pack_name)
    with open('pack.txt', 'w', encoding='utf8') as f:
        f.write(pack_name)
    base_path = f"{pack_name}/Resources/1.58.1/Databin/Client/"
    directories = ["Actor", "Shop", "Sound", "Skill", "Character", "Motion", "Global"]
    for directory in directories:
        os.makedirs(os.path.join(base_path, directory))
else:
    pass
#-----------------------------------------------
file_actor = "Resources/1.58.1/Databin/Client/Actor/heroSkin.bytes"
file_actor_mod = f"{pack_name}/Resources/1.58.1/Databin/Client/Actor/heroSkin.bytes"
shutil.copy(file_actor, file_actor_mod)
#giai(file_actor_mod)

file_shop = "Resources/1.58.1/Databin/Client/Shop/HeroSkinShop.bytes"
file_shop_mod = f"{pack_name}/Resources/1.58.1/Databin/Client/Shop/HeroSkinShop.bytes"
shutil.copy(file_shop, file_shop_mod)
giai(file_shop_mod)

file_sound1 = "Resources/1.58.1/Databin/Client/Sound/BattleBank.bytes"
file_sound_mod1 = f"{pack_name}/Resources/1.58.1/Databin/Client/Sound/BattleBank.bytes"
shutil.copy(file_sound1, file_sound_mod1)
giai(file_sound_mod1)

file_sound2 = "Resources/1.58.1/Databin/Client/Sound/ChatSound.bytes"
file_sound_mod2 = f"{pack_name}/Resources/1.58.1/Databin/Client/Sound/ChatSound.bytes"
shutil.copy(file_sound2, file_sound_mod2)
giai(file_sound_mod2)

file_sound3 = "Resources/1.58.1/Databin/Client/Sound/HeroSound.bytes"
file_sound_mod3 = f"{pack_name}/Resources/1.58.1/Databin/Client/Sound/HeroSound.bytes"
shutil.copy(file_sound3, file_sound_mod3)
giai(file_sound_mod3)

file_sound4 = "Resources/1.58.1/Databin/Client/Sound/LobbyBank.bytes"
file_sound_mod4 = f"{pack_name}/Resources/1.58.1/Databin/Client/Sound/LobbyBank.bytes"
shutil.copy(file_sound4, file_sound_mod4)
giai(file_sound_mod4)

file_sound5 = "Resources/1.58.1/Databin/Client/Sound/LobbySound.bytes"
file_sound_mod5 = f"{pack_name}/Resources/1.58.1/Databin/Client/Sound/LobbySound.bytes"
shutil.copy(file_sound5, file_sound_mod5)
giai(file_sound_mod5)

Sound_Files = f"{pack_name}/Resources/1.58.1/Databin/Client/Sound"

file_skill1 = "Resources/1.58.1/Databin/Client/Skill/liteBulletCfg.bytes"
file_mod_skill1 = f"{pack_name}/Resources/1.58.1/Databin/Client/Skill/liteBulletCfg.bytes"
shutil.copy(file_skill1, file_mod_skill1)
giai(file_mod_skill1)

file_skill2 = "Resources/1.58.1/Databin/Client/Skill/skillmark.bytes"
file_mod_skill2 = f"{pack_name}/Resources/1.58.1/Databin/Client/Skill/skillmark.bytes"
shutil.copy(file_skill2, file_mod_skill2)
giai(file_mod_skill2)

file_Character = "Resources/1.58.1/Databin/Client/Character/ResCharacterComponent.bytes"
file_mod_Character = f"{pack_name}/Resources/1.58.1/Databin/Client/Character/ResCharacterComponent.bytes"
shutil.copy(file_Character, file_mod_Character)
giai(file_mod_Character)

file_Modtion = "Resources/1.58.1/Databin/Client/Motion/ResSkinMotionBaseCfg.bytes"
file_mod_Modtion = f"{pack_name}/Resources/1.58.1/Databin/Client/Motion/ResSkinMotionBaseCfg.bytes"
shutil.copy(file_Modtion, file_mod_Modtion)
giai(file_mod_Modtion)

file_vien = "Resources/1.58.1/Databin/Client/Global/HeadImage.bytes"
file_mod_vien = f"{pack_name}/Resources/1.58.1/Databin/Client/Global/HeadImage.bytes"
shutil.copy(file_vien, file_mod_vien)
giai(file_mod_vien)

with zipfile.ZipFile('Resources/1.58.1/Ages/Prefab_Characters/Prefab_Hero/CommonActions.pkg.bytes') as zipf:
    zipf.extractall(f'{pack_name}/Resources/1.58.1/Ages/Prefab_Characters/Prefab_Hero/mod1/')
    giai(f'{pack_name}/Resources/1.58.1/Ages/Prefab_Characters/Prefab_Hero/mod1/commonresource/Back.xml')
#-----------------------------------------------
FILES = [file_actor_mod, file_shop_mod]

for IDCHECK in IDMODSKIN:
    ID = IDCHECK
    Show = 'n'
    IDB = int(ID).to_bytes(4, 'little')
    IDH = int(ID[0:3]).to_bytes(4, 'little')

    for File in FILES:
        with open(File, "rb") as file:
            Code = file.read()

        All = []
        Skin = b""
        Find = -10
        while True:
            Find = Code.find(b"\x00\x00" + IDH, Find + 10)
            if Find == -1:
                break
            elif str(int.from_bytes(Code[Find - 2:Find], 'little'))[:3] == ID[:3]:
                VT2 = int.from_bytes(Code[Find - 6:Find - 4], 'little')
                Code2 = Code[Find - 6:Find - 6 + VT2]
                All.append(Code2)
                if IDB in Code2:
                    Skin = Code2

        if not Skin:
            print(Fore.RED + f"\nKhông tìm thấy ID trong file {File}" + Fore.RESET)
            IDNew = input(Fore.CYAN + "\nNhập ID thay thế: " + Fore.RESET)
            IDK = int(IDNew).to_bytes(4, 'little')
            IDH2 = int(IDNew[0:3]).to_bytes(4, 'little')
            Find = Code.find(IDK + IDH2)
            Sum = int.from_bytes(Code[Find - 4:Find - 2], 'little')
            Skin = Code[Find - 4:Find - 4 + Sum]

        for Id in All:
            Cache = Skin.replace(Skin[4:6], Id[4:6], 1)
            Cache = Cache.replace(Cache[35:44], Id[35:40] + Cache[40:44], 1)

            if Show == "y":
                if Id == Skin:
                    Cache = Cache.replace(Skin[35:44], b"\x00" * 5 + b"\x14" + b"\x00" * 3, 1)
                if Id == All[0]:
                    Cache = Cache.replace(Id[35:44], Skin[35:44], 1)

            Hero = hex(int(ID[0:3]))[2:]
            if len(Hero) == 3:
                Hero = Hero[1:3] + "0" + Hero[0]
            else:
                Hero += "00"
            Hero += "0000"
            Hero = bytes.fromhex(Hero)

            Cache = Cache.replace(Cache[8:12], Hero, 1)

            if File == file_actor_mod and Id == All[0]:
                ID30 = b"\x07\x00\x00\x0030" + bytes(ID[0:3] + "0", "utf8") + b"\x00"
                XYZ = Cache[64]
                ID0 = Cache[64: 68 + XYZ]
                Cache = Cache.replace(ID0, ID30, 1)

                VT = Id.find(b"Hero_")
                NumHero = Id[VT - 4]
                HeroName = Id[VT - 4:VT + NumHero]
                Cache = Cache.replace(b"jpg\x00\x01\x00\x00\x00\x00", b"jpg\x00" + HeroName)

                Full = Cache.count(HeroName)
                if Full > 1:
                    Cache = Cache.replace(b"jpg\x00" + HeroName, b"jpg\x00\x01\x00\x00\x00\x00", Full - 1)

                EndTheCode = hex(len(Cache))
                if len(EndTheCode) == 5:
                    EndTheCode = EndTheCode[3:5] + "0" + EndTheCode[2:3]
                else:
                    EndTheCode = EndTheCode[4:6] + EndTheCode[2:4]
                EndTheCode = bytes.fromhex(EndTheCode)
                Cache = Cache.replace(Cache[0:2], EndTheCode, 1)

            Code = Code.replace(Id, Cache, 1)
            dieukienmod1=[]
            dieukienmod1.append(Cache)
            for dieukienmod2 in dieukienmod1:
                if b"Hero" in dieukienmod2:
                    dieukienmod = dieukienmod2
        with open(File, "wb") as file:
            file.write(Code)



for skin_id_input in IDMODSKIN:
    sound_directory = Sound_Files
    sound_files = os.listdir(sound_directory)
    all_skin_ids = []
    for i in range(21):
        if i < 10:
            i = "0" + str(i)
        all_skin_ids.append(b"\x00" + int(skin_id_input[0:3] + str(i)).to_bytes(4, byteorder="little"))

    initial_skin_id = all_skin_ids[0]
    selected_skin_id = all_skin_ids[int(skin_id_input[3:])]

    # Xóa selected và initial khỏi danh sách thay thế
    all_skin_ids.remove(selected_skin_id)
    all_skin_ids.remove(initial_skin_id)

    for sound_file_name in sound_files:
        with open(os.path.join(sound_directory, sound_file_name), "rb") as sound_file:
            sound_data = sound_file.read()

        # Patch đặc biệt theo từng skin cụ thể
        if skin_id_input == "13311":
            if sound_file_name == 'BattleBank.bytes':
                sound_data = sound_data.replace(b'\x9dO\x14', b'\xff3\x00')\
                                       .replace(b'\x9eO\x14', b'\xff3\x00')\
                                       .replace(b'\x9fO\x14', b'\xff3\x00')\
                                       .replace(b'\xa0O\x14', b'\xff3\x00')
            if sound_file_name == 'ChatSound.bytes':
                sound_data = sound_data.replace(b'\x9fO\x14', b'\xff3\x00')
            if sound_file_name == 'HeroSound.bytes':
                sound_data = sound_data.replace(b'\x9fO\x14', b'\xff3\x00')\
                                       .replace(b'\xa0O\x14', b'\xff3\x00')
            if sound_file_name == 'LobbyBank.bytes':
                sound_data = sound_data.replace(b'\xa0O\x14', b'\xff3\x00')
            if sound_file_name == 'LobbySound.bytes':
                sound_data = sound_data.replace(b'\xa0O\x14', b'\xff3\x00')

        if skin_id_input == "16707":
            if sound_file_name == 'BattleBank.bytes':
                sound_data = sound_data.replace(b'/~\x19', b'CA\x00')\
                                       .replace(b'0~\x19', b'CA\x00')\
                                       .replace(b'1~\x19', b'CA\x00')
            if sound_file_name == 'ChatSound.bytes':
                sound_data = sound_data.replace(b'0~\x19', b'CA\x00')
            if sound_file_name == 'HeroSound.bytes':
                sound_data = sound_data.replace(b'0~\x19', b'CA\x00')\
                                       .replace(b'1~\x19', b'CA\x00')
            if sound_file_name == 'LobbyBank.bytes':
                sound_data = sound_data.replace(b'0~\x19', b'CA\x00')
            if sound_file_name == 'LobbySound.bytes':
                sound_data = sound_data.replace(b'0~\x19', b'CA\x00')

        # Xử lý thay thế ID cho toàn bộ sound files
        if sound_file_name != "CoupleSound.bytes":
            for skin_id in all_skin_ids:
                skin_id += b"\x00" * 8
                sound_data = sound_data.replace(skin_id, b"\x0000" + b"\x00" * 10)
        else:
            for skin_id in all_skin_ids:
                skin_id += b"\x02\x00\x00\x00\x01"
                sound_data = sound_data.replace(skin_id, b"\x0000\x00\x00\x02\x00\x00\x00\x01")

        # Thay thế selected ID
        if sound_data.find(selected_skin_id) != -1:
            if sound_file_name != "CoupleSound.bytes":
                sound_data = sound_data.replace(initial_skin_id + b"\x00" * 8, b"\x0000" + b"\x00" * 10)
                sound_data = sound_data.replace(selected_skin_id + b"\x00" * 8, initial_skin_id + b"\x00" * 8)
            else:
                sound_data = sound_data.replace(initial_skin_id + b"\x02\x00\x00\x00\x01", b"\x0000\x00\x00\x02\x00\x00\x00\x01")
                sound_data = sound_data.replace(selected_skin_id + b"\x02\x00\x00\x00\x01", initial_skin_id + b"\x02\x00\x00\x00\x01")

        # Ghi đè lại file đã xử lý
        with open(os.path.join(sound_directory, sound_file_name), "wb") as sound_file:
            sound_file.write(sound_data)


file_paths = [file_mod_skill1, file_mod_skill2]
for user_id in IDMODSKIN:
    user_id_bytes = bytes(f"fects/{user_id[0:3]}_", "utf8")
    matching_files = []

    for file in file_paths:
        with open(file, "rb") as f:
            if user_id_bytes in f.read():
                matching_files.append(file)

    for file in matching_files:
        if user_id == '13311':
            with open(file, "rb") as f:
                code_content = f.read()
                code_content = code_content.replace(
                    b"prefab_skill_effects/hero_skill_effects/133_direnjie/",
                    b"prefab_skill_effects/component_effects/13311/13311_5/"
                )
            with open(file, "wb") as f:
                f.write(code_content)
            break  
        else:
            modified_codes = []
            buffer_codes = []

            with open(file, "rb") as f:
                begin_content = f.read(140)
                while True:
                    data_length = f.read(2)
                    if not data_length:
                        break
                    section_length = data_length[0] + data_length[1] * 256
                    code_section = data_length + f.read(section_length)
                    if user_id_bytes in code_section:
                        modified_codes.append(code_section)

            for code_section in modified_codes:
                start_index = code_section.find(user_id_bytes) + 6
                end_index = code_section.find(b"/", start_index) + 1
                hero_name = code_section[start_index:end_index]
                code_section = code_section.replace(
                    b"Prefab_Skill_Effects/Hero_Skill_Effects",
                    b"prefab_skill_effects/hero_skill_effects"
                )
                code_section = code_section.replace(
                    b"hero_skill_effects/" + hero_name,
                    b"hero_skill_effects/" + hero_name + bytes(user_id + "/", "utf8")
                )
                offset = code_section.find(b"prefab_skill_effects") - 4
                new_length = code_section[offset] + len(user_id) + 1
                length_bytes = new_length.to_bytes(4, "little")
                code_section = code_section[:offset] + length_bytes + code_section[offset+4:]
                total_len = len(code_section) - 2
                total_len_bytes = total_len.to_bytes(2, "little")
                code_section = total_len_bytes + code_section[2:]

                buffer_codes.append(code_section)

            
            with open(file, "rb") as f:
                original_content = f.read()

            for old_code, new_code in zip(modified_codes, buffer_codes):
                original_content = original_content.replace(old_code, new_code, 1)

            with open(file, "wb") as f:
                f.write(original_content)
        #print('Done')

for ID in IDMODSKIN:
    AllID = []
    for i in range(21):
        if i < 10:
            AllID.append(ID[0:3] + "0" + str(i))
        else:
            AllID.append(ID[0:3] + str(i))

    All_S = []
    for i in AllID:
        i_hex = hex(int(i))[2:]
        All_S.append(bytes.fromhex(f"{i_hex[2:4]}{i_hex[0:2]}0000"))

    with open(file_mod_Modtion, "rb") as f:
        begin = f.read(140)
        All_Code = []
        while True:
            SL = f.read(2)
            if SL == b"":
                break
            SL0 = SL[0] + SL[1] * 256
            Code = SL + f.read(SL0)
            if All_S[AllID.index(ID)] in Code:
                All_Code.append(Code)
            elif All_S[0] in Code:
                All_Code.append(Code)

    CodeDB = []
    CodeMD = []
    CodeMD2 = []

    for code in All_Code:
        if code[0:2] in b"6\x00S\x00":
            CodeDB.append(code)
        else:
            CodeMD.append(code)
            CodeMD2.append(code)

    aw = 0
    if len(CodeDB) > 1:
        print(f"Skin {ID} có {len(CodeDB)} kiểu nhảy đặc biệt → tự chọn kiểu đầu tiên")
        aw = 0

    if len(CodeDB) > 0:
        CodeR = CodeDB[aw]
        idmod = CodeR[21:25]
        for i, code in enumerate(CodeMD):
            for id in All_S:
                vt = code.find(id)
                if vt != -1:
                    codet = code[vt+4:vt+8]
                    code = code.replace(codet, idmod, 1)
                else:
                    break
            CodeMD[i] = code
    else:
        for i, code in enumerate(CodeMD):
            vt = code.find(All_S[AllID.index(ID)])
            idmod = code[vt+4:vt+8]
            for id in All_S:
                vt = code.find(id)
                if vt != -1:
                    codet = code[vt+4:vt+8]
                    code = code.replace(codet, idmod, 1)
                else:
                    break
            CodeMD[i] = code

    with open(file_mod_Modtion, "rb") as f:
        y = f.read()

    for i in range(len(CodeMD)):
        y = y.replace(CodeMD2[i], CodeMD[i], 1)

    if len(CodeMD) + len(CodeDB) == 0:
        for id in All_S:
            y = y.replace(id, b"\x00\x00\x00", 1)

    with open(file_mod_Modtion, "wb") as f:
        f.write(y)

CODE_BV_HERO = b''
def modify_skill_data(data, new_id, effect_name_lowercase, effect_name):
    modified_data = data.read()
    modified_data = modified_data.replace(string1, string1 + new_id)
    modified_data = modified_data.replace(string3, string3 + new_id)
    modified_data = modified_data.replace(string2, string2 + new_id)
    modified_data = modified_data.replace(string4, string4 + new_id)
    modified_data = modified_data.replace(b'tyEffect" value="true"', b'tyEffect" value="false"')
    modified_data = modified_data.replace(string5, string5 + new_id)
    modified_data = modified_data.replace(string7, string7 + new_id)
    modified_data.replace(SKIN_EFFECT_ID, new_id)
    return modified_data

for IDMODSKIN in IDMODSKIN1:
    zip_path = f'Resources/1.58.1/Ages/Prefab_Characters/Prefab_Hero/Actor_{IDMODSKIN[:3]}_Actions.pkg.bytes'
    Files_Directory_Path = f'{pack_name}/Resources/1.58.1/Ages/Prefab_Characters/Prefab_Hero/mod4/'

    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(Files_Directory_Path)
    
    #print(f"📂 Đã giải nén: {zip_path} -> {Files_Directory_Path}")
    #print("📁 Danh sách thư mục sau giải nén:", os.listdir(Files_Directory_Path))
    NAME_HERO = next((name for name in os.listdir(Files_Directory_Path) if name.startswith(IDMODSKIN[:3] + "_")), None)
    if not NAME_HERO:
        print(f"❌ Không tìm thấy thư mục cho ID {IDMODSKIN}")
        continue
    if IDMODSKIN in ("53002", "53702") or b"Skin_Icon_Skill" in dieukienmod or b"Skin_Icon_BackToTown" in dieukienmod:
        directory_path = f'{Files_Directory_Path}{NAME_HERO}/skill/'
        if not os.path.exists(directory_path):
            print(f"⚠️ Không có thư mục skill cho {NAME_HERO}")
            continue
        effect_name = NAME_HERO
        effect_name_db = effect_name[4:]
        effect_info = effect_name_db.capitalize()
        file_name = effect_name.replace(effect_name_db, effect_info)

        new_id = IDMODSKIN.encode()
        new_id_slash = new_id + b"/"
        effect_name_bytes = file_name.encode()
        effect_name_lower = effect_name_bytes.lower()

        string1 = b"hero_skill_effects/" + effect_name_lower + b"/"
        string2 = b"hero_skill_effects/" + effect_name_bytes + b"/"
        string3 = b"Hero_Skill_Effects/" + effect_name_lower + b"/"
        string4 = b"Hero_Skill_Effects/" + effect_name_bytes + b"/"
        string5 = b"hero_skill_effects/" + effect_name_bytes + b"/"
        string7 = b"Hero_Skill_Effects/" + effect_name_bytes + b"/"
        SKIN_EFFECT_ID = new_id + b"/" + new_id

        for file_item in os.listdir(directory_path):
            file_path = os.path.join(directory_path, file_item)
            giai(file_path)
            if IDMODSKIN != "16707" and 'Back' in file_item:
                continue

            if file_item.endswith('.xml'):
                with open(file_path, 'rb') as f:
                    modified = modify_skill_data(f, new_id_slash, effect_name_lower, effect_name_bytes)
                with open(file_path, 'wb') as f:
                    f.write(modified)

                if IDCHECK == '10611':
                    if file_item == 'U1B1.xml':
                        with open(file_path, 'rb') as f:
                            data = f.read().replace(
                                b'<Condition id="10" guid="2e5f463f-105d-4143-b786-e59ea8b34fa2" status="true" />',
                                b'\r\n    <!-- ' + AABBCC.encode('utf-8') + b' -->'
                            )
                        with open(file_path, 'wb') as f:
                            f.write(data)

                    if file_item == 'A3.xml':
                        with open(file_path, 'rb') as f:
                            data = f.read().replace(
                                b'<String name="clipName" value="Atk3"',
                                b'<String name="clipName" value="Atk1"'
                            )
                        with open(file_path, 'wb') as f:
                            f.write(data)

    #print(f"✅ Đã xử lý xong ID {IDMODSKIN}")

    if IDCHECK == "53002" or b"Skin_Icon_SoundEffect" in dieukienmod or b"Skin_Icon_Dialogue" in dieukienmod:
        if IDCHECK not in ["13311", "16707"]:
            directory_path = Files_Directory_Path + f'{NAME_HERO}' + '/skill/'        
            IDSOUND_S = IDMODSKIN
            if IDSOUND_S[3:4] == '0':
                IDSOUND_S = IDSOUND_S[:3] + IDSOUND_S[4:]
            IDSOUND1 = IDSOUND_S[3:]
            IDSOUND12 = IDSOUND1.encode()
            IDSOUND = b"_Skin" + IDSOUND12
            IDINFO = int(IDMODSKIN) + 1
            IDINFO = str(IDINFO)
            if IDINFO[3:4] == '0':
                IDINFO = IDINFO[:3] + IDINFO[4:]
            IDINFO = str(IDINFO)

            o = directory_path
            ID = (IDSOUND)
            File = os.listdir(o)
            for file in File:
                with open(o + file, 'rb') as f:
                    rpl = f.readlines()
                with open(o + file, 'rb') as f:
                    Rpl = f.read()
                Code = []
                for i in rpl:
                    if i.find(b'<String name="eventName" value="') != -1:
                        Code.append(i[40:i.find(b'" refParamName="" useRefParam="false" />')])
                for i in Code:
                    a = b'<String name="eventName" value="' + i + b'" refParamName="" useRefParam="false" />'
                    if Code:
                        Rpl = Rpl.replace(a, b'<String name="eventName" value="' + i + IDSOUND + b'" refParamName="" useRefParam="false" />')
                if Rpl != open(o + file, 'rb').read():
                    with open(o + file, 'wb') as f:
                        f.write(Rpl)
    
    if b"Skin_Icon_BackToTown" in dieukienmod or b"Skin_Icon_Animation" in dieukienmod:
        def extract_blocks(xml_content):
            result = []
            seen_resource_lines = set()
            seen_clipnames = {"home": False, "gohome": False}

            lines = xml_content.splitlines()
            inside_track = False
            block = []
            check_skin_block = None
            current_resource_line = ""
            current_clipname = ""
            is_check_skin_block = False

            for line in lines:
                if '<Track ' in line:
                    inside_track = True
                    block = [line]
                    current_resource_line = ""
                    current_clipname = ""
                    is_check_skin_block = False
                elif inside_track:
                    block.append(line)
                    lower_line = line.lower()
                    if '<String name="resourceName"' in line:
                        current_resource_line = line.strip()
                    if 'name="clipname"' in lower_line:
                        if 'value="home"' in lower_line:
                            current_clipname = "home"
                        elif 'value="gohome"' in lower_line:
                            current_clipname = "gohome"
                    if 'eventname="checkskinidtick"' in lower_line:
                            is_check_skin_block = True
                    if '</Track>' in line:
                        track_str = '\n'.join(block)
                        if is_check_skin_block and check_skin_block is None:
                            check_skin_block = track_str
                        elif current_resource_line and current_resource_line not in seen_resource_lines:
                            result.append(track_str)
                            seen_resource_lines.add(current_resource_line)
                        elif current_clipname in seen_clipnames and not seen_clipnames[current_clipname]:
                            result.append(track_str)
                            seen_clipnames[current_clipname] = True
                        inside_track = False
                        block = []
            if check_skin_block:
                return [check_skin_block] + result
            return result
        def remove_unwanted_lines(text):
            lines = text.splitlines()
            filtered_lines = []
            for line in lines:
                if ('<String name="parentResourceName"' in line or
					'<Enum name="ReplacementUsage"' in line or
					'<Enum name="ReplacementSubUsage"' in line or
					'<SkinOrAvatarList' in line):
                    continue
                filtered_lines.append(line)
            return '\n'.join(filtered_lines)
        def replace_resource_lines(text, NAME_HERO, IDMODSKIN):
            text = text.replace(
				'<String name="resourceName" value="" refParamName="strReturnCityFall" useRefParam="true" />',
				f'<String name="resourceName" value="prefab_skill_effects/hero_skill_effects/{NAME_HERO}/{IDMODSKIN}/huijidi_01" refParamName="" useRefParam="false" />'
			)
            text = text.replace(
				'<String name="resourceName" value="" refParamName="strReturnCityEffectPath" useRefParam="true" />',
				f'<String name="resourceName" value="prefab_skill_effects/hero_skill_effects/{NAME_HERO}/{IDMODSKIN}/huicheng_tongyong_01" refParamName="" useRefParam="false" />'
			)
            new_lines = []
            for line in text.splitlines():
                if '<int name="skinId"' in line:
                    new_lines.append(f'<int name="skinId" value="{IDMODSKIN[:3]}00" refParamName="" useRefParam="false" />')
                else:
                    new_lines.append(line)
            text = '\n'.join(new_lines)
            return text
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

        # ======== MAIN ========
        with open(f'{pack_name}/Resources/1.58.1/Ages/Prefab_Characters/Prefab_Hero/mod1/commonresource/Back.xml', "r", encoding="utf-8") as f:
            original_content = f.read()
        final_content = original_content
        for IDMODSKIN in IDMODSKIN1:
            try:
                if b"Skin_Icon_BackToTown" in dieukienmod or b"Skin_Icon_Animation" in dieukienmod:
                    NAME_HERO = None
                    HERO_NAME_LIST = os.listdir(Files_Directory_Path)
                    for HERO_NAME_ITEM in HERO_NAME_LIST:
                        if HERO_NAME_ITEM.startswith(IDMODSKIN[:3] + "_"):
                            NAME_HERO = HERO_NAME_ITEM
                            break
                    if NAME_HERO is None:
                        pass
                        continue
                    with open(f'{pack_name}/Resources/1.58.1/Ages/Prefab_Characters/Prefab_Hero/mod1/commonresource/Back.xml', "r", encoding="utf-8") as f:
                        content = f.read()
                    content = re.sub(r'\s*SkinAvatarFilterType="\d+"', '', content)
                    base_blocks = extract_blocks(content)

                    if len(base_blocks) < 3:
                        print("❌ Không tìm thấy đủ block phù hợp!")
                        continue

                    check_skin_block = base_blocks[0]
                    other_blocks = base_blocks[1:]

            # Xử lý checkskin block cho ID hiện tại
                    lines = check_skin_block.splitlines()
                    replaced_lines = []
                    for line in lines:
                        if '<int name="skinId"' in line:
                            replaced_lines.append(
                        f'        <int name="skinId" value="{IDMODSKIN[:3]}00" refParamName="" useRefParam="false" />'
                    )
                        else:
                            replaced_lines.append(line)
                    check_skin_block_mod = '\n'.join(replaced_lines)
                    check_skin_block_mod = re.sub(r'^.*<SkinOrAvatarList[^>]*/>.*\n?', '', check_skin_block_mod, flags=re.MULTILINE)

            # Phân loại block hiệu ứng và gohome/home
                    effect_blocks = []
                    gohome_home_blocks = []

                    for block in other_blocks:
                        clean_block = remove_unwanted_lines(block)
                        block_lower = clean_block.lower()
                        if 'clipname' in block_lower:
                            if 'value="home"' in block_lower or 'value="gohome"' in block_lower:
                                gohome_home_blocks.append(clean_block)
                        else:
                            replaced_block = replace_resource_lines(clean_block, NAME_HERO, IDMODSKIN)
                            effect_blocks.append(replaced_block)

            # Gom đủ 5 block (1 checkskin, 2 hiệu ứng, 2 home/gohome)
                    
                    # Gom đủ 5 block
                    all_blocks = [check_skin_block_mod] + effect_blocks[:2] + gohome_home_blocks[:2]
# Chèn dòng <Condition ...> vào mỗi block
# Gắn vào file XML
                    final_content = insert_blocks_before_action_close(final_content, all_blocks)
                    #print(f"✅ Đã xử lý xong {NAME_HERO} - {IDMODSKIN}")

            except Exception as e:
                print("❌ Lỗi xử lý:", str(e))
        with open(f'{pack_name}/Resources/1.58.1/Ages/Prefab_Characters/Prefab_Hero/mod1/commonresource/BackMod.xml', "w", encoding="utf-8") as f:
            f.write(final_content)
os.remove(f'{pack_name}/Resources/1.58.1/Ages/Prefab_Characters/Prefab_Hero/mod1/commonresource/Back.xml')

        # Đổi tên file BackMod.xml thành Back.xml
os.rename(
            f'{pack_name}/Resources/1.58.1/Ages/Prefab_Characters/Prefab_Hero/mod1/commonresource/BackMod.xml',
            f'{pack_name}/Resources/1.58.1/Ages/Prefab_Characters/Prefab_Hero/mod1/commonresource/Back.xml'
        )
with open(f'{pack_name}/Resources/1.58.1/Ages/Prefab_Characters/Prefab_Hero/mod1/commonresource/Back.xml', "r", encoding="utf-8") as f:
    target_content = f.read()

modified_count = 0
HEROS = os.listdir(Files_Directory_Path)

for ID_BACK in IDMODSKIN1:
    CHECK_ID = ID_BACK
    Skin_Back = ID_BACK[:3] + "00"
    found = False
    for NAME_HERO in HEROS:
        Path_Back = os.path.join(Files_Directory_Path, NAME_HERO, "skill")
        file_name = f"{CHECK_ID}_Back.xml"
        file_path = os.path.join(Path_Back, file_name)
        if not os.path.exists(file_path):
            continue

        with open(file_path, "r", encoding="utf-8") as f:
            source_content = f.read()

        # ⚙️ Dò các block <Track> trong file nguồn
        track_blocks = re.findall(r'\s*<Track trackName=.*?</Track>', source_content, flags=re.DOTALL)
        if not track_blocks:
            print(f"⚠️ Không tìm thấy block nào trong '{file_name}', bỏ qua.")
            continue

        # 🔍 Tìm dòng skinId tương ứng trong Back.xml
        pattern = rf'<int name="skinId" value="{Skin_Back}".*?/>'
        match = re.search(pattern, target_content)
        if not match:
            print(f"⚠️ Không tìm thấy dòng skinId {Skin_Back} trong Back.xml, bỏ qua '{file_name}'")
            continue

        # 📍 Tìm vị trí chèn sau </Track>
        insert_pos = target_content.find('</Event>', match.end())
        if insert_pos == -1:
            print(f"⚠️ Không tìm thấy </Event> sau dòng skinId trong '{file_name}'")
            continue
        insert_pos = target_content.find('</Track>', insert_pos)
        if insert_pos == -1:
            print(f"⚠️ Không tìm thấy </Track> sau </Event> trong '{file_name}'")
            continue
        insert_pos += len('</Track>')

        # 🧩 Chèn block vào Back.xml
        combined_blocks = "\n"+"\n".join(track_blocks)
        target_content = target_content[:insert_pos] + combined_blocks + target_content[insert_pos:]
        modified_count += 1
        #print(f"✅ Đã chèn {len(track_blocks)} block từ '{file_name}' vào Back.xml sau skinId {Skin_Back}")
        found = True
        break 
    if not found:
        pass
if modified_count > 0:
    with open(f'{pack_name}/Resources/1.58.1/Ages/Prefab_Characters/Prefab_Hero/mod1/commonresource/Back.xml', "w", encoding="utf-8") as f:
        f.write(target_content)
    #print(f"\n💾 Đã lưu thay đổi vào Back.xml ({modified_count} lần chèn)")
else:
    print("\n⚠️ Không có thay đổi nào được thực hiện trong Back.xml")
with open(f'{pack_name}/Resources/1.58.1/Ages/Prefab_Characters/Prefab_Hero/mod1/commonresource/Back.xml', "r", encoding="utf-8") as f:
    lines = [line for line in f if line.strip()]  # loại bỏ dòng trống (line.strip() == False)
with open(f'{pack_name}/Resources/1.58.1/Ages/Prefab_Characters/Prefab_Hero/mod1/commonresource/Back.xml', "w", encoding="utf-8") as f:
    f.writelines(lines)

IDMODSKININ = [str(num) for num in numbers]

# Dùng dict lưu tên hero theo từng ID
while True:
    for id_str in IDMODSKININ:
        IDINFO = int(id_str)
        IDINFO = str(IDINFO)

        # Bỏ số 0 ở giữa nếu có (VD: 15001 -> 1501)
        if len(IDINFO) > 3 and IDINFO[3:4] == '0':
            IDINFO = IDINFO[:3] + IDINFO[4:]

        #print("✅ Đang xử lý ID:", IDINFO)
        #print(IDINFO)
        
        # Process each ID individually
        try:
            Files_Directory_Path = f'Prefab_Hero/mod{IDINFO}/'
            # Create directory if it doesn't exist
            os.makedirs(Files_Directory_Path, exist_ok=True)
            
            # Use the first 3 characters of the current ID
            hero_id_prefix = IDINFO[:3]
            zip_path = f'Resources/1.58.1/Ages/Prefab_Characters/Prefab_Hero/Actor_{hero_id_prefix}_Actions.pkg.bytes'
            
            #print(f"\n\033[1;97mProcessing ID: {IDINFO}\033[0m")
            #print(f"\033[1;94mOpening file: {zip_path}\033[0m")
            
            if not os.path.exists(zip_path):
                print(f"\033[1;91mFile not found: {zip_path}\033[0m")
                continue
                
            with zipfile.ZipFile(zip_path) as File_Zip:
                File_Zip.extractall(Files_Directory_Path)
                
            HERO_NAME_LIST = os.listdir(Files_Directory_Path)
            for HERO_NAME_ITEM in HERO_NAME_LIST:
                NAME_HERO = HERO_NAME_ITEM
                #print(f"\033[1;92mFound hero: {NAME_HERO}\033[0m")
                
        except Exception as e:
            print(f"\033[1;91mError processing ID {IDINFO}: {str(e)}\033[0m")
            continue
        
        # NOTE: The following variables need to be defined before use:
        # sanitized_input, version, NAME_HERO, IDCHECK, phukienv, phukien,
        # ngoaihinhvaneovvang, ngoaihinhvaneovdo, ngoaihinhvaneov,
        # ngoaihinhkhieov, ngoaihinhdoveres, ngoaihinhxanhveres
        
        INFO_MOD = f'{pack_name}/Resources/1.58.1/Prefab_Characters/mod/'
        
        try:
            with zipfile.ZipFile(f'Resources/1.58.1/Prefab_Characters/Actor_'+f'{IDINFO[:3]}'+'_Infos.pkg.bytes') as f:
                f.extractall(INFO_MOD)
            
            duongdan = INFO_MOD + 'Prefab_Hero/' + f'{NAME_HERO}' + '/'
            newpath = duongdan + NAME_HERO + '_actorinfo.bytes'
            
            # NOTE: giai() function needs to be defined
            giai(newpath)
            IDCHECK = IDINFO
            def skincanmod(data):
                trc1 = r.find(timtrc, r.find(b'SkinPrefabG'))
                vt1 = r.find(b'JTCom0', trc1-300)
                a1 = r[vt1-31:]
                a3 = vt1 - 31
                skin1 = a1[:4]
                skin2 = int.from_bytes(skin1, byteorder='little')
                data = r[a3:a3+skin2]
                return data
            
            op = newpath
            trc = IDINFO
            with open(op, 'rb') as f:
                r = f.read()
                r1 = r
                timtrc = trc.encode()
            
            #skin
            mkcam = b''
            teninfobv1 = NAME_HERO
            if IDCHECK == '14111':
                teninfobv1 = '141_DiaoChan'
            tenefec2 = teninfobv1.encode()
            tenefec = teninfobv1.lower().encode()
            newteneffec = tenefec[4:].capitalize()
            newteneffec = tenefec[:4] + newteneffec
            str1 = b"hero_skill_effects/" + tenefec2 + b"/"
            str2 = b"hero_skill_effects/" + tenefec + b"/"
            str3 = b"Hero_Skill_Effects/" + tenefec2 + b"/"
            str4 = b"Hero_Skill_Effects/" + tenefec + b"/"
            str5 = b"hero_skill_effects/" + newteneffec + b"/"
            str7 = b"Hero_Skill_Effects/" + newteneffec + b"/"
            IDskineffecđbt = IDCHECK.encode() + b"/" + IDCHECK.encode()
            idnew = IDCHECK.encode() + b"/"
            mkcam = b''
            new1 = b''
            new1 += skincanmod(r)
            
            if IDCHECK == '13311':
                if phukienv == "vangv":
                    new1 = ngoaihinhvaneovvang
                if phukienv == "dov":
                    new1 = ngoaihinhvaneovdo
                if phukienv == '':
                    new1 = ngoaihinhvaneov
            if IDCHECK == '16707':
                new1 = ngoaihinhkhieov
            if IDCHECK == '52007':
                if phukien == "do":
                    new1 = ngoaihinhdoveres
                if phukien == "xanh":
                    new1 = ngoaihinhxanhveres
            
            IDskineffecđbt = IDCHECK.encode() + b"/" + IDCHECK.encode()
            idnew = IDCHECK.encode() + b'/'
            ID1 = IDCHECK.encode()
            
            if new1.find(b'prefab_skill_effects/hero_skill_effects/') != -1:
                FIND = new1.find(b'PreloadAnimatorEffects') - 8
                VT1 = new1[FIND:FIND+4]
                VTR = int.from_bytes(VT1, byteorder='little')
                VTM = new1[FIND:FIND+VTR]
                VTM9 = VTM
                VTM = (VTR+12).to_bytes(4, byteorder='little') + VTM[4:]
                ELe = VTM.find(b'Element') - 8
                ELe1 = VTM.find(b'Element') - 16
                VTRCM = VTM[:ELe-8]
                DAU = VTM[ELe:ELe+4]
                VTR = int.from_bytes(DAU, byteorder='little')
                VTM1 = VTM[ELe:ELe+VTR]
                VTM1 = (VTR+6).to_bytes(4, byteorder='little') + VTM1[4:]
                VTCUOI = VTM[ELe:]
                VTCUOI1 = VTM[ELe1:ELe1+8]
                tinh = VTM.count(b'Element')
                VTM = VTCUOI
                KB = 0
                CODEFULL = b''
                
                for i in range(tinh):
                    ELe = VTM.find(b'Element') - 8
                    DAU = VTM[ELe:ELe+4]
                    VTR = int.from_bytes(DAU, byteorder='little')
                    VTM1 = VTM[ELe:ELe+VTR]
                    if VTM1.find(b'Vprefab_skill_effects/hero_skill_effects/') == -1:
                        CODEFULL += VTM1
                        break
                    VTM1 = (VTR+6).to_bytes(4, byteorder='little') + VTM1[4:]
                    VTCUOI = VTM[VTR:]
                    ELe1 = VTM.find(b'Element') + 7
                    DAU1 = VTM[ELe1:ELe1+4]
                    VTR = int.from_bytes(DAU1, byteorder='little')
                    VTM2 = VTM[ELe1:ELe1+VTR]
                    VTM2 = (VTR+6).to_bytes(4, byteorder='little') + VTM2[4:]
                    newvt = VTM1.find(b'Vprefab_skill_effects/') - 8
                    MOI = VTM1[newvt:newvt+4]
                    VTR = int.from_bytes(MOI, byteorder='little')
                    VTR3 = VTM1[newvt:newvt+VTR]
                    VTM3 = (VTR+6).to_bytes(4, byteorder='little') + VTR3[4:]
                    CODE = VTM1[:15] + VTM2[:46] + VTM3 + b'\x04\x00\x00\x00\x04\x00\x00\x00'
                    VTM = VTCUOI
                    CODEFULL += CODE
                
                CODEFULL = CODEFULL.replace(str1, str1 + idnew).replace(str2, str2 + idnew)
                CODEFULL = len(VTRCM + VTCUOI1 + CODEFULL).to_bytes(4, byteorder='little') + VTRCM[4:] + (len(VTCUOI1 + CODEFULL)).to_bytes(4, byteorder='little') + VTCUOI1[4:] + CODEFULL
                new1 = new1.replace(VTM9, CODEFULL)
                new1 = len(new1).to_bytes(4, byteorder='little') + new1[4:]
                mkcam = b'\x05'
            
            skinmoi = new1
            skinprefag = r.find(b'SkinPrefabG') - 8
            tinhskinpre = r[skinprefag:skinprefag+4]
            tinhskinpre1 = int.from_bytes(tinhskinpre, byteorder='little')
            tinhskinpre2 = r[skinprefag:skinprefag+tinhskinpre1]
            JTCom0 = tinhskinpre2.count(b"JTCom0")
            beginskin = tinhskinpre2[:101]
            CodeSkinNew = beginskin + new1 * JTCom0
            tinhCodeSkinNew1 = CodeSkinNew[:93]
            tinhCodeSkinNew = CodeSkinNew[93:]
            Elenmen = len(tinhCodeSkinNew).to_bytes(4, byteorder='little') + tinhCodeSkinNew[4:]
            SkinPrefag1 = tinhCodeSkinNew1 + Elenmen
            SkinPrefag = len(SkinPrefag1).to_bytes(4, byteorder='little') + SkinPrefag1[4:]
            codeskinnew = r1.replace(tinhskinpre2, SkinPrefag)

            def ArtSkinPrefabLOD(data3):
                a = skinmoi.find(b'\x00ArtSkinPrefabLOD') - 7
                a10 = skinmoi.find(b'\x00ArtSkinPrefabLOD') - 3
                a3 = skinmoi[a:a+8]
                a4 = a3[4:]
                a2 = skinmoi[a:a+4]
                vitri = int.from_bytes(a2, byteorder='little')
                vitri2 = int.from_bytes(a4, byteorder='little')
                a5 = skinmoi[a:a+vitri]
                a25 = skinmoi[a10:a10+vitri2]
                a22 = skinmoi[a10:a10+vitri2].replace(b'\x00ArtSkinPrefabLOD', b'\x00ArtPrefabLOD')
                a13 = len(a22).to_bytes(4, byteorder='little') + a22[4:]
                code = a5.replace(a25, a13)
                data3 = len(code).to_bytes(4, byteorder='little') + code[4:]
                return data3
            
            def ArtSkinLobbyShowLOD(data4):
                a = skinmoi.find(b'\x00ArtSkinLobbyShowLOD') - 7
                a10 = skinmoi.find(b'\x00ArtSkinLobbyShowLOD') - 3
                a3 = skinmoi[a:a+8]
                a4 = a3[4:]
                a2 = skinmoi[a:a+4]
                vitri = int.from_bytes(a2, byteorder='little')
                vitri2 = int.from_bytes(a4, byteorder='little')
                a5 = skinmoi[a:a+vitri]
                a25 = skinmoi[a10:a10+vitri2]
                a22 = skinmoi[a10:a10+vitri2].replace(b'\x00ArtSkinLobbyShowLOD', b'\x00ArtLobbyShowLOD')
                a13 = len(a22).to_bytes(4, byteorder='little') + a22[4:]
                code = a5.replace(a25, a13)
                data4 = len(code).to_bytes(4, byteorder='little') + code[4:]
                return data4
            
            # NOTE: ArtSkinLobbyIdleShowLOD function needs to be defined
            def ArtSkinLobbyIdleShowLOD(data4):
                # Implementation needed
                a = camSkin.find(b'\x00ArtSkinLobbyIdleShowLOD')-7
                a10 = camSkin.find(b'\x00ArtSkinLobbyIdleShowLOD')-3
                a3=camSkin[a:a+8]
                a4=a3[4:]
                a2=camSkin[a:a+4]
                vitri=int.from_bytes(a2,byteorder='little')
                ne=camSkin[vitri:]
                vitri2=int.from_bytes(a4,byteorder='little')
                a5=camSkin[a:a+vitri]
                a25=camSkin[a10:a10+vitri2]
                a22=camSkin[a10:a10+vitri2].replace(b'\x00ArtSkinLobbyIdleShowLOD',b'\x00ArtLobbyIdleShowLOD')
                a13=len(a22).to_bytes(4,byteorder='little')+a22[4:]
                code=a5.replace(a25,a13)
                data4=len(code).to_bytes(4,byteorder='little')+code[4:]+ne
                return data4
            def ArtPrefabLODnew(data):
                a=ab.find(b'\x00ArtPrefabLOD')-7
                a2=ab[a:a+4]
                a3=ab[a:a+5]
                a4=a3[4:5]#so 10
                vitri=int.from_bytes(a2,byteorder='little')
                data=ab[a:a+vitri]
                return data
            def ArtPrefabLODExnew(data4):
                a=ab.find(b'\x00ArtPrefabLODEx')-7
                a2=ab[a:a+4]
                a3=ab[a:a+5]
                a4=a3[4:5]#so 10
                vitri=int.from_bytes(a2,byteorder='little')
                data4=ab[a:a+vitri]
                return data4
            def ArtSkinPrefabLODnew(data3):
                a=ab.find(b'\x00ArtSkinPrefabLOD')-7
                a10=ab.find(b'\x00ArtSkinPrefabLOD')-3
                a3=ab[a:a+8]
                a4=a3[4:]
                a2=ab[a:a+4]
                vitri=int.from_bytes(a2,byteorder='little')
                vitri2=int.from_bytes(a4,byteorder='little')
                a5=ab[a:a+vitri]
                a25=ab[a10:a10+vitri2]
                a22=ab[a10:a10+vitri2].replace(b'\x00ArtSkinPrefabLOD',b'\x00ArtPrefabLOD')
                a13=len(a22).to_bytes(4,byteorder='little')+a22[4:]
                code=a5.replace(a25,a13)
                data3=len(code).to_bytes(2,byteorder='little')+code[2:]
                return data3 
            def ArtSkinPrefabLODExnew(data2):
                a=ab.find(b'\x00ArtSkinPrefabLODEx')-7
                a10=ab.find(b'\x00ArtSkinPrefabLODEx')-3
                a3=ab[a:a+8]
                a4=a3[4:]
                a2=ab[a:a+4]
                vitri=int.from_bytes(a2,byteorder='little')
                vitri2=int.from_bytes(a4,byteorder='little')
                a5=ab[a:a+vitri]
                a25=ab[a10:a10+vitri2]
                a22=ab[a10:a10+vitri2].replace(b'\x00ArtSkinPrefabLODEx',b'\x00ArtPrefabLODEx')
                a13=len(a22).to_bytes(4,byteorder='little')+a22[4:]
                code=a5.replace(a25,a13)
                data2=len(code).to_bytes(4,byteorder='little')+code[4:]
                return data2
                
            #codeskinmd
            SkinMD = r[:skinprefag]
            #skinmd Art
            Art = SkinMD.find(b'ArtPrefabLOD') - 8
            tinhskinpre = SkinMD[Art:Art+4]
            tinhskinpre1 = int.from_bytes(tinhskinpre, byteorder='little')
            tinhskinpre2 = SkinMD[Art:Art+tinhskinpre1]
            #skinmd ArtLobbyShowLOD
            ArtLobby = SkinMD.find(b'ArtLobbyShowLOD') - 8
            tinhArtLobby = SkinMD[ArtLobby:ArtLobby+4]
            tinhArtLobby1 = int.from_bytes(tinhArtLobby, byteorder='little')
            tinhArtLobby2 = SkinMD[ArtLobby:ArtLobby+tinhArtLobby1]
            
            ArtSkinPrefab = b''
            ArtSkinPrefab += ArtSkinPrefabLOD(skinmoi)
            CodeNewMD = SkinMD.replace(tinhskinpre2, ArtSkinPrefab)
            
            ArtSkinLobby = b''
            ArtSkinLobby += ArtSkinLobbyShowLOD(skinmoi)
            CodeNewMD = CodeNewMD.replace(tinhArtLobby2, ArtSkinLobby)
            
            ArtLobbyIdle = CodeNewMD.find(b'ArtLobbyIdleShowLOD0') - 8
            cammd = CodeNewMD[ArtLobbyIdle:999999]
            ArtLobbyIdleSkin = skinmoi.find(b'ArtSkinLobbyIdleShowLOD') - 8
            camSkin = skinmoi[ArtLobbyIdleSkin:999999]
            camSkin = ArtSkinLobbyIdleShowLOD(camSkin)
            
            if mkcam == b'\x05':
                camSkin = camSkin.replace(CODEFULL, b'')
            
            CodeNewMD = CodeNewMD.replace(cammd, camSkin)
            CodeFull = codeskinnew.replace(SkinMD, CodeNewMD)
            RootDtrc = CodeFull[:84]
            RootDsau = CodeFull[84:]
            RootD1 = RootDsau[8:12]
            VTR = int.from_bytes(RootD1, byteorder='little')
            m = RootDsau.find(b'ArtPrefabLOD') - 8
            tinhRootDsau = len(RootDsau).to_bytes(4, byteorder='little') + RootDsau[4:]
            tinhRootDtrc = RootDtrc + tinhRootDsau
            CodeDayDu = len(tinhRootDtrc).to_bytes(4, byteorder='little') + tinhRootDtrc[4:]
            CodeDayDu = CodeDayDu.replace(b"Light<", b"00000<")
            CodeDayDu = CodeDayDu.replace(b'_LOD2', b'_LOD1').replace(b'_LOD3', b'_LOD1').replace(b'_Show2\x04', b'_Show1\x04').replace(b'_Show3\x04', b'_Show1\x04')
            tinhcam = CodeDayDu[:89]
            
            with open(op, 'wb') as f:
                f.write(CodeDayDu)
            
            o = open(op, 'rb')
            h = o.read(92)
            k = 0
            while True:
                r1 = o.read(4)
                if r1 == b'':
                    break
                KB = r1.hex()
                KB = KB[6:8] + KB[4:6] + KB[2:4] + KB[0:2]
                KB = int(KB, 16)
                O = r1 + o.read(KB-4)
                k += 1
            o.close()
            
            k = k.to_bytes(1, byteorder='little')
            tinhcam1 = CodeDayDu[:88] + k
            CodeDayDu = CodeDayDu.replace(tinhcam, tinhcam1)
            
            with open(op, 'wb') as f:
                f.write(CodeDayDu)
                
        except Exception as e:
            print(f"\033[1;91mError processing ID {IDINFO}: {str(e)}\033[0m")
            continue
    tiep_tuc = 'n'
    if tiep_tuc != 'y':
        break
#giai(newpath)
#print("INFOS [DONE!]")
Files_Directory = f'{pack_name}/Resources/1.58.1/Ages/Prefab_Characters/Prefab_Hero/mod4'
for folder_name in os.listdir(Files_Directory):
    folder_path = os.path.join(Files_Directory, folder_name)
    if os.path.isdir(folder_path) and folder_name[:3].isdigit():
        id_prefix = folder_name[:3]
        output_file = f'{pack_name}/Resources/1.58.1/Ages/Prefab_Characters/Prefab_Hero/Actor_{id_prefix}_Actions.pkg.bytes'

        with zipfile.ZipFile(output_file, 'w', compression=zipfile.ZIP_STORED) as zipf:
            for root, dirs, files in os.walk(folder_path):
                for file in files:
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, Files_Directory)
                    zipf.write(file_path, arcname)

        #print(f"✅ Đã nén: {output_file}")
        shutil.rmtree(folder_path)
shutil.rmtree(Files_Directory)


with zipfile.ZipFile(f'{pack_name}/Resources/1.58.1/Ages/Prefab_Characters/Prefab_Hero/CommonActions.pkg.bytes', 'w', compression=zipfile.ZIP_STORED) as zipf:
    for root, dirs, files in os.walk(f'{pack_name}/Resources/1.58.1/Ages/Prefab_Characters/Prefab_Hero/mod1'):
        for file in files:
            file_path = os.path.join(root, file)
            arcname = os.path.relpath(file_path, f'{pack_name}/Resources/1.58.1/Ages/Prefab_Characters/Prefab_Hero/mod1')  # giữ cả đường dẫn từ mod1/
            zipf.write(file_path, arcname)
shutil.rmtree(f'{pack_name}/Resources/1.58.1/Ages/Prefab_Characters/Prefab_Hero/mod1')
shutil.rmtree('Prefab_Hero')
for folder_name in os.listdir(f'{pack_name}/Resources/1.58.1/Prefab_Characters/mod/Prefab_Hero'):
    full_path = os.path.join(f'{pack_name}/Resources/1.58.1/Prefab_Characters/mod/Prefab_Hero', folder_name)

    if not os.path.isdir(full_path) or "_" not in folder_name:
        continue

    try:
        hero_id = folder_name.split("_")[0]
        zip_file_name = f"Actor_{hero_id}_Infos.pkg.bytes"
        zip_file_path = os.path.join(f'{pack_name}/Resources/1.58.1/Prefab_Characters/mod/Prefab_Hero', zip_file_name)

        with zipfile.ZipFile(zip_file_path, 'w', compression=zipfile.ZIP_STORED) as zipf:
            for root, _, files in os.walk(full_path):
                for file in files:
                    file_path = os.path.join(root, file)
                    rel_path = os.path.relpath(file_path, full_path)  # ✅ Thêm dòng này
                    arcname = os.path.join("Prefab_Hero", folder_name, rel_path)
                    zipf.write(file_path, arcname)

    except Exception as e:
        print(f"❌ Lỗi khi nén {folder_name}: {e}")

for idx, (ten_skin, skin_id_input) in enumerate(zip(TENSKIN, IDMODSKIN), start=1):

    print(f"\n🛠️ [{idx}] {ten_skin} ({skin_id_input})")
    print("───────────────────────────────────────────────")

    print("📄 Danh sách file XML đã mod:")
    print(f"   └─ {os.path.basename(file)}")

    print("\n🔊 File âm thanh đã mod:")
    print(f"   └─ {os.path.basename(sound_file_name)}")

    print("\n🎯 File Skill :")
    print(f"   └─ {os.path.basename(file_mod_skill1)}")
    print(f"   └─ {os.path.basename(file_mod_skill2)}")

    print("\n🎬 File Motion :")
    print(f"   └─ {os.path.basename(file_mod_Modtion)}")

    print("\n📦 File Actions :")
    print(f"   └─ {os.path.basename(output_file)}")

    print("\n🗂️ File Back.xml :")
    print(f"   └─ Back.xml")

    print("\n🧩 File Infos :")
    print(f"   └─ {os.path.basename(newpath)}")

    print("\n" + "-" * 50)
