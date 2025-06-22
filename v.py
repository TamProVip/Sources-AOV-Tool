import os; import re; import getopt; import random; import pyzstd; from xml.dom import minidom; from colorama import Fore; import sys; import shutil; import zipfile; import uuid; from collections import Counter; import xml.etree.ElementTree as ET

with open("ZSTD_DICT.xml", 'rb') as f:
    ZSTD_DICT = f.read()
ZSTD_LEVEL = 1

def giai(a):
    if os.path.isdir(a):
        for root, dirs, files in os.walk(a):
            if 'imprint' in root.lower():
                continue
            for file in files:
                file_path = os.path.join(root, file)
                _giaima_file(file_path)
    else:
        if 'imprint' not in a.lower():
            _giaima_file(a)

def _giaima_file(filepath):
    try:
        if not os.path.isfile(filepath):
            return

        with open(filepath, "rb") as f:
            input_blob = f.read()

        if b'"Jg' in input_blob or b"<?xml" in input_blob:
            return
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
            pass

    except Exception as e:
        pass

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
    #sys.exit()

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
    aaabbbcccnnn = pack_name
    ten_final = pack_name
    with open('List.txt', 'a', encoding='utf8') as f: 
        f.write(pack_name + '\n')

print(Fore.YELLOW + '-' * 50 + Fore.RESET)
if len(DANHSACH) >= 1:
    pack_name = input("Nhập Tên Pack Skin: ")
    os.mkdir(pack_name)
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
icon154 = b'q\x03\x00\x00(<\x00\x00\x9a\x00\x00\x00\x14\x00\x00\x00E2B78973E5DA0F49_##\x00\x00\x00\x00\x00\x14\x00\x00\x0020ACB10A3F5C4B9A_##\x00\x07\x00\x00\x00301540\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\n\x00\x00\x00\n\x00\x00\x00{\x02\x00\x00\x10\x00\x00\x00Share_15412.jpg\x00\x10\x00\x00\x00Share_15412.jpg\x00\x10\x00\x00\x00Share_15412.jpg\x00\n\x00\x00\x0015412.jpg\x00\x08\x00\x00\x00\x10\x00\x00\x00Skin_Icon_Model\x00\x14\x00\x00\x005AFB0F28AFD223F5_##\x00\x10\x00\x00\x00Skin_Icon_Skill\x00\x14\x00\x00\x0053AF2640805E7163_##\x00\x13\x00\x00\x00Skin_Icon_Dialogue\x00\x14\x00\x00\x00BF08C3E00D2DC1EC_##\x00\x16\x00\x00\x00Skin_Icon_SoundEffect\x00\x14\x00\x00\x00727C8C77DC33BCAB_##\x00\x15\x00\x00\x00Skin_Icon_Atmosphere\x00\x14\x00\x00\x0082D4F38570FF05F5_##\x00\x14\x00\x00\x00Skin_Icon_Animation\x00\x14\x00\x00\x002048DFA5BAFC6E13_##\x00\x15\x00\x00\x00Skin_Icon_BackToTown\x00\x14\x00\x00\x00BFB1C5549350A312_##\x00\x14\x00\x00\x00Skin_Icon_HeadFrame\x00\x14\x00\x00\x005CF3DDF4FFF3F0A7_##\x00\x01\x00\x00\x00\x00\x01\x00\x00\x00\x00\x01\x00\x00\x00\x00\x01\x00\x00\x00\x00%\x00\x00\x00BG_Yena_15413/BG_Commons_01_Platform\x00\x01\x00\x00\x00\x00\x01\x00\x00\x00\x00\x01\x00\x00\x00\x00\n\x00\x00\x00\n\x00\x00\x00\x01\x00\x00\x00\x00\x01\x00\x00\x00\x00\x01\x00\x00\x00\x00\x01\x00\x00\x00\x00\x01\x00\x01\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x02\x01\xa6\t\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x12\x00\x00\x003015412_B43_1.jpg\x00\x10\x00\x00\x003015412head.jpg\x00\x0e\x00\x00\x00Hero_1540.png\x00\x01\x01\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\x01\x00\x00\x00\x00\x01\x00\x00\x00\x00\x01\x00\x00\x00\x00'
icon154fix = b'^\x03\x00\x00(<\x00\x00\x9a\x00\x00\x00\x14\x00\x00\x00E2B78973E5DA0F49_##\x00\x00\x00\x00\x00\x14\x00\x00\x0020ACB10A3F5C4B9A_##\x00\x07\x00\x00\x00301540\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\n\x00\x00\x00\n\x00\x00\x00{\x02\x00\x00\x10\x00\x00\x00Share_15412.jpg\x00\x10\x00\x00\x00Share_15412.jpg\x00\x10\x00\x00\x00Share_15412.jpg\x00\n\x00\x00\x0015412.jpg\x00\x08\x00\x00\x00\x10\x00\x00\x00Skin_Icon_Model\x00\x14\x00\x00\x005AFB0F28AFD223F5_##\x00\x10\x00\x00\x00Skin_Icon_Skill\x00\x14\x00\x00\x0053AF2640805E7163_##\x00\x13\x00\x00\x00Skin_Icon_Dialogue\x00\x14\x00\x00\x00BF08C3E00D2DC1EC_##\x00\x16\x00\x00\x00Skin_Icon_SoundEffect\x00\x14\x00\x00\x00727C8C77DC33BCAB_##\x00\x15\x00\x00\x00Skin_Icon_Atmosphere\x00\x14\x00\x00\x0082D4F38570FF05F5_##\x00\x14\x00\x00\x00Skin_Icon_Animation\x00\x14\x00\x00\x002048DFA5BAFC6E13_##\x00\x15\x00\x00\x00Skin_Icon_BackToTown\x00\x14\x00\x00\x00BFB1C5549350A312_##\x00\x14\x00\x00\x00Skin_Icon_HeadFrame\x00\x14\x00\x00\x005CF3DDF4FFF3F0A7_##\x00\x01\x00\x00\x00\x00\x01\x00\x00\x00\x00\x01\x00\x00\x00\x00\x01\x00\x00\x00\x00%\x00\x00\x00BG_Yena_15413/BG_Commons_01_Platform\x00\x01\x00\x00\x00\x00\x01\x00\x00\x00\x00\x01\x00\x00\x00\x00\n\x00\x00\x00\n\x00\x00\x00\x01\x00\x00\x00\x00\x01\x00\x00\x00\x00\x01\x00\x00\x00\x00\x01\x00\x00\x00\x00\x01\x00\x01\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x02\x01\xa6\t\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x0c\x00\x00\x003015412.jpg\x00\x10\x00\x00\x003015412head.jpg\x00\x01\x00\x00\x00\x00\x01\x01\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\x01\x00\x00\x00\x00\x01\x00\x00\x00\x00\x01\x00\x00\x00\x00'
iconvalheinevo1 = b'\x13\x03\x00\x00\xff3\x00\x00\x85\x00\x00\x00\x14\x00\x00\x00F9B9135D9DECEB62_##\x00\x0b\x00\x00\x00\x14\x00\x00\x0075939F64822D8D0D_##\x00\x08\x00\x00\x003013311\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\n\x00\x00\x00\n\x00\x00\x00\x00\x00\x00\x00\x10\x00\x00\x00Share_13311.jpg\x00\x10\x00\x00\x00Share_13311.jpg\x00\x10\x00\x00\x00Share_13311.jpg\x00\n\x00\x00\x0013311.jpg\x00\x05\x00\x00\x00\x10\x00\x00\x00Skin_Icon_Model\x00\x14\x00\x00\x00D1188909BCF1A796_##\x00\x10\x00\x00\x00Skin_Icon_Skill\x00\x14\x00\x00\x008771C9DA02F4FEA6_##\x00\x16\x00\x00\x00Skin_Icon_SoundEffect\x00\x14\x00\x00\x008D69A8C30826E8D2_##\x00\x13\x00\x00\x00Skin_Icon_Dialogue\x00\x14\x00\x00\x006740D42BD5B8DAF3_##\x00\x15\x00\x00\x00Skin_Icon_Atmosphere\x00\x14\x00\x00\x002231A8E028E42D2D_##\x00\x15\x00\x00\x00Skin_Icon_BackToTown\x00\x14\x00\x00\x00D74BB3893108A06A_##\x00\x01\x00\x00\x00\x00\x01\x00\x00\x00\x00\x01\x00\x00\x00\x00\x01\x00\x00\x00\x00\x01\x00\x00\x00\x00\x01\x00\x00\x00\x00\x01\x00\x00\x00\x00\x01\x00\x00\x00\x00%\x00\x00\x00BG_Commons_01/BG_Commons_01_Platform\x00\x01\x00\x00\x00\x00\x01\x00\x00\x00\x00\x01\x00\x00\x00\x00\n\x00\x00\x00\n\x00\x00\x00\x01\x00\x00\x00\x00\x01\x00\x00\x00\x00\x01\x00\x00\x00\x00\x01\x00\x00\x00\x00\x01\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x02\x01x\n\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x0c\x00\x00\x003013311.jpg\x00\x10\x00\x00\x003013311head.jpg\x00\x01\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\x01\x00\x00\x00\x00\x01\x00\x00\x00\x00\x01\x00\x00\x00\x00'
iconvalheinevo5 = b'/\x03\x00\x00\xff3\x00\x00\x85\x00\x00\x00\x14\x00\x00\x00F9B9135D9DECEB62_##\x00\x0b\x00\x00\x00\x14\x00\x00\x0075939F64822D8D0D_##\x00\n\x00\x00\x003013311_2\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\n\x00\x00\x00\n\x00\x00\x00\x00\x00\x00\x00\x12\x00\x00\x00Share_13311_2.jpg\x00\x12\x00\x00\x00Share_13311_2.jpg\x00\x12\x00\x00\x00Share_13311_2.jpg\x00\x0c\x00\x00\x0013311_2.jpg\x00\x05\x00\x00\x00\x10\x00\x00\x00Skin_Icon_Model\x00\x14\x00\x00\x00D1188909BCF1A796_##\x00\x10\x00\x00\x00Skin_Icon_Skill\x00\x14\x00\x00\x008771C9DA02F4FEA6_##\x00\x16\x00\x00\x00Skin_Icon_SoundEffect\x00\x14\x00\x00\x008D69A8C30826E8D2_##\x00\x13\x00\x00\x00Skin_Icon_Dialogue\x00\x14\x00\x00\x006740D42BD5B8DAF3_##\x00\x15\x00\x00\x00Skin_Icon_Atmosphere\x00\x14\x00\x00\x002231A8E028E42D2D_##\x00\x15\x00\x00\x00Skin_Icon_BackToTown\x00\x14\x00\x00\x00D74BB3893108A06A_##\x00\x01\x00\x00\x00\x00\x01\x00\x00\x00\x00\x01\x00\x00\x00\x00\x01\x00\x00\x00\x00\x01\x00\x00\x00\x00\x01\x00\x00\x00\x00\x01\x00\x00\x00\x00\x01\x00\x00\x00\x003\x00\x00\x00BG_DiRenJie_13312_T3/BG_yinyingzhishou_01_platform\x00\x01\x00\x00\x00\x00\x01\x00\x00\x00\x00\x01\x00\x00\x00\x00\n\x00\x00\x00\n\x00\x00\x00\x01\x00\x00\x00\x00\x01\x00\x00\x00\x00\x01\x00\x00\x00\x00\x01\x00\x00\x00\x00\x01\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x02\x01x\n\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x0e\x00\x00\x003013311_2.jpg\x00\x12\x00\x00\x003013311_1head.jpg\x00\x01\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\x01\x00\x00\x00\x00\x01\x00\x00\x00\x00\x01\x00\x00\x00\x00'
bacvalheinevo1 = b'\r\x01\x00\x00\xff3\x00\x00\x85\x00\x00\x00\x14\x00\x00\x00D898FD6DC80FD88F_##\x00\x0b\x00\x00\x00\x14\x00\x00\x0062C20D284D202339_##\x00\x14\x00\x00\x00105E41477A829A72_##\x00\x01\x01\x00\x00\x00\x00\x01\x00\x00\x00\x00\n\x00\x00\x0013311.png\x00\x00\x00\x01\x00\x00\x00\x00\x00\xc7\x00\x00\x00\x00\x00\x00\x00\x00\x00L\x02\x00\x00\x00\x00\x00\x00\x00\x00\x00\xc4\x0b=\x00\x00\xf7\x07\x02\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x0f\x00\x00\x0020220902000000\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xdd\x83\x01\x00\x01\x01\x00\x00\x06,\x00\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x03\x00\x00\x00\x00\x01\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00'
bacvalheinevo5 = b'\x15\x01\x00\x00\xff3\x00\x00\x85\x00\x00\x00\x14\x00\x00\x000B0B75B334002849_##\x00\x0b\x00\x00\x00\x14\x00\x00\x006B7679BBD5264133_##\x00\x14\x00\x00\x00942E74C2AD28AE4C_##\x00\x01\x01\x00\x00\x00\x00\x01\x00\x00\x00\x00\x12\x00\x00\x00Awake_Label_5.png\x00\x01\x00\x01\x00\x00\x00\x00\x01\xc7\x00\x00\x00\x00\x00\x00\x00\x00\x00L\x02\x00\x00\x00\x00\x01\x00\x00\x00\x00\x8a\t=\x00\x00\x9f\x8c\x02\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x0f\x00\x00\x0020210318060000\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x17\x86\x01\x00\x01\x01\x00\x00\x06:\x00\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x03\x00\x00\x00\x00\x01\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00'
iconngokhongevo1 = b'\\\x03\x00\x00CA\x00\x00\xa7\x00\x00\x00\x14\x00\x00\x00EBC0C74462FF4B6A_##\x00\x07\x00\x00\x00\x14\x00\x00\x00DDB8BB646733B67E_##\x00\x07\x00\x00\x00301677\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\n\x00\x00\x00\n\x00\x00\x00\x00\x00\x00\x00\x10\x00\x00\x00Share_16707.jpg\x00\x10\x00\x00\x00Share_16707.jpg\x00\x10\x00\x00\x00Share_16707.jpg\x00\n\x00\x00\x0016707.jpg\x00\x08\x00\x00\x00\x10\x00\x00\x00Skin_Icon_Model\x00\x14\x00\x00\x008407CA15068FFAAA_##\x00\x14\x00\x00\x00Skin_Icon_Animation\x00\x14\x00\x00\x00C35E60871AB1288B_##\x00\x15\x00\x00\x00Skin_Icon_Atmosphere\x00\x14\x00\x00\x007CD9214682BAB4D9_##\x00\x15\x00\x00\x00Skin_Icon_BackToTown\x00\x14\x00\x00\x0030F7AD035D47227A_##\x00\x10\x00\x00\x00Skin_Icon_Skill\x00\x14\x00\x00\x00B64FCE08AE9DDFE5_##\x00\x16\x00\x00\x00Skin_Icon_SoundEffect\x00\x14\x00\x00\x0051BF047372097407_##\x00\x13\x00\x00\x00Skin_Icon_Dialogue\x00\x14\x00\x00\x00E51142379BF893FC_##\x00\x14\x00\x00\x00Skin_Icon_HeadFrame\x00\x14\x00\x00\x00B68080AD661210A0_##\x00\x01\x00\x00\x00\x00\x01\x00\x00\x00\x00\x01\x00\x00\x00\x00\x01\x00\x00\x00\x00%\x00\x00\x00BG_Commons_01/BG_Commons_01_Platform\x00\x01\x00\x00\x00\x00\x01\x00\x00\x00\x00\x01\x00\x00\x00\x00\n\x00\x00\x00\n\x00\x00\x00\x01\x00\x00\x00\x00\x01\x00\x00\x00\x00\x01\x00\x00\x00\x00\x01\x00\x00\x00\x00\x01\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x02\x01N\t\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x0b\x00\x00\x00301677.jpg\x00\x0f\x00\x00\x00301677head.jpg\x00\x01\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\x01\x00\x00\x00\x00\x01\x00\x00\x00\x00\x01\x00\x00\x00\x00'
iconngokhongevo5 = b'r\x03\x00\x00CA\x00\x00\xa7\x00\x00\x00\x14\x00\x00\x00EBC0C74462FF4B6A_##\x00\x07\x00\x00\x00\x14\x00\x00\x00DDB8BB646733B67E_##\x00\t\x00\x00\x00301677_2\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\n\x00\x00\x00\n\x00\x00\x00\x00\x00\x00\x00\x12\x00\x00\x00Share_16707_2.jpg\x00\x12\x00\x00\x00Share_16707_2.jpg\x00\x12\x00\x00\x00Share_16707_2.jpg\x00\x0c\x00\x00\x0016707_2.jpg\x00\x08\x00\x00\x00\x10\x00\x00\x00Skin_Icon_Model\x00\x14\x00\x00\x008407CA15068FFAAA_##\x00\x14\x00\x00\x00Skin_Icon_Animation\x00\x14\x00\x00\x00C35E60871AB1288B_##\x00\x15\x00\x00\x00Skin_Icon_Atmosphere\x00\x14\x00\x00\x007CD9214682BAB4D9_##\x00\x15\x00\x00\x00Skin_Icon_BackToTown\x00\x14\x00\x00\x0030F7AD035D47227A_##\x00\x10\x00\x00\x00Skin_Icon_Skill\x00\x14\x00\x00\x00B64FCE08AE9DDFE5_##\x00\x16\x00\x00\x00Skin_Icon_SoundEffect\x00\x14\x00\x00\x0051BF047372097407_##\x00\x13\x00\x00\x00Skin_Icon_Dialogue\x00\x14\x00\x00\x00E51142379BF893FC_##\x00\x14\x00\x00\x00Skin_Icon_HeadFrame\x00\x14\x00\x00\x00B68080AD661210A0_##\x00\x01\x00\x00\x00\x00\x01\x00\x00\x00\x00\x01\x00\x00\x00\x00\x01\x00\x00\x00\x00-\x00\x00\x00BG_wukongjuexing2/BG_wukongjuexing2_Platform\x00\x01\x00\x00\x00\x00\x01\x00\x00\x00\x00\x01\x00\x00\x00\x00\n\x00\x00\x00\n\x00\x00\x00\x01\x00\x00\x00\x00\x01\x00\x00\x00\x00\x01\x00\x00\x00\x00\x01\x00\x00\x00\x00\x01\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x02\x01N\t\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\r\x00\x00\x00301677_2.jpg\x00\x11\x00\x00\x00301677_2head.jpg\x00\x01\x00\x00\x00\x00\x01\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\x01\x00\x00\x00\x00\x01\x00\x00\x00\x00\x01\x00\x00\x00\x00'
bacngokhongevo1 = b'CA\x00\x00\xa7\x00\x00\x00\x14\x00\x00\x000B0B75B334002849_##\x00\x07\x00\x00\x00\x14\x00\x00\x006B7679BBD5264133_##\x00\x14\x00\x00\x00942E74C2AD28AE4C_##\x00\x01\x01\x00\x00\x00\x00\x01\x00\x00\x00\x00\x12\x00\x00\x00Awake_Label_1.png'    
bacngokhongevo5 = b'CA\x00\x00\xa7\x00\x00\x00\x14\x00\x00\x000B0B75B334002849_##\x00\x07\x00\x00\x00\x14\x00\x00\x006B7679BBD5264133_##\x00\x14\x00\x00\x00942E74C2AD28AE4C_##\x00\x01\x01\x00\x00\x00\x00\x01\x00\x00\x00\x00\x12\x00\x00\x00Awake_Label_5.png'

#-----------------------------------------------
for IDMODSKIN in IDMODSKIN:
    index = DANHSACH.index(IDMODSKIN)
    TENSKIN_NOW = TENSKIN[index] 
    print('-' * 53)
    print(f"{TENSKIN_NOW:^53}")
    print('-' * 53)
    SKINEOV = ''
    if IDMODSKIN == '13311':
        SKINEOV = "r"
    if IDMODSKIN == '16707':
        SKINEOV = "b"
    if IDMODSKIN == '15412':
        SKINEOV = "y"
    if IDMODSKIN == '51015':
        SKINEOV = "l"

    nhap_id = IDMODSKIN
    IDCHECK = IDMODSKIN
    IDSOUND_S = IDMODSKIN
    phukien = ''
    phukienv = ''

    if IDCHECK == '52007':
        phukien1 = input(
            '\033[1;97m[\033[1;91m?\033[1;97m] Mod Component:\n'
            '\033[1;97m [1] \033[1;92mGreen\n'
            '\033[1;97m [2] \033[1;92mRed\n'
            '\033[1;97m [3] \033[1;92mNo Mod Component\n'
            '\033[1;97m[•] INPUT: '
        )
        if phukien1 == "1":
            phukien = 'xanh'
        if phukien1 == "2":
            phukien = 'do'

    if IDCHECK == '13311':
        phukien1v = '3' 
        if phukien1v == "1":
            phukienv = 'vangv'
        if phukien1v == "2":
            phukienv = 'dov'

    if IDCHECK in ["16707"]:
        duongdan = file_actor_mod
        try:
            with open(duongdan, 'rb') as f:
                codenew = f.read()
            codenew = codenew.replace(iconngokhongevo1, iconngokhongevo5)
            with open(duongdan, 'wb') as f:
                f.write(codenew)
        except:
            pass

        duongdan2 = file_shop_mod
        try:
            with open(duongdan2, 'rb') as f:
                codenew = f.read()
            codenew = codenew.replace(bacngokhongevo1, bacngokhongevo5)
            with open(duongdan2, 'wb') as f:
                f.write(codenew)
        except:
            pass

    ID = IDCHECK
    IDB = int(ID).to_bytes(4, byteorder="little")
    IDH = int(ID[0:3]).to_bytes(4, byteorder="little")
    Files = [file_actor_mod, file_shop_mod]

    for File in Files:
        All = []
        Skin = ""
        with open(File, "rb") as file:
            Code = file.read()

        Find = -10
        while True:
            Find = Code.find(b"\x00\x00" + IDH, Find + 10)
            if Find == -1:
                break
            elif str(int.from_bytes(Code[Find - 2:Find], byteorder="little"))[0:3] == ID[0:3]:
                VT2 = int.from_bytes(Code[Find - 6:Find - 4], byteorder="little")
                Code2 = Code[Find - 6:Find - 6 + VT2]
                All.append(Code2)
                if Code2.find(IDB) != -1:
                    Skin = Code2

        if Skin == "":
            IDNew = IDCHECK[:3] + "00"
            IDK = int(IDNew).to_bytes(4, byteorder="little")
            IDH2 = int(IDNew[0:3]).to_bytes(4, byteorder="little")
            Find = Code.find(IDK + IDH2)
            Sum = int.from_bytes(Code[Find - 4:Find - 2], byteorder="little")
            Skin = Code[Find - 4:Find - 4 + Sum]

        for Id in All:
            Cache = Skin.replace(Skin[4:6], Id[4:6], 1)
            Cache = Cache.replace(Cache[35:44], Id[35:40] + Cache[40:44], 1)

            Hero = hex(int(ID[0:3]))[2:]
            if len(Hero) == 3:
                Hero = Hero[1:3] + "0" + Hero[0]
            else:
                Hero += "00"
            Hero += "0000"
            Hero = bytes.fromhex(Hero)
            Cache = Cache.replace(Cache[8:12], Hero, 1)

            if File == Files[0] and Id == All[0]:
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

                EndTheCode = hex(len(Cache))
                if len(EndTheCode) == 5:
                    EndTheCode = EndTheCode[3:5] + "0" + EndTheCode[2:3]
                else:
                    EndTheCode = EndTheCode[4:6] + EndTheCode[2:4]
                EndTheCode = bytes.fromhex(EndTheCode)
                Cache = Cache.replace(Cache[0:2], EndTheCode, 1)

            Code = Code.replace(Id, Cache, 1)

            dieukienmod1 = [Cache]
            for dieukienmod2 in dieukienmod1:
                if b"Hero" in dieukienmod2:
                    dieukienmod = dieukienmod2

        with open(File, "wb") as file:
            file.write(Code)
    if len(IDMODSKIN1) == 1:
        if b'Skin_Icon_HeadFrame' in dieukienmod:
            chedovien='1'
            if chedovien == '1':
                data = dieukienmod
                target = b'\x00\x00\x10\x00\x00\x00Share_'+IDCHECK.encode()+b'.jpg'
                index = data.find(target) - 2
                two_bytes_before = data[index:index+2]
                print(two_bytes_before)
            if chedovien == '2':
                idvien=input('viền cần mod : ')
                two_bytes_before=bytes.fromhex(str(idvien))
            if two_bytes_before != b'\x00\x00':
                if chedovien in ['1', '2']:

                    inp=file_mod_vien
                    with open(inp,'rb') as f:
                        ab=f.read()
                    a=two_bytes_before
                    i=ab.find(a)-4
                    vt=ab[i:i+4]
                    vtr=int.from_bytes(vt,byteorder='little')
                    vt1=ab[i:i+vtr]
                    print(f"[vt1 block hex] {vt1.hex()}")
                    
                    id2='6500'
                    a1=bytes.fromhex(str(id2))
                    f.close()
                    i1=ab.find(a1)-4
                    vt11=ab[i1:i1+4]
                    vtr1=int.from_bytes(vt11,byteorder='little')
                    print(f"[vt2] offset = {i1}, length = {vtr1}")
                    vt2=ab[i1:i1+vtr1]
                    print(f"[vt2 block hex] {vt2.hex()}")
                    vt1=vt1.replace(a,a1)
                    print(f"[vt1_new] Modified block size: {len(vt1)}")
                    vt11=ab.replace(vt2,vt1)
                    print(f"[ab check] vt2 exists after replace: {vt2 in vt11}")
                    print(f"[count vt2] Leftover count: {vt11.count(vt2)}")
                    with open(inp,'wb') as go:
                        go.write(vt11)
            else:
                print('không tìm thấy viền (vui lòng nhập thủ công)')


    print('[✓] Âm Thanh Databin')
    if IDCHECK == "53002" or b"Skin_Icon_SoundEffect" in dieukienmod or b"Skin_Icon_Dialogue" in dieukienmod:
        skin_id_input = IDMODSKIN
        sound_directory = Sound_Files
        sound_files = os.listdir(sound_directory)

        all_skin_ids = []
        for i in range(21):
            i_str = f"{i:02d}"  # 00 -> 20
            all_skin_ids.append(b"\x00" + int(skin_id_input[:3] + i_str).to_bytes(4, "little"))

        initial_skin_id = all_skin_ids[0]
        selected_skin_id = all_skin_ids[int(skin_id_input[3:])]

        all_skin_ids.remove(selected_skin_id)
        all_skin_ids.remove(initial_skin_id)

        for sound_file_name in sound_files:
            with open(os.path.join(sound_directory, sound_file_name), "rb") as sound_file:
                sound_data = sound_file.read()

            # ID đặc biệt 13311
            if skin_id_input == "13311":
                if sound_file_name == 'BattleBank.bytes':
                    sound_data = sound_data.replace(b'\x9dO\x14', b'\xff3\x00').replace(b'\x9eO\x14', b'\xff3\x00').replace(b'\x9fO\x14', b'\xff3\x00').replace(b'\xa0O\x14', b'\xff3\x00')
                if sound_file_name == 'ChatSound.bytes':
                    sound_data = sound_data.replace(b'\x9fO\x14', b'\xff3\x00')
                if sound_file_name == 'HeroSound.bytes':
                    sound_data = sound_data.replace(b'\x9fO\x14', b'\xff3\x00').replace(b'\xa0O\x14', b'\xff3\x00')
                if sound_file_name == 'LobbyBank.bytes':
                    sound_data = sound_data.replace(b'\xa0O\x14', b'\xff3\x00')
                if sound_file_name == 'LobbySound.bytes':
                    sound_data = sound_data.replace(b'\xa0O\x14', b'\xff3\x00')

            # ID đặc biệt 16707
            if skin_id_input == "16707":
                if sound_file_name == 'BattleBank.bytes':
                    sound_data = sound_data.replace(b'/~\x19', b'CA\x00').replace(b'0~\x19', b'CA\x00').replace(b'1~\x19', b'CA\x00')
                if sound_file_name == 'ChatSound.bytes':
                    sound_data = sound_data.replace(b'0~\x19', b'CA\x00')
                if sound_file_name == 'HeroSound.bytes':
                    sound_data = sound_data.replace(b'0~\x19', b'CA\x00').replace(b'1~\x19', b'CA\x00')
                if sound_file_name == 'LobbyBank.bytes':
                    sound_data = sound_data.replace(b'0~\x19', b'CA\x00')
                if sound_file_name == 'LobbySound.bytes':
                    sound_data = sound_data.replace(b'0~\x19', b'CA\x00')

            # Xóa các skin ID khác
            if sound_file_name != "CoupleSound.bytes":
                for skin_id in all_skin_ids:
                    skin_id += b"\x00" * 8
                    sound_data = sound_data.replace(skin_id, b"\x0000" + b"\x00" * 10)
            else:
                for skin_id in all_skin_ids:
                    skin_id += b"\x02\x00\x00\x00\x01"
                    sound_data = sound_data.replace(skin_id, b"\x0000\x00\x00\x02\x00\x00\x00\x01")

            # Gắn skin mới vào
            if selected_skin_id in sound_data:
                if sound_file_name != "CoupleSound.bytes":
                    sound_data = sound_data.replace(initial_skin_id + b"\x00" * 8, b"\x0000" + b"\x00" * 10)
                    sound_data = sound_data.replace(selected_skin_id + b"\x00" * 8, initial_skin_id + b"\x00" * 8)
                else:
                    sound_data = sound_data.replace(initial_skin_id + b"\x02\x00\x00\x00\x01", b"\x0000\x00\x00\x02\x00\x00\x00\x01")
                    sound_data = sound_data.replace(selected_skin_id + b"\x02\x00\x00\x00\x01", initial_skin_id + b"\x02\x00\x00\x00\x01")

            # Ghi lại file
            with open(os.path.join(sound_directory, sound_file_name), "wb") as sound_file:
                sound_file.write(sound_data)
            
            # In từng file
            print(f"     Sound: {sound_file_name}  Done")
        #print("-"*53)
    print(f"{'+ Trạng Thái Mod':<25}")
    if IDCHECK == "53002" or b"Skin_Icon_Skill" in dieukienmod or b"Skin_Icon_BackToTown" in dieukienmod:
        file_paths = [file_mod_skill1, file_mod_skill2]
        matching_files = []
        user_id = IDMODSKIN
        user_id_bytes = bytes(f"fects/{user_id[0:3]}_", "utf8")

        for file in file_paths:
            if user_id_bytes in open(file, "rb").read():
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
    #print('-'*53)
    print(f"    Mod Skill Effect ID: {user_id}")
    if matching_files:
        for file in matching_files:
            print(f"   [-] {os.path.basename(file):<25} Done!")
    else:
        print("    [x] SkillMark Not Found")
        
    file_path = file_mod_Modtion
    skin_id = IDMODSKIN
    all_ids = []
    for i in range(21):
        if i < 10:
            all_ids.append(skin_id[0:3] + "0" + str(i))
        else:
            all_ids.append(skin_id[0:3] + str(i))

    all_patterns = []

    for id in all_ids:
        hex_id = hex(int(id))[2:]
        all_patterns.append(bytes.fromhex(f"{hex_id[2:4]}{hex_id[0:2]}0000"))

    with open(file_path, "rb") as file:
        file_start = file.read(140)
        all_codes = []
        while True:
            segment_length = file.read(2)
            if segment_length == b"":
                file.close()
                break
            segment_length_value = segment_length[0] + segment_length[1] * 256 + 2
            code = segment_length + file.read(segment_length_value)
            if all_patterns[all_ids.index(skin_id)] in code:
                all_codes.append(code)
            elif all_patterns[0] in code:
                all_codes.append(code)

    dance_codes = []
    dance_codes_database = []
    dance_codes_mod = []
    for code in all_codes:
        if code[0:2] in b"6\x00S\x00":
            dance_codes_database.append(code)
        else:
            dance_codes.append(code)
            dance_codes_mod.append(code)

    dance_selection = 0
    if len(dance_codes_database) > 1:
        dance_selection = int(1) - 1

    if len(dance_codes_database) > 0:
        selected_dance_code = dance_codes_database[dance_selection]
        dance_mod_id = selected_dance_code[21:25]
        for code in dance_codes:
            index = dance_codes.index(code)
            for pattern in all_patterns:
                position = code.find(pattern)
                if position != -1:
                    code_to_replace = code[position + 4:position + 8]
                    code = code.replace(code_to_replace, dance_mod_id, 1)
                else:
                    break
            dance_codes[index] = code
    else:
        for code in dance_codes:
            index = dance_codes.index(code)
            position_ref = code.find(all_patterns[all_ids.index(skin_id)])
            dance_mod_id = code[position_ref + 4:position_ref + 8]
            for pattern in all_patterns:
                position = code.find(pattern)
                if position != -1:
                    code_to_replace = code[position + 4:position + 8]
                    code = code.replace(code_to_replace, dance_mod_id, 1)
                else:
                    break
            dance_codes[index] = code

    with open(file_path, "rb") as file:
        content = file.read()
        file.close()

    for i in range(len(dance_codes_mod)):
        content = content.replace(dance_codes_mod[i], dance_codes[i], 1)

    if len(dance_codes) + len(dance_codes_database) == 0:
        for pattern in all_patterns:
            content = content.replace(pattern, b"00\x00\x00", 1)

    with open(file_path, "wb") as file:
        file.write(content)
    #print("—" * 53)
    print(f"    Mod Motion ID: {ID}")
#-----------------------------------------------
    zip_path = f'Resources/1.58.1/Ages/Prefab_Characters/Prefab_Hero/Actor_{IDMODSKIN[:3]}_Actions.pkg.bytes'
    Files_Directory_Path = f'{pack_name}/Resources/1.58.1/Ages/Prefab_Characters/Prefab_Hero/mod4/'
    print(f'    Skill Ages - Actor_{IDMODSKIN[:3]}_Actions.pkg.bytes')
    phukien = ""
    if IDMODSKIN == '52007':
        print(f"[✓] Chọn phụ kiện Veres ({IDMODSKIN}):")
        chon = input("1. Đỏ  |  2. Xanh: ").strip()
        if chon == "1":
            phukien = "do"
        elif chon == "2":
            phukien = "xanh"
        else:
            print("[-] Không dùng phụ kiện.")
    if IDMODSKIN == '13311':
        print(f"[✓] Chọn phụ kiện Veres ({IDMODSKIN}):")
        chon = input("1. Đỏ  |  2. Xanh: ").strip()
        if chon == "1":
            phukienv = "dov"
        elif chon == "2":
            phukien = "xanh"
        else:
            print("[-] Không dùng phụ kiện.")
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(Files_Directory_Path)

    NAME_HERO = next((name for name in os.listdir(Files_Directory_Path) if name.startswith(IDMODSKIN[:3] + "_")), None)
    if not NAME_HERO:
        print(f"❌ Không tìm thấy thư mục cho ID {IDMODSKIN}")
        continue

    Id_Skin = IDMODSKIN.encode()
    Name_Hero = NAME_HERO.encode()
    HD = b'n'
    Skins = b'y'

    FILES_XML = []
    for root, dirs, files in os.walk(Files_Directory_Path):
        for file in files:
            if file.endswith('.xml'):
                FILES_XML.append(os.path.join(root, file))

    for file_path in FILES_XML:
        giai(file_path)

        with open(file_path, 'rb') as f:
            All = f.read()

        if b'"Jg\x00' not in All:
            ListAll = All.split(b'\r\n')
            CODE_EFF = [x for x in ListAll if b'prefab_skill_effects/hero_skill_effects/' in x.lower()]
            if len(CODE_EFF) == 0:
                continue

            for text in CODE_EFF:
                if Id_Skin not in [b'13311', b'16707']:
                    text1 = re.sub(
                        re.escape(b"prefab_skill_effects/hero_skill_effects/" + Name_Hero + b'/'),
                        b"prefab_skill_effects/hero_skill_effects/" + Name_Hero + b'/' + Id_Skin + b'/',
                        text,
                        flags=re.IGNORECASE
                    )
                    text1 = text1.replace(b'/' + Id_Skin + b'/' + Id_Skin + b'/', b'/' + Id_Skin + b'/')
                else:
                    ID_EOV = Id_Skin + b'_5/'
                    text1 = re.sub(
                        re.escape(b"prefab_skill_effects/hero_skill_effects/" + Name_Hero + b'/'),
                        b"prefab_skill_effects/component_effects/" + Id_Skin + b'/' + ID_EOV,
                        text,
                        flags=re.IGNORECASE
                    )

                if HD == b'y':
                    text1 = text1.replace(b'" refParamName=""', b'.prefab" refParamName=""')
                    text1 = text1.replace(b'_E.prefab"', b'_E"').replace(b'_e.prefab"', b'_e"')
                    text1 = text1.replace(b'.prefab.prefab" refParamName=""', b'.prefab" refParamName=""')

                All = All.replace(text, text1)
            if Skins == b'y' and b'bUseTargetSkinEffect' not in All:
                new_lines = []
                for line in All.split(b'\r\n'):
                    new_lines.append(line)
                    if b'<String name="resourceName"' in line:
                        new_lines.append(b'        <int name="frameRate" value="120" refParamName="" useRefParam="false" />\n        <bool name="bUseTargetSkinEffect" value="true" refParamName="" useRefParam="false"/>')
                All = b'\r\n'.join(new_lines)

            
            # Regex linh hoạt: bắt <int ... name="skinId" ... value="16307" ... />
            CheckSkinIdTick = ('<int name="skinId" value="'+IDMODSKIN+'" refParamName="" useRefParam="false" />').encode()
            CheckSkinIdTick0 = ('<int name="skinId" value="'+IDMODSKIN[:3]+'00'+'" refParamName="" useRefParam="false" />').encode()
            if CheckSkinIdTick in All:
                All = All.replace(CheckSkinIdTick, CheckSkinIdTick0)
                print(f'  CheckSkinIdTick : {os.path.basename(file_path)}')
            All = All.replace(b'bAllowEmptyEffect" value="true"', b'bAllowEmptyEffect" value="false"')
            with open(file_path, 'wb') as f:
                f.write(All)
            AABBCC = 'YtbTâmModAOV'
#---------------—------------———----------------
            if IDMODSKIN == '10611' and 'U1B1.xml' in file_path:
                with open(file_path, 'rb') as f:
                    rpl = f.read()
                    rpl = re.sub(
                        br'<Condition id="[^"]+" guid="2e5f463f-105d-4143-b786-e59ea8b34fa2" status="true" />',
                        b'<!-- ' + AABBCC.encode('utf-8') + b' -->', rpl)
                with open(file_path, 'wb') as f:
                    f.write(rpl)
#---------------—------------———----------------
            if IDMODSKIN == '10611' and 'A3.xml' in file_path: 
                with open(file_path, 'rb') as f:
                    rpl = f.read().replace(b'<String name="clipName" value="Atk3"', b'<String name="clipName" value="Atk1"')
                with open(file_path, 'wb') as f:
                    f.write(rpl)
#---------------—------------———----------------
            if IDMODSKIN[:3] == '531' and '531gm.xml' in file_path and '53107_Back.xml' in file_path:
                with open(file_path, 'rb') as f:
                    rpl = f.read()
                    rpl = rpl.replace(b'531_Keera/53107/5318_Keera_S_LOD1', b'531_Keera/5318_Keera_S_LOD1')
                with open(file_path, 'wb') as f:
                    f.write(rpl)
#---------------—------------———----------------
            if IDMODSKIN[:3] == '531' and '531gm_1.xml' in file_path:
                with open(file_path, 'rb') as f:
                    rpl = f.read()
                    rpl = rpl.replace(b'531_Keera/53107/5318_Keera_LOD1', b'531_Keera/5318_Keera_LOD1')
                with open(file_path, 'wb') as f:
                    f.write(rpl)
#---------------—------------———----------------
            if IDMODSKIN == '11107' and 'death.xml' not in file_path.lower():
                with open(file_path, 'rb') as f:
                    rpl = f.read().replace(
                    b'<String name="clipName" value="',
                    b'<String name="clipName" value="11107/'
        )
                with open(file_path, 'wb') as f:
                    f.write(rpl)
#---------------—------------———----------------
            if IDMODSKIN == '15704' and 'death.xml' not in file_path.lower():
                with open(file_path, 'rb') as f:
                    rpl = f.read().replace(
                    b'<String name="clipName" value="',
                    b'<String name="clipName" value="15704/'
        )
                with open(file_path, 'wb') as f:
                    f.write(rpl)
#---------------—------------———----------------
            if IDMODSKIN[:3] == '521' and IDMODSKIN != '52108' and any(x in file_path for x in ['S1B3', 'S1B4']):
                with open(file_path, 'rb') as f:
                    rpl = f.read()
                    rpl = rpl.replace(b'Florentino_spell01_bullet03_2"', b'Florentino_spell01_bullet03"')
                    rpl = rpl.replace(b'Florentino_spell01_bullet03_fade_2"', b'Florentino_spell01_bullet03_fade"')
                    rpl = rpl.replace(b'Florentino_spell01_bullet03_2_e"', b'Florentino_spell01_bullet03_e"')
                    rpl = rpl.replace(b'Florentino_spell01_buff01_2"', b'Florentino_spell01_buff01"')
                    rpl = rpl.replace(b'Florentino_spell01_bullet03_3"', b'Florentino_spell01_bullet03"')
                    rpl = rpl.replace(b'Florentino_spell01_bullet03_fade_3"', b'Florentino_spell01_bullet03_fade"')
                    rpl = rpl.replace(b'Florentino_spell01_bullet03_3_e"', b'Florentino_spell01_bullet03_e"')
                    rpl = rpl.replace(b'Florentino_spell01_buff01_3"', b'Florentino_spell01_buff01"')

                with open(file_path, 'wb') as f:
                    f.write(rpl)
#---------------—------------———----------------
            if IDMODSKIN == '10603' and 'death.xml' not in file_path.lower():
                with open(file_path, 'rb') as f:
                    rpl = f.read().replace(
                    b'<String name="clipName" value="',
                    b'<String name="clipName" value="10603/'
        )
                with open(file_path, 'wb') as f:
                    f.write(rpl)
#---------------—------------———----------------
            if IDMODSKIN == '54402' and 'A4B1.xml' in file_path:
                with open(file_path, 'rb') as f:
                    rpl = f.read()
                    rpl = rpl.replace(b'prefab_skill_effects/hero_skill_effects/544_Painter/54402/Painter_Atk4_blue',b'prefab_skill_effects/hero_skill_effects/544_Painter/Painter_Atk4_blue').replace(b'prefab_skill_effects/hero_skill_effects/544_Painter/54402/Painter_Atk4_red',b'prefab_skill_effects/hero_skill_effects/544_Painter/Painter_Atk4_red')
                with open(file_path, 'wb') as f:
                    f.write(rpl)
#---------------—------------———----------------
            if IDMODSKIN == '15412' and 'P12E2.xml' in file_path:
                with open(file_path, 'rb') as f:
                    rpl = f.read()
                    rpl = rpl.replace(b'Prefab_Skill_Effects/Hero_Skill_Effects/154_HuaMuLan/15412/15413_HuaMuLan_Red', b'Prefab_Skill_Effects/Hero_Skill_Effects/154_HuaMuLan/15413_HuaMuLan_Red')
                with open(file_path, 'wb') as f:
                    f.write(rpl)
#---------------—------------———----------------
            if IDMODSKIN =='52007':
                if phukien == "do":
                    with open(file_path, 'rb') as f:
                        rpl = f.read().replace(b'prefab_skill_effects/hero_skill_effects/520_Veres/52007/',b'prefab_skill_effects/component_effects/52007/5200402/')
                    with open(file_path, 'wb') as f:
                        f.write(rpl)
                elif phukien == "xanh":
                    with open(file_path, 'rb') as f:
                        rpl = f.read().replace(
                b'prefab_skill_effects/hero_skill_effects/520_Veres/52007/',
                b'prefab_skill_effects/component_effects/52007/5200401/'
            )
                    with open(file_path, 'wb') as f:
                        f.write(rpl)
#---------------—------------———----------------
            if IDMODSKIN == '13011' and 'S2B2_13011' in file_path and 'S2B3_13011' in file_path and 'S2B1.xml' in file_path:
                with open(file_path, 'rb') as f:
                    rpl = f.read()
                    rpl = rpl.replace(
                    b'      <Event>', 
                    b'      </Event>\n      <SkinOrAvatarList id="13011"/>', 1)
                with open(file_path, 'wb') as f:
                    f.write(rpl)
#---------------—------------———----------------
            if IDMODSKIN == '13011' and 'A1.xml' in file_path:
                with open(file_path, 'rb') as f:
                    rpl = f.read()
                    rpl = rpl.replace(b'  </Action>', b'    <Track trackName="AnhYeuEm" eventType="GetHolidayResourcePathTick" guid="9e8a16b4-5d54-4b43-b149-8160e9054175" enabled="true" useRefParam="false" refParamName="" r="0.000" g="0.000" b="0.000" execOnForceStopped="false" execOnActionCompleted="false" stopAfterLastEvent="true">\n      <Condition id="25" guid="Cut" status="true"/>\n      <Event eventName="GetHolidayResourcePathTick" time="0.000" isDuration="false" guid="5f29c189-96ab-44ff-9fdc-82c83264c461">\n        <String name="holidayResourcePathPrefix" value="prefab_skill_effects/Inner_game_effect/returncity_holidays/holiday0/huijidi" refParamName="" useRefParam="false"/>\n        <String name="outPathParamName" value="AnhYeuEm" refParamName="" useRefParam="false"/>\n      </Event>\n    </Track>\n    <Track trackName="AnhYeuEm" eventType="GetHolidayResourcePathTick" guid="345352d8-7e2b-4e5c-98e1-e66c22f47551" enabled="true" useRefParam="false" refParamName="" r="0.000" g="0.000" b="0.000" execOnForceStopped="false" execOnActionCompleted="false" stopAfterLastEvent="true">\n      <Condition id="25" guid="Cut" status="true"/>\n      <Event eventName="GetHolidayResourcePathTick" time="0.000" isDuration="false" guid="7b59dc67-c1aa-4b8b-8643-01f4e0cc03fd">\n        <String name="holidayResourcePathPrefix" value="prefab_skill_effects/hero_skill_effects/130_GongBenWuZang/13011/huicheng_tongyong_01" refParamName="" useRefParam="false"/>\n        <String name="outPathParamName" value="AnhYeuEm" refParamName="" useRefParam="false"/>\n      </Event>\n    </Track>\n    <Track trackName="AnhYeuEm" eventType="GetHolidayResourcePathTick" guid="87f96f4c-55cd-4b02-813b-27e638fcae38" enabled="true" useRefParam="false" refParamName="" r="0.000" g="0.000" b="0.000" execOnForceStopped="false" execOnActionCompleted="false" stopAfterLastEvent="true">\n      <Condition id="26" guid="Cut" status="true"/>\n      <Event eventName="GetHolidayResourcePathTick" time="0.000" isDuration="false" guid="187465f4-e4e7-4c6d-9c38-add261d99fa9">\n        <String name="holidayResourcePathPrefix" value="prefab_skill_effects/hero_skill_effects/130_GongBenWuZang/13011/jiasu_tongyong_01" refParamName="" useRefParam="false"/>\n        <String name="outPathParamName" value="AnhYeuEm" refParamName="" useRefParam="false"/>\n      </Event>\n    </Track>\n  </Action>')
                with open(file_path, 'wb') as f:
                    f.write(rpl)
#---------------—------------———----------------
            if IDMODSKIN == '13011' and 'UCS.xml' in file_path:
                    with open(file_path, 'rb') as f: 
                        rpl = f.read().replace(b'  <Action tag="" length="0.600" loop="false">\r\n    <Track trackName="CameraShakeDuration0" eventType="CameraShakeDuration" guid="20c9a92f-6c8b-4320-bec5-eb48f5e4b418" enabled="true" useRefParam="false" refParamName="" r="0.000" g="0.000" b="0.000" execOnForceStopped="false" execOnActionCompleted="false" stopAfterLastEvent="true">\r\n      <Event eventName="CameraShakeDuration" time="0.000" length="0.600" isDuration="true" guid="54e19b05-d68f-4c09-90dd-4ad5d3422cae">\r\n        <bool name="useMainCamera" value="true" refParamName="" useRefParam="false" />\r\n        <bool name="filter_self" value="true" refParamName="" useRefParam="false" />\r\n        <bool name="canBeCover" value="false" refParamName="" useRefParam="false" />\r\n        <Vector3 name="shakeRange" x="0.200" y="0.400" z="0.200" refParamName="" useRefParam="false" />\r\n        <bool name="bUseCustomCurveMode" value="true" refParamName="" useRefParam="false" />\r\n        <String name="curvesPath" value="Prefab_Skill_Assets/CameraShakeCurves/nor04" refParamName="" useRefParam="false" />\r\n      </Event>\r\n    </Track>',b'  <Action tag="" length="1.000" loop="false">\r\n    <Track trackName="TriggerParticle0" eventType="TriggerParticle" guid="f7cc90e1-0903-43fb-91ec-7fa8e0998295" enabled="true" useRefParam="false" refParamName="" r="0.000" g="0.000" b="0.000" execOnForceStopped="false" execOnActionCompleted="false" stopAfterLastEvent="true">\r\n      <Event eventName="TriggerParticle" time="0.000" length="1.000" isDuration="true" guid="f720cf9e-c348-4163-a5e5-c13004eafd10">\r\n        <TemplateObject name="targetId" id="0" objectName="self" isTemp="false" refParamName="" useRefParam="false" />\r\n        <String name="resourceName" value="prefab_skill_effects/hero_skill_effects/130_gongbenwuzang/13011/gongbenwuzang_attack01_spell01_1" refParamName="" useRefParam="false" />\r\n        <Vector3 name="bindPosOffset" x="0.000" y="1.000" z="0.500" refParamName="" useRefParam="false" />\r\n        <Vector3i name="scalingInt" x="10000" y="10000" z="10000" refParamName="" useRefParam="false" />\r\n        <bool name="bUseRealScaling" value="true" refParamName="" useRefParam="false" />\r\n        <bool name="bOnlyFollowPos" value="true" refParamName="" useRefParam="false" />\r\n        <bool name="b1stTickParentRot" value="true" refParamName="" useRefParam="false" />\r\n        <String name="syncAnimationName" value="" refParamName="" useRefParam="false" />\r\n        <String name="customTagName" value="" refParamName="" useRefParam="false" />\r\n      </Event>\r\n    </Track>')
                    with open(file_path, 'wb') as f:
                         f.write(rpl)
#---------------—------------———----------------
            if IDMODSKIN == '13011' and "S2.xml" in file_path and "S21.xml" in file_path and "S22.xml" in file_path:
                with open(file_path, 'rb') as f: rpl = f.read().replace(b'"PlayAnimDuration" guid="9d243092-f160-4189-a9da-f132595032c9" enabled="true"',b'"PlayAnimDuration" guid="9d243092-f160-4189-a9da-f132595032c9" enabled="false"').replace(b'        <bool name="bEqual" value="true" refParamName="" useRefParam="false" />\r\n        <bool name="bSkipLogicCheck" value="false" refParamName="" useRefParam="false" />', b'').replace(b'        <bool name="bEqual" value="true" refParamName="" useRefParam="false" />\r\n        <bool name="bSkipLogicCheck" value="true" refParamName="" useRefParam="false" />', b'        <bool name="bSkipLogicCheck" value="true" refParamName="" useRefParam="false" />').replace(b'        <bool name="bEqual" value="false" refParamName="" useRefParam="false" />\r\n        <bool name="bSkipLogicCheck" value="false" refParamName="" useRefParam="false" />', b'     <bool name="bEqual" value="false" refParamName="" useRefParam="false" />').replace(b'        <bool name="useNegateValue" value="false" refParamName="" useRefParam="false" />\r\n        <Array name="skinIdArray" refParamName="" useRefParam="false" type="int" />\r\n      </Event>\r\n    </Track>', b'      </Event>\r\n    </Track>')
                with open(file_path, 'wb') as f:
                    f.write(rpl)
#---------------—------------———----------------
            if IDMODSKIN == '13011' and 'S2.xml' in file_path:
                with open(file_path, 'rb') as f: rpl = f.read().replace(b'    <Track trackName="13011_22" eventType="PlayAnimDuration" guid="346663c5-53c1-4f57-9196-8ea5aec7bafb" enabled="true" useRefParam="false" refParamName="" r="0.000" g="0.000" b="0.000" execOnForceStopped="false" execOnActionCompleted="false" stopAfterLastEvent="true">\r\n      <Condition id="5" guid="1d2453a9-f234-4489-90f4-dde12f642d17" status="true" />',b'    <Track trackName="13011_22" eventType="PlayAnimDuration" guid="346663c5-53c1-4f57-9196-8ea5aec7bafb" enabled="true" useRefParam="false" refParamName="" r="0.000" g="0.000" b="0.000" execOnForceStopped="false" execOnActionCompleted="false" stopAfterLastEvent="true">').replace(b'    <Track trackName="ChangeSpringDuration5" eventType="ChangeSpringDuration" guid="fc54f26a-3264-4759-b526-2609b8aa6fc0" enabled="true" useRefParam="false" refParamName="" r="0.000" g="0.000" b="0.000" execOnForceStopped="false" execOnActionCompleted="false" stopAfterLastEvent="true">\r\n      <Condition id="5" guid="1d2453a9-f234-4489-90f4-dde12f642d17" status="true" />', b'    <Track trackName="ChangeSpringDuration5" eventType="ChangeSpringDuration" guid="fc54f26a-3264-4759-b526-2609b8aa6fc0" enabled="true" useRefParam="false" refParamName="" r="0.000" g="0.000" b="0.000" execOnForceStopped="false" execOnActionCompleted="false" stopAfterLastEvent="true">')
                with open(file_path, 'wb') as f:
                    f.write(rpl)
#---------------—------------———----------------
            if IDMODSKIN == '13011' and 'S21.xml' in file_path:
                ABCD = []
                with open(file_path, 'rb') as file:
                    xml_bytes = file.read()#.decode('utf-8')
                    start_phrase = b'<Track trackName="'
                    end_phrase = b'</Track>' 
                    start_index = xml_bytes.find(start_phrase)
                    end_index = xml_bytes.find(end_phrase, start_index)
                    while start_index != -1 and end_index != -1:
                        track_text = xml_bytes[start_index:end_index + len(end_phrase)]
                        start_index = xml_bytes.find(start_phrase, end_index)
                        end_index = xml_bytes.find(end_phrase, start_index)
                        if b'a07302eb-cb3b-4146-9996-d018f92247aa' in track_text:
                            ABCD.append(track_text)
                                #print(track_text)
                                #track_text = track_text.encode()
                        
                for track_text in ABCD:
                    with open(file_path, 'rb') as file:
                        xml_bytes = file.read()
                    modified_data =b'    <Track trackName="\xe5\xa4\xa7\xe9\x83\xa8\xe5\x88\x86\xe7\x9a\xae\xe8\x82\xa4\xe7\x9a\x84\xe7\x89\xb9\xe6\x95\x88\xe5\xad\x90\xe5\xbc\xb91" eventType="SpawnBulletTick" guid="7255b095-38a9-420b-96c1-0fc359ef272d" enabled="true" useRefParam="false" refParamName="" r="0.000" g="0.000" b="0.000" execOnForceStopped="false" execOnActionCompleted="false" stopAfterLastEvent="true">\r\n      <Condition id="6" guid="6b3a8d20-c4c6-4d17-83e1-b60201720bb2" status="true" />\r\n      <Event eventName="SpawnBulletTick" time="0.000" isDuration="false" guid="0fe84e6b-f4b9-491b-a802-c85858c85dd3">\r\n        <TemplateObject name="targetId" id="0" objectName="self" isTemp="false" refParamName="" useRefParam="false" />\r\n        <String name="ActionName" value="prefab_characters/prefab_hero/130_gongbenwuzang/skill/UCS" refParamName="" useRefParam="false" />\r\n      </Event>\r\n    </Track>'
                    modified_data1 = xml_bytes.replace(track_text, modified_data)
                    with open(file_path, 'wb') as file:
                        file.write(modified_data1)
                with open(file_path, 'rb') as f: rpl = f.read().replace(b'    <Track trackName="13011_22" eventType="PlayAnimDuration" guid="346663c5-53c1-4f57-9196-8ea5aec7bafb" enabled="true" useRefParam="false" refParamName="" r="0.000" g="0.000" b="0.000" execOnForceStopped="false" execOnActionCompleted="false" stopAfterLastEvent="true">\r\n      <Condition id="5" guid="753f3471-d461-40e5-b0d9-9305c2d4615d" status="true" />',b'    <Track trackName="13011_22" eventType="PlayAnimDuration" guid="346663c5-53c1-4f57-9196-8ea5aec7bafb" enabled="true" useRefParam="false" refParamName="" r="0.000" g="0.000" b="0.000" execOnForceStopped="false" execOnActionCompleted="false" stopAfterLastEvent="true">').replace(b'prefab_skill_effects/hero_skill_effects/130_gongbenwuzang/13011/GongBenWuZang_attack01_spell01_2', b'Nhung').replace(b'    <Track trackName="ChangeSpringDuration6" eventType="ChangeSpringDuration" guid="6d7eb5bc-f19e-4c58-ac74-9ef746b58e86" enabled="true" useRefParam="false" refParamName="" r="0.000" g="0.000" b="0.000" execOnForceStopped="false" execOnActionCompleted="false" stopAfterLastEvent="true">\r\n      <Condition id="5" guid="753f3471-d461-40e5-b0d9-9305c2d4615d" status="true" />', b'    <Track trackName="ChangeSpringDuration6" eventType="ChangeSpringDuration" guid="6d7eb5bc-f19e-4c58-ac74-9ef746b58e86" enabled="true" useRefParam="false" refParamName="" r="0.000" g="0.000" b="0.000" execOnForceStopped="false" execOnActionCompleted="false" stopAfterLastEvent="true">')
                with open(file_path, 'wb') as f:
                    f.write(rpl)
#---------------—------------———----------------
            if IDMODSKIN == '13011' and 'S22.xml' in file_path:
                ABCD = []
                with open(file_path, 'rb') as file:
                    xml_bytes = file.read()#.decode('utf-8')
                    start_phrase = b'<Track trackName="'
                    end_phrase = b'</Track>' 
                    start_index = xml_bytes.find(start_phrase)
                    end_index = xml_bytes.find(end_phrase, start_index)
                    while start_index != -1 and end_index != -1:
                        track_text = xml_bytes[start_index:end_index + len(end_phrase)]
                        start_index = xml_bytes.find(start_phrase, end_index)
                        end_index = xml_bytes.find(end_phrase, start_index)
                        if b'a07302eb-cb3b-4146-9996-d018f92247aa' in track_text:
                            ABCD.append(track_text)
                                #print(track_text)
                                #track_text = track_text.encode()
                for track_text in ABCD:
                    if b'guid="6d1d27e2-efcc-4365-a0a0-c650d4ca16ef"' in track_text:
                        continue
                    with open(file_path, 'rb') as file:
                        xml_bytes = file.read()
                    modified_data = b'    <Track trackName="\xe5\xa4\xa7\xe9\x83\xa8\xe5\x88\x86\xe7\x9a\xae\xe8\x82\xa4\xe7\x9a\x84\xe7\x89\xb9\xe6\x95\x88\xe5\xad\x90\xe5\xbc\xb92" eventType="SpawnBulletTick" guid="7255b095-38a9-420b-96c1-0fc359ef272d" enabled="true" useRefParam="false" refParamName="" r="0.000" g="0.000" b="0.000" execOnForceStopped="false" execOnActionCompleted="false" stopAfterLastEvent="true">\r\n      <Condition id="6" guid="8d5e99b6-7c14-4d52-930f-cf8653835641" status="true" />\r\n      <Event eventName="SpawnBulletTick" time="0.000" isDuration="false" guid="0fe84e6b-f4b9-491b-a802-c85858c85dd3">\r\n        <TemplateObject name="targetId" id="0" objectName="self" isTemp="false" refParamName="" useRefParam="false" />\r\n        <String name="ActionName" value="prefab_characters/prefab_hero/130_gongbenwuzang/skill/13011_back" refParamName="" useRefParam="false" />\r\n      </Event>\r\n    </Track>'              
                    modified_data1 = xml_bytes.replace(track_text, modified_data)
                    with open(file_path, 'wb') as file:
                        file.write(modified_data1)
                with open(file_path, 'rb') as f: rpl = f.read().replace(b'    <Track trackName="13011_22" eventType="PlayAnimDuration" guid="346663c5-53c1-4f57-9196-8ea5aec7bafb" enabled="true" useRefParam="false" refParamName="" r="0.000" g="0.000" b="0.000" execOnForceStopped="false" execOnActionCompleted="false" stopAfterLastEvent="true">\r\n      <Condition id="5" guid="cea185dc-6db5-47e8-9a5f-fbf0f2aabacb" status="true" />',b'    <Track trackName="13011_22" eventType="PlayAnimDuration" guid="346663c5-53c1-4f57-9196-8ea5aec7bafb" enabled="true" useRefParam="false" refParamName="" r="0.000" g="0.000" b="0.000" execOnForceStopped="false" execOnActionCompleted="false" stopAfterLastEvent="true">').replace(b'    <Track trackName="ChangeSpringDuration7" eventType="ChangeSpringDuration" guid="4e903727-596c-4844-9b0c-c882335080b9" enabled="true" useRefParam="false" refParamName="" r="0.000" g="0.000" b="0.000" execOnForceStopped="false" execOnActionCompleted="false" stopAfterLastEvent="true">\r\n      <Condition id="5" guid="cea185dc-6db5-47e8-9a5f-fbf0f2aabacb" status="true" />', b'    <Track trackName="ChangeSpringDuration7" eventType="ChangeSpringDuration" guid="4e903727-596c-4844-9b0c-c882335080b9" enabled="true" useRefParam="false" refParamName="" r="0.000" g="0.000" b="0.000" execOnForceStopped="false" execOnActionCompleted="false" stopAfterLastEvent="true">')
                with open(file_path, 'wb') as f:
                    f.write(rpl)
#---------------—------------———----------------
            if IDMODSKIN == '13011' and 'S2B1.xml' in file_path:
                with open(file_path, 'rb') as f: rpl = f.read().replace(b'      </Event>\r\n    </Track>\r\n    <Track trackName="AutoY" eventType="HitTriggerTick" guid="9749148c-8e56-47f6-89e8-70c4ed334ef0" enabled="true" useRefParam="false" refParamName="" r="0.000" g="0.000" b="0.000" execOnForceStopped="false" execOnActionCompleted="false" stopAfterLastEvent="true">\r\n      <Event eventName="HitTriggerTick" time="0.000" isDuration="false" guid="62578072-d0be-44f1-bf0d-d8c1de538873">\r\n        <TemplateObject name="targetId" id="0" objectName="self" isTemp="false" refParamName="" useRefParam="false" />\r\n        <int name="SelfSkillCombineID_1" value="130006" refParamName="" useRefParam="false" />\r\n        <TemplateObject name="triggerId" id="-1" objectName="None" isTemp="false" refParamName="" useRefParam="false" />\r\n      </Event>\r\n    </Track>',b'      </Event>\r\n    </Track>').replace(b'  <Action tag="" length="2.000" loop="false">', b'  <Action tag="" length="2.000" loop="false">\r\n    <Track trackName="TriggerParticle0" eventType="TriggerParticle" guid="39adb49e-b73a-4b00-ab89-1cc90a2f6860" enabled="true" useRefParam="false" refParamName="" r="0.000" g="0.000" b="0.000" execOnForceStopped="false" execOnActionCompleted="false" stopAfterLastEvent="true">\r\n      <Event eventName="TriggerParticle" time="0.000" length="1.000" isDuration="true" guid="879c7677-a1d1-4da3-a387-a65149b7d0b7">\r\n        <TemplateObject name="targetId" id="0" objectName="self" isTemp="true" refParamName="" useRefParam="false" />\r\n        <String name="resourceName" value="prefab_skill_effects/hero_skill_effects/130_gongbenwuzang/13011/gongbenwuzang_attack01_spell01" refParamName="" useRefParam="false" />\r\n        <Vector3 name="bindPosOffset" x="0.000" y="1.000" z="0.500" refParamName="" useRefParam="false" />\r\n        <Vector3i name="scalingInt" x="10000" y="10000" z="10000" refParamName="" useRefParam="false" />\r\n        <bool name="bUseRealScaling" value="true" refParamName="" useRefParam="false" />\r\n        <bool name="bOnlyFollowPos" value="true" refParamName="" useRefParam="false" />\r\n        <bool name="b1stTickParentRot" value="true" refParamName="" useRefParam="false" />\r\n        <String name="syncAnimationName" value="" refParamName="" useRefParam="false" />\r\n        <String name="customTagName" value="" refParamName="" useRefParam="false" />\r\n      </Event>\r\n    </Track>')
                with open(file_path, 'wb') as f:
                    f.write(rpl)
#---------------—------------———----------------
            if IDMODSKIN[:3] =='524' and 'A1E9.xml' in file_path:
                with open(file_path, 'rb') as f:
                    rpl = f.read().replace(b'prefab_skill_effects/hero_skill_effects/524_Capheny/'+IDMODSKIN.encode()+b'/Atk1_FireRange',b'prefab_skill_effects/hero_skill_effects/524_Capheny/Atk1_FireRange')
                with open(file_path, 'wb') as f:
                    f.write(rpl)
#---------------—------------———----------------
            if IDMODSKIN[:3] =='537' and 'S12.xml' in file_path:
                with open(file_path, 'rb') as f:
                    rpl = f.read().replace(b'prefab_skill_effects/hero_skill_effects/537_Trip/Trip_attack_spell01_1prefab_skill_effects/hero_skill_effects/537_Trip/Trip_attack_spell01_1prefab_skill_effects/hero_skill_effects/537_Trip/Trip_attack_spell01_1_S',b'prefab_skill_effects/hero_skill_effects/537_Trip/Trip_attack_spell01_1_S')
                with open(file_path, 'wb') as f:
                    f.write(rpl)
#---------------—------------———----------------
            if IDMODSKIN =='11119' and 'A1B1.xml' in file_path:
                with open(file_path, 'rb') as f: rpl = f.read().replace(b'<String name="prefabName" value="prefab_characters/commonempty" refParamName="" useRefParam="false" />', b'<String name="prefabName" value="prefab_skill_effects/hero_skill_effects/111_sunshangxiang/11119/sunshangxiang_fly_01b" refParamName="" useRefParam="false" />\r\n        <Vector3i name="translation" x="0" y="750" z="0" refParamName="" useRefParam="false" />')
                with open(file_path,'wb') as f: 
                    f.write(rpl)
#---------------—------------———----------------
                if IDMODSKIN =='11119' and 'A2B1.xml' in file_path:
                    with open(file_path, 'rb') as f: rpl = f.read().replace(b'<String name="prefabName" value="prefab_characters/commonempty" refParamName="" useRefParam="false" />',b'<String name="prefabName" value="prefab_skill_effects/hero_skill_effects/111_sunshangxiang/11119/sunshangxiang_fly_01b" refParamName="" useRefParam="false" />\r\n        <Vector3i name="translation" x="0" y="700" z="0" refParamName="" useRefParam="false" />')
                    with open(file_path,'wb') as f: 
                        f.write(rpl)
#---------------—------------———----------------
            if IDMODSKIN =='13015' and 'A4.xml' in file_path:
                with open(file_path, 'rb') as f: rpl = f.read().replace(b'<bool name="useNegateValue" value="true"', b'<bool name="useNegateValue" value="false"')
                with open(file_path,'wb') as f: 
                    f.write(rpl)
#---------------—------------———----------------
            if IDMODSKIN =='53702' and 'S12.xml' in file_path:
                with open(file_path, 'rb') as f: rpl = f.read().replace(b'prefab_skill_effects/hero_skill_effects/537_Trip/53702/Trip_attack_spell01_1prefab_skill_effects/hero_skill_effects/537_Trip/53702/Trip_attack_spell01_1prefab_skill_effects/hero_skill_effects/537_Trip/53702/Trip_attack_spell01_1_S', b'Prefab_Skill_Effects/Hero_Skill_Effects/537_Trip/53702/Trip_attack_spell01_1_S')
                with open(file_path,'wb') as f: 
                    f.write(rpl)
#---------------—------------———----------------
            if IDMODSKIN =='15012' and 'U1.xml' in file_path:
                with open(file_path, 'rb') as f: rpl = f.read().replace(b'<String name="prefab" value="prefab_skill_effects/hero_skill_effects/150_Hanxin_spellC_01"',b'<String name="prefab" value="prefab_skill_effects/hero_skill_effects/150_hanxin/15012/150_Hanxin_spellC_01"')
                with open(file_path, 'wb') as f:
                    f.write(rpl)
#---------------—------------———----------------
            if IDMODSKIN == '13311':
                with open(file_path, 'rb') as f: rpl = f.read().replace(b'prefab_skill_effects/hero_skill_effects/133_direnjie/13311/',b'prefab_skill_effects/component_effects/13311/13311_5/').replace(b'"Play_DiRenJie_Attack_1"', b'"Play_DiRenJie_Attack_1_Skin11_AW2"').replace(b'"Play_DiRenJie_Voice_Short"', b'"Play_DiRenJie_Voice_Short_Skin11_AW3"').replace(b'"Play_DiRenJie_Attack_Hit_1"', b'"Play_DiRenJie_Attack_Hit_1_Skin11_AW2"').replace(b'"Play_DiRenJie_Skill_A"', b'"Play_DiRenJie_Skill_A_Skin11_AW2"').replace(b'"Play_DiRenJie_Voice_Anger"', b'"Play_DiRenJie_Voice_Anger_Skin11_AW3"').replace(b'"Play_DiRenJie_Skill_A_Hit"', b'"Play_DiRenJie_Skill_A_Hit_Skin11_AW2"').replace(b'"Play_DiRenJie_Attack_Hit_2"', b'"Play_DiRenJie_Attack_Hit_2_Skin11_AW2"').replace(b'"Play_DiRenJie_Skill_B"', b'"Play_DiRenJie_Skill_B_Skin11_AW2"').replace(b'"Play_DiRenJie_Skill_B_Hit"', b'"Play_DiRenJie_Skill_B_Hit_Skin11_AW2"').replace(b'"Play_DiRenJie_Card_Red"', b'"Play_DiRenJie_Card_Red_Skin11_AW2"').replace(b'"Play_DiRenJie_Card_Blue"', b'"Play_DiRenJie_Card_Blue_Skin11_AW2"').replace(b'"Play_DiRenJie_Card_Yellow"', b'"Play_DiRenJie_Card_Yellow_Skin11_AW2"').replace(b'"Play_DiRenJie_Voice_Dead"', b'"Play_DiRenJie_Voice_Dead_Skin11_AW3"').replace(b'"Play_DiRenJie_Voice_Skill_B"', b'"Play_DiRenJie_Voice_Skill_B_Skin11_AW3"').replace(b'"Play_DiRenJie_Skill_C"', b'"Play_DiRenJie_Skill_C_Skin11_AW2"').replace(b'"Play_DiRenJie_Voice_Skill_C"', b'"Play_DiRenJie_Voice_Skill_C_Skin11_AW3"').replace(b'"Play_DiRenJie_Skill_C_Hit"', b'"Play_DiRenJie_Skill_C_Hit_Skin11_AW2"')
                with open(file_path,'wb') as f: 
                    f.write(rpl)
#---------------—------------———----------------
            if IDMODSKIN == '13311' and 'U1' in file_path:
                if phukienv == "dov":
                    with open(file_path, 'rb') as f:
                        rpl = f.read().replace(b'prefab_skill_effects/component_effects/13311/13311_5/',b'prefab_skill_effects/component_effects/13311/1331102/')
                    with open(file_path, 'wb') as f:
                        f.write(rpl)
#---------------—------------———----------------
            if IDMODSKIN == '16707':
                with open(file_path, 'rb') as f: rpl = f.read().replace(b'prefab_skill_effects/hero_skill_effects/167_wukong/16707/',b'prefab_skill_effects/component_effects/16707/16707_5/').replace(b'"Play_Back_WuKong"', b'"Play_Back_WuKong_Skin7_AW3"').replace(b'"Play_WuKong_Attack_1"', b'"Play_WuKong_Attack_1_Skin7_AW3"').replace(b'"Play_WuKong_VO_Short"', b'"Play_WuKong_VO_Short_Skin7_AW4"').replace(b'"Play_WuKong_Attack_Hit_1"', b'"Play_WuKong_Attack_Hit_1_Skin7_AW3"').replace(b'"Play_WuKong_Attack_2"', b'"Play_WuKong_Attack_2_Skin7_AW3"').replace(b'"Play_WuKong_VO_Anger"', b'"Play_WuKong_VO_Anger_Skin7_AW4"').replace(b'"Play_WuKong_Skill_Passive_Hit1"', b'"Play_WuKong_Skill_Passive_Hit1_Skin7_AW3"').replace(b'"Play_WuKong_Skill_Passive_Hit2"', b'"Play_WuKong_Skill_Passive_Hit2_Skin7_AW3"').replace(b'"Play_WuKong_Skill_Passive_Hit3"', b'"Play_WuKong_Skill_Passive_Hit3_Skin7_AW3"').replace(b'"Play_WuKong_Skill_B_2"', b'"Play_WuKong_Skill_B_2_Skin7_AW3"').replace(b'"Play_WuKong_Skill_B_Hit"', b'"Play_WuKong_Skill_B_Hit_Skin7_AW3"').replace(b'"Play_WuKong_VO_Dead"', b'"Play_WuKong_VO_Dead_Skin7_AW4"').replace(b'"Play_WuKong_Skill_A_2"', b'"Play_WuKong_Skill_A_2_Skin7_AW3"').replace(b'"Play_WuKong_Skill_A_Hit"', b'"Play_WuKong_Skill_A_Hit_Skin7_AW3"').replace(b'"Play_WuKong_Skill_A_1"', b'"Play_WuKong_Skill_A_1_Skin7_AW3"').replace(b'"Play_WuKong_VO_Skill_A"', b'"Play_WuKong_VO_Skill_A_Skin7_AW4"').replace(b'"Play_WuKong_Skill_A_Run"', b'"Play_WuKong_Skill_A_Run_Skin7_AW3"').replace(b'"Stop_WuKong_Skill_A_Run"', b'"Stop_WuKong_Skill_A_Run_Skin7_AW3"').replace(b'"Play_WuKong_Skill_B_1"', b'"Play_WuKong_Skill_B_1_Skin7_AW3"').replace(b'"Play_WuKong_VO_Skill_B"', b'"Play_WuKong_VO_Skill_B_Skin7_AW4"').replace(b'"Play_WuKong_Skill_C"', b'"Play_WuKong_Skill_C_Skin7_AW3"').replace(b'"Play_WuKong_VO_Skill_C"', b'"Play_WuKong_VO_Skill_C_Skin7_AW4"').replace(b'"Play_WuKong_Skill_C_01"', b'"Play_WuKong_Skill_C_01_Skin7_AW3"').replace(b'"Play_WuKong_Skill_C_02"', b'"Play_WuKong_Skill_C_02_Skin7_AW3"').replace(b'"Play_WuKong_Skill_C_Hit"', b'"Play_WuKong_Skill_C_Hit_Skin7_AW3"')
                with open(file_path,'wb') as f: f.write(rpl)
#---------------—------------———----------------
            if IDMODSKIN == '16707' and 'U1B0.xml' in file_path:
                with open(file_path, 'rb') as f: rpl = f.read().replace(b'<String name="resourceName" value="prefab_skill_effects/component_effects/16707/16707_5/wukong_attack_spell03" refParamName="" useRefParam="false" />', b'<String name="resourceName" value="prefab_skill_effects/component_effects/16707/16707_5/wukong_attack_spell03_1" refParamName="" useRefParam="false" />\r\n         <String name="resourceName2" value="prefab_skill_effects/component_effects/16707/16707_5/wukong_attack_spell03_1" refParamName="" useRefParam="false" />')
                with open(file_path,'wb') as f: f.write(rpl)
#---------------—------------———----------------
            if IDMODSKIN == '16307' and 'P2.xml' in file_path:
                with open(file_path, 'rb') as f:
                    rpl = f.read()
                    rpl = rpl.replace(b'"skinId" value="16307"', b'"skinId" value="16300"')
                with open(file_path,'wb') as f:
                    f.write(rpl)
#---------------—------------———----------------
            if IDMODSKIN =='15012' and 'U1.xml' in file_path:
                with open(file_path, 'rb') as f: rpl = f.read().replace(b'<String name="prefab" value="prefab_skill_effects/hero_skill_effects/150_Hanxin_spellC_01"',b'<String name="prefab" value="prefab_skill_effects/hero_skill_effects/150_hanxin/15012/150_Hanxin_spellC_01"')
                with open(file_path, 'wb') as f: f.write(rpl)
#---------------—------------———----------------
            if IDMODSKIN == '13210' and 'S1E1.xml' in file_path:
                with open(file_path, 'rb') as f: rpl = f.read().replace(b'\r\n        <String name="resourceName" value="prefab_skill_effects/hero_skill_effects/132_makeboluo/Makeboluo_hurt_01" refParamName="" useRefParam="false" />', b'\r\n        <String name="resourceName" value="Prefab_Skill_Effects/Hero_Skill_Effects/132_MaKeBoLuo/13210/Makeboluo_spell01_hurt_01" refParamName="" useRefParam="false" />\r        <String name="resourceName2" value="Prefab_Skill_Effects/Hero_Skill_Effects/132_MaKeBoLuo/13210/Makeboluo_spell01_hurt_02" refParamName="" useRefParam="false" />\r        <String name="resourceName3" value="Prefab_Skill_Effects/Hero_Skill_Effects/132_MaKeBoLuo/13210/Makeboluo_spell01_hurt_03" refParamName="" useRefParam="false" />')
                with open(file_path,'wb') as f: f.write(rpl)
            if IDMODSKIN == '13210':
                def checkskin(a,ID):
                    pz=a.split(b'</Track>')
                    b=[]
                    for code in pz:
                        if b'CheckSkinIdTick' in code and b'<int name="skinId" value="'+ID in code and b'bEqual" value="f' not in code:
                            a=a.replace(code,code.replace(b'<int name="skinId" value="'+ID,b'<int name="skinId" value="'+ID[:3]+'00'))
                        if b'CheckSkinIdTick' in code and b'<int name="skinId" value="'+ID in code and b'bEqual" value="f' in code:
                            condition=code[code.find(b'guid="'):code.find(b'" enabled="',code.find(b'guid="'))]
                            b.append(condition)
                    p=a.find(b'<Track trackName="')
                    while p!=-1:
                        p2=a.find(b'</Track>',p)
                        code=a[p:p2]
                        for z in b:
                            if z in code :
                                a=a.replace(code,code.replace(b'" enabled="true"',b'" enabled="false"'))
                        p=a.find(b'<Track trackName="',p2)
                    return a
                def fix_condition(a):
                    p=a.find(b'<Condition id="')
                    while p!=-1:
                        p2=a.find(b'" guid="',p)
                        condition=a[p:a.find(b'" status="',p)]
                        ID=a[p2:a.find(b'" status="',p2)]
                        check=a[p+15:a.find(b'"',p+15)]
                        if len(ID)>10:
                            pz=a.split(b'</Track>')
                            for i in range(len(pz)):
                                if ID in pz[i] and condition not in pz[i]:
                                    if check.decode()!=str(i):
                                        a=a.replace(condition,b'<Condition id="'+str(i).encode('utf-8')+ID)
                        p=a.find(b'<Condition id="',p2)
                    return a
                with open(file_path,'rb') as f:
                    a=f.read()
            if IDMODSKIN == '13210' and any(x in file_path for x in ['S1B0.xml', 'S11B0.xml', 'S12B0.xml']):
                a=a.replace(b'hero_skill_effects/132_makeboluo/',b'hero_skill_effects/132_makeboluo/TamDepTrai/')
                a=a.replace(b'  </Action>',b'    <Track trackName="1" eventType="CheckSkillCombineConditionTick" guid="Mod_By_TamDepTrai_Mod_132111" enabled="true" useRefParam="false" refParamName="" r="0.000" g="0.000" b="0.000" execOnForceStopped="false" execOnActionCompleted="false" stopAfterLastEvent="true">\r\n      <Event eventName="CheckSkillCombineConditionTick" time="0.000" isDuration="false" guid="b0dbc04b-5f6d-4610-a37b-b5240f304825">\r\n        <TemplateObject name="targetId" id="0" objectName="self" isTemp="false" refParamName="" useRefParam="false" />\r\n        <int name="skillCombineId" value="132111" refParamName="" useRefParam="false" />\r\n        <Enum name="checkOPType" value="3" refParamName="" useRefParam="false" />\r\n        <int name="skillCombineLevel" value="1" refParamName="" useRefParam="false" />\r\n      </Event>\r\n    </Track>\r\n    <Track trackName="2" eventType="CheckSkillCombineConditionTick" guid="Mod_By_TamDepTrai_Mod_132112" enabled="true" useRefParam="false" refParamName="" r="0.000" g="0.000" b="0.000" execOnForceStopped="false" execOnActionCompleted="false" stopAfterLastEvent="true">\r\n      <Event eventName="CheckSkillCombineConditionTick" time="0.000" isDuration="false" guid="fb9ffe1e-fc80-463c-aa04-7e4749711ab8">\r\n        <TemplateObject name="targetId" id="0" objectName="self" isTemp="false" refParamName="" useRefParam="false" />\r\n        <int name="skillCombineId" value="132112" refParamName="" useRefParam="false" />\r\n        <Enum name="checkOPType" value="3" refParamName="" useRefParam="false" />\r\n        <int name="skillCombineLevel" value="1" refParamName="" useRefParam="false" />\r\n      </Event>\r\n    </Track>\r\n    <Track trackName="3" eventType="CheckSkillCombineConditionTick" guid="Mod_By_TamDepTrai_Mod_132113" enabled="true" useRefParam="false" refParamName="" r="0.000" g="0.000" b="0.000" execOnForceStopped="false" execOnActionCompleted="false" stopAfterLastEvent="true">\r\n      <Event eventName="CheckSkillCombineConditionTick" time="0.000" isDuration="false" guid="6786a65e-f11b-484a-a0ae-613c7521f69e">\r\n        <TemplateObject name="targetId" id="0" objectName="self" isTemp="false" refParamName="" useRefParam="false" />\r\n        <int name="skillCombineId" value="132113" refParamName="" useRefParam="false" />\r\n        <Enum name="checkOPType" value="3" refParamName="" useRefParam="false" />\r\n        <int name="skillCombineLevel" value="1" refParamName="" useRefParam="false" />\r\n      </Event>\r\n    </Track>\r\n    <Track trackName="TriggerParticle0" eventType="TriggerParticle" guid="91aaf49d-c92c-4481-9957-e3b0448f1479" enabled="true" useRefParam="false" refParamName="" r="0.000" g="0.000" b="0.000" execOnForceStopped="false" execOnActionCompleted="false" stopAfterLastEvent="true">\r\n      <Condition id="TamDepTrai" guid="Mod_By_TamDepTrai_Mod_132111" status="true" />\r\n      <Event eventName="TriggerParticle" time="0.000" length="1.400" isDuration="true" guid="51311a35-66be-4940-9a41-431050e09e2b">\r\n        <TemplateObject name="targetId" id="0" objectName="self" isTemp="false" refParamName="" useRefParam="false" />\r\n        <TemplateObject name="objectSpaceId" id="0" objectName="self" isTemp="false" refParamName="" useRefParam="false" />\r\n        <String name="resourceName" value="prefab_skill_effects/hero_skill_effects/132_makeboluo/Makeboluo_spell01_attack_01" refParamName="" useRefParam="false" />\r\n        <Vector3i name="scalingInt" x="10000" y="10000" z="10000" refParamName="" useRefParam="false" />\r\n        <String name="syncAnimationName" value="" refParamName="" useRefParam="false" />\r\n        <String name="customTagName" value="" refParamName="" useRefParam="false" />\r\n      </Event>\r\n    </Track>\r\n    <Track trackName="TriggerParticle0" eventType="TriggerParticle" guid="91aaf49d-c92c-4481-9957-e3b0448f1479" enabled="true" useRefParam="false" refParamName="" r="0.000" g="0.000" b="0.000" execOnForceStopped="false" execOnActionCompleted="false" stopAfterLastEvent="true">\r\n      <Condition id="TamDepTrai" guid="Mod_By_TamDepTrai_Mod_132111" status="true" />\r\n      <Event eventName="TriggerParticle" time="0.000" length="1.400" isDuration="true" guid="51311a35-66be-4940-9a41-431050e09e2b">\r\n        <TemplateObject name="targetId" id="0" objectName="self" isTemp="false" refParamName="" useRefParam="false" />\r\n        <TemplateObject name="objectSpaceId" id="0" objectName="self" isTemp="false" refParamName="" useRefParam="false" />\r\n        <String name="resourceName" value="prefab_skill_effects/hero_skill_effects/132_makeboluo/Makeboluo_spell01_attack_01_1" refParamName="" useRefParam="false" />\r\n        <Vector3i name="scalingInt" x="10000" y="10000" z="10000" refParamName="" useRefParam="false" />\r\n        <String name="syncAnimationName" value="" refParamName="" useRefParam="false" />\r\n        <String name="customTagName" value="" refParamName="" useRefParam="false" />\r\n      </Event>\r\n    </Track>\r\n    <Track trackName="TriggerParticle0" eventType="TriggerParticle" guid="91aaf49d-c92c-4481-9957-e3b0448f1479" enabled="true" useRefParam="false" refParamName="" r="0.000" g="0.000" b="0.000" execOnForceStopped="false" execOnActionCompleted="false" stopAfterLastEvent="true">\r\n      <Condition id="TamDepTrai" guid="Mod_By_TamDepTrai_Mod_132112" status="true" />\r\n      <Event eventName="TriggerParticle" time="0.000" length="1.400" isDuration="true" guid="51311a35-66be-4940-9a41-431050e09e2b">\r\n        <TemplateObject name="targetId" id="0" objectName="self" isTemp="false" refParamName="" useRefParam="false" />\r\n        <TemplateObject name="objectSpaceId" id="0" objectName="self" isTemp="false" refParamName="" useRefParam="false" />\r\n        <String name="resourceName" value="prefab_skill_effects/hero_skill_effects/132_makeboluo/Makeboluo_spell01_attack_02" refParamName="" useRefParam="false" />\r\n        <Vector3i name="scalingInt" x="10000" y="10000" z="10000" refParamName="" useRefParam="false" />\r\n        <String name="syncAnimationName" value="" refParamName="" useRefParam="false" />\r\n        <String name="customTagName" value="" refParamName="" useRefParam="false" />\r\n      </Event>\r\n    </Track>\r\n    <Track trackName="TriggerParticle0" eventType="TriggerParticle" guid="91aaf49d-c92c-4481-9957-e3b0448f1479" enabled="true" useRefParam="false" refParamName="" r="0.000" g="0.000" b="0.000" execOnForceStopped="false" execOnActionCompleted="false" stopAfterLastEvent="true">\r\n      <Condition id="TamDepTrai" guid="Mod_By_TamDepTrai_Mod_132112" status="true" />\r\n      <Event eventName="TriggerParticle" time="0.000" length="1.400" isDuration="true" guid="51311a35-66be-4940-9a41-431050e09e2b">\r\n        <TemplateObject name="targetId" id="0" objectName="self" isTemp="false" refParamName="" useRefParam="false" />\r\n        <TemplateObject name="objectSpaceId" id="0" objectName="self" isTemp="false" refParamName="" useRefParam="false" />\r\n        <String name="resourceName" value="prefab_skill_effects/hero_skill_effects/132_makeboluo/Makeboluo_spell01_attack_02_1" refParamName="" useRefParam="false" />\r\n        <Vector3i name="scalingInt" x="10000" y="10000" z="10000" refParamName="" useRefParam="false" />\r\n        <String name="syncAnimationName" value="" refParamName="" useRefParam="false" />\r\n        <String name="customTagName" value="" refParamName="" useRefParam="false" />\r\n      </Event>\r\n    </Track>\r\n    <Track trackName="TriggerParticle0" eventType="TriggerParticle" guid="91aaf49d-c92c-4481-9957-e3b0448f1479" enabled="true" useRefParam="false" refParamName="" r="0.000" g="0.000" b="0.000" execOnForceStopped="false" execOnActionCompleted="false" stopAfterLastEvent="true">\r\n      <Condition id="TamDepTrai" guid="Mod_By_TamDepTrai_Mod_132113" status="true" />\r\n      <Event eventName="TriggerParticle" time="0.000" length="1.400" isDuration="true" guid="51311a35-66be-4940-9a41-431050e09e2b">\r\n        <TemplateObject name="targetId" id="0" objectName="self" isTemp="false" refParamName="" useRefParam="false" />\r\n        <TemplateObject name="objectSpaceId" id="0" objectName="self" isTemp="false" refParamName="" useRefParam="false" />\r\n        <String name="resourceName" value="prefab_skill_effects/hero_skill_effects/132_makeboluo/Makeboluo_spell01_attack_03" refParamName="" useRefParam="false" />\r\n        <Vector3i name="scalingInt" x="10000" y="10000" z="10000" refParamName="" useRefParam="false" />\r\n        <String name="syncAnimationName" value="" refParamName="" useRefParam="false" />\r\n        <String name="customTagName" value="" refParamName="" useRefParam="false" />\r\n      </Event>\r\n    </Track>\r\n    <Track trackName="TriggerParticle0" eventType="TriggerParticle" guid="91aaf49d-c92c-4481-9957-e3b0448f1479" enabled="true" useRefParam="false" refParamName="" r="0.000" g="0.000" b="0.000" execOnForceStopped="false" execOnActionCompleted="false" stopAfterLastEvent="true">\r\n      <Condition id="TamDepTrai" guid="Mod_By_TamDepTrai_Mod_132113" status="true" />\r\n      <Event eventName="TriggerParticle" time="0.000" length="1.400" isDuration="true" guid="51311a35-66be-4940-9a41-431050e09e2b">\r\n        <TemplateObject name="targetId" id="0" objectName="self" isTemp="false" refParamName="" useRefParam="false" />\r\n        <TemplateObject name="objectSpaceId" id="0" objectName="self" isTemp="false" refParamName="" useRefParam="false" />\r\n        <String name="resourceName" value="prefab_skill_effects/hero_skill_effects/132_makeboluo/Makeboluo_spell01_attack_03_1'+b'  </Action>')
                a=a.replace(b'  </Action>',b'" refParamName="" useRefParam="false" />\r\n        <Vector3i name="scalingInt" x="10000" y="10000" z="10000" refParamName="" useRefParam="false" />\r\n        <String name="syncAnimationName" value="" refParamName="" useRefParam="false" />\r\n        <String name="customTagName" value="" refParamName="" useRefParam="false" />\r\n      </Event>\r\n    </Track>\r\n    <Track trackName="TriggerParticle0" eventType="TriggerParticle" guid="91aaf49d-c92c-4481-9957-e3b0448f1479" enabled="true" useRefParam="false" refParamName="" r="0.000" g="0.000" b="0.000" execOnForceStopped="false" execOnActionCompleted="false" stopAfterLastEvent="true">\r\n      <Condition id="TamDepTrai" guid="Mod_By_TamDepTrai_Mod_132111" status="false" />\r\n      <Condition id="TamDepTrai" guid="Mod_By_TamDepTrai_Mod_132112" status="false" />\r\n      <Condition id="TamDepTrai" guid="Mod_By_TamDepTrai_Mod_132113" status="false" />\r\n      <Event eventName="TriggerParticle" time="0.000" length="1.400" isDuration="true" guid="51311a35-66be-4940-9a41-431050e09e2b">\r\n        <TemplateObject name="targetId" id="0" objectName="self" isTemp="false" refParamName="" useRefParam="false" />\r\n        <TemplateObject name="objectSpaceId" id="0" objectName="self" isTemp="false" refParamName="" useRefParam="false" />\r\n        <String name="resourceName" value="prefab_skill_effects/hero_skill_effects/132_makeboluo/Makeboluo_spell01_attack_01" refParamName="" useRefParam="false" />\r\n        <Vector3i name="scalingInt" x="10000" y="10000" z="10000" refParamName="" useRefParam="false" />\r\n        <String name="syncAnimationName" value="" refParamName="" useRefParam="false" />\r\n        <String name="customTagName" value="" refParamName="" useRefParam="false" />\r\n      </Event>\r\n    </Track>\r\n    <Track trackName="TriggerParticle0" eventType="TriggerParticle" guid="91aaf49d-c92c-4481-9957-e3b0448f1479" enabled="true" useRefParam="false" refParamName="" r="0.000" g="0.000" b="0.000" execOnForceStopped="false" execOnActionCompleted="false" stopAfterLastEvent="true">\r\n      <Condition id="TamDepTrai" guid="Mod_By_TamDepTrai_Mod_132111" status="false" />\r\n      <Condition id="TamDepTrai" guid="Mod_By_TamDepTrai_Mod_132112" status="false" />\r\n      <Condition id="TamDepTrai" guid="Mod_By_TamDepTrai_Mod_132113" status="false" />\r\n      <Event eventName="TriggerParticle" time="0.000" length="1.400" isDuration="true" guid="51311a35-66be-4940-9a41-431050e09e2b">\r\n        <TemplateObject name="targetId" id="0" objectName="self" isTemp="false" refParamName="" useRefParam="false" />\r\n        <TemplateObject name="objectSpaceId" id="0" objectName="self" isTemp="false" refParamName="" useRefParam="false" />\r\n        <String name="resourceName" value="prefab_skill_effects/hero_skill_effects/132_makeboluo/Makeboluo_spell01_attack_01_1" refParamName="" useRefParam="false" />\r\n        <Vector3i name="scalingInt" x="10000" y="10000" z="10000" refParamName="" useRefParam="false" />\r\n        <String name="syncAnimationName" value="" refParamName="" useRefParam="false" />\r\n        <String name="customTagName" value="" refParamName="" useRefParam="false" />\r\n      </Event>\r\n    </Track>\r\n    <Track trackName="T2\xe9\x9a\x8f\xe6\x9c\xba1 \xe9\x9f\xb3\xe6\x95\x88" eventType="PlayHeroSoundTick" guid="f92f38f7-c71a-4ea3-abfc-c8e4eb5b3865" enabled="true" useRefParam="false" refParamName="" r="0.000" g="0.000" b="0.000" execOnForceStopped="false" execOnActionCompleted="false" stopAfterLastEvent="true">\r\n      <Condition id="TamDepTrai" guid="Mod_By_TamDepTrai_Mod_132111" status="true" />\r\n      <Event eventName="PlayHeroSoundTick" time="0.000" isDuration="false" guid="9b862449-dea5-4cee-b1f0-8b1b3724ca8f">\r\n        <TemplateObject name="targetId" id="0" objectName="self" isTemp="false" refParamName="" useRefParam="false" />\r\n        <TemplateObject name="sourceId" id="0" objectName="self" isTemp="false" refParamName="" useRefParam="false" />\r\n        <String name="eventName" value="Play_13210_Hayate_SkillA_03" refParamName="" useRefParam="false" />\r\n        <bool name="useSkinSwitch" value="false" refParamName="" useRefParam="false" />\r\n      </Event>\r\n    </Track>\r\n    <Track trackName="T2\xe9\x9a\x8f\xe6\x9c\xba2 \xe9\x9f\xb3\xe6\x95\x88" eventType="PlayHeroSoundTick" guid="c7107416-30e0-4ee8-83fa-5f97bb948faf" enabled="true" useRefParam="false" refParamName="" r="0.000" g="0.000" b="0.000" execOnForceStopped="false" execOnActionCompleted="false" stopAfterLastEvent="true">\r\n      <Condition id="TamDepTrai" guid="Mod_By_TamDepTrai_Mod_132112" status="true" />\r\n      <Event eventName="PlayHeroSoundTick" time="0.000" isDuration="false" guid="4a8d55af-a3b6-4c1a-b7b9-830ea761ccf9">\r\n        <TemplateObject name="targetId" id="0" objectName="self" isTemp="false" refParamName="" useRefParam="false" />\r\n        <TemplateObject name="sourceId" id="0" objectName="self" isTemp="false" refParamName="" useRefParam="false" />\r\n        <String name="eventName" value="Play_13210_Hayate_SkillA_01" refParamName="" useRefParam="false" />\r\n        <bool name="useSkinSwitch" value="false" refParamName="" useRefParam="false" />\r\n      </Event>\r\n    </Track>\r\n    <Track trackName="T2\xe9\x9a\x8f\xe6\x9c\xba3 \xe9\x9f\xb3\xe6\x95\x88" eventType="PlayHeroSoundTick" guid="bca0dd8d-b83a-49da-982c-6cadaef3966a" enabled="true" useRefParam="false" refParamName="" r="0.000" g="0.000" b="0.000" execOnForceStopped="false" execOnActionCompleted="false" stopAfterLastEvent="true">\r\n      <Condition id="TamDepTrai" guid="Mod_By_TamDepTrai_Mod_132113" status="true" />\r\n      <Event eventName="PlayHeroSoundTick" time="0.000" isDuration="false" guid="129a0664-39ba-43af-9d93-43c6b7d64878">\r\n        <TemplateObject name="targetId" id="0" objectName="self" isTemp="false" refParamName="" useRefParam="false" />\r\n        <TemplateObject name="sourceId" id="0" objectName="self" isTemp="false" refParamName="" useRefParam="false" />\r\n        <String name="eventName" value="Play_13210_Hayate_SkillA_02" refParamName="" useRefParam="false" />\r\n        <bool name="useSkinSwitch" value="false" refParamName="" useRefParam="false" />\r\n      </Event>\r\n    </Track>\r\n    <Track trackName="T2\xe9\x9a\x8f\xe6\x9c\xba1 \xe9\x9f\xb3\xe6\x95\x88" eventType="PlayHeroSoundTick" guid="f92f38f7-c71a-4ea3-abfc-c8e4eb5b3865" enabled="true" useRefParam="false" refParamName="" r="0.000" g="0.000" b="0.000" execOnForceStopped="false" execOnActionCompleted="false" stopAfterLastEvent="true">\r\n      <Condition id="TamDepTrai" guid="Mod_By_TamDepTrai_Mod_132111" status="false" />\r\n      <Condition id="TamDepTrai" guid="Mod_By_TamDepTrai_Mod_132112" status="false" />\r\n      <Condition id="TamDepTrai" guid="Mod_By_TamDepTrai_Mod_132113" status="false" />\r\n      <Event eventName="PlayHeroSoundTick" time="0.000" isDuration="false" guid="9b862449-dea5-4cee-b1f0-8b1b3724ca8f">\r\n        <TemplateObject name="targetId" id="0" objectName="self" isTemp="false" refParamName="" useRefParam="false" />\r\n        <TemplateObject name="sourceId" id="0" objectName="self" isTemp="false" refParamName="" useRefParam="false" />\r\n        <String name="eventName" value="Play_13210_Hayate_SkillA_03" refParamName="" useRefParam="false" />\r\n        <bool name="useSkinSwitch" value="false" refParamName="" useRefParam="false" />\r\n      </Event>\r\n    </Track>\r\n    <Track trackName="T2\xe9\x9a\x8f\xe6\x9c\xba1" eventType="HitTriggerTick" guid="810de6b2-8b68-4614-8762-84bbafe2e77a" enabled="true" useRefParam="false" refParamName="" r="0.000" g="0.000" b="0.000" execOnForceStopped="false" execOnActionCompleted="false" stopAfterLastEvent="true">\r\n      <Condition id="TamDepTrai" guid="Mod_By_TamDepTrai_Mod_132111" status="false" />\r\n      <Condition id="TamDepTrai" guid="Mod_By_TamDepTrai_Mod_132112" status="false" />\r\n      <Condition id="TamDepTrai" guid="Mod_By_TamDepTrai_Mod_132113" status="false" />\r\n      <Event eventName="HitTriggerTick" time="0.000" isDuration="false" guid="06468bb9-532f-4c15-819f-4ea3434f2a47">\r\n        <TemplateObject name="targetId" id="0" objectName="self" isTemp="false" refParamName="" useRefParam="false" />\r\n        <int name="SelfSkillCombineID_1" value="132111" refParamName="" useRefParam="false" />\r\n        <TemplateObject name="triggerId" id="-1" objectName="None" isTemp="false" refParamName="" useRefParam="false" />\r\n      </Event>\r\n    </Track>\r\n'+b'  </Action>')
                a=fix_condition(a)
                with open(file_path,'wb') as f:f.write(a)
#-----------------------------------------------
    if IDCHECK not in ["13311", "16707"]:
        directory_path = Files_Directory_Path + f'{NAME_HERO}' + '/skill/'        
        IDSOUND_S = IDMODSKIN

        if IDSOUND_S[3:4] == '0':
            IDSOUND_S = IDSOUND_S[:3] + IDSOUND_S[4:]

        IDSOUND1 = IDSOUND_S[3:]
        IDSOUND12 = IDSOUND1.encode()
        IDSOUND = b"_Skin" + IDSOUND12

        IDINFO = str(int(IDMODSKIN) + 1)
        if IDINFO[3:4] == '0':
            IDINFO = IDINFO[:3] + IDINFO[4:]

        for file in os.listdir(directory_path):
            filepath = directory_path + file
            with open(filepath, 'rb') as f:
                content = f.read()

            lines = content.split(b'\r\n')
            code_lines = [
                line[40:line.find(b'" refParamName="" useRefParam="false" />')]
                for line in lines
                if b'<String name="eventName" value="' in line
            ]

            modified = False
            for code in code_lines:
                if IDSOUND in code:
                    continue
                a = b'<String name="eventName" value="' + code + b'" refParamName="" useRefParam="false" />'
                b = b'<String name="eventName" value="' + code + IDSOUND + b'" refParamName="" useRefParam="false" />\n        <bool name="useSkinSwitch" value="false" refParamName="" useRefParam="false"/>'
                if a in content:
                    content = content.replace(a, b)
                    modified = True

            if modified:
                with open(filepath, 'wb') as f:
                    f.write(content)
                    
#-----------------------------------------------
    if IDCHECK == '15009':
        for file in ["BlueBuff.xml", "RedBuff_Slow.xml"]:
            duongdan = f"{pack_name}/Resources/1.58.1/Ages/Prefab_Characters/Prefab_Hero/mod1/PassiveResource/{file}"
            giai(duongdan)
            with open(duongdan, 'rb') as f:
                content = f.read().replace(
                    b"CheckSkinIdVirtualTick", b"CheckHeroIdTick"
                    ).replace(
                    b'"skinId" value="15009"', b'"heroId" value="150"'
                    )
            with open(duongdan, 'wb') as f:
                f.write(content)
    if IDCHECK == '15013':
        Youtuber_Name = f'{pack_name}/Resources/1.58.1/Ages/Prefab_Characters/Prefab_Hero/mod1/PassiveResource/BlueBuff_CD.xml'
        giai(Youtuber_Name)
        with open(Youtuber_Name, 'rb') as f:
            noidung = f.read()
        noidung = noidung.replace(b"CheckSkinIdTick", b"CheckHeroIdTick")\
                         .replace(b'"skinId" value="15013"', b'"heroId" value="150"')\
                         .replace(b'prefab_skill_effects/hero_skill_effects/15013/', 
                                  b'prefab_skill_effects/hero_skill_effects/150_hanxin/15013/')
        with open(Youtuber_Name, 'wb') as f:
            f.write(noidung)
#-----------------------------------------------
    if IDCHECK == "11107" or IDCHECK == "14111":
        with zipfile.ZipFile(f'Resources/1.58.1/Ages/Prefab_Characters/Prefab_Organ_Age.pkg.bytes') as f:
            f.extractall(f'{pack_name}/files/Resources/1.58.1/Ages/Prefab_Characters/mod2/')
            TRU1 = (f'{pack_name}/files/Resources/1.58.1/Ages/Prefab_Characters/mod2/Prefab_Organ/Crystal/New_BlueCrystal/Skill/')
            TRU2 = (f'{pack_name}/files/Resources/1.58.1/Ages/Prefab_Characters/mod2/Prefab_Organ/Crystal/New_RedCrystal/Skill/')
            TRU3 = (f'{pack_name}/files/Resources/1.58.1/Ages/Prefab_Characters/mod2/Prefab_Organ/Tower/New_BlueTower/Skill/')
            TRU4 = (f'{pack_name}/files/Resources/1.58.1/Ages/Prefab_Characters/mod2/Prefab_Organ/Tower/New_BlueTower_High/Skill/')
            TRU5 = (f'{pack_name}/files/Resources/1.58.1/Ages/Prefab_Characters/mod2/Prefab_Organ/Tower/New_RedTower/Skill/')
            TRU6 = (f'{pack_name}/files/Resources/1.58.1/Ages/Prefab_Characters/mod2/Prefab_Organ/Tower/New_RedTower_High/Skill/')
            f.close()
        folder_path1 = [TRU1, TRU2, TRU3, TRU4, TRU5, TRU6]
        for folder_path in folder_path1:
            for filename in os.listdir(folder_path):
                file_path = os.path.join(folder_path, filename)
                giai(file_path)
                try:
                    with open(file_path, 'r', encoding='utf-8') as file:
                        content = file.readlines()

                    with open(file_path, 'w', encoding='utf-8') as file:
                        for line in content:
                            if '<String name="prefabName"' in line:
                                parts = line.split('/')
                                if len(parts) >= 5:
                                    parts[4] = '1/' + parts[4]
                                    line = '/'.join(parts)
                            elif '<String name="resourceName"' in line:
                                parts = line.split('/')
                                if len(parts) >= 3:
                                    parts[2] = '1/' + parts[2]
                                    line = '/'.join(parts)
                            file.write(line)
                except UnicodeDecodeError:
                    print(f"Files Encryptes JG: {file_path}")
                    continue
#-----------------------------------------------
    if IDCHECK in ("50108","14111","11107","15009","13015"):
        organSkin = "Resources/1.58.1/Databin/Client/Actor/organSkin.bytes"
        organSkin_mod = f"{pack_name}/Resources/1.58.1/Databin/Client/Actor/organSkin.bytes"
        shutil.copy(organSkin, organSkin_mod)
        giai(organSkin_mod)

    if IDCHECK in ("50108","14111","11107","15009","13015"):
        ID = IDCHECK
        file = open(organSkin_mod, "rb")
        IDN = str(hex(int(ID)))
        IDN = IDN[4:6] + IDN[2:4]
        IDN = bytes.fromhex(IDN)
        ALL_ID = []
        MD = int(ID[0:3] + "00")
        for IDNew in range(21):
            ALL_ID.append(str(MD))
            MD += 1
        ALL_ID.remove(ID)
        for x in range(20):
            IDK = str(hex(int(ALL_ID[x])))
            IDK = IDK[4:6] + IDK[2:4]
            IDK = bytes.fromhex(IDK)
            ALL_ID[x] = IDK
        Begin = file.read(140)
        Read = b"\x00"
        All = []
        while Read != b"":
            Read = file.read(36)
            if Read.find(IDN) != -1:
                All.append(Read)
            try:
                Max = Read[4] + (Read[5]*256)
                Max0 = str(hex(Max))
                if len(Max0) == 4:
                    Max0 = Max0[2:4] + "00"
                if len(Max0) == 5:
                    Max0 = Max0[3:5] + "0" + Max0[2]
                if len(Max0) == 6:
                    Max0 = Max0[4:6] + Max0[2:4]
                Max0 = bytes.fromhex(Max0)
            except:
                None
        file.close()
        file = open(organSkin_mod, "ab+")
        Read0 = file.read()
        for i in range(len(ALL_ID)):
            for j in range(len(All)):
                CT = All[j]
                if CT.find(IDN) != -1:
                    CT = CT.replace(IDN,ALL_ID[i])
                else:
                    CT = CT.replace(ALL_ID[i-1],ALL_ID[i])
                CTN = str(hex(Max0[0]+(Max0[1]*256)+1))
                if len(CTN) == 4:
                    CTN = CTN[2:4]
                if len(CTN) == 5:
                    CTN = CTN[3:5] + "0" + CTN[2]
                if len(CTN) == 6:
                    CTN = CTN[4:6] + CTN[2:4]
                CTN = bytes.fromhex(CTN)
                OZ = b" \x00\x00\x00"
                if len(CTN) == 1:
                    CT = CT.replace(OZ+CT[4:6],OZ+CTN+b"\x00",1)
                if len(CTN) == 2:
                    CT = CT.replace(OZ+CT[4:6],OZ+CTN,1)
                All[j] = CT
                XXX = file.write(CT)
                Max0 = CT[4:6]
        file.close()
        file = open(organSkin_mod, "rb")
        Read = file.read()
        Read = Read.replace(Begin[12:14],Max0,1)
        file.close()
        file = open(organSkin_mod, "wb")
        Z = file.write(Read)
        file.close()
#-----------------------------------------------

#-----------------------------------------------
    if b"Skin_Icon_BackToTown" in dieukienmod or b"Skin_Icon_Animation" in dieukienmod:
        import uuid, os, re

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
            return '\n'.join([
                line for line in lines if not any(x in line for x in [
                    '<String name="parentResourceName"',
                    '<Enum name="ReplacementUsage"',
                    '<Enum name="ReplacementSubUsage"',
                    '<SkinOrAvatarList'
                ])
            ])

        def replace_resource_lines(text, NAME_HERO, IDMODSKIN):
            text = text.replace(
                '<String name="resourceName" value="" refParamName="strReturnCityFall" useRefParam="true" />',
                f'<String name="resourceName" value="prefab_skill_effects/hero_skill_effects/{NAME_HERO}/{IDMODSKIN}/huijidi_01" refParamName="" useRefParam="false" />'
            )
            text = text.replace(
                '<String name="resourceName" value="" refParamName="strReturnCityEffectPath" useRefParam="true" />',
                f'<String name="resourceName" value="prefab_skill_effects/hero_skill_effects/{NAME_HERO}/{IDMODSKIN}/huicheng_tongyong_01" refParamName="" useRefParam="false" />'
            )
            return '\n'.join([
                f'<int name="skinId" value="{IDMODSKIN[:3]}00" refParamName="" useRefParam="false" />' if '<int name="skinId"' in line else line
                for line in text.splitlines()
            ])

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

        IDMODSKIN = IDMODSKIN1[0]
        NAME_HERO = next((x for x in os.listdir(Files_Directory_Path) if x.startswith(IDMODSKIN[:3] + "_")), None)
        if not NAME_HERO:
            print("❌ Không tìm thấy tên hero.")
        else:
            back_path = f'{pack_name}/Resources/1.58.1/Ages/Prefab_Characters/Prefab_Hero/mod1/commonresource/Back.xml'
            with open(back_path, "r", encoding="utf-8") as f:
                content = f.read()
            content = re.sub(r'\s*SkinAvatarFilterType="\d+"', '', content)
            base_blocks = extract_blocks(content)

            if len(base_blocks) >= 3:
                check_skin_block = base_blocks[0]
                other_blocks = base_blocks[1:]

                check_skin_block_mod = '\n'.join([
                    f'        <int name="skinId" value="{IDMODSKIN[:3]}00" refParamName="" useRefParam="false" />' if '<int name="skinId"' in line else line
                    for line in check_skin_block.splitlines()
                ])
                check_skin_block_mod = re.sub(r'^.*<SkinOrAvatarList[^>]*/>.*\n?', '', check_skin_block_mod, flags=re.MULTILINE)

                effect_blocks = []
                gohome_home_blocks = []
                for block in other_blocks:
                    clean_block = remove_unwanted_lines(block)
                    block_lower = clean_block.lower()
                    if 'clipname' in block_lower and ('home' in block_lower or 'gohome' in block_lower):
                        gohome_home_blocks.append(clean_block)
                    else:
                        effect_blocks.append(replace_resource_lines(clean_block, NAME_HERO, IDMODSKIN))

                all_blocks = [check_skin_block_mod] + effect_blocks[:2] + gohome_home_blocks[:2]

                with open(back_path, "r", encoding="utf-8") as f:
                    original_content = f.read()
                final_content = insert_blocks_before_action_close(original_content, all_blocks)

                with open(back_path, "w", encoding="utf-8") as f:
                    f.write(final_content)

            # --- Thêm block từ skin khác ---
            with open(back_path, "r", encoding="utf-8") as f:
                target_content = f.read()
            modified_count = 0
            for NAME_HERO in os.listdir(Files_Directory_Path):
                Path_Back = os.path.join(Files_Directory_Path, NAME_HERO, "skill")
                file_name = f"{IDMODSKIN}_Back.xml"
                file_path = os.path.join(Path_Back, file_name)
                if not os.path.exists(file_path):
                    continue
                with open(file_path, "r", encoding="utf-8") as f:
                    source_content = f.read()
                track_blocks = re.findall(r'\s*<Track trackName=.*?</Track>', source_content, flags=re.DOTALL)
                if not track_blocks:
                    continue
                skin_back = IDMODSKIN[:3] + "00"
                pattern = rf'<int name="skinId" value="{skin_back}".*?/>'
                match = re.search(pattern, target_content)
                if not match:
                    continue
                insert_pos = target_content.find('</Event>', match.end())
                insert_pos = target_content.find('</Track>', insert_pos)
                if insert_pos == -1:
                    continue
                insert_pos += len('</Track>')
                combined_blocks = "\n" + "\n".join(track_blocks)
                target_content = target_content[:insert_pos] + combined_blocks + target_content[insert_pos:]
                modified_count += 1
                break
            if modified_count > 0:
                with open(back_path, "w", encoding="utf-8") as f:
                    f.write(target_content)

            # --- Thêm Condition ---
            with open(back_path, "r", encoding="utf-8") as f:
                lines = [line for line in f if line.strip()]
            with open(back_path, "w", encoding="utf-8") as f:
                f.writelines(lines)

            with open(back_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            new_lines = []
            count = 0
            in_insert_mode = False
            line_check = f'<int name="skinId" value="{IDMODSKIN[:3]}00" refParamName="" useRefParam="false" />'
            for i in range(len(lines)):
                line = lines[i]
                if not in_insert_mode and '<Track trackName=' in line:
                    count += 1
                if line_check in line:
                    in_insert_mode = True
                elif in_insert_mode and 'CheckSkinIdTick' in line and line_check not in line:
                    in_insert_mode = False
                new_lines.append(line)
                if in_insert_mode and '<Track trackName=' in line:
                    guid = str(uuid.uuid4())
                    condition_line = f'      <Condition id="{count-1}" guid="{guid}" status="true" />\r\n'
                    new_lines.append(condition_line)
            with open(back_path, 'w', encoding='utf-8') as f:
                f.writelines(new_lines)
            print("    Back.xml hoàn tất")

#-----------------------------------------------
    duonggia = f'{pack_name}/Resources/1.58.1/Ages/Prefab_Characters/Prefab_Hero/mod1/commonresource/HasteE1.xml'
    giai(duonggia)
    if IDMODSKIN == "53002" or b'Skin_Icon_Atmosphere' in dieukienmod:
        with open(duonggia, 'r', encoding='utf-8') as f:
            text = f.read()
        text = text.replace(
            f'<int name="skinId" value="{IDMODSKIN}" refParamName="" useRefParam="false" />',
            f'<int name="skinId" value="{str(IDMODSKIN)[:3]}00" refParamName="" useRefParam="false" />'
        )
        with open(duonggia, 'w', encoding='utf-8') as f:
            f.write(text)

        with open(duonggia, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        text = ''.join(lines)
        matches = re.findall(r'<int name="skinId" value="(\d+)" refParamName="" useRefParam="false" />', text)
        if not matches:
            print("[!] Không tìm thấy dòng <int name='skinId'...>")
            exit()
        id_skin_goc = matches[0]

        skin_line_index = next((i for i, line in enumerate(lines) if id_skin_goc in line), None)
        start = next((i for i in range(skin_line_index, -1, -1) if '<Track trackName=' in lines[i]), None)
        end = next((i for i in range(skin_line_index, len(lines)) if '</Track>' in lines[i]), None)
        block_skinid = lines[start:end+1]

        pattern_effect = re.compile(r'jiasu_tongyong_0[12]')
        effect_blocks = []
        seen = set()
        i = 0
        while i < len(lines):
            if '<Track trackName=' in lines[i]:
                block_start = i
                while i < len(lines) and '</Track>' not in lines[i]:
                    i += 1
                block_end = i
                block = lines[block_start:block_end+1]
                block_text = ''.join(block)
                match = pattern_effect.search(block_text)
                if match:
                    eff_name = match.group(0)
                    if eff_name not in seen:
                        seen.add(eff_name)
                        block = [l for l in block if '<Condition ' not in l]
                        effect_blocks.append(block)
                        if len(effect_blocks) == 2:
                            break
            i += 1

        if len(effect_blocks) < 2:
            print("[!] Không đủ block hiệu ứng.")
            exit()

        insert_index = next((i for i in range(len(lines)-1, -1, -1) if '</Action>' in lines[i]), None)
        if insert_index is None:
            print("[!] Không tìm thấy </Action>")
            exit()

        all_inserted = []

        prefix = IDMODSKIN[:3]
        zip_path = f'Resources/1.58.1/Ages/Prefab_Characters/Prefab_Hero/Actor_{prefix}_Actions.pkg.bytes'
        mod5_dir = f'mod5/{IDMODSKIN}/'
        if not os.path.exists(mod5_dir) or not os.listdir(mod5_dir):
            os.makedirs(mod5_dir, exist_ok=True)
            try:
                with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                    zip_ref.extractall(mod5_dir)
            except:
                print(f"[!] Không giải nén được file: {zip_path}")
        NAME_HERO = next((name for name in os.listdir(mod5_dir) if name.startswith(prefix + "_")), None)
        if NAME_HERO:
            block_clone = [
                l.replace(id_skin_goc, IDMODSKIN[:3] + '00') if '<int name="skinId"' in l else l.replace(id_skin_goc, IDMODSKIN)
                for l in block_skinid
            ]
            effect_clones = []
            for eff_block in effect_blocks:
                eff_clone = [
                    re.sub(r'common_effects', f'hero_skill_effects/{NAME_HERO}/{IDMODSKIN}', l)
                    for l in eff_block
                ]
                effect_clones.append(eff_clone)
            all_inserted += block_clone + effect_clones[0] + effect_clones[1]

            with open(duonggia, 'w', encoding='utf-8') as f:
                f.writelines(lines[:insert_index] + all_inserted + lines[insert_index:])
            print(f"[✓] Gia Tốc: {os.path.basename(duonggia)} Done")
        else:
            print("[-] Không tìm thấy thư mục NAME_HERO trong mod5/")
    else:
        print(f"[-] Bỏ qua {IDMODSKIN}, không thỏa điều kiện mod.")

    idkt = IDMODSKIN[:3] + "00"
    lc = f'<int name="skinId" value="{idkt}" refParamName="" useRefParam="false" />'
    fp = f'{pack_name}/Resources/1.58.1/Ages/Prefab_Characters/Prefab_Hero/mod1/commonresource/HasteE1.xml'
    with open(fp, 'r', encoding='utf-8') as f:
        ls = f.readlines()
    nl = []
    idx = 0
    insert = False
    for i in range(len(ls)):
        l = ls[i]
        if not insert and '<Track trackName=' in l:
            idx += 1
        if lc in l:
            insert = True
        elif insert and 'CheckSkinIdTick' in l and lc not in l:
            insert = False
        nl.append(l)
        if insert and '<Track trackName=' in l:
            gid = str(uuid.uuid4())
            cd = f'      <Condition id="{idx - 1}" guid="{gid}" status="true" />\r\n'
            nl.append(cd)
    with open(fp, 'w', encoding='utf-8') as f:
        f.writelines(nl)

#-----------------------------------------------
    if IDMODSKIN == "16707":
        print(f"[-] Bỏ qua ID {IDMODSKIN}, không xử lý.")
        continue 
    INFO_MOD = f'{pack_name}/Resources/1.58.1/Prefab_Characters/mod/'
    with zipfile.ZipFile(f'Resources/1.58.1/Prefab_Characters/Actor_{IDINFO[:3]}_Infos.pkg.bytes') as f:
        f.extractall(INFO_MOD)
        f.close()
    duong_prefab = INFO_MOD + 'Prefab_Hero/'
    name_hero_list = os.listdir(duong_prefab)
    NAME_HERO = None

    for name in name_hero_list:
        path = os.path.join(duong_prefab, name)
        if name.lower().startswith(f"{IDINFO[:3]}_") and os.path.isdir(path):
            if any(f.lower().endswith('_actorinfo.bytes') for f in os.listdir(path)):
                NAME_HERO = name
                break

    if NAME_HERO is None:
        print(f"[!] Không tìm thấy thư mục NAME_HERO bắt đầu bằng {IDINFO[:3]}_ hoặc không chứa *_actorinfo.bytes")
        exit()

    đuongan = os.path.join(duong_prefab, NAME_HERO)
    actorinfo_file = next(
        (f for f in os.listdir(đuongan) if f.lower().endswith('_actorinfo.bytes')),
        None
    )

    if actorinfo_file is None:
        print(f"[!] Không tìm thấy file *_actorinfo.bytes trong {đuongan}")
        exit()
    newpath = os.path.join(đuongan, actorinfo_file)
    giai(newpath)
    def skincanmod(data):
        trc1=r.find(timtrc,r.find(b'SkinPrefabG'))
        vt1=r.find(b'JTCom0',trc1-300)
        a1=r[vt1-31:]
        a3=vt1 - 31
        skin1=a1[:4]
        skin2=int.from_bytes(skin1,byteorder='little')
        data=r[a3:a3+skin2]
        #open('kb','wb').write(data)
        return data
    op = newpath


    trc=IDINFO
    with open(op,'rb') as f:
        r=f.read()
        r1=r
        timtrc = trc.encode()
        f.close()
    #skin
    mkcam=b''
    teninfobv1=NAME_HERO
    if IDCHECK == '14111':
        teninfobv1='141_DiaoChan'
    tenefec2=teninfobv1.encode()
    tenefec=teninfobv1.lower().encode()
    newteneffec=tenefec[4:].capitalize()
    newteneffec=tenefec[:4]+newteneffec
    str1 = b"hero_skill_effects/" + tenefec2 + b"/"
    str2 = b"hero_skill_effects/" + tenefec + b"/"
    str3 = b"Hero_Skill_Effects/" + tenefec2 + b"/"
    str4 = b"Hero_Skill_Effects/" + tenefec + b"/"
    str5 = b"hero_skill_effects/" + newteneffec + b"/"
    str7 = b"Hero_Skill_Effects/" + newteneffec + b"/"
    IDskineffecđbt=IDCHECK.encode()+b"/"+IDCHECK.encode()
    idnew=IDCHECK.encode()+b"/"
    mkcam =b''
    new1=b''
    new1+=skincanmod(r)
    if IDCHECK == '13311':
        if phukienv == "vangv":
            new1=ngoaihinhvaneovvang
            print('vanpkvang')
        if phukienv == "dov":
            new1=ngoaihinhvaneovdo
        if phukienv == '':
            new1=ngoaihinhvaneov
    if IDCHECK == '16707':
        new1=ngoaihinhkhieov
    if IDCHECK == '52007':
        if phukien == "do":
            new1=ngoaihinhdoveres
        if phukien == "xanh":
            new1=ngoaihinhxanhveres
    IDskineffecđbt=IDCHECK.encode()+b"/"+IDCHECK.encode()
    idnew=IDCHECK.encode()+b'/'
    ID1=IDCHECK.encode()
    if new1.find(b'prefab_skill_effects/hero_skill_effects/')!= -1:#rpl = f.read().replace(str1,str1+ idnew).replace(str3,str3 + idnew).replace(str2,str2 + idnew).replace(str4,str4 + idnew).replace(b"""tyEffect" value="true""",b"""tyEffect" value="false""").replace(str5,str5+ idnew).replace(str6,str6 + idnew).replace(str7,str7 + idnew).replace(str8,str8 + idnew)
        FIND=new1.find(b'PreloadAnimatorEffects')-8
        VT1=new1[FIND:FIND+4]
        VTR=int.from_bytes(VT1,byteorder='little')
        VTM=new1[FIND:FIND+VTR]
        VTM9=VTM
        VTM=(VTR+12).to_bytes(4,byteorder='little')+VTM[4:]
        ELe=VTM.find(b'Element')-8
        ELe1=VTM.find(b'Element')-16
        VTRCM=VTM[:ELe-8] #vt đầu PreloadAnimatorEffects
        DAU=VTM[ELe:ELe+4]
        VTR=int.from_bytes(DAU,byteorder='little')
        VTM1=VTM[ELe:ELe+VTR]#chuẩn
        VTM1=(VTR+6).to_bytes(4,byteorder='little')+VTM1[4:]
        VTCUOI=VTM[ELe:]#owr cuoois
        VTCUOI1=VTM[ELe1:ELe1+8] #đếm full eleme
        tinh=VTM.count(b'Element')
        VTM=VTCUOI
        KB=0
        CODEFULL=b''
        for i in range(tinh):
                ELe=VTM.find(b'Element')-8
                DAU=VTM[ELe:ELe+4]
                VTR=int.from_bytes(DAU,byteorder='little')
                VTM1=VTM[ELe:ELe+VTR]#chuẩn
                if VTM1.find(b'Vprefab_skill_effects/hero_skill_effects/') == -1:
                    CODEFULL+=VTM1
                    break
                VTM1=(VTR+6).to_bytes(4,byteorder='little')+VTM1[4:]
                VTCUOI=VTM[VTR:]
                ELe1=VTM.find(b'Element')+7
                DAU1=VTM[ELe1:ELe1+4]
                VTR=int.from_bytes(DAU1,byteorder='little')
                VTM2=VTM[ELe1:ELe1+VTR]#đếm r
                VTM2=(VTR+6).to_bytes(4,byteorder='little')+VTM2[4:]
                newvt=VTM1.find(b'Vprefab_skill_effects/')-8
                MOI=VTM1[newvt:newvt+4]
                VTR=int.from_bytes(MOI,byteorder='little')
                VTR3=VTM1[newvt:newvt+VTR]
                VTM3=(VTR+6).to_bytes(4,byteorder='little')+VTR3[4:]
                CODE=VTM1[:15]+VTM2[:46]+VTM3+b'\x04\x00\x00\x00\x04\x00\x00\x00'
                VTM=VTCUOI
                CODEFULL+=CODE
        CODEFULL=CODEFULL.replace(str1,str1+ idnew).replace(str2,str2 + idnew)#.to_bytes(4,byteorder='little')
        CODEFULL=len(VTRCM+VTCUOI1+CODEFULL).to_bytes(4,byteorder='little')+VTRCM[4:]+(len(VTCUOI1+CODEFULL)).to_bytes(4,byteorder='little')+VTCUOI1[4:]+CODEFULL
        new1=new1.replace(VTM9,CODEFULL)
        new1=len(new1).to_bytes(4,byteorder='little')+new1[4:]
        mkcam = b'\x05'#\x05
    if new1.find(b'Prefab_Skill_Effects/Hero_Skill_Effects/')!= -1:#rpl = f.read().replace(str1,str1+ idnew).replace(str3,str3 + idnew).replace(str2,str2 + idnew).replace(str4,str4 + idnew).replace(b"""tyEffect" value="true""",b"""tyEffect" value="false""").replace(str5,str5+ idnew).replace(str6,str6 + idnew).replace(str7,str7 + idnew).replace(str8,str8 + idnew)
        FIND=new1.find(b'PreloadAnimatorEffects')-8
        VT1=new1[FIND:FIND+4]
        VTR=int.from_bytes(VT1,byteorder='little')
        VTM=new1[FIND:FIND+VTR]
        VTM9=VTM
        VTM=(VTR+12).to_bytes(4,byteorder='little')+VTM[4:]
        ELe=VTM.find(b'Element')-8
        ELe1=VTM.find(b'Element')-16
        VTRCM=VTM[:ELe-8] #vt đầu PreloadAnimatorEffects
        DAU=VTM[ELe:ELe+4]
        VTR=int.from_bytes(DAU,byteorder='little')
        VTM1=VTM[ELe:ELe+VTR]#chuẩn
        VTM1=(VTR+6).to_bytes(4,byteorder='little')+VTM1[4:]
        VTCUOI=VTM[ELe:]#owr cuoois
        VTCUOI1=VTM[ELe1:ELe1+8] #đếm full eleme
        tinh=VTM.count(b'Element')
        VTM=VTCUOI
        KB=0
        CODEFULL=b''
        for i in range(tinh):
                ELe=VTM.find(b'Element')-8
                DAU=VTM[ELe:ELe+4]
                VTR=int.from_bytes(DAU,byteorder='little')
                VTM1=VTM[ELe:ELe+VTR]#chuẩn
                if VTM1.find(b'VPrefab_Skill_Effects/Hero_Skill_Effects/') == -1:
                    CODEFULL+=VTM1
                    break
                VTM1=(VTR+6).to_bytes(4,byteorder='little')+VTM1[4:]
                VTCUOI=VTM[VTR:]
                ELe1=VTM.find(b'Element')+7
                DAU1=VTM[ELe1:ELe1+4]
                VTR=int.from_bytes(DAU1,byteorder='little')
                VTM2=VTM[ELe1:ELe1+VTR]#đếm r
                VTM2=(VTR+6).to_bytes(4,byteorder='little')+VTM2[4:]
                newvt=VTM1.find(b'VPrefab_Skill_Effects/')-8
                MOI=VTM1[newvt:newvt+4]
                VTR=int.from_bytes(MOI,byteorder='little')
                VTR3=VTM1[newvt:newvt+VTR]
                VTM3=(VTR+6).to_bytes(4,byteorder='little')+VTR3[4:]
                CODE=VTM1[:15]+VTM2[:46]+VTM3+b'\x04\x00\x00\x00\x04\x00\x00\x00'
                VTM=VTCUOI
                CODEFULL+=CODE
        CODEFULL=CODEFULL.replace(str3,str3 + idnew).replace(str4,str4 + idnew)#.to_bytes(4,byteorder='little')
        CODEFULL=len(VTRCM+VTCUOI1+CODEFULL).to_bytes(4,byteorder='little')+VTRCM[4:]+(len(VTCUOI1+CODEFULL)).to_bytes(4,byteorder='little')+VTCUOI1[4:]+CODEFULL
        new1=new1.replace(VTM9,CODEFULL)
        new1=len(new1).to_bytes(4,byteorder='little')+new1[4:]
        mkcam = b'\x05'#\x05
    skinmoi=new1
    skinprefag=r.find(b'SkinPrefabG')-8
    tinhskinpre=r[skinprefag:skinprefag+4]
    tinhskinpre1=int.from_bytes(tinhskinpre,byteorder='little')
    tinhskinpre2=r[skinprefag:skinprefag+tinhskinpre1] #
    JTCom0 = tinhskinpre2.count(b"JTCom0")
    beginskin=tinhskinpre2[:101]
    CodeSkinNew=beginskin+new1*JTCom0 #
    tinhCodeSkinNew1=CodeSkinNew[:93]
    tinhCodeSkinNew=CodeSkinNew[93:]
    Elenmen=len(tinhCodeSkinNew).to_bytes(4,byteorder='little')+tinhCodeSkinNew[4:]
    SkinPrefag1=tinhCodeSkinNew1+Elenmen
    SkinPrefag=len(SkinPrefag1).to_bytes(4,byteorder='little')+SkinPrefag1[4:]
    codeskinnew=r1.replace(tinhskinpre2,SkinPrefag)

    def ArtSkinPrefabLOD(data3):
        a=skinmoi.find(b'\x00ArtSkinPrefabLOD')-7
        a10=skinmoi.find(b'\x00ArtSkinPrefabLOD')-3
        a3=skinmoi[a:a+8]
        a4=a3[4:]
        a2=skinmoi[a:a+4]
        vitri=int.from_bytes(a2,byteorder='little')
        vitri2=int.from_bytes(a4,byteorder='little')
        a5=skinmoi[a:a+vitri]
        a25=skinmoi[a10:a10+vitri2]
        a22=skinmoi[a10:a10+vitri2].replace(b'\x00ArtSkinPrefabLOD',b'\x00ArtPrefabLOD')
        a13=len(a22).to_bytes(4,byteorder='little')+a22[4:]
        code=a5.replace(a25,a13)
        data3=len(code).to_bytes(4,byteorder='little')+code[4:]
        return data3 
    def ArtSkinLobbyShowLOD(data4):
        a=skinmoi.find(b'\x00ArtSkinLobbyShowLOD')-7
        a10=skinmoi.find(b'\x00ArtSkinLobbyShowLOD')-3
        a3=skinmoi[a:a+8]
        a4=a3[4:]
        a2=skinmoi[a:a+4]
        vitri=int.from_bytes(a2,byteorder='little')
        vitri2=int.from_bytes(a4,byteorder='little')
        a5=skinmoi[a:a+vitri]
        a25=skinmoi[a10:a10+vitri2]
        a22=skinmoi[a10:a10+vitri2].replace(b'\x00ArtSkinLobbyShowLOD',b'\x00ArtLobbyShowLOD')
        a13=len(a22).to_bytes(4,byteorder='little')+a22[4:]
        code=a5.replace(a25,a13)
        data4=len(code).to_bytes(4,byteorder='little')+code[4:]
        return data4
    def ArtSkinLobbyIdleShowLOD(data4):
        a = camSkin.find(b'\x00ArtSkinLobbyIdleShowLOD') - 7
        a10 = camSkin.find(b'\x00ArtSkinLobbyIdleShowLOD') - 3
        a3 = camSkin[a:a+8]
        a4 = a3[4:]
        a2 = camSkin[a:a+4]
        vitri = int.from_bytes(a2, byteorder='little')
        ne = camSkin[vitri:]
        vitri2 = int.from_bytes(a4, byteorder='little')
        a5 = camSkin[a:a+vitri]
        a25 = camSkin[a10:a10+vitri2]
        a22 = camSkin[a10:a10+vitri2].replace(b'\x00ArtSkinLobbyIdleShowLOD', b'\x00ArtLobbyIdleShowLOD')
        a13 = len(a22).to_bytes(4, byteorder='little') + a22[4:]
        code = a5.replace(a25, a13)
        data4 = len(code).to_bytes(4, byteorder='little') + code[4:] + ne
        return data4

    def ArtPrefabLODnew(data):
        a = ab.find(b'\x00ArtPrefabLOD') - 7
        a2 = ab[a:a+4]
        a3 = ab[a:a+5]
        a4 = a3[4:5]  # so 10
        vitri = int.from_bytes(a2, byteorder='little')
        data = ab[a:a+vitri]
        return data

    def ArtPrefabLODExnew(data4):
        a = ab.find(b'\x00ArtPrefabLODEx') - 7
        a2 = ab[a:a+4]
        a3 = ab[a:a+5]
        a4 = a3[4:5]  # so 10
        vitri = int.from_bytes(a2, byteorder='little')
        data4 = ab[a:a+vitri]
        return data4

    def ArtSkinPrefabLODnew(data3):
        a = ab.find(b'\x00ArtSkinPrefabLOD') - 7
        a10 = ab.find(b'\x00ArtSkinPrefabLOD') - 3
        a3 = ab[a:a+8]
        a4 = a3[4:]
        a2 = ab[a:a+4]
        vitri = int.from_bytes(a2, byteorder='little')
        vitri2 = int.from_bytes(a4, byteorder='little')
        a5 = ab[a:a+vitri]
        a25 = ab[a10:a10+vitri2]
        a22 = ab[a10:a10+vitri2].replace(b'\x00ArtSkinPrefabLOD', b'\x00ArtPrefabLOD')
        a13 = len(a22).to_bytes(4, byteorder='little') + a22[4:]
        code = a5.replace(a25, a13)
        data3 = len(code).to_bytes(2, byteorder='little') + code[2:]
        return data3

    def ArtSkinPrefabLODExnew(data2):
        a = ab.find(b'\x00ArtSkinPrefabLODEx') - 7
        a10 = ab.find(b'\x00ArtSkinPrefabLODEx') - 3
        a3 = ab[a:a+8]
        a4 = a3[4:]
        a2 = ab[a:a+4]
        vitri = int.from_bytes(a2, byteorder='little')
        vitri2 = int.from_bytes(a4, byteorder='little')
        a5 = ab[a:a+vitri]
        a25 = ab[a10:a10+vitri2]
        a22 = ab[a10:a10+vitri2].replace(b'\x00ArtSkinPrefabLODEx', b'\x00ArtPrefabLODEx')
        a13 = len(a22).to_bytes(4, byteorder='little') + a22[4:]
        code = a5.replace(a25, a13)
        data2 = len(code).to_bytes(4, byteorder='little') + code[4:]
        return data2

    #codeskinmd
    SkinMD=r[:skinprefag]

    #skinmd Art
    Art=SkinMD.find(b'ArtPrefabLOD')-8
    tinhskinpre=SkinMD[Art:Art+4]
    tinhskinpre1=int.from_bytes(tinhskinpre,byteorder='little')
    tinhskinpre2=SkinMD[Art:Art+tinhskinpre1] #
    #skinmd ArtLobbyShowLOD
    ArtLobby=SkinMD.find(b'ArtLobbyShowLOD')-8
    tinhArtLobby=SkinMD[ArtLobby:ArtLobby+4]
    tinhArtLobby1=int.from_bytes(tinhArtLobby,byteorder='little')
    tinhArtLobby2=SkinMD[ArtLobby:ArtLobby+tinhArtLobby1] #
    ArtSkinPrefab=b''
    ArtSkinPrefab+=ArtSkinPrefabLOD(skinmoi)
    CodeNewMD=SkinMD.replace(tinhskinpre2,ArtSkinPrefab)
    ArtSkinLobby=b''
    ArtSkinLobby+=ArtSkinLobbyShowLOD(skinmoi)
    CodeNewMD=CodeNewMD.replace(tinhArtLobby2,ArtSkinLobby)
    ArtLobbyIdle=CodeNewMD.find(b'ArtLobbyIdleShowLOD0')-8
    cammd=CodeNewMD[ArtLobbyIdle:999999]
    ArtLobbyIdleSkin=skinmoi.find(b'ArtSkinLobbyIdleShowLOD')-8
    camSkin=skinmoi[ArtLobbyIdleSkin:999999]
    camSkin=ArtSkinLobbyIdleShowLOD(camSkin)
    if mkcam == b'\x05':
        camSkin=camSkin.replace(CODEFULL,b'')
    CodeNewMD=CodeNewMD.replace(cammd,camSkin)
    CodeFull=codeskinnew.replace(SkinMD,CodeNewMD)
    RootDtrc=CodeFull[:84]
    RootDsau=CodeFull[84:]
    RootD1=RootDsau[8:12]
    VTR=int.from_bytes(RootD1,byteorder='little')#ArtPrefabLOD
    m=RootDsau.find(b'ArtPrefabLOD')-8
    FIXTRIEUVAN=b'\x61\x00\x00\x00\x19\x00\x00\x00\x75\x73\x65\x53\x74\x61\x74\x65\x44\x72\x69\x76\x65\x6E\x4D\x65\x63\x61\x6E\x69\x6D\x3C\x00\x00\x00\x03\x00\x00\x00\x0D\x00\x00\x00\x06\x00\x00\x00\x4A\x54\x50\x72\x69\x1A\x00\x00\x00\x08\x00\x00\x00\x54\x79\x70\x65\x53\x79\x73\x74\x65\x6D\x2E\x42\x6F\x6F\x6C\x65\x61\x6E\x0D\x00\x00\x00\x05\x00\x00\x00\x56\x54\x72\x75\x65\x04\x00\x00\x00'
    #if IDCHECK == '12912':
        #RootDsau=RootDsau[:VTR+8]+FIXTRIEUVAN+RootDsau[m:] 
    tinhRootDsau=len(RootDsau).to_bytes(4,byteorder='little')+RootDsau[4:]
    tinhRootDtrc=RootDtrc+tinhRootDsau
    CodeDayDu=len(tinhRootDtrc).to_bytes(4,byteorder='little')+tinhRootDtrc[4:]
    CodeDayDu=CodeDayDu.replace(b"Light<",b"00000<")
    CodeDayDu = CodeDayDu.replace(b"imeline<", b"1234567<")
    CodeDayDu = CodeDayDu.replace(b"ArtPrefabLODEx", b"ModByKunnAOVdz")
    infthem = '1'
    lodinf = '1'
    showinf = '1'
    if infthem == "1":
        if showinf == "1":
            CodeDayDu=CodeDayDu.replace(b"Show2\x04", b"Show1\x04")
            CodeDayDu=CodeDayDu.replace(b"Show3\x04", b"Show1\x04")
        if showinf == "2":
            CodeDayDu=CodeDayDu.replace(b"Show1\x04", b"Show2\x04")
            CodeDayDu=CodeDayDu.replace(b"Show3\x04", b"Show2\x04")
        if showinf == "3":
            CodeDayDu=CodeDayDu.replace(b"Show1\x04", b"Show3\x04")
            CodeDayDu=CodeDayDu.replace(b"Show2\x04", b"Show3\x04")
        if lodinf == "1":
            CodeDayDu=CodeDayDu.replace(b"LOD2", b"LOD1")
            CodeDayDu=CodeDayDu.replace(b"LOD3", b"LOD1")
        if lodinf =="2":
            CodeDayDu=CodeDayDu.replace(b"LOD1", b"LOD2")
            CodeDayDu=CodeDayDu.replace(b"LOD3", b"LOD2")
        if lodinf =="3":
            CodeDayDu=CodeDayDu.replace(b"LOD1", b"LOD3")
            CodeDayDu=CodeDayDu.replace(b"LOD2", b"LOD3")
            
    tinhcam=CodeDayDu[:89]
    with open(op,'wb')as f: f.write(CodeDayDu)
    o=open(op,'rb')
    h=o.read(92)
    k=0
    while True:
        r1=o.read(4)
        if r1==b'':
            break
        KB=r1.hex()
        KB=KB[6:8]+KB[4:6]+KB[2:4]+KB[0:2]
        KB=int(KB,16)
        O=r1+o.read(KB-4)
        k+=1
    o.close()
    k=k.to_bytes(1,byteorder='little')
    tinhcam1=CodeDayDu[:88]+k
    CodeDayDu=CodeDayDu.replace(tinhcam,tinhcam1)
    with open(op,'wb')as f: f.write(CodeDayDu)

#-----------------------------------------------
class StringBytes:
    def __init__(self, String):
        self.String = String
        self.OldString = String

    def tell(self):
        return len(self.OldString) - len(self.String)

    def seek(self, I, O=0):
        if O == 0:
            self.String = self.OldString[I:]
        elif O == 1:
            self.String = self.String[I:]

    def read(self, Int=None):
        if Int is None:
            return b""
        R = self.String[:Int]
        self.String = self.String[Int:]
        return R


class Bytes_XML:
    def decode(String):
        def get_int(A):
            return int.from_bytes(A.read(4), 'little')

        def get_str(A, pos=None):
            if pos is not None:
                A.seek(pos, 0)
            ofs = get_int(A)
            stri = A.read(ofs - 4)
            return stri.decode()

        def get_attr(A, pos=None):
            if pos is None:
                pos = A.tell()
            ofs = get_int(A)
            type = get_int(A)
            if type == 5:
                stri = A.read(ofs - 8).decode()[1:]
                check_four(A)
                A.seek(pos + ofs, 0)
                return stri
            else:
                if type == 6:
                    stri = A.read(ofs - 8).decode()
                    if stri.startswith('JT'):
                        if stri == 'JTArr':
                            stri = 'Array'
                        elif stri == 'JTPri':
                            stri = 'String'
                        else:
                            stri = stri[2:]
                        name = 'var'
                    else:
                        name = 'var_Raw'
                elif type == 8:
                    stri2 = A.read(ofs - 8).decode()
                    if stri2.startswith('Type'):
                        stri = stri2[4:]
                        name = 'type'
                    else:
                        stri = stri2
                        name = 'type_Raw'
                else:
                    stri = A.read(ofs - 8).decode()
                    name = str(type)
                    A.seek(pos + ofs, 0)
                return {name: stri}

        def check_four(A):
            if get_int(A) != 4:
                A.seek(-4, 1)

        def get_node(A, fid=None, sta=None):
            global i
            ofs = get_int(A)
            stri = get_str(A)
            myid = i
            i += 1
            A.seek(4, 1)
            aidx = get_int(A)
            ite = False
            attr = {}
            for _ in range(aidx):
                attr1 = get_attr(A)
                if isinstance(attr1, str):
                    text1 = attr1
                    ite = True
                else:
                    attr.update(attr1)
            if fid is None:
                nod[myid] = ET.SubElement(root, stri, attrib=attr)
            else:
                nod[myid] = ET.SubElement(nod[fid], stri, attrib=attr)
            if ite:
                if text1 == '':
                    nod[myid].set("value", " ")
                else:
                    nod[myid].set("value", text1)
            check_four(A)
            chk = sta + ofs - A.tell()
            if chk > 12:
                A.seek(4, 1)
                sidx = get_int(A)
                for _ in range(sidx):
                    get_node(A, myid, A.tell())
            A.seek(sta + ofs, 0)

        A = StringBytes(String)
        global i, nod, root
        i = 0
        nod = {}
        ofs = get_int(A)
        stri = get_str(A)
        A.seek(4, 1)
        aidx = get_int(A)
        ite = False
        attr = {}
        for _ in range(aidx):
            attr1 = get_attr(A)
            if isinstance(attr1, str):
                text1 = attr1
                ite = True
            else:
                attr.update(attr1)
        root = ET.Element(stri, attrib=attr)
        if ite:
            root.set("value", text1)
        check_four(A)
        chk = ofs - A.tell()
        if chk > 12:
            A.seek(4, 1)
            sidx = get_int(A)
            for _ in range(sidx):
                get_node(A, None, A.tell())

        try:
            xml_str = minidom.parseString(ET.tostring(root, "utf-8").decode()).toprettyxml(indent="  ", newl="\r\n")
            return xml_str.encode('utf-8')  # always return bytes
        except Exception as e:
            print("[LỖI decode] minidom thất bại:", e)
            return ET.tostring(root, "utf-8")  # fallback: still bytes


    def encode(xmlfile):
        def byteint(num):
            return num.to_bytes(4, byteorder='little')

        def bytestr(stri):
            outbyte = byteint(len(stri) + 4) + stri.encode()
            return outbyte

        def byteattr(key, attr):
            if key == 'var':
                stri = 'JT' + attr[key] if attr[key] not in ['Array', 'String'] else {'Array': 'JTArr', 'String': 'JTPri'}[attr[key]]
                aid = 6
            elif key == 'var_Raw':
                stri = attr[key]
                aid = 6
            elif key == 'type':
                stri = 'Type' + attr[key]
                aid = 8
            elif key == 'type_Raw':
                stri = attr[key]
                aid = 8
            elif key == "value":
                return b""
            else:
                stri = attr[key]
                aid = int(key)
            stripro = stri.encode()
            return byteint(len(stripro) + 8) + byteint(aid) + stripro

        def bytenode(node):
            name = bytestr(node.tag)
            attr_data = b''
            aindex = len(node.attrib)
            plus = 8
            for key in node.attrib:
                if key == "value":
                    aindex -= 1
                attr_data += byteattr(key, node.attrib)
            if node.get("value") and not node.get("value").startswith('\n'):
                val = node.get("value")
                if val == " ":
                    val = ""
                stripro = ('V' + val).encode()
                attr_data += byteint(len(stripro) + 8) + byteint(5) + stripro + byteint(4)
                aindex += 1
                plus = 4
            attr_data = byteint(len(attr_data) + plus) + byteint(aindex) + attr_data + byteint(4)
            child_data = b''
            if len(node):
                children = [bytenode(child) for child in node]
                child_data = b''.join(children)
                child_data = byteint(len(child_data) + 8) + byteint(len(children)) + child_data
            else:
                child_data = byteint(4)
            return byteint(len(name + attr_data + child_data) + 4) + name + attr_data + child_data

        tree = ET.fromstring(xmlfile)
        return bytenode(tree)
                       
def process_file(file_path_FL, LC):
    with open(file_path_FL, "rb") as f:
        G = f.read()

    try:
        if LC == "1":
            decoded = Bytes_XML.decode(G)
            if decoded:
                with open(file_path_FL, "wb") as f1:
                    f1.write(decoded)
            else:
                print(f"[LỖI] Không decode được file: {file_path_FL}")
        elif LC == "2":
            encoded = Bytes_XML.encode(G.decode())
            with open(file_path_FL, "wb") as f1:
                f1.write(encoded)
    except Exception as e:
        print(f"[LỖI] Lỗi khi xử lý file: {file_path_FL} → {e}")
                      
def process_directory(directory_path, LC):
    process_file(directory_path, LC)
#-----------------------------------------------
for IdCheck in IDMODSKIN1:
    phukien = ''
    phukienv = ''

    if IdCheck == '52007':
        print(f"[✓] Chọn phụ kiện cho Veres ({IdCheck}):")
        phukien1 = input("[1] Xanh  | [2] Đỏ | [3] Không dùng phụ kiện: ").strip()
        if phukien1 == "1":
            phukien = 'xanh'
        elif phukien1 == "2":
            phukien = 'do'
        elif phukien1 == "3":
            phukien = ''
        else:
            print("[-] Lựa chọn không hợp lệ cho Veres.")

    if IdCheck == '13311':
        print(f"[✓] Chọn phụ kiện cho Valhein ({IdCheck}):")
        phukien1v = input("[1] Vàng | [2] Đỏ | [3] Không dùng phụ kiện: ").strip()
        if phukien1v == "1":
            phukienv = 'vangv'
        elif phukien1v == "2":
            phukienv = 'dov'
        elif phukien1v == "3":
            phukienv = ''
        else:
            print("[-] Lựa chọn không hợp lệ cho Valhein.")
    if phukien == 'do' and IDMODSKIN == '52007':
        Directory = f'{pack_name}/Resources/1.58.1/Prefab_Characters/mod/Prefab_Hero/520_Veres/520_Veres_actorinfo.bytes'
        LC = '1'
        process_directory(Directory, LC)

        with open(Directory, 'rb') as f:
            InfosVeres = f.read()
            InfosVeres = InfosVeres.replace(b'5208_Veres_LOD', b'Component/5208_Veres_RT_3_LOD').replace(b'5208_Veres_Show', b'Component/5208_Veres_RT_3_Show')

        with open(Directory, 'wb') as f:
            f.write(InfosVeres)

        LC = '2'
        process_directory(Directory, LC)
        print('✓ Infos Veres - Phụ Kiện Đỏ: Đã Mod Xong')

    elif phukienv == 'dov' and IDMODSKIN == '13311':
        Directory = f'{pack_name}/Resources/1.58.1/Prefab_Characters/mod/Prefab_Hero/133_DiRenJie/133_DiRenJie_actorinfo.bytes'
        LC = '1'
        process_directory(Directory, LC)

        with open(Directory, 'rb') as f:
            InfosValhein = f.read()
            InfosValhein = InfosValhein.replace(b'13312_DiRenJie_AW1_LOD', b'Awaken/13312_DiRenJie_04_LOD')\
                                       .replace(b'13312_DiRenJie_AW1_Show', b'Component/13312_DiRenJie_AW5_RT_3_Show')\
                                       .replace(b'1331_DiRenJie_Cam', b'Awaken/13312_DiRenJie_AW5_Cam')

        with open(Directory, 'wb') as f:
            f.write(InfosValhein)

        LC = '2'
        process_directory(Directory, LC)
        print('✓ Infos Valhein - Phụ Kiện Đỏ Ver: Đã Mod Xong')

    elif IDMODSKIN == '16707':
        with zipfile.ZipFile('Resources/1.58.1/Prefab_Characters/Actor_167_Infos.pkg.bytes') as zipc:
            zipc.extractall(f'{pack_name}/Resources/1.58.1/Prefab_Characters/mod')

        DuongDan1 = f'{pack_name}/Resources/1.58.1/Prefab_Characters/mod/Prefab_Hero/167_WuKong/167_WuKong_actorinfo.bytes'
        giai(DuongDan1)
        LC = '1'
        process_directory(DuongDan1, LC)

        with open(DuongDan1, "rb") as f:
            data = f.read()

        pattern_1678 = re.compile(
            rb'<ArtSkinPrefabLOD[^>]*>\s*<Element[^>]*1678_SunWuKong_AW1_LOD1.*?</LookAt>',
            re.DOTALL
        )
        match_1678 = pattern_1678.search(data)
        if not match_1678:
            print("❌ Không tìm thấy block 1678.")
            exit()
        block_1678 = match_1678.group()

        pattern_block_dau = re.compile(
            rb'<ArtPrefabLOD[^>]*>.*?<ArtSkinLobbyShowCamera[^>]*?/>',
            re.DOTALL
        )
        data = pattern_block_dau.sub(block_1678, data)

        pattern_all_skin_blocks = re.compile(
            rb'(<ArtSkinPrefabLOD[^>]*>.*?</LookAt>)',
            re.DOTALL
        )

        def replace_skin_block(match):
            block = match.group()
            if b'1678_SunWuKong_AW1' in block:
                return block
            return block_1678

        data_moi = pattern_all_skin_blocks.sub(replace_skin_block, data)

        with open(DuongDan1, "wb") as f:
            f.write(data_moi)

        with open(DuongDan1, "rb") as f:
            data = f.read()

        data = data.replace(
            b'1678_SunWuKong_AW1',
            b'1678_SunWuKong_AW5'
        ).replace(
            b'<ArtSkinLobbyShowCamera var="String" type="System.String" value="Prefab_Characters/Prefab_Hero/167_WuKong/1678_SunWuKong_AW5_Cam"/>',
            b'<ArtSkinLobbyShowCamera var="String" type="System.String" value="Prefab_Characters/Prefab_Hero/167_WuKong/Awaken/1678_SunWuKong_03_Cam"/>\n      <ArtSkinLobbyShowMovie var="String" type="System.String" value="Prefab_Characters/Prefab_Hero/167_WuKong/Awaken/1678_SunWuKong_03_Movie"/>'
        ).replace(
            b'<ArtSkinPrefabLOD var="Array" type="System.String[]">',
            b'<ArtPrefabLOD var="Array" type="System.String[]">', 1
        ).replace(
            b'</ArtSkinPrefabLOD>',
            b'</ArtPrefabLOD>', 1
        ).replace(
            b'<ArtSkinPrefabLODEx var="Array" type="System.String[]">',
            b'<ArtPrefabLODEx var="Array" type="System.String[]">', 1
        ).replace(
            b'</ArtSkinPrefabLODEx>',
            b'</ArtPrefabLODEx>', 1
        ).replace(
            b'<ArtSkinLobbyShowLOD var="Array" type="System.String[]">',
            b'<ArtLobbyShowLOD var="Array" type="System.String[]">', 1
        ).replace(
            b'</ArtSkinLobbyShowLOD>',
            b'</ArtLobbyShowLOD>', 1
        ).replace(
            b'<ArtSkinLobbyIdleShowLOD',
            b'<ArtLobbyIdleShowLOD', 1
        ).replace(
            b'</ArtSkinLobbyIdleShowLOD>',
            b'</ArtLobbyIdleShowLOD>', 1
        )


        with open(DuongDan1, "wb") as f:
            f.write(data)

        LC = '2'
        process_directory(DuongDan1, LC)

    else:
        print(f'    Phu Kien : Khong Support.')

#-----------------------------------------------
    Files_Directory = f'{pack_name}/Resources/1.58.1/Ages/Prefab_Characters/Prefab_Hero/mod4'
    if os.path.exists(Files_Directory):
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
                shutil.rmtree(folder_path)
        shutil.rmtree(Files_Directory)

mod1_dir = f'{pack_name}/Resources/1.58.1/Ages/Prefab_Characters/Prefab_Hero/mod1'
if os.path.exists(mod1_dir):
    with zipfile.ZipFile(f'{pack_name}/Resources/1.58.1/Ages/Prefab_Characters/Prefab_Hero/CommonActions.pkg.bytes', 'w', compression=zipfile.ZIP_STORED) as zipf:
        for root, dirs, files in os.walk(mod1_dir):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, mod1_dir)
                zipf.write(file_path, arcname)
    shutil.rmtree(mod1_dir)

mod_dir = f'{pack_name}/Resources/1.58.1/Prefab_Characters/mod/Prefab_Hero'
if os.path.exists(mod_dir):
    for folder_name in os.listdir(mod_dir):
        full_path = os.path.join(mod_dir, folder_name)
        if not os.path.isdir(full_path) or "_" not in folder_name:
            continue
        try:
            hero_id = folder_name.split("_")[0]
            zip_file_name = f"Actor_{hero_id}_Infos.pkg.bytes"
            zip_file_path = os.path.join(f'{pack_name}/Resources/1.58.1/Prefab_Characters', zip_file_name)

            with zipfile.ZipFile(zip_file_path, 'w', compression=zipfile.ZIP_STORED) as zipf:
                for root, _, files in os.walk(full_path):
                    for file in files:
                        file_path = os.path.join(root, file)
                        rel_path = os.path.relpath(file_path, full_path)
                        arcname = os.path.join("Prefab_Hero", folder_name, rel_path)
                        zipf.write(file_path, arcname)
            print(f"  {os.path.basename(zip_file_path)} Done")
        except Exception as e:
            print(f"❌ Lỗi khi nén {folder_name}: {e}")
    shutil.rmtree(f'{pack_name}/Resources/1.58.1/Prefab_Characters/mod/')

if os.path.exists('mod5'):
    shutil.rmtree('mod5')
#-----------------------------------------------