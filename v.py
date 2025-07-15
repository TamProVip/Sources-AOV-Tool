import os; import re; import getopt; import random; import pyzstd; from xml.dom import minidom; from colorama import Fore; import sys; import shutil; import zipfile; import uuid; from collections import Counter; import xml.etree.ElementTree as ET; from collections import defaultdict; import os as O, binascii as X; from pathlib import Path; from random import randint; import datetime

# Đọc version từ file
try:
    folders = os.listdir("Resources")
    Ver = next((f for f in folders if os.path.isdir(os.path.join("Resources", f))), "Unknown")
except:
    Ver = "Unknown"

width = shutil.get_terminal_size(fallback=(80, 20)).columns

def print_centered(line):
    text_only = line.encode('ascii', 'ignore').decode() 
    spaces = max((width - len(text_only)) // 2, 0)
    print(" " * spaces + line)

# In banner
print("╭" + "─" * (width - 2) + "╮")
print_centered("  Ytb Tâm Mod AOV")
print_centered("  Tool: Mod Skin Engine")
print_centered(f"  Version : {Ver}")
print("╰" + "─" * (width - 2) + "╯")
print()

# In thêm info
print_centered(f" {datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
print_centered(f" Python {os.sys.version.split()[0]}")

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

def enc(path1=None):
    if path1 is None: path1 = input("Nhập đường dẫn: ")
    for path in path1.split():
        files = []
        if os.path.isdir(path):
            for f1, _, f2 in os.walk(path):
                if 'imprint' not in f1.lower():
                    files += [os.path.join(f1, f) for f in f2 if f.endswith(('.xml','.bytes','.txt'))]
        elif os.path.isfile(path): files = [path]
        for file in files:
            try:
                with open(file, 'rb') as f: b = f.read()
                c = pyzstd.compress(b, 1, pyzstd.ZstdDict(ZSTD_DICT))
                if file.endswith('.xml'): c += b"ModByYtbTamPro"
                c += c[len(c)//2:len(c)//2+randint(3,4)]
                c = b'"J\x00\xef' + len(b).to_bytes(4,'little') + c
                with open(file, 'wb') as f: f.write(c)
            except Exception as e:
                pass

#print("\033[36m[III]. Chọn Chức Năng Fix Lag\n   [1].Fix Lag AssetRefs\n   [2].Fix Lag Born\n   [3].Không Fix Lag")
fixlag = '1'#input("\n>>> ")

def process_input_numbers(numbers):
    return numbers 

input_numbers = input('\n\t' + "ID: ")
numbers = [int(num) for num in input_numbers.split()]
results = process_input_numbers(numbers)

if results is None:
    sys.exit()

result_str = ' '.join(map(str, results))
IDD = result_str
IDMODSKIN = IDD.split()
IDMODSKIN1 = IDD.split()

if len(IDMODSKIN1) == 1:
    print(Fore.RED + "Chỉ 1 ID được nhập vào. Tool sẽ thoát." + Fore.RESET)
    #sys.exit()

DANHSACH = IDD.split()

with open(f'Resources/1.59.1/Databin/Client/Actor/heroSkin.bytes', 'rb') as f:
    a = f.read()
if b'"J\x00' in a:
    giai(f'Resources/1.59.1/Databin/Client/Actor/heroSkin.bytes')

FILES_MAP = [
    f'Resources/1.59.1/Languages/VN_Garena_VN/languageMap.txt',
    f'Resources/1.59.1/Languages/VN_Garena_VN/languageMap_Newbie.txt',
    f'Resources/1.59.1/Languages/VN_Garena_VN/languageMap_WorldConcept.txt',
    f'Resources/1.59.1/Languages/VN_Garena_VN/languageMap_Xls.txt',
    f'Resources/1.59.1/Languages/VN_Garena_VN/lanMapIncremental.txt'
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
        with open(f'Resources/1.59.1/Databin/Client/Actor/heroSkin.bytes', 'rb') as f:
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
                FolderMod = ((A + b' ' + B).decode(errors='ignore'))
                FolderMod = ''.join(char for char in FolderMod if char not in ['/', '\\', ':', '*', '?', '"', '<', '>', '|'])

                if FolderMod.strip() != '' and '[ex]' not in FolderMod:
                    TENSKIN.append(FolderMod)
            except:
                continue 
aaabbbcccnnn = ''
for FolderMod in TENSKIN:
    aaabbbcccnnn = FolderMod
    ten_final = FolderMod
    with open('List.txt', 'a', encoding='utf8') as f: 
        f.write(FolderMod + '\n')

print(Fore.YELLOW + '-' * 50 + Fore.RESET)

if len(DANHSACH) >= 1:
    FolderMod = input("Nhập Tên Pack Skin: ")
else:
    pass

if not os.path.exists(FolderMod):
    os.makedirs(FolderMod)
directorie = f'{FolderMod}/Resources/1.59.1/AssetRefs/Hero'
os.makedirs(directorie, exist_ok=True)
base_path = f"{FolderMod}/Resources/1.59.1/Databin/Client/"
directories = ["Actor", "Shop", "Sound", "Skill", "Character", "Motion", "Global"]
for directory in directories:
    os.makedirs(os.path.join(base_path, directory), exist_ok=True)
#-----------------------------------------------
file_actor = "Resources/1.59.1/Databin/Client/Actor/heroSkin.bytes"
file_actor_mod = f"{FolderMod}/Resources/1.59.1/Databin/Client/Actor/heroSkin.bytes"
shutil.copy(file_actor, file_actor_mod)
#giai(file_actor_mod)

file_shop = "Resources/1.59.1/Databin/Client/Shop/HeroSkinShop.bytes"
file_shop_mod = f"{FolderMod}/Resources/1.59.1/Databin/Client/Shop/HeroSkinShop.bytes"
shutil.copy(file_shop, file_shop_mod)
giai(file_shop_mod)

file_sound1 = "Resources/1.59.1/Databin/Client/Sound/BattleBank.bytes"
file_sound_mod1 = f"{FolderMod}/Resources/1.59.1/Databin/Client/Sound/BattleBank.bytes"
shutil.copy(file_sound1, file_sound_mod1)
giai(file_sound_mod1)

file_sound2 = "Resources/1.59.1/Databin/Client/Sound/ChatSound.bytes"
file_sound_mod2 = f"{FolderMod}/Resources/1.59.1/Databin/Client/Sound/ChatSound.bytes"
shutil.copy(file_sound2, file_sound_mod2)
giai(file_sound_mod2)

file_sound3 = "Resources/1.59.1/Databin/Client/Sound/HeroSound.bytes"
file_sound_mod3 = f"{FolderMod}/Resources/1.59.1/Databin/Client/Sound/HeroSound.bytes"
shutil.copy(file_sound3, file_sound_mod3)
giai(file_sound_mod3)

file_sound4 = "Resources/1.59.1/Databin/Client/Sound/LobbyBank.bytes"
file_sound_mod4 = f"{FolderMod}/Resources/1.59.1/Databin/Client/Sound/LobbyBank.bytes"
shutil.copy(file_sound4, file_sound_mod4)
giai(file_sound_mod4)

file_sound5 = "Resources/1.59.1/Databin/Client/Sound/LobbySound.bytes"
file_sound_mod5 = f"{FolderMod}/Resources/1.59.1/Databin/Client/Sound/LobbySound.bytes"
shutil.copy(file_sound5, file_sound_mod5)
giai(file_sound_mod5)

Sound_Files = f"{FolderMod}/Resources/1.59.1/Databin/Client/Sound"

file_skill1 = "Resources/1.59.1/Databin/Client/Skill/liteBulletCfg.bytes"
file_mod_skill1 = f"{FolderMod}/Resources/1.59.1/Databin/Client/Skill/liteBulletCfg.bytes"
shutil.copy(file_skill1, file_mod_skill1)
giai(file_mod_skill1)

file_skill2 = "Resources/1.59.1/Databin/Client/Skill/skillmark.bytes"
file_mod_skill2 = f"{FolderMod}/Resources/1.59.1/Databin/Client/Skill/skillmark.bytes"
shutil.copy(file_skill2, file_mod_skill2)
giai(file_mod_skill2)

file_Character = "Resources/1.59.1/Databin/Client/Character/ResCharacterComponent.bytes"
file_mod_Character = f"{FolderMod}/Resources/1.59.1/Databin/Client/Character/ResCharacterComponent.bytes"
shutil.copy(file_Character, file_mod_Character)
giai(file_mod_Character)

file_Modtion = "Resources/1.59.1/Databin/Client/Motion/ResSkinMotionBaseCfg.bytes"
file_mod_Modtion = f"{FolderMod}/Resources/1.59.1/Databin/Client/Motion/ResSkinMotionBaseCfg.bytes"
shutil.copy(file_Modtion, file_mod_Modtion)
giai(file_mod_Modtion)

file_vien = "Resources/1.59.1/Databin/Client/Global/HeadImage.bytes"
file_mod_vien = f"{FolderMod}/Resources/1.59.1/Databin/Client/Global/HeadImage.bytes"
shutil.copy(file_vien, file_mod_vien)
giai(file_mod_vien)

with zipfile.ZipFile('Resources/1.59.1/Ages/Prefab_Characters/Prefab_Hero/CommonActions.pkg.bytes') as zipf:
    zipf.extractall(f'{FolderMod}/Resources/1.59.1/Ages/Prefab_Characters/Prefab_Hero/mod1/')
    giai(f'{FolderMod}/Resources/1.59.1/Ages/Prefab_Characters/Prefab_Hero/mod1/commonresource/Back.xml')
#-----------------------------------------------
ngoaihinhkhieov=b'B\x10\x00\x00\x0b\x00\x00\x00ElementE\x00\x00\x00\x02\x00\x00\x00\r\x00\x00\x00\x06\x00\x00\x00JTCom0\x00\x00\x00\x08\x00\x00\x00TypeAssets.Scripts.GameLogic.SkinElement\x04\x00\x00\x00\xea\x0f\x00\x00\x0e\x00\x00\x00\x10\x02\x00\x00\x14\x00\x00\x00ArtSkinPrefabLOD0\x00\x00\x00\x02\x00\x00\x00\r\x00\x00\x00\x06\x00\x00\x00JTArr\x1b\x00\x00\x00\x08\x00\x00\x00TypeSystem.String[]\x04\x00\x00\x00\xc4\x01\x00\x00\x03\x00\x00\x00\x94\x00\x00\x00\x0b\x00\x00\x00Element}\x00\x00\x00\x03\x00\x00\x00\r\x00\x00\x00\x06\x00\x00\x00JTPri\x19\x00\x00\x00\x08\x00\x00\x00TypeSystem.StringO\x00\x00\x00\x05\x00\x00\x00VPrefab_Characters/Prefab_Hero/167_WuKong/Awaken/1678_sunwukong_03_LOD1\x04\x00\x00\x00\x04\x00\x00\x00\x94\x00\x00\x00\x0b\x00\x00\x00Element}\x00\x00\x00\x03\x00\x00\x00\r\x00\x00\x00\x06\x00\x00\x00JTPri\x19\x00\x00\x00\x08\x00\x00\x00TypeSystem.StringO\x00\x00\x00\x05\x00\x00\x00VPrefab_Characters/Prefab_Hero/167_WuKong/Awaken/1678_sunwukong_03_LOD2\x04\x00\x00\x00\x04\x00\x00\x00\x94\x00\x00\x00\x0b\x00\x00\x00Element}\x00\x00\x00\x03\x00\x00\x00\r\x00\x00\x00\x06\x00\x00\x00JTPri\x19\x00\x00\x00\x08\x00\x00\x00TypeSystem.StringO\x00\x00\x00\x05\x00\x00\x00VPrefab_Characters/Prefab_Hero/167_WuKong/Awaken/1678_sunwukong_03_LOD3\x04\x00\x00\x00\x04\x00\x00\x00\xa4\x00\x00\x00\x16\x00\x00\x00ArtSkinPrefabLODEx0\x00\x00\x00\x02\x00\x00\x00\r\x00\x00\x00\x06\x00\x00\x00JTArr\x1b\x00\x00\x00\x08\x00\x00\x00TypeSystem.String[]\x04\x00\x00\x00V\x00\x00\x00\x01\x00\x00\x00N\x00\x00\x00\x0b\x00\x00\x00Element7\x00\x00\x00\x03\x00\x00\x00\r\x00\x00\x00\x06\x00\x00\x00JTPri\x19\x00\x00\x00\x08\x00\x00\x00TypeSystem.String\t\x00\x00\x00\x05\x00\x00\x00V\x04\x00\x00\x00\x04\x00\x00\x00\x16\x02\x00\x00\x17\x00\x00\x00ArtSkinLobbyShowLOD0\x00\x00\x00\x02\x00\x00\x00\r\x00\x00\x00\x06\x00\x00\x00JTArr\x1b\x00\x00\x00\x08\x00\x00\x00TypeSystem.String[]\x04\x00\x00\x00\xc7\x01\x00\x00\x03\x00\x00\x00\x95\x00\x00\x00\x0b\x00\x00\x00Element~\x00\x00\x00\x03\x00\x00\x00\r\x00\x00\x00\x06\x00\x00\x00JTPri\x19\x00\x00\x00\x08\x00\x00\x00TypeSystem.StringP\x00\x00\x00\x05\x00\x00\x00VPrefab_Characters/Prefab_Hero/167_WuKong/Awaken/1678_sunwukong_03_Show1\x04\x00\x00\x00\x04\x00\x00\x00\x95\x00\x00\x00\x0b\x00\x00\x00Element~\x00\x00\x00\x03\x00\x00\x00\r\x00\x00\x00\x06\x00\x00\x00JTPri\x19\x00\x00\x00\x08\x00\x00\x00TypeSystem.StringP\x00\x00\x00\x05\x00\x00\x00VPrefab_Characters/Prefab_Hero/167_WuKong/Awaken/1678_sunwukong_03_Show2\x04\x00\x00\x00\x04\x00\x00\x00\x95\x00\x00\x00\x0b\x00\x00\x00Element~\x00\x00\x00\x03\x00\x00\x00\r\x00\x00\x00\x06\x00\x00\x00JTPri\x19\x00\x00\x00\x08\x00\x00\x00TypeSystem.StringP\x00\x00\x00\x05\x00\x00\x00VPrefab_Characters/Prefab_Hero/167_WuKong/Awaken/1678_sunwukong_03_Show3\x04\x00\x00\x00\x04\x00\x00\x00E\x01\x00\x00\x1b\x00\x00\x00ArtSkinLobbyIdleShowLOD0\x00\x00\x00\x02\x00\x00\x00\r\x00\x00\x00\x06\x00\x00\x00JTArr\x1b\x00\x00\x00\x08\x00\x00\x00TypeSystem.String[]\x04\x00\x00\x00\xf2\x00\x00\x00\x03\x00\x00\x00N\x00\x00\x00\x0b\x00\x00\x00Element7\x00\x00\x00\x03\x00\x00\x00\r\x00\x00\x00\x06\x00\x00\x00JTPri\x19\x00\x00\x00\x08\x00\x00\x00TypeSystem.String\t\x00\x00\x00\x05\x00\x00\x00V\x04\x00\x00\x00\x04\x00\x00\x00N\x00\x00\x00\x0b\x00\x00\x00Element7\x00\x00\x00\x03\x00\x00\x00\r\x00\x00\x00\x06\x00\x00\x00JTPri\x19\x00\x00\x00\x08\x00\x00\x00TypeSystem.String\t\x00\x00\x00\x05\x00\x00\x00V\x04\x00\x00\x00\x04\x00\x00\x00N\x00\x00\x00\x0b\x00\x00\x00Element7\x00\x00\x00\x03\x00\x00\x00\r\x00\x00\x00\x06\x00\x00\x00JTPri\x19\x00\x00\x00\x08\x00\x00\x00TypeSystem.String\t\x00\x00\x00\x05\x00\x00\x00V\x04\x00\x00\x00\x04\x00\x00\x00\xa2\x00\x00\x00\x1a\x00\x00\x00ArtSkinLobbyShowCamera|\x00\x00\x00\x03\x00\x00\x00\r\x00\x00\x00\x06\x00\x00\x00JTPri\x19\x00\x00\x00\x08\x00\x00\x00TypeSystem.StringN\x00\x00\x00\x05\x00\x00\x00VPrefab_Characters/Prefab_Hero/167_wukong/Awaken/1678_sunwukong_03_Cam\x04\x00\x00\x00\x04\x00\x00\x00\xa3\x00\x00\x00\x19\x00\x00\x00ArtSkinLobbyShowMovie~\x00\x00\x00\x03\x00\x00\x00\r\x00\x00\x00\x06\x00\x00\x00JTPri\x19\x00\x00\x00\x08\x00\x00\x00TypeSystem.StringP\x00\x00\x00\x05\x00\x00\x00VPrefab_Characters/Prefab_Hero/167_wukong/Awaken/1678_sunwukong_03_Movie\x04\x00\x00\x00\x04\x00\x00\x00Y\x00\x00\x00\x11\x00\x00\x00useNewMecanim<\x00\x00\x00\x03\x00\x00\x00\r\x00\x00\x00\x06\x00\x00\x00JTPri\x1a\x00\x00\x00\x08\x00\x00\x00TypeSystem.Boolean\r\x00\x00\x00\x05\x00\x00\x00VTrue\x04\x00\x00\x00\x04\x00\x00\x00W\x00\x00\x00\x0f\x00\x00\x00bUnityLight<\x00\x00\x00\x03\x00\x00\x00\r\x00\x00\x00\x06\x00\x00\x00JTPri\x1a\x00\x00\x00\x08\x00\x00\x00TypeSystem.Boolean\r\x00\x00\x00\x05\x00\x00\x00VTrue\x04\x00\x00\x00\x04\x00\x00\x00a\x00\x00\x00\x19\x00\x00\x00bUseCodeAnimComponent<\x00\x00\x00\x03\x00\x00\x00\r\x00\x00\x00\x06\x00\x00\x00JTPri\x1a\x00\x00\x00\x08\x00\x00\x00TypeSystem.Boolean\r\x00\x00\x00\x05\x00\x00\x00VTrue\x04\x00\x00\x00\x04\x00\x00\x00f\x00\x00\x00\x08\x00\x00\x00MSAAR\x00\x00\x00\x03\x00\x00\x00\x0e\x00\x00\x00\x06\x00\x00\x00JTEnum2\x00\x00\x00\x08\x00\x00\x00TypeAssets.Scripts.GameLogic.EAntiAliasing\n\x00\x00\x00\x05\x00\x00\x00V2\x04\x00\x00\x00\x04\x00\x00\x00$\x03\x00\x00\x1a\x00\x00\x00PreloadAnimatorEffects0\x00\x00\x00\x02\x00\x00\x00\r\x00\x00\x00\x06\x00\x00\x00JTArr\x1b\x00\x00\x00\x08\x00\x00\x00TypeSystem.String[]\x04\x00\x00\x00\xd2\x02\x00\x00\x05\x00\x00\x00\x8e\x00\x00\x00\x0b\x00\x00\x00Elementw\x00\x00\x00\x03\x00\x00\x00\r\x00\x00\x00\x06\x00\x00\x00JTPri\x19\x00\x00\x00\x08\x00\x00\x00TypeSystem.StringI\x00\x00\x00\x05\x00\x00\x00Vprefab_skill_effects/hero_skill_effects/167_WuKong/wukong_Sprint\x04\x00\x00\x00\x04\x00\x00\x00\x93\x00\x00\x00\x0b\x00\x00\x00Element|\x00\x00\x00\x03\x00\x00\x00\r\x00\x00\x00\x06\x00\x00\x00JTPri\x19\x00\x00\x00\x08\x00\x00\x00TypeSystem.StringN\x00\x00\x00\x05\x00\x00\x00Vprefab_skill_effects/hero_skill_effects/167_WuKong/wukong_Sprint_Idle\x04\x00\x00\x00\x04\x00\x00\x00\x93\x00\x00\x00\x0b\x00\x00\x00Element|\x00\x00\x00\x03\x00\x00\x00\r\x00\x00\x00\x06\x00\x00\x00JTPri\x19\x00\x00\x00\x08\x00\x00\x00TypeSystem.StringN\x00\x00\x00\x05\x00\x00\x00Vprefab_skill_effects/hero_skill_effects/167_WuKong/wukong_Sprint_Loop\x04\x00\x00\x00\x04\x00\x00\x00\x92\x00\x00\x00\x0b\x00\x00\x00Element{\x00\x00\x00\x03\x00\x00\x00\r\x00\x00\x00\x06\x00\x00\x00JTPri\x19\x00\x00\x00\x08\x00\x00\x00TypeSystem.StringM\x00\x00\x00\x05\x00\x00\x00Vprefab_skill_effects/hero_skill_effects/167_WuKong/wukong_Sprint_Run\x04\x00\x00\x00\x04\x00\x00\x00\x84\x00\x00\x00\x0b\x00\x00\x00Elementm\x00\x00\x00\x03\x00\x00\x00\r\x00\x00\x00\x06\x00\x00\x00JTPri\x19\x00\x00\x00\x08\x00\x00\x00TypeSystem.String?\x00\x00\x00\x05\x00\x00\x00Vprefab_skill_effects/Dance_Effects/167/dance_03_texiao\x04\x00\x00\x00\x04\x00\x00\x00\x86\x03\x00\x00\n\x00\x00\x00LookAtF\x00\x00\x00\x02\x00\x00\x00\r\x00\x00\x00\x06\x00\x00\x00JTCom1\x00\x00\x00\x08\x00\x00\x00TypeAssets.Scripts.GameLogic.CameraLookAt\x04\x00\x00\x00.\x03\x00\x00\x04\x00\x00\x00B\x01\x00\x00\n\x00\x00\x00Offset4\x00\x00\x00\x02\x00\x00\x00\r\x00\x00\x00\x06\x00\x00\x00JTCom\x1f\x00\x00\x00\x08\x00\x00\x00TypeUnityEngine.Vector3\x04\x00\x00\x00\xfc\x00\x00\x00\x03\x00\x00\x00S\x00\x00\x00\x05\x00\x00\x00xB\x00\x00\x00\x03\x00\x00\x00\r\x00\x00\x00\x06\x00\x00\x00JTPri\x19\x00\x00\x00\x08\x00\x00\x00TypeSystem.Single\x14\x00\x00\x00\x05\x00\x00\x00V-0.05998039\x04\x00\x00\x00\x04\x00\x00\x00P\x00\x00\x00\x05\x00\x00\x00y?\x00\x00\x00\x03\x00\x00\x00\r\x00\x00\x00\x06\x00\x00\x00JTPri\x19\x00\x00\x00\x08\x00\x00\x00TypeSystem.Single\x11\x00\x00\x00\x05\x00\x00\x00V1.389713\x04\x00\x00\x00\x04\x00\x00\x00Q\x00\x00\x00\x05\x00\x00\x00z@\x00\x00\x00\x03\x00\x00\x00\r\x00\x00\x00\x06\x00\x00\x00JTPri\x19\x00\x00\x00\x08\x00\x00\x00TypeSystem.Single\x12\x00\x00\x00\x05\x00\x00\x00V-2.490662\x04\x00\x00\x00\x04\x00\x00\x00B\x01\x00\x00\r\x00\x00\x00Direction4\x00\x00\x00\x02\x00\x00\x00\r\x00\x00\x00\x06\x00\x00\x00JTCom\x1f\x00\x00\x00\x08\x00\x00\x00TypeUnityEngine.Vector3\x04\x00\x00\x00\xf9\x00\x00\x00\x03\x00\x00\x00T\x00\x00\x00\x05\x00\x00\x00xC\x00\x00\x00\x03\x00\x00\x00\r\x00\x00\x00\x06\x00\x00\x00JTPri\x19\x00\x00\x00\x08\x00\x00\x00TypeSystem.Single\x15\x00\x00\x00\x05\x00\x00\x00V1.831149E-07\x04\x00\x00\x00\x04\x00\x00\x00T\x00\x00\x00\x05\x00\x00\x00yC\x00\x00\x00\x03\x00\x00\x00\r\x00\x00\x00\x06\x00\x00\x00JTPri\x19\x00\x00\x00\x08\x00\x00\x00TypeSystem.Single\x15\x00\x00\x00\x05\x00\x00\x00V-8.35189E-09\x04\x00\x00\x00\x04\x00\x00\x00I\x00\x00\x00\x05\x00\x00\x00z8\x00\x00\x00\x03\x00\x00\x00\r\x00\x00\x00\x06\x00\x00\x00JTPri\x19\x00\x00\x00\x08\x00\x00\x00TypeSystem.Single\n\x00\x00\x00\x05\x00\x00\x00V1\x04\x00\x00\x00\x04\x00\x00\x00P\x00\x00\x00\x0c\x00\x00\x00Duration8\x00\x00\x00\x03\x00\x00\x00\r\x00\x00\x00\x06\x00\x00\x00JTPri\x19\x00\x00\x00\x08\x00\x00\x00TypeSystem.Single\n\x00\x00\x00\x05\x00\x00\x00V1\x04\x00\x00\x00\x04\x00\x00\x00R\x00\x00\x00\r\x00\x00\x00CameraFOV9\x00\x00\x00\x03\x00\x00\x00\r\x00\x00\x00\x06\x00\x00\x00JTPri\x19\x00\x00\x00\x08\x00\x00\x00TypeSystem.Single\x0b\x00\x00\x00\x05\x00\x00\x00V17\x04\x00\x00\x00\x04\x00\x00\x00m\x00\x00\x00\x0f\x00\x00\x00LightConfigR\x00\x00\x00\x02\x00\x00\x00\r\x00\x00\x00\x06\x00\x00\x00JTCom=\x00\x00\x00\x08\x00\x00\x00TypeAssets.Scripts.GameLogic.PrepareBattleLightConfig\x04\x00\x00\x00\x04\x00\x00\x00'
#-----------------------------------------------
bacvalheinevo1 = b'\r\x01\x00\x00\xff3\x00\x00\x85\x00\x00\x00\x14\x00\x00\x00D898FD6DC80FD88F_##\x00\x0b\x00\x00\x00\x14\x00\x00\x0062C20D284D202339_##\x00\x14\x00\x00\x00105E41477A829A72_##\x00\x01\x01\x00\x00\x00\x00\x01\x00\x00\x00\x00\n\x00\x00\x0013311.png\x00\x00\x00\x01\x00\x00\x00\x00\x00\xc7\x00\x00\x00\x00\x00\x00\x00\x00\x00L\x02\x00\x00\x00\x00\x00\x00\x00\x00\x00\xc4\x0b=\x00\x00\xf7\x07\x02\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x0f\x00\x00\x0020220902000000\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xdd\x83\x01\x00\x01\x01\x00\x00\x06,\x00\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x03\x00\x00\x00\x00\x01\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00'
#-----------------------------------------------
bacvalheinevo5 = b'\x15\x01\x00\x00\xff3\x00\x00\x85\x00\x00\x00\x14\x00\x00\x000B0B75B334002849_##\x00\x0b\x00\x00\x00\x14\x00\x00\x006B7679BBD5264133_##\x00\x14\x00\x00\x00942E74C2AD28AE4C_##\x00\x01\x01\x00\x00\x00\x00\x01\x00\x00\x00\x00\x12\x00\x00\x00Awake_Label_6.png\x00\x01\x00\x01\x00\x00\x00\x00\x01\xc7\x00\x00\x00\x00\x00\x00\x00\x00\x00L\x02\x00\x00\x00\x00\x01\x00\x00\x00\x00\x8a\t=\x00\x00\x9f\x8c\x02\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x0f\x00\x00\x0020210318060000\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x17\x86\x01\x00\x01\x01\x00\x00\x06:\x00\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x03\x00\x00\x00\x00\x01\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00'
#-----------------------------------------------
bgbuterbac1 = b' \x01\x00\x00d-\x00\x00t\x00\x00\x00\x14\x00\x00\x0059AFBB630F219764_##\x00\x14\x00\x00\x00\x14\x00\x00\x00A07C714FC9B4B897_##\x00\x14\x00\x00\x004E514D7070D9574D_##\x00\x01\x01\x00\x00\x00\x00\x01\x00\x00\x00\x00\n\x00\x00\x0011620.png\x00\x00\x00\x14\x00\x00\x001236D7EB468A4620_##'
#-----------------------------------------------
bgbuterbac5= b'(\x01\x00\x00d-\x00\x00t\x00\x00\x00\x14\x00\x00\x000B0B75B334002849_##\x00\x00\x00\x00\x00\x14\x00\x00\x006B7679BBD5264133_##\x00\x14\x00\x00\x00942E74C2AD28AE4C_##\x00\x01\x01\x00\x00\x00\x00\x01\x00\x00\x00\x00\x12\x00\x00\x00Awake_Label_6.png\x00\x00\x00\x14\x00\x00\x001236D7EB468A4620_##' # BG Toi Thuong
#-----------------------------------------------
bacngokhongevo1 = b'\x00CA\x00\x00\xa7\x00\x00\x00\x14\x00\x00\x000B0B75B334002849_##\x00\x07\x00\x00\x00\x14\x00\x00\x006B7679BBD5264133_##\x00\x14\x00\x00\x00942E74C2AD28AE4C_##\x00\x01\x01\x00\x00\x00\x00\x01\x00\x00\x00\x00\x12\x00\x00\x00Awake_Label_1.png'    
bacngokhongevo5 = b'\x00CA\x00\x00\xa7\x00\x00\x00\x14\x00\x00\x000B0B75B334002849_##\x00\x07\x00\x00\x00\x14\x00\x00\x006B7679BBD5264133_##\x00\x14\x00\x00\x00942E74C2AD28AE4C_##\x00\x01\x01\x00\x00\x00\x00\x01\x00\x00\x00\x00\x12\x00\x00\x00Awake_Label_6.png'
#-----------------------------------------------
ngoaihinhdoveres = b'9\t\x00\x00\x0b\x00\x00\x00ElementE\x00\x00\x00\x02\x00\x00\x00\r\x00\x00\x00\x06\x00\x00\x00JTCom0\x00\x00\x00\x08\x00\x00\x00TypeAssets.Scripts.GameLogic.SkinElement\x04\x00\x00\x00\xe1\x08\x00\x00\x0b\x00\x00\x00\x10\x02\x00\x00\x14\x00\x00\x00ArtSkinPrefabLOD0\x00\x00\x00\x02\x00\x00\x00\r\x00\x00\x00\x06\x00\x00\x00JTArr\x1b\x00\x00\x00\x08\x00\x00\x00TypeSystem.String[]\x04\x00\x00\x00\xc4\x01\x00\x00\x03\x00\x00\x00\x94\x00\x00\x00\x0b\x00\x00\x00Element}\x00\x00\x00\x03\x00\x00\x00\r\x00\x00\x00\x06\x00\x00\x00JTPri\x19\x00\x00\x00\x08\x00\x00\x00TypeSystem.StringO\x00\x00\x00\x05\x00\x00\x00VPrefab_Characters/Prefab_Hero/520_Veres/Component/5208_Veres_RT_3_LOD2\x04\x00\x00\x00\x04\x00\x00\x00\x94\x00\x00\x00\x0b\x00\x00\x00Element}\x00\x00\x00\x03\x00\x00\x00\r\x00\x00\x00\x06\x00\x00\x00JTPri\x19\x00\x00\x00\x08\x00\x00\x00TypeSystem.StringO\x00\x00\x00\x05\x00\x00\x00VPrefab_Characters/Prefab_Hero/520_Veres/Component/5208_Veres_RT_3_LOD2\x04\x00\x00\x00\x04\x00\x00\x00\x94\x00\x00\x00\x0b\x00\x00\x00Element}\x00\x00\x00\x03\x00\x00\x00\r\x00\x00\x00\x06\x00\x00\x00JTPri\x19\x00\x00\x00\x08\x00\x00\x00TypeSystem.StringO\x00\x00\x00\x05\x00\x00\x00VPrefab_Characters/Prefab_Hero/520_Veres/Component/5208_Veres_RT_3_LOD2\x04\x00\x00\x00\x04\x00\x00\x00\xa4\x00\x00\x00\x16\x00\x00\x00ArtSkinPrefabLODEx0\x00\x00\x00\x02\x00\x00\x00\r\x00\x00\x00\x06\x00\x00\x00JTArr\x1b\x00\x00\x00\x08\x00\x00\x00TypeSystem.String[]\x04\x00\x00\x00V\x00\x00\x00\x01\x00\x00\x00N\x00\x00\x00\x0b\x00\x00\x00Element7\x00\x00\x00\x03\x00\x00\x00\r\x00\x00\x00\x06\x00\x00\x00JTPri\x19\x00\x00\x00\x08\x00\x00\x00TypeSystem.String\t\x00\x00\x00\x05\x00\x00\x00V\x04\x00\x00\x00\x04\x00\x00\x00\x16\x02\x00\x00\x17\x00\x00\x00ArtSkinLobbyShowLOD0\x00\x00\x00\x02\x00\x00\x00\r\x00\x00\x00\x06\x00\x00\x00JTArr\x1b\x00\x00\x00\x08\x00\x00\x00TypeSystem.String[]\x04\x00\x00\x00\xc7\x01\x00\x00\x03\x00\x00\x00\x95\x00\x00\x00\x0b\x00\x00\x00Element~\x00\x00\x00\x03\x00\x00\x00\r\x00\x00\x00\x06\x00\x00\x00JTPri\x19\x00\x00\x00\x08\x00\x00\x00TypeSystem.StringP\x00\x00\x00\x05\x00\x00\x00VPrefab_Characters/Prefab_Hero/520_Veres/Component/5208_Veres_RT_3_Show2\x04\x00\x00\x00\x04\x00\x00\x00\x95\x00\x00\x00\x0b\x00\x00\x00Element~\x00\x00\x00\x03\x00\x00\x00\r\x00\x00\x00\x06\x00\x00\x00JTPri\x19\x00\x00\x00\x08\x00\x00\x00TypeSystem.StringP\x00\x00\x00\x05\x00\x00\x00VPrefab_Characters/Prefab_Hero/520_Veres/Component/5208_Veres_RT_3_Show2\x04\x00\x00\x00\x04\x00\x00\x00\x95\x00\x00\x00\x0b\x00\x00\x00Element~\x00\x00\x00\x03\x00\x00\x00\r\x00\x00\x00\x06\x00\x00\x00JTPri\x19\x00\x00\x00\x08\x00\x00\x00TypeSystem.StringP\x00\x00\x00\x05\x00\x00\x00VPrefab_Characters/Prefab_Hero/520_Veres/Component/5208_Veres_RT_3_Show2\x04\x00\x00\x00\x04\x00\x00\x00E\x01\x00\x00\x1b\x00\x00\x00ArtSkinLobbyIdleShowLOD0\x00\x00\x00\x02\x00\x00\x00\r\x00\x00\x00\x06\x00\x00\x00JTArr\x1b\x00\x00\x00\x08\x00\x00\x00TypeSystem.String[]\x04\x00\x00\x00\xf2\x00\x00\x00\x03\x00\x00\x00N\x00\x00\x00\x0b\x00\x00\x00Element7\x00\x00\x00\x03\x00\x00\x00\r\x00\x00\x00\x06\x00\x00\x00JTPri\x19\x00\x00\x00\x08\x00\x00\x00TypeSystem.String\t\x00\x00\x00\x05\x00\x00\x00V\x04\x00\x00\x00\x04\x00\x00\x00N\x00\x00\x00\x0b\x00\x00\x00Element7\x00\x00\x00\x03\x00\x00\x00\r\x00\x00\x00\x06\x00\x00\x00JTPri\x19\x00\x00\x00\x08\x00\x00\x00TypeSystem.String\t\x00\x00\x00\x05\x00\x00\x00V\x04\x00\x00\x00\x04\x00\x00\x00N\x00\x00\x00\x0b\x00\x00\x00Element7\x00\x00\x00\x03\x00\x00\x00\r\x00\x00\x00\x06\x00\x00\x00JTPri\x19\x00\x00\x00\x08\x00\x00\x00TypeSystem.String\t\x00\x00\x00\x05\x00\x00\x00V\x04\x00\x00\x00\x04\x00\x00\x00\x93\x00\x00\x00\x1a\x00\x00\x00ArtSkinLobbyShowCameram\x00\x00\x00\x03\x00\x00\x00\r\x00\x00\x00\x06\x00\x00\x00JTPri\x19\x00\x00\x00\x08\x00\x00\x00TypeSystem.String?\x00\x00\x00\x05\x00\x00\x00VPrefab_Characters/Prefab_Hero/520_Veres/5208_Veres_Cam\x04\x00\x00\x00\x04\x00\x00\x00Z\x00\x00\x00\x16\x00\x00\x00CamInterpolateTime8\x00\x00\x00\x03\x00\x00\x00\r\x00\x00\x00\x06\x00\x00\x00JTPri\x19\x00\x00\x00\x08\x00\x00\x00TypeSystem.Single\n\x00\x00\x00\x05\x00\x00\x00V7\x04\x00\x00\x00\x04\x00\x00\x00^\x00\x00\x00\x18\x00\x00\x00Cam02InterpolateTime:\x00\x00\x00\x03\x00\x00\x00\r\x00\x00\x00\x06\x00\x00\x00JTPri\x19\x00\x00\x00\x08\x00\x00\x00TypeSystem.Single\x0c\x00\x00\x00\x05\x00\x00\x00V1.1\x04\x00\x00\x00\x04\x00\x00\x00`\x00\x00\x00\x1c\x00\x00\x00Cam02InterpolateDuration8\x00\x00\x00\x03\x00\x00\x00\r\x00\x00\x00\x06\x00\x00\x00JTPri\x19\x00\x00\x00\x08\x00\x00\x00TypeSystem.Single\n\x00\x00\x00\x05\x00\x00\x00V2\x04\x00\x00\x00\x04\x00\x00\x00V\x00\x00\x00\x1a\x00\x00\x00PreloadAnimatorEffects0\x00\x00\x00\x02\x00\x00\x00\r\x00\x00\x00\x06\x00\x00\x00JTArr\x1b\x00\x00\x00\x08\x00\x00\x00TypeSystem.String[]\x04\x00\x00\x00\x04\x00\x00\x00\\\x00\x00\x00\n\x00\x00\x00LookAtF\x00\x00\x00\x02\x00\x00\x00\r\x00\x00\x00\x06\x00\x00\x00JTCom1\x00\x00\x00\x08\x00\x00\x00TypeAssets.Scripts.GameLogic.CameraLookAt\x04\x00\x00\x00\x04\x00\x00\x00m\x00\x00\x00\x0f\x00\x00\x00LightConfigR\x00\x00\x00\x02\x00\x00\x00\r\x00\x00\x00\x06\x00\x00\x00JTCom=\x00\x00\x00\x08\x00\x00\x00TypeAssets.Scripts.GameLogic.PrepareBattleLightConfig\x04\x00\x00\x00\x04\x00\x00\x00'
ngoaihinhxanhveres= b'9\t\x00\x00\x0b\x00\x00\x00ElementE\x00\x00\x00\x02\x00\x00\x00\r\x00\x00\x00\x06\x00\x00\x00JTCom0\x00\x00\x00\x08\x00\x00\x00TypeAssets.Scripts.GameLogic.SkinElement\x04\x00\x00\x00\xe1\x08\x00\x00\x0b\x00\x00\x00\x10\x02\x00\x00\x14\x00\x00\x00ArtSkinPrefabLOD0\x00\x00\x00\x02\x00\x00\x00\r\x00\x00\x00\x06\x00\x00\x00JTArr\x1b\x00\x00\x00\x08\x00\x00\x00TypeSystem.String[]\x04\x00\x00\x00\xc4\x01\x00\x00\x03\x00\x00\x00\x94\x00\x00\x00\x0b\x00\x00\x00Element}\x00\x00\x00\x03\x00\x00\x00\r\x00\x00\x00\x06\x00\x00\x00JTPri\x19\x00\x00\x00\x08\x00\x00\x00TypeSystem.StringO\x00\x00\x00\x05\x00\x00\x00VPrefab_Characters/Prefab_Hero/520_Veres/Component/5208_Veres_RT_2_LOD2\x04\x00\x00\x00\x04\x00\x00\x00\x94\x00\x00\x00\x0b\x00\x00\x00Element}\x00\x00\x00\x03\x00\x00\x00\r\x00\x00\x00\x06\x00\x00\x00JTPri\x19\x00\x00\x00\x08\x00\x00\x00TypeSystem.StringO\x00\x00\x00\x05\x00\x00\x00VPrefab_Characters/Prefab_Hero/520_Veres/Component/5208_Veres_RT_2_LOD2\x04\x00\x00\x00\x04\x00\x00\x00\x94\x00\x00\x00\x0b\x00\x00\x00Element}\x00\x00\x00\x03\x00\x00\x00\r\x00\x00\x00\x06\x00\x00\x00JTPri\x19\x00\x00\x00\x08\x00\x00\x00TypeSystem.StringO\x00\x00\x00\x05\x00\x00\x00VPrefab_Characters/Prefab_Hero/520_Veres/Component/5208_Veres_RT_2_LOD2\x04\x00\x00\x00\x04\x00\x00\x00\xa4\x00\x00\x00\x16\x00\x00\x00ArtSkinPrefabLODEx0\x00\x00\x00\x02\x00\x00\x00\r\x00\x00\x00\x06\x00\x00\x00JTArr\x1b\x00\x00\x00\x08\x00\x00\x00TypeSystem.String[]\x04\x00\x00\x00V\x00\x00\x00\x01\x00\x00\x00N\x00\x00\x00\x0b\x00\x00\x00Element7\x00\x00\x00\x03\x00\x00\x00\r\x00\x00\x00\x06\x00\x00\x00JTPri\x19\x00\x00\x00\x08\x00\x00\x00TypeSystem.String\t\x00\x00\x00\x05\x00\x00\x00V\x04\x00\x00\x00\x04\x00\x00\x00\x16\x02\x00\x00\x17\x00\x00\x00ArtSkinLobbyShowLOD0\x00\x00\x00\x02\x00\x00\x00\r\x00\x00\x00\x06\x00\x00\x00JTArr\x1b\x00\x00\x00\x08\x00\x00\x00TypeSystem.String[]\x04\x00\x00\x00\xc7\x01\x00\x00\x03\x00\x00\x00\x95\x00\x00\x00\x0b\x00\x00\x00Element~\x00\x00\x00\x03\x00\x00\x00\r\x00\x00\x00\x06\x00\x00\x00JTPri\x19\x00\x00\x00\x08\x00\x00\x00TypeSystem.StringP\x00\x00\x00\x05\x00\x00\x00VPrefab_Characters/Prefab_Hero/520_Veres/Component/5208_Veres_RT_2_Show2\x04\x00\x00\x00\x04\x00\x00\x00\x95\x00\x00\x00\x0b\x00\x00\x00Element~\x00\x00\x00\x03\x00\x00\x00\r\x00\x00\x00\x06\x00\x00\x00JTPri\x19\x00\x00\x00\x08\x00\x00\x00TypeSystem.StringP\x00\x00\x00\x05\x00\x00\x00VPrefab_Characters/Prefab_Hero/520_Veres/Component/5208_Veres_RT_2_Show2\x04\x00\x00\x00\x04\x00\x00\x00\x95\x00\x00\x00\x0b\x00\x00\x00Element~\x00\x00\x00\x03\x00\x00\x00\r\x00\x00\x00\x06\x00\x00\x00JTPri\x19\x00\x00\x00\x08\x00\x00\x00TypeSystem.StringP\x00\x00\x00\x05\x00\x00\x00VPrefab_Characters/Prefab_Hero/520_Veres/Component/5208_Veres_RT_2_Show2\x04\x00\x00\x00\x04\x00\x00\x00E\x01\x00\x00\x1b\x00\x00\x00ArtSkinLobbyIdleShowLOD0\x00\x00\x00\x02\x00\x00\x00\r\x00\x00\x00\x06\x00\x00\x00JTArr\x1b\x00\x00\x00\x08\x00\x00\x00TypeSystem.String[]\x04\x00\x00\x00\xf2\x00\x00\x00\x03\x00\x00\x00N\x00\x00\x00\x0b\x00\x00\x00Element7\x00\x00\x00\x03\x00\x00\x00\r\x00\x00\x00\x06\x00\x00\x00JTPri\x19\x00\x00\x00\x08\x00\x00\x00TypeSystem.String\t\x00\x00\x00\x05\x00\x00\x00V\x04\x00\x00\x00\x04\x00\x00\x00N\x00\x00\x00\x0b\x00\x00\x00Element7\x00\x00\x00\x03\x00\x00\x00\r\x00\x00\x00\x06\x00\x00\x00JTPri\x19\x00\x00\x00\x08\x00\x00\x00TypeSystem.String\t\x00\x00\x00\x05\x00\x00\x00V\x04\x00\x00\x00\x04\x00\x00\x00N\x00\x00\x00\x0b\x00\x00\x00Element7\x00\x00\x00\x03\x00\x00\x00\r\x00\x00\x00\x06\x00\x00\x00JTPri\x19\x00\x00\x00\x08\x00\x00\x00TypeSystem.String\t\x00\x00\x00\x05\x00\x00\x00V\x04\x00\x00\x00\x04\x00\x00\x00\x93\x00\x00\x00\x1a\x00\x00\x00ArtSkinLobbyShowCameram\x00\x00\x00\x03\x00\x00\x00\r\x00\x00\x00\x06\x00\x00\x00JTPri\x19\x00\x00\x00\x08\x00\x00\x00TypeSystem.String?\x00\x00\x00\x05\x00\x00\x00VPrefab_Characters/Prefab_Hero/520_Veres/5208_Veres_Cam\x04\x00\x00\x00\x04\x00\x00\x00Z\x00\x00\x00\x16\x00\x00\x00CamInterpolateTime8\x00\x00\x00\x03\x00\x00\x00\r\x00\x00\x00\x06\x00\x00\x00JTPri\x19\x00\x00\x00\x08\x00\x00\x00TypeSystem.Single\n\x00\x00\x00\x05\x00\x00\x00V7\x04\x00\x00\x00\x04\x00\x00\x00^\x00\x00\x00\x18\x00\x00\x00Cam02InterpolateTime:\x00\x00\x00\x03\x00\x00\x00\r\x00\x00\x00\x06\x00\x00\x00JTPri\x19\x00\x00\x00\x08\x00\x00\x00TypeSystem.Single\x0c\x00\x00\x00\x05\x00\x00\x00V1.1\x04\x00\x00\x00\x04\x00\x00\x00`\x00\x00\x00\x1c\x00\x00\x00Cam02InterpolateDuration8\x00\x00\x00\x03\x00\x00\x00\r\x00\x00\x00\x06\x00\x00\x00JTPri\x19\x00\x00\x00\x08\x00\x00\x00TypeSystem.Single\n\x00\x00\x00\x05\x00\x00\x00V2\x04\x00\x00\x00\x04\x00\x00\x00V\x00\x00\x00\x1a\x00\x00\x00PreloadAnimatorEffects0\x00\x00\x00\x02\x00\x00\x00\r\x00\x00\x00\x06\x00\x00\x00JTArr\x1b\x00\x00\x00\x08\x00\x00\x00TypeSystem.String[]\x04\x00\x00\x00\x04\x00\x00\x00\\\x00\x00\x00\n\x00\x00\x00LookAtF\x00\x00\x00\x02\x00\x00\x00\r\x00\x00\x00\x06\x00\x00\x00JTCom1\x00\x00\x00\x08\x00\x00\x00TypeAssets.Scripts.GameLogic.CameraLookAt\x04\x00\x00\x00\x04\x00\x00\x00m\x00\x00\x00\x0f\x00\x00\x00LightConfigR\x00\x00\x00\x02\x00\x00\x00\r\x00\x00\x00\x06\x00\x00\x00JTCom=\x00\x00\x00\x08\x00\x00\x00TypeAssets.Scripts.GameLogic.PrepareBattleLightConfig\x04\x00\x00\x00\x04\x00\x00\x00'
#-----------------------------------------------
def Track_Guid_Skill(directory_path):
    for file in os.listdir(directory_path):
        file_path = os.path.join(directory_path, file)
        with open(file_path, "rb") as r0:
            context = r0.read()
            Tracks = re.findall(rb'<Track trackName="(.*?)</Track>', context, re.DOTALL)
            if Tracks:
                for i in range(len(Tracks)):
                    trackName = Tracks[i]
                    guid_track = (re.findall(rb'guid="(.+?)" enabled', trackName)[0]).decode()
                    print(f"  🔹 Track #{i} - GUID: {guid_track}")
                    guid_true = str.encode(f'id="{i}" guid="{guid_track}"')
                    IdGuidFalse = re.findall(str.encode(rf'id="(.+?)" guid="{guid_track}"'), context)
                    if IdGuidFalse:
                        for j in range(len(IdGuidFalse)):
                            j = IdGuidFalse[j].decode()
                            guid_false = str.encode(f'id="{j}" guid="{guid_track}"')
                            context = context.replace(guid_false, guid_true)
        with open(file_path, "wb") as w0:
            w0.write(context)
#-----------------------------------------------
class StringBytes:
    def __init__(self,String):
        self.String=String
        self.OldString=String
    def tell(self):
        return len(self.OldString)-len(self.String)
    def seek(self,I,O=0):
        if O==0:
            self.String=self.OldString[I:]
        elif O==1:
            self.String=self.String[I:]
    def read(self,Int=None):
        if Int==None:
            if type(self.String)==str:
                return ""
            else:
                return b""
        R=self.String[:Int]
        self.String=self.String[Int:]
        return R
class Bytes_XML:
    def decode(String):
        def get_int(A):
            return int.from_bytes(A.read(4), 'little')        
        def get_str(A, pos=None):
            if pos is not None:
                A.seek(pos, 0)
            ofs = get_int(A)
            stri = A.read(ofs-4)
            return stri.decode()        
        def get_node(A, fid=None, sta=None):
            global i
            ofs = get_int(A)
            stri = get_str(A)
            stri1 = stri
            myid = i
            i += 1
            A.seek(4, 1)
            aidx = get_int(A)
            ite = False
            attr = {}
            for j in range(0, aidx):
                attr1 = get_attr(A)
                if type(attr1) == str:
                    text1 = attr1
                    ite = True
                else:
                    attr.update(attr1)
            if fid is None:
                nod[myid] = ET.SubElement(root, stri1, attrib=attr)
            else:
                nod[myid] = ET.SubElement(nod[fid], stri1, attrib=attr)
            if ite:
                if text1 == '':
                    nod[myid].set("value",' ')
                else:
                    nod[myid].set("value",text1)
            check_four(A)
            chk = sta + ofs - A.tell()
            if chk > 12:
                A.seek(4, 1)
                sidx = get_int(A)
                for h in range(0, sidx):
                    get_node(A, myid, A.tell())
            A.seek(sta + ofs, 0)        
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
                    if stri[0:2] == 'JT':
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
                    if stri2[0:4] == 'Type':
                        stri = stri2[4:]
                        name = 'type'
                    else:
                        stri = stri2
                        name = 'type_Raw'
                else:
                    stri = A.read(ofs - 8).decode()
                    name = str(type)
                    A.seek(pos + ofs, 0)
                return {name:stri}
        def check_four(A):
            if get_int(A) != 4:
                A.seek(-4, 1)
        A=StringBytes(String)
        global i, nod, root
        i = 0
        nod = {}
        ofs = get_int(A)
        stri = get_str(A)
        stri1 = stri
        A.seek(4, 1)
        aidx = get_int(A)
        ite = False
        attr = {}
        for j in range(0, aidx):
            attr1 = get_attr(A)
            if type(attr1) == str:
                text1 = attr1
                ite = True
            else:
                attr.update(attr1)
        root = ET.Element(stri1, attrib=attr)
        if ite:
            nod[myid].set("value",text1)
        check_four(A)
        chk = ofs - A.tell()
        if chk > 12:
            A.seek(4, 1)
            sidx = get_int(A)
            for h in range(0, sidx):
                get_node(A, None, A.tell())
        try:return minidom.parseString(ET.tostring(root,"utf-8").decode()).toprettyxml(indent="  ",newl="\r\n").encode()
        except: return ET.tostring(root,"utf-8").decode()
    def encode(xmlfile):
        def byteint(num):
            return num.to_bytes(4, byteorder='little')
        def bytestr(stri):
            outbyte = byteint(len(stri) + 4)
            outbyte = outbyte + stri.encode()
            return outbyte
        def byteattr(key, attr):
            if key == 'var':
                if attr[key] == 'Array':
                    stri = 'JTArr'
                elif attr[key] == 'String':
                    stri = 'JTPri'
                else:
                    stri = 'JT' + attr[key]
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
            elif key == "value": return b""
            else:
                import unicodedata
                if unicodedata.numeric(key):
                    stri = attr[key]
                    aid = int(key)
            stripro = stri.encode()
            outbyte = byteint(len(stripro) + 8) + byteint(aid) + stripro
            return outbyte
        def bytenode(node):
            iftex = False
            name1 = node.tag
            name = bytestr(name1)
            attr1 = b''
            aindex = len(node.attrib)
            plus = 8
            for key in node.attrib:
                if key=="value":aindex-=1
                attr1 = attr1 + byteattr(key, node.attrib)
            if (node.get("value") != None) and (node.get("value")[0:1] != '\n'):
                if node.get("value") == ' ':
                    stri1 = ''
                else:
                    stri1 = node.get("value")
                iftex = True
                stripro = ('V' + stri1).encode()
                attr1 = attr1 + byteint(len(stripro) + 8) + byteint(5) + stripro + byteint(4)
                aindex += 1
                plus = 4
            attr1 = byteint(len(attr1) + plus) + byteint(aindex) + attr1 + byteint(4)
            alchild = b''
            if len(node):
                cindex = 0
                for child in node:
                    alchild = alchild + bytenode(child)
                    cindex += 1
                alchild = byteint(len(alchild) + 8) + byteint(cindex) + alchild
            else:
                if iftex == False:
                    alchild = byteint(4)
            bnode = name + attr1 + alchild
            bnode = byteint(len(bnode) + 4) + bnode
            return bnode
        tree = ET.fromstring(xmlfile)
        byt = bytenode(tree)
        return byt
                          
def process_file(file_path_FL, LC):
    with open(file_path_FL, "rb") as f:
        G = f.read()
        with open(file_path_FL, "wb") as f1:
            try:
                if LC == "1":
                    f1.write(Bytes_XML.decode(G))
                elif LC == "2":
                    f1.write(Bytes_XML.encode(G.decode()))
            except Exception as e:
                pass
        
def process_directory(directory_path, LC):
    file_path_FL = directory_path
    process_file(file_path_FL, LC) 
#-----------------------------------------------
ngoaihinhvaneov=b'/\x0c\x00\x00\x0b\x00\x00\x00ElementE\x00\x00\x00\x02\x00\x00\x00\r\x00\x00\x00\x06\x00\x00\x00JTCom0\x00\x00\x00\x08\x00\x00\x00TypeAssets.Scripts.GameLogic.SkinElement\x04\x00\x00\x00\xd7\x0b\x00\x00\n\x00\x00\x00\x16\x02\x00\x00\x14\x00\x00\x00ArtSkinPrefabLOD0\x00\x00\x00\x02\x00\x00\x00\r\x00\x00\x00\x06\x00\x00\x00JTArr\x1b\x00\x00\x00\x08\x00\x00\x00TypeSystem.String[]\x04\x00\x00\x00\xca\x01\x00\x00\x03\x00\x00\x00\x96\x00\x00\x00\x0b\x00\x00\x00Element\x7f\x00\x00\x00\x03\x00\x00\x00\r\x00\x00\x00\x06\x00\x00\x00JTPri\x19\x00\x00\x00\x08\x00\x00\x00TypeSystem.StringQ\x00\x00\x00\x05\x00\x00\x00VPrefab_Characters/Prefab_Hero/133_DiRenJie/Awaken/13312_DiRenJie_04_LOD1\x04\x00\x00\x00\x04\x00\x00\x00\x96\x00\x00\x00\x0b\x00\x00\x00Element\x7f\x00\x00\x00\x03\x00\x00\x00\r\x00\x00\x00\x06\x00\x00\x00JTPri\x19\x00\x00\x00\x08\x00\x00\x00TypeSystem.StringQ\x00\x00\x00\x05\x00\x00\x00VPrefab_Characters/Prefab_Hero/133_DiRenJie/Awaken/13312_DiRenJie_04_LOD2\x04\x00\x00\x00\x04\x00\x00\x00\x96\x00\x00\x00\x0b\x00\x00\x00Element\x7f\x00\x00\x00\x03\x00\x00\x00\r\x00\x00\x00\x06\x00\x00\x00JTPri\x19\x00\x00\x00\x08\x00\x00\x00TypeSystem.StringQ\x00\x00\x00\x05\x00\x00\x00VPrefab_Characters/Prefab_Hero/133_DiRenJie/Awaken/13312_DiRenJie_04_LOD3\x04\x00\x00\x00\x04\x00\x00\x00\xa4\x00\x00\x00\x16\x00\x00\x00ArtSkinPrefabLODEx0\x00\x00\x00\x02\x00\x00\x00\r\x00\x00\x00\x06\x00\x00\x00JTArr\x1b\x00\x00\x00\x08\x00\x00\x00TypeSystem.String[]\x04\x00\x00\x00V\x00\x00\x00\x01\x00\x00\x00N\x00\x00\x00\x0b\x00\x00\x00Element7\x00\x00\x00\x03\x00\x00\x00\r\x00\x00\x00\x06\x00\x00\x00JTPri\x19\x00\x00\x00\x08\x00\x00\x00TypeSystem.String\t\x00\x00\x00\x05\x00\x00\x00V\x04\x00\x00\x00\x04\x00\x00\x00\x1c\x02\x00\x00\x17\x00\x00\x00ArtSkinLobbyShowLOD0\x00\x00\x00\x02\x00\x00\x00\r\x00\x00\x00\x06\x00\x00\x00JTArr\x1b\x00\x00\x00\x08\x00\x00\x00TypeSystem.String[]\x04\x00\x00\x00\xcd\x01\x00\x00\x03\x00\x00\x00\x97\x00\x00\x00\x0b\x00\x00\x00Element\x80\x00\x00\x00\x03\x00\x00\x00\r\x00\x00\x00\x06\x00\x00\x00JTPri\x19\x00\x00\x00\x08\x00\x00\x00TypeSystem.StringR\x00\x00\x00\x05\x00\x00\x00VPrefab_Characters/Prefab_Hero/133_DiRenJie/Awaken/13312_DiRenJie_04_Show1\x04\x00\x00\x00\x04\x00\x00\x00\x97\x00\x00\x00\x0b\x00\x00\x00Element\x80\x00\x00\x00\x03\x00\x00\x00\r\x00\x00\x00\x06\x00\x00\x00JTPri\x19\x00\x00\x00\x08\x00\x00\x00TypeSystem.StringR\x00\x00\x00\x05\x00\x00\x00VPrefab_Characters/Prefab_Hero/133_DiRenJie/Awaken/13312_DiRenJie_04_Show2\x04\x00\x00\x00\x04\x00\x00\x00\x97\x00\x00\x00\x0b\x00\x00\x00Element\x80\x00\x00\x00\x03\x00\x00\x00\r\x00\x00\x00\x06\x00\x00\x00JTPri\x19\x00\x00\x00\x08\x00\x00\x00TypeSystem.StringR\x00\x00\x00\x05\x00\x00\x00VPrefab_Characters/Prefab_Hero/133_DiRenJie/Awaken/13312_DiRenJie_04_Show3\x04\x00\x00\x00\x04\x00\x00\x00E\x01\x00\x00\x1b\x00\x00\x00ArtSkinLobbyIdleShowLOD0\x00\x00\x00\x02\x00\x00\x00\r\x00\x00\x00\x06\x00\x00\x00JTArr\x1b\x00\x00\x00\x08\x00\x00\x00TypeSystem.String[]\x04\x00\x00\x00\xf2\x00\x00\x00\x03\x00\x00\x00N\x00\x00\x00\x0b\x00\x00\x00Element7\x00\x00\x00\x03\x00\x00\x00\r\x00\x00\x00\x06\x00\x00\x00JTPri\x19\x00\x00\x00\x08\x00\x00\x00TypeSystem.String\t\x00\x00\x00\x05\x00\x00\x00V\x04\x00\x00\x00\x04\x00\x00\x00N\x00\x00\x00\x0b\x00\x00\x00Element7\x00\x00\x00\x03\x00\x00\x00\r\x00\x00\x00\x06\x00\x00\x00JTPri\x19\x00\x00\x00\x08\x00\x00\x00TypeSystem.String\t\x00\x00\x00\x05\x00\x00\x00V\x04\x00\x00\x00\x04\x00\x00\x00N\x00\x00\x00\x0b\x00\x00\x00Element7\x00\x00\x00\x03\x00\x00\x00\r\x00\x00\x00\x06\x00\x00\x00JTPri\x19\x00\x00\x00\x08\x00\x00\x00TypeSystem.String\t\x00\x00\x00\x05\x00\x00\x00V\x04\x00\x00\x00\x04\x00\x00\x00\xa5\x00\x00\x00\x1a\x00\x00\x00ArtSkinLobbyShowCamera\x7f\x00\x00\x00\x03\x00\x00\x00\r\x00\x00\x00\x06\x00\x00\x00JTPri\x19\x00\x00\x00\x08\x00\x00\x00TypeSystem.StringQ\x00\x00\x00\x05\x00\x00\x00VPrefab_Characters/Prefab_Hero/133_DiRenJie/Awaken/13312_DiRenJie_AW5_Cam\x04\x00\x00\x00\x04\x00\x00\x00^\x00\x00\x00\x18\x00\x00\x00Cam02InterpolateTime:\x00\x00\x00\x03\x00\x00\x00\r\x00\x00\x00\x06\x00\x00\x00JTPri\x19\x00\x00\x00\x08\x00\x00\x00TypeSystem.Single\x0c\x00\x00\x00\x05\x00\x00\x00V1.5\x04\x00\x00\x00\x04\x00\x00\x00b\x00\x00\x00\x1c\x00\x00\x00Cam02InterpolateDuration:\x00\x00\x00\x03\x00\x00\x00\r\x00\x00\x00\x06\x00\x00\x00JTPri\x19\x00\x00\x00\x08\x00\x00\x00TypeSystem.Single\x0c\x00\x00\x00\x05\x00\x00\x00V0.9\x04\x00\x00\x00\x04\x00\x00\x00V\x00\x00\x00\x1a\x00\x00\x00PreloadAnimatorEffects0\x00\x00\x00\x02\x00\x00\x00\r\x00\x00\x00\x06\x00\x00\x00JTArr\x1b\x00\x00\x00\x08\x00\x00\x00TypeSystem.String[]\x04\x00\x00\x00\x04\x00\x00\x00\x8c\x03\x00\x00\n\x00\x00\x00LookAtF\x00\x00\x00\x02\x00\x00\x00\r\x00\x00\x00\x06\x00\x00\x00JTCom1\x00\x00\x00\x08\x00\x00\x00TypeAssets.Scripts.GameLogic.CameraLookAt\x04\x00\x00\x004\x03\x00\x00\x04\x00\x00\x00B\x01\x00\x00\n\x00\x00\x00Offset4\x00\x00\x00\x02\x00\x00\x00\r\x00\x00\x00\x06\x00\x00\x00JTCom\x1f\x00\x00\x00\x08\x00\x00\x00TypeUnityEngine.Vector3\x04\x00\x00\x00\xfc\x00\x00\x00\x03\x00\x00\x00S\x00\x00\x00\x05\x00\x00\x00xB\x00\x00\x00\x03\x00\x00\x00\r\x00\x00\x00\x06\x00\x00\x00JTPri\x19\x00\x00\x00\x08\x00\x00\x00TypeSystem.Single\x14\x00\x00\x00\x05\x00\x00\x00V-0.07000029\x04\x00\x00\x00\x04\x00\x00\x00P\x00\x00\x00\x05\x00\x00\x00y?\x00\x00\x00\x03\x00\x00\x00\r\x00\x00\x00\x06\x00\x00\x00JTPri\x19\x00\x00\x00\x08\x00\x00\x00TypeSystem.Single\x11\x00\x00\x00\x05\x00\x00\x00V1.539993\x04\x00\x00\x00\x04\x00\x00\x00Q\x00\x00\x00\x05\x00\x00\x00z@\x00\x00\x00\x03\x00\x00\x00\r\x00\x00\x00\x06\x00\x00\x00JTPri\x19\x00\x00\x00\x08\x00\x00\x00TypeSystem.Single\x12\x00\x00\x00\x05\x00\x00\x00V-3.739998\x04\x00\x00\x00\x04\x00\x00\x00H\x01\x00\x00\r\x00\x00\x00Direction4\x00\x00\x00\x02\x00\x00\x00\r\x00\x00\x00\x06\x00\x00\x00JTCom\x1f\x00\x00\x00\x08\x00\x00\x00TypeUnityEngine.Vector3\x04\x00\x00\x00\xff\x00\x00\x00\x03\x00\x00\x00S\x00\x00\x00\x05\x00\x00\x00xB\x00\x00\x00\x03\x00\x00\x00\r\x00\x00\x00\x06\x00\x00\x00JTPri\x19\x00\x00\x00\x08\x00\x00\x00TypeSystem.Single\x14\x00\x00\x00\x05\x00\x00\x00V0.002750125\x04\x00\x00\x00\x04\x00\x00\x00S\x00\x00\x00\x05\x00\x00\x00yB\x00\x00\x00\x03\x00\x00\x00\r\x00\x00\x00\x06\x00\x00\x00JTPri\x19\x00\x00\x00\x08\x00\x00\x00TypeSystem.Single\x14\x00\x00\x00\x05\x00\x00\x00V0.009888734\x04\x00\x00\x00\x04\x00\x00\x00Q\x00\x00\x00\x05\x00\x00\x00z@\x00\x00\x00\x03\x00\x00\x00\r\x00\x00\x00\x06\x00\x00\x00JTPri\x19\x00\x00\x00\x08\x00\x00\x00TypeSystem.Single\x12\x00\x00\x00\x05\x00\x00\x00V0.9999473\x04\x00\x00\x00\x04\x00\x00\x00P\x00\x00\x00\x0c\x00\x00\x00Duration8\x00\x00\x00\x03\x00\x00\x00\r\x00\x00\x00\x06\x00\x00\x00JTPri\x19\x00\x00\x00\x08\x00\x00\x00TypeSystem.Single\n\x00\x00\x00\x05\x00\x00\x00V1\x04\x00\x00\x00\x04\x00\x00\x00R\x00\x00\x00\r\x00\x00\x00CameraFOV9\x00\x00\x00\x03\x00\x00\x00\r\x00\x00\x00\x06\x00\x00\x00JTPri\x19\x00\x00\x00\x08\x00\x00\x00TypeSystem.Single\x0b\x00\x00\x00\x05\x00\x00\x00V17\x04\x00\x00\x00\x04\x00\x00\x00m\x00\x00\x00\x0f\x00\x00\x00LightConfigR\x00\x00\x00\x02\x00\x00\x00\r\x00\x00\x00\x06\x00\x00\x00JTCom=\x00\x00\x00\x08\x00\x00\x00TypeAssets.Scripts.GameLogic.PrepareBattleLightConfig\x04\x00\x00\x00\x04\x00\x00\x00'
ngoaihinhvaneovvang=b'J\x0c\x00\x00\x0b\x00\x00\x00ElementE\x00\x00\x00\x02\x00\x00\x00\r\x00\x00\x00\x06\x00\x00\x00JTCom0\x00\x00\x00\x08\x00\x00\x00TypeAssets.Scripts.GameLogic.SkinElement\x04\x00\x00\x00\r\x0c\x00\x00\n\x00\x00\x00\x16\x02\x00\x00\x14\x00\x00\x00ArtSkinPrefabLOD0\x00\x00\x00\x02\x00\x00\x00\r\x00\x00\x00\x06\x00\x00\x00JTArr\x1b\x00\x00\x00\x08\x00\x00\x00TypeSystem.String[]\x04\x00\x00\x00\xca\x01\x00\x00\x03\x00\x00\x00\x96\x00\x00\x00\x0b\x00\x00\x00Element\x7f\x00\x00\x00\x03\x00\x00\x00\r\x00\x00\x00\x06\x00\x00\x00JTPri\x19\x00\x00\x00\x08\x00\x00\x00TypeSystem.StringQ\x00\x00\x00\x05\x00\x00\x00VPrefab_Characters/Prefab_Hero/133_DiRenJie/Awaken/13312_DiRenJie_04_LOD2\x04\x00\x00\x00\x04\x00\x00\x00\x96\x00\x00\x00\x0b\x00\x00\x00Element\x7f\x00\x00\x00\x03\x00\x00\x00\r\x00\x00\x00\x06\x00\x00\x00JTPri\x19\x00\x00\x00\x08\x00\x00\x00TypeSystem.StringQ\x00\x00\x00\x05\x00\x00\x00VPrefab_Characters/Prefab_Hero/133_DiRenJie/Awaken/13312_DiRenJie_04_LOD2\x04\x00\x00\x00\x04\x00\x00\x00\x96\x00\x00\x00\x0b\x00\x00\x00Element\x7f\x00\x00\x00\x03\x00\x00\x00\r\x00\x00\x00\x06\x00\x00\x00JTPri\x19\x00\x00\x00\x08\x00\x00\x00TypeSystem.StringQ\x00\x00\x00\x05\x00\x00\x00VPrefab_Characters/Prefab_Hero/133_DiRenJie/Awaken/13312_DiRenJie_04_LOD2\x04\x00\x00\x00\x04\x00\x00\x00\xa4\x00\x00\x00\x16\x00\x00\x00ArtSkinPrefabLODEx0\x00\x00\x00\x02\x00\x00\x00\r\x00\x00\x00\x06\x00\x00\x00JTArr\x1b\x00\x00\x00\x08\x00\x00\x00TypeSystem.String[]\x04\x00\x00\x00V\x00\x00\x00\x01\x00\x00\x00N\x00\x00\x00\x0b\x00\x00\x00Element7\x00\x00\x00\x03\x00\x00\x00\r\x00\x00\x00\x06\x00\x00\x00JTPri\x19\x00\x00\x00\x08\x00\x00\x00TypeSystem.String\t\x00\x00\x00\x05\x00\x00\x00V\x04\x00\x00\x00\x04\x00\x00\x007\x02\x00\x00\x17\x00\x00\x00ArtSkinLobbyShowLOD0\x00\x00\x00\x02\x00\x00\x00\r\x00\x00\x00\x06\x00\x00\x00JTArr\x1b\x00\x00\x00\x08\x00\x00\x00TypeSystem.String[]\x04\x00\x00\x00\xe8\x01\x00\x00\x03\x00\x00\x00\xa0\x00\x00\x00\x0b\x00\x00\x00Element\x89\x00\x00\x00\x03\x00\x00\x00\r\x00\x00\x00\x06\x00\x00\x00JTPri\x19\x00\x00\x00\x08\x00\x00\x00TypeSystem.String[\x00\x00\x00\x05\x00\x00\x00VPrefab_Characters/Prefab_Hero/133_DiRenJie/Component/13312_DiRenJie_AW5_RT_2_Show2\x04\x00\x00\x00\x04\x00\x00\x00\xa0\x00\x00\x00\x0b\x00\x00\x00Element\x89\x00\x00\x00\x03\x00\x00\x00\r\x00\x00\x00\x06\x00\x00\x00JTPri\x19\x00\x00\x00\x08\x00\x00\x00TypeSystem.String[\x00\x00\x00\x05\x00\x00\x00VPrefab_Characters/Prefab_Hero/133_DiRenJie/Component/13312_DiRenJie_AW5_RT_2_Show2\x04\x00\x00\x00\x04\x00\x00\x00\xa0\x00\x00\x00\x0b\x00\x00\x00Element\x89\x00\x00\x00\x03\x00\x00\x00\r\x00\x00\x00\x06\x00\x00\x00JTPri\x19\x00\x00\x00\x08\x00\x00\x00TypeSystem.String[\x00\x00\x00\x05\x00\x00\x00VPrefab_Characters/Prefab_Hero/133_DiRenJie/Component/13312_DiRenJie_AW5_RT_2_Show2\x04\x00\x00\x00\x04\x00\x00\x00E\x01\x00\x00\x1b\x00\x00\x00ArtSkinLobbyIdleShowLOD0\x00\x00\x00\x02\x00\x00\x00\r\x00\x00\x00\x06\x00\x00\x00JTArr\x1b\x00\x00\x00\x08\x00\x00\x00TypeSystem.String[]\x04\x00\x00\x00\xf2\x00\x00\x00\x03\x00\x00\x00N\x00\x00\x00\x0b\x00\x00\x00Element7\x00\x00\x00\x03\x00\x00\x00\r\x00\x00\x00\x06\x00\x00\x00JTPri\x19\x00\x00\x00\x08\x00\x00\x00TypeSystem.String\t\x00\x00\x00\x05\x00\x00\x00V\x04\x00\x00\x00\x04\x00\x00\x00N\x00\x00\x00\x0b\x00\x00\x00Element7\x00\x00\x00\x03\x00\x00\x00\r\x00\x00\x00\x06\x00\x00\x00JTPri\x19\x00\x00\x00\x08\x00\x00\x00TypeSystem.String\t\x00\x00\x00\x05\x00\x00\x00V\x04\x00\x00\x00\x04\x00\x00\x00N\x00\x00\x00\x0b\x00\x00\x00Element7\x00\x00\x00\x03\x00\x00\x00\r\x00\x00\x00\x06\x00\x00\x00JTPri\x19\x00\x00\x00\x08\x00\x00\x00TypeSystem.String\t\x00\x00\x00\x05\x00\x00\x00V\x04\x00\x00\x00\x04\x00\x00\x00\xa5\x00\x00\x00\x1a\x00\x00\x00ArtSkinLobbyShowCamera\x7f\x00\x00\x00\x03\x00\x00\x00\r\x00\x00\x00\x06\x00\x00\x00JTPri\x19\x00\x00\x00\x08\x00\x00\x00TypeSystem.StringQ\x00\x00\x00\x05\x00\x00\x00VPrefab_Characters/Prefab_Hero/133_DiRenJie/Awaken/13312_DiRenJie_AW5_Cam\x04\x00\x00\x00\x04\x00\x00\x00^\x00\x00\x00\x18\x00\x00\x00Cam02InterpolateTime:\x00\x00\x00\x03\x00\x00\x00\r\x00\x00\x00\x06\x00\x00\x00JTPri\x19\x00\x00\x00\x08\x00\x00\x00TypeSystem.Single\x0c\x00\x00\x00\x05\x00\x00\x00V1.5\x04\x00\x00\x00\x04\x00\x00\x00b\x00\x00\x00\x1c\x00\x00\x00Cam02InterpolateDuration:\x00\x00\x00\x03\x00\x00\x00\r\x00\x00\x00\x06\x00\x00\x00JTPri\x19\x00\x00\x00\x08\x00\x00\x00TypeSystem.Single\x0c\x00\x00\x00\x05\x00\x00\x00V0.9\x04\x00\x00\x00\x04\x00\x00\x00V\x00\x00\x00\x1a\x00\x00\x00PreloadAnimatorEffects0\x00\x00\x00\x02\x00\x00\x00\r\x00\x00\x00\x06\x00\x00\x00JTArr\x1b\x00\x00\x00\x08\x00\x00\x00TypeSystem.String[]\x04\x00\x00\x00\x04\x00\x00\x00\x8c\x03\x00\x00\n\x00\x00\x00LookAtF\x00\x00\x00\x02\x00\x00\x00\r\x00\x00\x00\x06\x00\x00\x00JTCom1\x00\x00\x00\x08\x00\x00\x00TypeAssets.Scripts.GameLogic.CameraLookAt\x04\x00\x00\x004\x03\x00\x00\x04\x00\x00\x00B\x01\x00\x00\n\x00\x00\x00Offset4\x00\x00\x00\x02\x00\x00\x00\r\x00\x00\x00\x06\x00\x00\x00JTCom\x1f\x00\x00\x00\x08\x00\x00\x00TypeUnityEngine.Vector3\x04\x00\x00\x00\xfc\x00\x00\x00\x03\x00\x00\x00S\x00\x00\x00\x05\x00\x00\x00xB\x00\x00\x00\x03\x00\x00\x00\r\x00\x00\x00\x06\x00\x00\x00JTPri\x19\x00\x00\x00\x08\x00\x00\x00TypeSystem.Single\x14\x00\x00\x00\x05\x00\x00\x00V-0.07000029\x04\x00\x00\x00\x04\x00\x00\x00P\x00\x00\x00\x05\x00\x00\x00y?\x00\x00\x00\x03\x00\x00\x00\r\x00\x00\x00\x06\x00\x00\x00JTPri\x19\x00\x00\x00\x08\x00\x00\x00TypeSystem.Single\x11\x00\x00\x00\x05\x00\x00\x00V1.539993\x04\x00\x00\x00\x04\x00\x00\x00Q\x00\x00\x00\x05\x00\x00\x00z@\x00\x00\x00\x03\x00\x00\x00\r\x00\x00\x00\x06\x00\x00\x00JTPri\x19\x00\x00\x00\x08\x00\x00\x00TypeSystem.Single\x12\x00\x00\x00\x05\x00\x00\x00V-3.739998\x04\x00\x00\x00\x04\x00\x00\x00H\x01\x00\x00\r\x00\x00\x00Direction4\x00\x00\x00\x02\x00\x00\x00\r\x00\x00\x00\x06\x00\x00\x00JTCom\x1f\x00\x00\x00\x08\x00\x00\x00TypeUnityEngine.Vector3\x04\x00\x00\x00\xff\x00\x00\x00\x03\x00\x00\x00S\x00\x00\x00\x05\x00\x00\x00xB\x00\x00\x00\x03\x00\x00\x00\r\x00\x00\x00\x06\x00\x00\x00JTPri\x19\x00\x00\x00\x08\x00\x00\x00TypeSystem.Single\x14\x00\x00\x00\x05\x00\x00\x00V0.002750125\x04\x00\x00\x00\x04\x00\x00\x00S\x00\x00\x00\x05\x00\x00\x00yB\x00\x00\x00\x03\x00\x00\x00\r\x00\x00\x00\x06\x00\x00\x00JTPri\x19\x00\x00\x00\x08\x00\x00\x00TypeSystem.Single\x14\x00\x00\x00\x05\x00\x00\x00V0.009888734\x04\x00\x00\x00\x04\x00\x00\x00Q\x00\x00\x00\x05\x00\x00\x00z@\x00\x00\x00\x03\x00\x00\x00\r\x00\x00\x00\x06\x00\x00\x00JTPri\x19\x00\x00\x00\x08\x00\x00\x00TypeSystem.Single\x12\x00\x00\x00\x05\x00\x00\x00V0.9999473\x04\x00\x00\x00\x04\x00\x00\x00P\x00\x00\x00\x0c\x00\x00\x00Duration8\x00\x00\x00\x03\x00\x00\x00\r\x00\x00\x00\x06\x00\x00\x00JTPri\x19\x00\x00\x00\x08\x00\x00\x00TypeSystem.Single\n\x00\x00\x00\x05\x00\x00\x00V1\x04\x00\x00\x00\x04\x00\x00\x00R\x00\x00\x00\r\x00\x00\x00CameraFOV9\x00\x00\x00\x03\x00\x00\x00\r\x00\x00\x00\x06\x00\x00\x00JTPri\x19\x00\x00\x00\x08\x00\x00\x00TypeSystem.Single\x0b\x00\x00\x00\x05\x00\x00\x00V17\x04\x00\x00\x00\x04\x00\x00\x00m\x00\x00\x00\x0f\x00\x00\x00LightConfigR\x00\x00\x00\x02\x00\x00\x00\r\x00\x00\x00\x06\x00\x00\x00JTCom=\x00\x00\x00\x08\x00\x00\x00TypeAssets.Scripts.GameLogic.PrepareBattleLightConfig\x04\x00\x00\x00\x04\x00\x00\x00'
ngoaihinhvaneovdo= b'J\x0c\x00\x00\x0b\x00\x00\x00ElementE\x00\x00\x00\x02\x00\x00\x00\r\x00\x00\x00\x06\x00\x00\x00JTCom0\x00\x00\x00\x08\x00\x00\x00TypeAssets.Scripts.GameLogic.SkinElement\x04\x00\x00\x00\r\x0c\x00\x00\n\x00\x00\x00\x16\x02\x00\x00\x14\x00\x00\x00ArtSkinPrefabLOD0\x00\x00\x00\x02\x00\x00\x00\r\x00\x00\x00\x06\x00\x00\x00JTArr\x1b\x00\x00\x00\x08\x00\x00\x00TypeSystem.String[]\x04\x00\x00\x00\xca\x01\x00\x00\x03\x00\x00\x00\x96\x00\x00\x00\x0b\x00\x00\x00Element\x7f\x00\x00\x00\x03\x00\x00\x00\r\x00\x00\x00\x06\x00\x00\x00JTPri\x19\x00\x00\x00\x08\x00\x00\x00TypeSystem.StringQ\x00\x00\x00\x05\x00\x00\x00VPrefab_Characters/Prefab_Hero/133_DiRenJie/Awaken/13312_DiRenJie_04_LOD2\x04\x00\x00\x00\x04\x00\x00\x00\x96\x00\x00\x00\x0b\x00\x00\x00Element\x7f\x00\x00\x00\x03\x00\x00\x00\r\x00\x00\x00\x06\x00\x00\x00JTPri\x19\x00\x00\x00\x08\x00\x00\x00TypeSystem.StringQ\x00\x00\x00\x05\x00\x00\x00VPrefab_Characters/Prefab_Hero/133_DiRenJie/Awaken/13312_DiRenJie_04_LOD2\x04\x00\x00\x00\x04\x00\x00\x00\x96\x00\x00\x00\x0b\x00\x00\x00Element\x7f\x00\x00\x00\x03\x00\x00\x00\r\x00\x00\x00\x06\x00\x00\x00JTPri\x19\x00\x00\x00\x08\x00\x00\x00TypeSystem.StringQ\x00\x00\x00\x05\x00\x00\x00VPrefab_Characters/Prefab_Hero/133_DiRenJie/Awaken/13312_DiRenJie_04_LOD2\x04\x00\x00\x00\x04\x00\x00\x00\xa4\x00\x00\x00\x16\x00\x00\x00ArtSkinPrefabLODEx0\x00\x00\x00\x02\x00\x00\x00\r\x00\x00\x00\x06\x00\x00\x00JTArr\x1b\x00\x00\x00\x08\x00\x00\x00TypeSystem.String[]\x04\x00\x00\x00V\x00\x00\x00\x01\x00\x00\x00N\x00\x00\x00\x0b\x00\x00\x00Element7\x00\x00\x00\x03\x00\x00\x00\r\x00\x00\x00\x06\x00\x00\x00JTPri\x19\x00\x00\x00\x08\x00\x00\x00TypeSystem.String\t\x00\x00\x00\x05\x00\x00\x00V\x04\x00\x00\x00\x04\x00\x00\x007\x02\x00\x00\x17\x00\x00\x00ArtSkinLobbyShowLOD0\x00\x00\x00\x02\x00\x00\x00\r\x00\x00\x00\x06\x00\x00\x00JTArr\x1b\x00\x00\x00\x08\x00\x00\x00TypeSystem.String[]\x04\x00\x00\x00\xe8\x01\x00\x00\x03\x00\x00\x00\xa0\x00\x00\x00\x0b\x00\x00\x00Element\x89\x00\x00\x00\x03\x00\x00\x00\r\x00\x00\x00\x06\x00\x00\x00JTPri\x19\x00\x00\x00\x08\x00\x00\x00TypeSystem.String[\x00\x00\x00\x05\x00\x00\x00VPrefab_Characters/Prefab_Hero/133_DiRenJie/Component/13312_DiRenJie_AW5_RT_3_Show2\x04\x00\x00\x00\x04\x00\x00\x00\xa0\x00\x00\x00\x0b\x00\x00\x00Element\x89\x00\x00\x00\x03\x00\x00\x00\r\x00\x00\x00\x06\x00\x00\x00JTPri\x19\x00\x00\x00\x08\x00\x00\x00TypeSystem.String[\x00\x00\x00\x05\x00\x00\x00VPrefab_Characters/Prefab_Hero/133_DiRenJie/Component/13312_DiRenJie_AW5_RT_3_Show2\x04\x00\x00\x00\x04\x00\x00\x00\xa0\x00\x00\x00\x0b\x00\x00\x00Element\x89\x00\x00\x00\x03\x00\x00\x00\r\x00\x00\x00\x06\x00\x00\x00JTPri\x19\x00\x00\x00\x08\x00\x00\x00TypeSystem.String[\x00\x00\x00\x05\x00\x00\x00VPrefab_Characters/Prefab_Hero/133_DiRenJie/Component/13312_DiRenJie_AW5_RT_3_Show2\x04\x00\x00\x00\x04\x00\x00\x00E\x01\x00\x00\x1b\x00\x00\x00ArtSkinLobbyIdleShowLOD0\x00\x00\x00\x02\x00\x00\x00\r\x00\x00\x00\x06\x00\x00\x00JTArr\x1b\x00\x00\x00\x08\x00\x00\x00TypeSystem.String[]\x04\x00\x00\x00\xf2\x00\x00\x00\x03\x00\x00\x00N\x00\x00\x00\x0b\x00\x00\x00Element7\x00\x00\x00\x03\x00\x00\x00\r\x00\x00\x00\x06\x00\x00\x00JTPri\x19\x00\x00\x00\x08\x00\x00\x00TypeSystem.String\t\x00\x00\x00\x05\x00\x00\x00V\x04\x00\x00\x00\x04\x00\x00\x00N\x00\x00\x00\x0b\x00\x00\x00Element7\x00\x00\x00\x03\x00\x00\x00\r\x00\x00\x00\x06\x00\x00\x00JTPri\x19\x00\x00\x00\x08\x00\x00\x00TypeSystem.String\t\x00\x00\x00\x05\x00\x00\x00V\x04\x00\x00\x00\x04\x00\x00\x00N\x00\x00\x00\x0b\x00\x00\x00Element7\x00\x00\x00\x03\x00\x00\x00\r\x00\x00\x00\x06\x00\x00\x00JTPri\x19\x00\x00\x00\x08\x00\x00\x00TypeSystem.String\t\x00\x00\x00\x05\x00\x00\x00V\x04\x00\x00\x00\x04\x00\x00\x00\xa5\x00\x00\x00\x1a\x00\x00\x00ArtSkinLobbyShowCamera\x7f\x00\x00\x00\x03\x00\x00\x00\r\x00\x00\x00\x06\x00\x00\x00JTPri\x19\x00\x00\x00\x08\x00\x00\x00TypeSystem.StringQ\x00\x00\x00\x05\x00\x00\x00VPrefab_Characters/Prefab_Hero/133_DiRenJie/Awaken/13312_DiRenJie_AW5_Cam\x04\x00\x00\x00\x04\x00\x00\x00^\x00\x00\x00\x18\x00\x00\x00Cam02InterpolateTime:\x00\x00\x00\x03\x00\x00\x00\r\x00\x00\x00\x06\x00\x00\x00JTPri\x19\x00\x00\x00\x08\x00\x00\x00TypeSystem.Single\x0c\x00\x00\x00\x05\x00\x00\x00V1.5\x04\x00\x00\x00\x04\x00\x00\x00b\x00\x00\x00\x1c\x00\x00\x00Cam02InterpolateDuration:\x00\x00\x00\x03\x00\x00\x00\r\x00\x00\x00\x06\x00\x00\x00JTPri\x19\x00\x00\x00\x08\x00\x00\x00TypeSystem.Single\x0c\x00\x00\x00\x05\x00\x00\x00V0.9\x04\x00\x00\x00\x04\x00\x00\x00V\x00\x00\x00\x1a\x00\x00\x00PreloadAnimatorEffects0\x00\x00\x00\x02\x00\x00\x00\r\x00\x00\x00\x06\x00\x00\x00JTArr\x1b\x00\x00\x00\x08\x00\x00\x00TypeSystem.String[]\x04\x00\x00\x00\x04\x00\x00\x00\x8c\x03\x00\x00\n\x00\x00\x00LookAtF\x00\x00\x00\x02\x00\x00\x00\r\x00\x00\x00\x06\x00\x00\x00JTCom1\x00\x00\x00\x08\x00\x00\x00TypeAssets.Scripts.GameLogic.CameraLookAt\x04\x00\x00\x004\x03\x00\x00\x04\x00\x00\x00B\x01\x00\x00\n\x00\x00\x00Offset4\x00\x00\x00\x02\x00\x00\x00\r\x00\x00\x00\x06\x00\x00\x00JTCom\x1f\x00\x00\x00\x08\x00\x00\x00TypeUnityEngine.Vector3\x04\x00\x00\x00\xfc\x00\x00\x00\x03\x00\x00\x00S\x00\x00\x00\x05\x00\x00\x00xB\x00\x00\x00\x03\x00\x00\x00\r\x00\x00\x00\x06\x00\x00\x00JTPri\x19\x00\x00\x00\x08\x00\x00\x00TypeSystem.Single\x14\x00\x00\x00\x05\x00\x00\x00V-0.07000029\x04\x00\x00\x00\x04\x00\x00\x00P\x00\x00\x00\x05\x00\x00\x00y?\x00\x00\x00\x03\x00\x00\x00\r\x00\x00\x00\x06\x00\x00\x00JTPri\x19\x00\x00\x00\x08\x00\x00\x00TypeSystem.Single\x11\x00\x00\x00\x05\x00\x00\x00V1.539993\x04\x00\x00\x00\x04\x00\x00\x00Q\x00\x00\x00\x05\x00\x00\x00z@\x00\x00\x00\x03\x00\x00\x00\r\x00\x00\x00\x06\x00\x00\x00JTPri\x19\x00\x00\x00\x08\x00\x00\x00TypeSystem.Single\x12\x00\x00\x00\x05\x00\x00\x00V-3.739998\x04\x00\x00\x00\x04\x00\x00\x00H\x01\x00\x00\r\x00\x00\x00Direction4\x00\x00\x00\x02\x00\x00\x00\r\x00\x00\x00\x06\x00\x00\x00JTCom\x1f\x00\x00\x00\x08\x00\x00\x00TypeUnityEngine.Vector3\x04\x00\x00\x00\xff\x00\x00\x00\x03\x00\x00\x00S\x00\x00\x00\x05\x00\x00\x00xB\x00\x00\x00\x03\x00\x00\x00\r\x00\x00\x00\x06\x00\x00\x00JTPri\x19\x00\x00\x00\x08\x00\x00\x00TypeSystem.Single\x14\x00\x00\x00\x05\x00\x00\x00V0.002750125\x04\x00\x00\x00\x04\x00\x00\x00S\x00\x00\x00\x05\x00\x00\x00yB\x00\x00\x00\x03\x00\x00\x00\r\x00\x00\x00\x06\x00\x00\x00JTPri\x19\x00\x00\x00\x08\x00\x00\x00TypeSystem.Single\x14\x00\x00\x00\x05\x00\x00\x00V0.009888734\x04\x00\x00\x00\x04\x00\x00\x00Q\x00\x00\x00\x05\x00\x00\x00z@\x00\x00\x00\x03\x00\x00\x00\r\x00\x00\x00\x06\x00\x00\x00JTPri\x19\x00\x00\x00\x08\x00\x00\x00TypeSystem.Single\x12\x00\x00\x00\x05\x00\x00\x00V0.9999473\x04\x00\x00\x00\x04\x00\x00\x00P\x00\x00\x00\x0c\x00\x00\x00Duration8\x00\x00\x00\x03\x00\x00\x00\r\x00\x00\x00\x06\x00\x00\x00JTPri\x19\x00\x00\x00\x08\x00\x00\x00TypeSystem.Single\n\x00\x00\x00\x05\x00\x00\x00V1\x04\x00\x00\x00\x04\x00\x00\x00R\x00\x00\x00\r\x00\x00\x00CameraFOV9\x00\x00\x00\x03\x00\x00\x00\r\x00\x00\x00\x06\x00\x00\x00JTPri\x19\x00\x00\x00\x08\x00\x00\x00TypeSystem.Single\x0b\x00\x00\x00\x05\x00\x00\x00V17\x04\x00\x00\x00\x04\x00\x00\x00m\x00\x00\x00\x0f\x00\x00\x00LightConfigR\x00\x00\x00\x02\x00\x00\x00\r\x00\x00\x00\x06\x00\x00\x00JTCom=\x00\x00\x00\x08\x00\x00\x00TypeAssets.Scripts.GameLogic.PrepareBattleLightConfig\x04\x00\x00\x00\x04\x00\x00\x00'
#-----------------------------------------------
"""def AddGetHolidayResourcePath(directory_path: str):
    for file in os.listdir(directory_path):
        if file.endswith(".xml"):
            input_path = os.path.join(directory_path, file)

            try:
                with open(input_path, "rb") as f:
                    xml_data = f.read()
            except Exception as e:
                continue

            lines = xml_data.split(b'\n')
            i = 0

            while i < len(lines):
                line = lines[i]
                try:
                    match = re.search(rb'<string name="resourcename(?:[123])?" value="prefab_skill_effects(.*?)"', line.lower())
                except UnicodeDecodeError:
                    i += 1
                    continue

                if match:
                    resource_path = match.group(1).decode(errors='ignore')
                    if "tongyong_effects/indicator" in resource_path.lower():
                        i += 1
                        continue

                    short_name = resource_path.strip('/').split('/')[-1]
                    guid = str(uuid.uuid4()).lower()

                    track_start = i
                    while track_start >= 0 and b'<Track ' not in lines[track_start]:
                        track_start -= 1

                    track_end = i
                    while track_end < len(lines) and b'</Track>' not in lines[track_end]:
                        track_end += 1

                    condition_lines = []
                    for j in range(track_start, track_end):
                        if b'<Condition ' in lines[j]:
                            condition_lines.append(lines[j].decode(errors='ignore'))

                    name_match = re.search(rb'name="(resourcename[0-9]*)"', line.lower())
                    attr_name = name_match.group(1).decode() if name_match else "resourceName"
                    new_line = f'        <String name="{attr_name}" value="" refParamName="{short_name}" useRefParam="false" />'
                    lines[i] = new_line.encode()

                    insert_block = [
                        f'    <Track trackName="MMNAOV[FixEffectsSkin]" eventType="GetHolidayResourcePathTick" guid="{guid}" enabled="true" useRefParam="false" refParamName="" r="0.000" g="0.000" b="0.000" execOnForceStopped="false" execOnActionCompleted="false" stopAfterLastEvent="true">'
                    ]
                    insert_block += condition_lines
                    insert_block += [
                        f'      <Event eventName="GetHolidayResourcePathTick" time="0.000" isDuration="false" guid="{guid}">',
                        f'        <String name="holidayResourcePathPrefix" value="prefab_skill_effects{resource_path}" refParamName="" useRefParam="false" />',
                        f'        <String name="outPathParamName" value="{short_name}" refParamName="" useRefParam="false" />',
                        f'        <String name="outSoundEventParamName" value="" refParamName="" useRefParam="false" />',
                        f'      </Event>',
                        f'    </Track>'
                    ]

                    for block_line in reversed(insert_block):
                        lines.insert(track_start, block_line.encode())

                    i = track_end + len(insert_block)
                else:
                    i += 1

            try:
                with open(input_path, "wb") as f:
                    f.write(b'\n'.join(lines))
                print(f" File: {file}")
                print(" Block đã chèn:\n" + '\n'.join(insert_block))
                print('-' * 60)

            except Exception as e:
                pass"""
def AddGetHolidayResourcePath(directory_path):
    for file in os.listdir(directory_path):
        file_path = os.path.join(directory_path, file)
        with open(file_path, "rb") as r0:
            context = r0.read()
            tracks = re.findall(rb'(<Track .*?</Track>)', context, re.DOTALL)
            if tracks:
                for track in tracks:
                    if isinstance(track, bytes):
                        if re.search(rb'enabled="false"', track):
                            continue
                        resource_match = re.search(rb'<String name="(.*?)" value="prefab_skill_effects(.*?)"', track)
                        resource_name = resource_match.group(2).decode() if resource_match else ""
                        short_name = resource_name.split("/")[-1] if resource_name else ""
                        getholiday = f'''<Track trackName="MMNAOV[FixEffectsSkin]" eventType="GetHolidayResourcePathTick" guid="MOD-BY-MMNAOV-ANCAPLAMCHO" enabled="true" useRefParam="false" refParamName="" r="0.000" g="0.000" b="0.000" execOnForceStopped="false" execOnActionCompleted="false" stopAfterLastEvent="true">\n      <Event eventName="GetHolidayResourcePathTick" time="0.000" isDuration="false" guid="MOD-BY-MMN-DZ">\n        <String name="holidayResourcePathPrefix" value="prefab_skill_effects{resource_name}" refParamName="" useRefParam="false" />\n        <String name="outPathParamName" value="{short_name}" refParamName="" useRefParam="false" />\n        <String name="outSoundEventParamName" value="" refParamName="" useRefParam="false" />\n      </Event>\n    </Track>\n    '''
                        if resource_name:
                            updated_track = re.sub(rb'<String name="(.*?)" value="prefab_skill_effects.*?" refParamName="" useRefParam="false" />', f'<String name="\\1" value="" refParamName="{short_name}" useRefParam="true" />'.encode(), track)
                            combined_tracks = getholiday.encode() + updated_track
                            context = context.replace(track, combined_tracks)
                            print(context)
        with open(file_path, "wb") as w0:
            w0.write(context)
def hex_to_dec(a):
    len(a)
    a=a[::-1]
    a=a.hex()
    a=int(a,16)
    return a
def dec_to_hex(a):
    a=hex(a)[2:]
    if len(a)%2==1:
        a='0'+a
    return (bytes.fromhex(a))[::-1]
#-----------------------------------------------
for IDMODSKIN in IDMODSKIN1:
    index = DANHSACH.index(IDMODSKIN)
    TENSKIN_NOW = TENSKIN[index]
    fileasset = f'Resources/1.59.1/AssetRefs/Hero/{IDMODSKIN[:3]}_AssetRef.bytes'
    fileasset_mod2 = f'{FolderMod}/Resources/1.59.1/AssetRefs/Hero/{IDMODSKIN[:3]}_AssetRef.bytes'
    shutil.copy(fileasset, fileasset_mod2)
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
    skinid = IDMODSKIN.encode()
    IDSOUND_S = IDMODSKIN
    phukien = ''
    phukienb = ''
    phukienv = ''
    IDINFO=int(IDMODSKIN)+1
    IDINFO=str(IDINFO)
    if str(IDINFO)[3:4] == '0':
        IDINFO=IDINFO[:3]+IDINFO[4:]
    IDINFO=str(IDINFO)

    if IDCHECK == '52007':
        phukien1 = input(
            '\033[1;97m[\033[1;91m?\033[1;97m] Mod Component:\n'
            '\033[1;97m [1] \033[1;92mBlue\n'
            '\033[1;97m [2] \033[1;92mRed\n'
            '\033[1;97m [3] \033[1;92mNo Mod Component\n'
            '\033[1;97m[•] INPUT: '
        )
        if phukien1 == "1":
            phukien = 'xanh'
        if phukien1 == "2":
            phukien = 'do'
    if IDCHECK == '13311':
        phukien1v = input(
            '\033[1;97m[\033[1;91m?\033[1;97m] Mod Component:\n'
            '\033[1;97m [1] \033[1;92mGreen\n'
            '\033[1;97m [2] \033[1;92mRed\n'
            '\033[1;97m [3] \033[1;92mNo Mod Component\n'
            '\033[1;97m[•] INPUT: '
        )
        if phukien1v == "1":
            phukienv = 'vangv'
        if phukien1v == "2":
            phukienv = 'dov'
    if IDCHECK == '11620':
        phukien12 = input(
            '\033[1;97m[\033[1;91m?\033[1;97m] Mod Component:\n'
            '\033[1;97m [1] \033[1;92mPurple\n'
            '\033[1;97m [2] \033[1;92mRed\n'
            '\033[1;97m [3] \033[1;92mNo Mod Component\n'
            '\033[1;97m[•] INPUT: '
        )
        if phukien12 == "1":
            phukienb = 'tim'
        if phukien12 == "2":
            phukienb = 'do'
    if IDMODSKIN == '11620':
        try:
            with open(file_shop_mod, 'rb') as f:
                codenew = f.read()
            codenew = codenew.replace(bgbuterbac1, bgbuterbac5)
            with open(file_shop_mod, 'wb') as f:
                f.write(codenew)
            print('Awaken_Label_1 --> Awaken_Label_5')
        except:
            print("⚠ Không thể thay background Shop. Bỏ qua...")
    if IDMODSKIN == '13311':
        try:
            with open(file_shop_mod, 'rb') as f:
                codenew = f.read()
            codenew = codenew.replace(bacvalheinevo1, bacvalheinevo5)
            with open(file_shop_mod, 'wb') as f:
                f.write(codenew)
            print('Awaken_Label_1 --> Awaken_Label_5')
        except:
            print("⚠ Không thể thay background Shop. Bỏ qua...")
    if IDMODSKIN == '16707':
        try:
            with open(file_shop_mod, 'rb') as f:
                codenew = f.read()
            codenew = codenew.replace(bacngokhongevo1, bacngokhongevo5)
            with open(file_shop_mod, 'wb') as f:
                f.write(codenew)
            print('Awaken_Label_1 --> Awaken_Label_5')
        except:
            print("⚠ Không thể thay background Shop. Bỏ qua...")
            
    try:
        id_mod = dec_to_hex(int(skinid.decode()))
        id_0 = dec_to_hex(int(skinid[:3].decode() + '00'))
        hero_actor = dec_to_hex(int(skinid[:3].decode()))
        
        with open(file_actor_mod, 'rb') as f:
            strin = f.read()
        pos_mod = strin.find(id_mod + b'\x00\x00' + hero_actor)
        pos_base = strin.find(id_0 + b'\x00\x00' + hero_actor)
        
        if pos_mod != -1 and pos_base != -1:
            actor_mod = strin[pos_mod - 4:pos_mod + hex_to_dec(strin[pos_mod - 4:pos_mod - 2])]
            actor_0 = strin[pos_base - 4:pos_base + hex_to_dec(strin[pos_base - 4:pos_base - 2])]
    
            if skinid == b'16707':
                actor_mod = actor_mod[:4] + actor_0[4:10] + actor_mod[10:36] + b'\x00' + actor_mod[37:]
                actor_mod=actor_mod.replace(b'\x07\x00\x00\x00301677',b'\x07\x00\x00\x00301670',1)
                actor_mod=actor_mod.replace(b'\x10\x00\x00\x00Share_16707\x2ejpg',b'\x12\x00\x00\x00Share_16707_2\x2ejpg').replace(b'\x0a\x00\x00\x0016707\x2ejpg',b'\x0c\x00\x00\x0016707_2\x2ejpg').replace(b'\x0b\x00\x00\x00301677\x2ejpg',b'\x0d\x00\x00\x00301677_2\x2ejpg').replace(b'\x0f\x00\x00\x00301677head\x2ejpg',b'\x11\x00\x00\x00301677_2head\x2ejpg').replace(b'\x25\x00\x00\x00\x42\x47\x5f\x43\x6f\x6d\x6d\x6f\x6e\x73\x5f\x30\x31\x2f\x42\x47\x5f\x43\x6f\x6d\x6d\x6f\x6e\x73\x5f\x30\x31\x5f\x50\x6c\x61\x74\x66\x6f\x72\x6d',b'\x2d\x00\x00\x00\x42\x47\x5f\x77\x75\x6b\x6f\x6e\x67\x6a\x75\x65\x78\x69\x6e\x67\x32\x2f\x42\x47\x5f\x77\x75\x6b\x6f\x6e\x67\x6a\x75\x65\x78\x69\x6e\x67\x32\x5f\x50\x6c\x61\x74\x66\x6f\x72\x6d')
            elif skinid == b'10620':
                actor_mod = actor_mod[:4] + actor_0[4:10] + actor_mod[10:36] + b'\x00' + actor_mod[37:]
                actor_mod = actor_mod.replace(b'\x08\x00\x00\x003010620', b'\x07\x00\x00\x00301060', 1)
            elif skinid == b'13311':
                actor_mod = actor_mod[:4] + actor_0[4:10] + actor_mod[10:36] + b'\x00' + actor_mod[37:]
                actor_mod=actor_mod.replace(b'\x08\x00\x00\x003013311',b'\x07\x00\x00\x00301330',1)
                actor_mod=actor_mod.replace(b'\x10\x00\x00\x00Share_13311\x2ejpg',b'\x12\x00\x00\x00Share_13311_2\x2ejpg').replace(b'\x0a\x00\x00\x0013311\x2ejpg',b'\x0c\x00\x00\x0013311_2\x2ejpg').replace(b'\x0c\x00\x00\x003013311\x2ejpg',b'\x0e\x00\x00\x003013311_2\x2ejpg').replace(b'\x10\x00\x00\x003013311head\x2ejpg',b'\x12\x00\x00\x003013311_2head\x2ejpg').replace(b'\x25\x00\x00\x00\x42\x47\x5f\x43\x6f\x6d\x6d\x6f\x6e\x73\x5f\x30\x31\x2f\x42\x47\x5f\x43\x6f\x6d\x6d\x6f\x6e\x73\x5f\x30\x31\x5f\x50\x6c\x61\x74\x66\x6f\x72\x6d',b'\x33\x00\x00\x00\x42\x47\x5f\x44\x69\x52\x65\x6e\x4a\x69\x65\x5f\x31\x33\x33\x31\x32\x5f\x54\x33\x2f\x42\x47\x5f\x79\x69\x6e\x79\x69\x6e\x67\x7a\x68\x69\x73\x68\x6f\x75\x5f\x30\x31\x5f\x70\x6c\x61\x74\x66\x6f\x72\x6d')
            elif skinid == b'11620':
                actor_mod = actor_mod[:4] + actor_0[4:10] + actor_mod[10:36] + b'\x00' + actor_mod[37:]
                actor_mod=actor_mod.replace(b'\x08\x00\x00\x003011620',b'\x07\x00\x00\x00301160',1)
                actor_mod=actor_mod.replace(
                b'\x25\x00\x00\x00\x42\x47\x5F\x43\x6F\x6D\x6D\x6F\x6E\x73\x5F\x30\x31\x2F\x42\x47\x5F\x43\x6F\x6D\x6D\x6F\x6E\x73\x5F\x30\x31\x5F\x50\x6C\x61\x74\x66\x6F\x72\x6D\x00',
                b'\x36\x00\x00\x00\x42\x47\x5F\x44\x61\x6F\x46\x65\x6E\x67\x4A\x69\x4E\x69\x61\x6E\x67\x5F\x31\x31\x36\x32\x31\x2F\x42\x47\x5F\x79\x69\x6E\x79\x69\x6E\x67\x7A\x68\x69\x73\x68\x6F\x75\x5F\x30\x31\x5F\x70\x6C\x61\x74\x66\x6F\x72\x6D\x00').replace(
                b'\x10\x00\x00\x00Share_11620\x2ejpg',
                b'\x12\x00\x00\x00Share_11620_2\x2ejpg').replace(
b'\x0a\x00\x00\x0011620\x2ejpg',
                b'\x0c\x00\x00\x0011620_2\x2ejpg').replace(
                b'\x0c\x00\x00\x003011620\x2ejpg',
                b'\x0e\x00\x00\x003011620_2\x2ejpg').replace(
                b'\x10\x00\x00\x003011620head\x2ejpg',
                b'\x12\x00\x00\x003011620_2head\x2ejpg')
            elif skinid == b'15412':
                actor_mod = actor_mod[:4] + actor_0[4:10] + actor_mod[10:36] + b'\x00' + actor_mod[37:]
                actor_mod = actor_mod.replace(
                    b'\x08\x00\x00\x003015412', b'\x07\x00\x00\x00301540', 1
                ).replace(
                    b'\x12\x00\x00\x003015412_B43_1', b'\x0c\x00\x00\x003015412', 1
                )
            else:
                nhanDangId_0 = actor_0[64:]
                nhanDangId_0 = nhanDangId_0[:hex_to_dec(nhanDangId_0[:2]) + 4]
    
                actor_mod = (
                    actor_mod[:64] + nhanDangId_0 +
                    actor_mod[64 + hex_to_dec(actor_mod[64:66]) + 4:]
                )
                actor_mod = actor_mod.replace(id_mod + b'\x00\x00' + hero_actor, id_0 + b'\x00\x00' + hero_actor)
                actor_mod = actor_mod[:36] + b'\x00' + actor_mod[37:]
            actor_mod = dec_to_hex(len(actor_mod) - 4) + actor_mod[2:]
            dieukienmod=actor_mod
            strin = strin.replace(actor_0, actor_mod, 1)
        with open(file_actor_mod, 'wb') as f:
            f.write(strin)
    
    except Exception as bug:
        print(bug)
        print('\n\t\033[0m          [   \033[1;31mKhông Mod Heroskin Mặc Định\033[0m    ]')
#-----------------------------------------------
    print('Mod Skin Phụ')
    try:
        for nnn in range(1,30):
            #nnn=int(nnn.decode()[3:])-1
            with open(file_actor_mod,'rb') as f:
                strin = f.read()
                hero_actor=dec_to_hex(int(skinid[:3].decode()))
                id_mod=dec_to_hex(int(skinid.decode()))
                pos = strin.find(id_mod+b'\x00\x00'+hero_actor)
                if pos!=-1:
                    actor_mod = strin[pos-4:pos+hex_to_dec(strin[pos-4:pos-2])]
                    if skinid==b'16707':
                        actor_mod=actor_mod.replace(b'\x07\x00\x00\x00301677',b'\x09\x00\x00\x00301677_2',1)
                        actor_mod=actor_mod.replace(b'\x10\x00\x00\x00Share_16707\x2ejpg',b'\x12\x00\x00\x00Share_16707_2\x2ejpg').replace(b'\x0a\x00\x00\x0016707\x2ejpg',b'\x0c\x00\x00\x0016707_2\x2ejpg').replace(b'\x0b\x00\x00\x00301677\x2ejpg',b'\x0d\x00\x00\x00301677_2\x2ejpg').replace(b'\x0f\x00\x00\x00301677head\x2ejpg',b'\x11\x00\x00\x00301677_2head\x2ejpg').replace(b'\x25\x00\x00\x00\x42\x47\x5f\x43\x6f\x6d\x6d\x6f\x6e\x73\x5f\x30\x31\x2f\x42\x47\x5f\x43\x6f\x6d\x6d\x6f\x6e\x73\x5f\x30\x31\x5f\x50\x6c\x61\x74\x66\x6f\x72\x6d',b'\x2d\x00\x00\x00\x42\x47\x5f\x77\x75\x6b\x6f\x6e\x67\x6a\x75\x65\x78\x69\x6e\x67\x32\x2f\x42\x47\x5f\x77\x75\x6b\x6f\x6e\x67\x6a\x75\x65\x78\x69\x6e\x67\x32\x5f\x50\x6c\x61\x74\x66\x6f\x72\x6d')
                        actor_mod=dec_to_hex(len(actor_mod)-4)+actor_mod[2:]
                    if skinid==b'13311':
                        actor_mod=actor_mod.replace(b'\x08\x00\x00\x003013311',b'\x0a\x00\x00\x003013311_2',1)
                        actor_mod=actor_mod.replace(b'\x10\x00\x00\x00Share_13311\x2ejpg',b'\x12\x00\x00\x00Share_13311_2\x2ejpg').replace(b'\x0a\x00\x00\x0013311\x2ejpg',b'\x0c\x00\x00\x0013311_2\x2ejpg').replace(b'\x0c\x00\x00\x003013311\x2ejpg',b'\x0e\x00\x00\x003013311_2\x2ejpg').replace(b'\x10\x00\x00\x003013311head\x2ejpg',b'\x12\x00\x00\x003013311_2head\x2ejpg').replace(b'\x25\x00\x00\x00\x42\x47\x5f\x43\x6f\x6d\x6d\x6f\x6e\x73\x5f\x30\x31\x2f\x42\x47\x5f\x43\x6f\x6d\x6d\x6f\x6e\x73\x5f\x30\x31\x5f\x50\x6c\x61\x74\x66\x6f\x72\x6d',b'\x33\x00\x00\x00\x42\x47\x5f\x44\x69\x52\x65\x6e\x4a\x69\x65\x5f\x31\x33\x33\x31\x32\x5f\x54\x33\x2f\x42\x47\x5f\x79\x69\x6e\x79\x69\x6e\x67\x7a\x68\x69\x73\x68\x6f\x75\x5f\x30\x31\x5f\x70\x6c\x61\x74\x66\x6f\x72\x6d')
                        actor_mod=dec_to_hex(len(actor_mod)-4)+actor_mod[2:]
                    if skinid==b'11620':
                        actor_mod=actor_mod.replace(b'\x08\x00\x00\x003011620',b'\x0a\x00\x00\x003011620_1',1)
                        actor_mod=actor_mod.replace(b'\x25\x00\x00\x00\x42\x47\x5F\x43\x6F\x6D\x6D\x6F\x6E\x73\x5F\x30\x31\x2F\x42\x47\x5F\x43\x6F\x6D\x6D\x6F\x6E\x73\x5F\x30\x31\x5F\x50\x6C\x61\x74\x66\x6F\x72\x6D\x00',b'\x36\x00\x00\x00\x42\x47\x5F\x44\x61\x6F\x46\x65\x6E\x67\x4A\x69\x4E\x69\x61\x6E\x67\x5F\x31\x31\x36\x32\x31\x2F\x42\x47\x5F\x79\x69\x6E\x79\x69\x6E\x67\x7A\x68\x69\x73\x68\x6F\x75\x5F\x30\x31\x5F\x70\x6C\x61\x74\x66\x6F\x72\x6D\x00').replace(b'\x10\x00\x00\x00Share_11620\x2ejpg',b'\x12\x00\x00\x00Share_11620_2\x2ejpg').replace(b'\x0a\x00\x00\x0011620\x2ejpg',b'\x0c\x00\x00\x0011620_2\x2ejpg').replace(b'\x0c\x00\x00\x003011620\x2ejpg',b'\x0e\x00\x00\x003011620_2\x2ejpg').replace(b'\x10\x00\x00\x003011620head\x2ejpg',b'\x12\x00\x00\x003011620_2head\x2ejpg')
                        actor_mod=dec_to_hex(len(actor_mod)-4)+actor_mod[2:]
                    id_2=dec_to_hex(int(skinid[:3].decode())*100+nnn)
                    pos = strin.find(id_2+b'\x00\x00'+hero_actor)
                    if pos !=-1:
                        actor_2 = strin[pos-4:pos+hex_to_dec(strin[pos-4:pos-2])]
                        re_2 = actor_mod[:4]+id_2+actor_mod[6:][:30]+dec_to_hex(nnn)+actor_mod[37:]
                        if re_2!=b'' and actor_2!=b'' and nnn!=int(skinid[3:].decode()):
                            strin=strin.replace(actor_2,re_2)
                            with open(file_actor_mod,'wb') as f1:
                                f1.write(strin)
    except Exception as bug:
        print(bug)
    
    try:
        with open(file_shop_mod, 'rb') as f: d = f.read()
    except:
        pass
    i1 = int(IDMODSKIN).to_bytes(4, 'little')
    i2 = int(IDMODSKIN[:3] + '00').to_bytes(4, 'little')
    
    try: d = bytearray(open(file_actor_mod,'rb').read())
    except: print(" File lỗi"); exit()
    
    p1 = d.find(i1)
    p2 = d.find(i2)
    if p1 == -1 or p2 == -1: pass
    
    b1 = bytearray(d[p1:p1+33])
    b2 = bytearray(d[p2:p2+33])
    print(b1)
    print(b2)
    
    b1[-1], b2[-1] = b2[-1], b1[-1]
    d[p1:p1+33] = b1
    d[p2:p2+33] = b2
    
    open(file_actor_mod,'wb').write(d)

    ID = IDMODSKIN
    Show = 'y'  # input("\n \033[1;36mShow Name? (y/n): ")
    IDB = int(ID).to_bytes(4, byteorder="little")
    IDH = int(ID[0:3]).to_bytes(4, byteorder="little")
    Files = [file_shop_mod]
    
    for File in Files:
        All = []
        Skin = ""
        file = open(File, "rb")
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
            print("\n \033[1;31m The id couldn't be found in " + File + " file!")
            if "HeroSkinShop.bytes" in File:
                continue 
            IDNew = input("\n\033[1;36m  Enter an alternate skin ID: ")
            IDK = int(IDNew).to_bytes(4, byteorder="little")
            Find = -1
            while True:
                Find = Code.find(b"\x00\x00" + IDK, Find + 1)
                if str(int.from_bytes(Code[Find - 6:Find - 8], byteorder="little")) == IDNew[0:3]:
                    Sum = int.from_bytes(Code[Find - 2:Find], byteorder="little")
                    Skin = Code[Find - 2:Find - 2 + Sum]
                    break
    
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
                    EndTheCode = hex(len(Cache))
                    if len(EndTheCode) == 5:
                        EndTheCode = EndTheCode[3:5] + "0" + EndTheCode[2:3]
                    else:
                        EndTheCode = EndTheCode[4:6] + EndTheCode[2:4]
                    EndTheCode = bytes.fromhex(EndTheCode)
                    Cache = Cache.replace(Cache[0:2], EndTheCode, 1)
    
            Code = Code.replace(Id, Cache, 1)
        file = open(File, "wb")
        file.write(Code)
        file.close()

#----------------------------------------------
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
                    id2='6500'
                    a1=bytes.fromhex(str(id2))
                    f.close()
                    i1=ab.find(a1)-4
                    vt11=ab[i1:i1+4]
                    vtr1=int.from_bytes(vt11,byteorder='little')
                    vt2=ab[i1:i1+vtr1]
                    vt1=vt1.replace(a,a1)
                    vt11=ab.replace(vt2,vt1)
                    with open(inp,'wb') as go:
                        go.write(vt11)
            else:
                print('không tìm thấy viền (vui lòng nhập thủ công)')

#----------------------------------------------
    if fixlag == '1':
        if b"Skin_Icon_Skill" in dieukienmod or IDCHECK == "53702":
            fileasset_mod = f'{FolderMod}/Resources/1.59.1/AssetRefs/Hero/{IDMODSKIN[:3]}_AssetRef.bytes'
            giai(fileasset_mod)
            id=IDCHECK
            if IDCHECK == "13311":
                with open(fileasset_mod,'rb') as f:rpl=f.read()
                CODETONG = rpl.replace(b"prefab_skill_effects/hero_skill_effects/133_direnjie/", b"prefab_skill_effects/component_effects/13311/13311_5/")
                with open(fileasset_mod,'wb') as f:f.write(CODETONG)
                print(f'  [✓] Fix Lag  {os.path.basename(fileasset_mod)}')
                
            elif IDCHECK == "16707":
                with open(fileasset_mod,'rb') as f:rpl=f.read();f.close()
                CACHE=[]
                VTR=rpl[rpl.find(b'particlesInFirstLayer')-8:rpl.find(b'particlesInFirstLayer')-4];VTC=rpl[rpl.find(b'particlesInFirstLayer')-8:rpl.find(b'animationsw')-8]
                DAU1=rpl[:rpl.find(b'particlesInFirstLayer')-8]
                VTF=b''
                if rpl.find(b'skinSubset') != -1:
                    VTF=rpl[rpl.find(b'skinSubset')-8:]
                    CUOI1=rpl[rpl.find(b'animationsw')-8:rpl.find(b'skinSubset')-8]
                else:
                    CUOI1=rpl[rpl.find(b'animationsw')-8:]
                while True:
                    if VTC == b'': break
                    CACHE.append(VTC[:int.from_bytes((VTC[:4]),'little')])
                    VTC=VTC[int.from_bytes((VTC[:4]),'little'):]
                CODETONG=b''
                for i in CACHE:
                    VT=i.find(b'Element')-8
                    VTDAU=i[VT-8:VT]
                    DAU=i[:VT-8]
                    VTD=i[VT:]
                    CODE=b''
                    for ig in range(i.count(b'Element')):
                        VTC=VTD[:int.from_bytes((VTD[:4]),'little')]
                        VT=VTC[103:111]
                        VT1=VTC[111:121]
                        VT2=VTC[121:167]
                        Cuoi=VTC[int.from_bytes(VTC[167:171],'little')+167:]
                        VTT=VTC[167:int.from_bytes(VTC[167:171],'little')+167]
                        if VTT.find(id[:3].encode())!= -1:
                            IDEOV = "16707_5"
                            RPL=VTT[4:].replace(b"hero_skill_effects/167_wukong/",b"component_effects/16707/16707_5/").replace(b"Hero_Skill_Effects/167_wukong/",b"component_effects/16707/16707_5/");RPL=RPL.replace(IDEOV.encode()+b'/'+IDEOV.encode(),IDEOV.encode())
                        else:RPL=VTT[4:]
                        RPL=len(b'\x0b\x00\x00\x00\x0b\x00\x00\x00ElementT\x00\x00\x00\x02\x00\x00\x00\r\x00\x00\x00\x06\x00\x00\x00JTCom?\x00\x00\x00\x08\x00\x00\x00TypeAssetRefAnalyser.Pair`2[System.String,System.Int32]\x04\x00\x00\x00'+len(VT+(len(VT1+len(VT2+(len(RPL)+4).to_bytes(4,'little')+RPL).to_bytes(4,'little')+VT2[4:]+(len(RPL)+4).to_bytes(4,'little')+RPL)+8).to_bytes(4,'little')+VT1[4:]+len(VT2+(len(RPL)+4).to_bytes(4,'little')+RPL).to_bytes(4,'little')+VT2[4:]+(len(RPL)+4).to_bytes(4,'little')+RPL+Cuoi).to_bytes(4,'little')+VT[4:]+(len(VT1+len(VT2+(len(RPL)+4).to_bytes(4,'little')+RPL).to_bytes(4,'little')+VT2[4:]+(len(RPL)+4).to_bytes(4,'little')+RPL)+8).to_bytes(4,'little')+VT1[4:]+len(VT2+(len(RPL)+4).to_bytes(4,'little')+RPL).to_bytes(4,'little')+VT2[4:]+(len(RPL)+4).to_bytes(4,'little')+RPL+Cuoi).to_bytes(4,'little')+b'\x0b\x00\x00\x00ElementT\x00\x00\x00\x02\x00\x00\x00\r\x00\x00\x00\x06\x00\x00\x00JTCom?\x00\x00\x00\x08\x00\x00\x00TypeAssetRefAnalyser.Pair`2[System.String,System.Int32]\x04\x00\x00\x00'+len(VT+(len(VT1+len(VT2+(len(RPL)+4).to_bytes(4,'little')+RPL).to_bytes(4,'little')+VT2[4:]+(len(RPL)+4).to_bytes(4,'little')+RPL)+8).to_bytes(4,'little')+VT1[4:]+len(VT2+(len(RPL)+4).to_bytes(4,'little')+RPL).to_bytes(4,'little')+VT2[4:]+(len(RPL)+4).to_bytes(4,'little')+RPL+Cuoi).to_bytes(4,'little')+VT[4:]+(len(VT1+len(VT2+(len(RPL)+4).to_bytes(4,'little')+RPL).to_bytes(4,'little')+VT2[4:]+(len(RPL)+4).to_bytes(4,'little')+RPL)+8).to_bytes(4,'little')+VT1[4:]+len(VT2+(len(RPL)+4).to_bytes(4,'little')+RPL).to_bytes(4,'little')+VT2[4:]+(len(RPL)+4).to_bytes(4,'little')+RPL+Cuoi
                        CODE+=RPL
                        VTD=VTD[int.from_bytes((VTD[:4]),'little'):]
                    CODE=len(DAU+len(CODE+VTDAU).to_bytes(4,'little')+VTDAU[4:]+CODE).to_bytes(4,'little')+DAU[4:]+len(CODE+VTDAU).to_bytes(4,'little')+VTDAU[4:]+CODE;CODETONG+=CODE
                if id in('15704','11107'):
                    VTP=CUOI1[:149]
                    CUOI=CUOI1[149:]
                    ELEMENT=[]
                    while True:
                        VT=CUOI[:4]
                        if CUOI==b'': break
                        ELEMENT.append(CUOI[:int.from_bytes(VT,'little')])
                        CUOI=CUOI[int.from_bytes(VT,'little'):]
                    CUOI1=b''
                    for VTC in ELEMENT:
                        VT=VTC[103:111]
                        VT1=VTC[111:121]
                        VT2=VTC[121:167]
                        Cuoi=VTC[int.from_bytes(VTC[167:171],'little')+167:]
                        VTT=VTC[167:int.from_bytes(VTC[167:171],'little')+167]
                        RPL=VTT[4:]
                        RPL=RPL[:5]+id.encode()+b'/'+RPL[5:]
                        RPL=len(b'\x0b\x00\x00\x00\x0b\x00\x00\x00ElementT\x00\x00\x00\x02\x00\x00\x00\r\x00\x00\x00\x06\x00\x00\x00JTCom?\x00\x00\x00\x08\x00\x00\x00TypeAssetRefAnalyser.Pair`2[System.String,System.Int32]\x04\x00\x00\x00'+len(VT+(len(VT1+len(VT2+(len(RPL)+4).to_bytes(4,'little')+RPL).to_bytes(4,'little')+VT2[4:]+(len(RPL)+4).to_bytes(4,'little')+RPL)+8).to_bytes(4,'little')+VT1[4:]+len(VT2+(len(RPL)+4).to_bytes(4,'little')+RPL).to_bytes(4,'little')+VT2[4:]+(len(RPL)+4).to_bytes(4,'little')+RPL+Cuoi).to_bytes(4,'little')+VT[4:]+(len(VT1+len(VT2+(len(RPL)+4).to_bytes(4,'little')+RPL).to_bytes(4,'little')+VT2[4:]+(len(RPL)+4).to_bytes(4,'little')+RPL)+8).to_bytes(4,'little')+VT1[4:]+len(VT2+(len(RPL)+4).to_bytes(4,'little')+RPL).to_bytes(4,'little')+VT2[4:]+(len(RPL)+4).to_bytes(4,'little')+RPL+Cuoi).to_bytes(4,'little')+b'\x0b\x00\x00\x00ElementT\x00\x00\x00\x02\x00\x00\x00\r\x00\x00\x00\x06\x00\x00\x00JTCom?\x00\x00\x00\x08\x00\x00\x00TypeAssetRefAnalyser.Pair`2[System.String,System.Int32]\x04\x00\x00\x00'+len(VT+(len(VT1+len(VT2+(len(RPL)+4).to_bytes(4,'little')+RPL).to_bytes(4,'little')+VT2[4:]+(len(RPL)+4).to_bytes(4,'little')+RPL)+8).to_bytes(4,'little')+VT1[4:]+len(VT2+(len(RPL)+4).to_bytes(4,'little')+RPL).to_bytes(4,'little')+VT2[4:]+(len(RPL)+4).to_bytes(4,'little')+RPL+Cuoi).to_bytes(4,'little')+VT[4:]+(len(VT1+len(VT2+(len(RPL)+4).to_bytes(4,'little')+RPL).to_bytes(4,'little')+VT2[4:]+(len(RPL)+4).to_bytes(4,'little')+RPL)+8).to_bytes(4,'little')+VT1[4:]+len(VT2+(len(RPL)+4).to_bytes(4,'little')+RPL).to_bytes(4,'little')+VT2[4:]+(len(RPL)+4).to_bytes(4,'little')+RPL+Cuoi
                        CUOI1+=RPL
                    CUOI1=VTP[:141]+(len(CUOI1)+8).to_bytes(4,'little')+VTP[145:]+CUOI1
                CODETONG=len(DAU1[:83]+len((DAU1[83:91]+(len(DAU1[91:183]+len(DAU1[183:]+CODETONG+CUOI1).to_bytes(4,'little')+DAU1[187:]+CODETONG+CUOI1).to_bytes(4,'little')+DAU1[95:183]+len(DAU1[183:]+CODETONG+CUOI1).to_bytes(4,'little')+DAU1[187:]+CODETONG+CUOI1)+VTF)).to_bytes(4,'little')+DAU1[87:91]+(len(DAU1[91:183]+len(DAU1[183:]+CODETONG+CUOI1).to_bytes(4,'little')+DAU1[187:]+CODETONG+CUOI1).to_bytes(4,'little')+DAU1[95:183]+len(DAU1[183:]+CODETONG+CUOI1).to_bytes(4,'little')+DAU1[187:]+CODETONG+CUOI1)+VTF).to_bytes(4,'little')+DAU1[4:83]+len((DAU1[83:91]+(len(DAU1[91:183]+len(DAU1[183:]+CODETONG+CUOI1).to_bytes(4,'little')+DAU1[187:]+CODETONG+CUOI1).to_bytes(4,'little')+DAU1[95:183]+len(DAU1[183:]+CODETONG+CUOI1).to_bytes(4,'little')+DAU1[187:]+CODETONG+CUOI1)+VTF)).to_bytes(4,'little')+DAU1[87:91]+(len(DAU1[91:183]+len(DAU1[183:]+CODETONG+CUOI1).to_bytes(4,'little')+DAU1[187:]+CODETONG+CUOI1).to_bytes(4,'little')+DAU1[95:183]+len(DAU1[183:]+CODETONG+CUOI1).to_bytes(4,'little')+DAU1[187:]+CODETONG+CUOI1)+VTF
                #with open('kb1.bytes','wb') as f:f.write(CODETONG)
                with open(fileasset_mod,'wb') as f:f.write(CODETONG)
                
                print(f'  [✓] Fix Lag  {os.path.basename(fileasset_mod)}')
#----------------------------------------------
            if IDCHECK == "52007":
                if phukien == "do" or "xanh":
                    with open(fileasset_mod,'rb') as f:rpl=f.read();f.close()
                    CACHE=[]
                    VTR=rpl[rpl.find(b'particlesInFirstLayer')-8:rpl.find(b'particlesInFirstLayer')-4];VTC=rpl[rpl.find(b'particlesInFirstLayer')-8:rpl.find(b'animationsw')-8]
                    DAU1=rpl[:rpl.find(b'particlesInFirstLayer')-8]
                    VTF=b''
                    if rpl.find(b'skinSubset') != -1:
                        VTF=rpl[rpl.find(b'skinSubset')-8:]
                        CUOI1=rpl[rpl.find(b'animationsw')-8:rpl.find(b'skinSubset')-8]
                    else:
                        CUOI1=rpl[rpl.find(b'animationsw')-8:]
                    while True:
                        if VTC == b'': break
                        CACHE.append(VTC[:int.from_bytes((VTC[:4]),'little')])
                        VTC=VTC[int.from_bytes((VTC[:4]),'little'):]
                    CODETONG=b''
                    for i in CACHE:
                        VT=i.find(b'Element')-8
                        VTDAU=i[VT-8:VT]
                        DAU=i[:VT-8]
                        VTD=i[VT:]
                        CODE=b''
                        for ig in range(i.count(b'Element')):
                            VTC=VTD[:int.from_bytes((VTD[:4]),'little')]
                            VT=VTC[103:111]
                            VT1=VTC[111:121]
                            VT2=VTC[121:167]
                            Cuoi=VTC[int.from_bytes(VTC[167:171],'little')+167:]
                            VTT=VTC[167:int.from_bytes(VTC[167:171],'little')+167]
                            if VTT.find(id[:3].encode())!= -1:
                                if phukien == "do":
                                    PHUKHIENDO = "5200402"
                                    RPL=VTT[4:].replace(b"hero_skill_effects/520_Veres/",b"component_effects/52007/5200402/").replace(b"hero_skill_effects/520_Veres/",b"component_effects/52007/5200402/");RPL=RPL.replace(PHUKHIENDO.encode()+b'/'+PHUKHIENDO.encode(),PHUKHIENDO.encode())
                                if phukien == "xanh":
                                    PHUKHIENDO = "5200401"
                                    RPL=VTT[4:].replace(b"hero_skill_effects/520_Veres/",b"component_effects/52007/5200401/").replace(b"hero_skill_effects/520_Veres/",b"component_effects/52007/5200401/");RPL=RPL.replace(PHUKHIENDO.encode()+b'/'+PHUKHIENDO.encode(),PHUKHIENDO.encode())

                            else:RPL=VTT[4:]
                            RPL=len(b'\x0b\x00\x00\x00\x0b\x00\x00\x00ElementT\x00\x00\x00\x02\x00\x00\x00\r\x00\x00\x00\x06\x00\x00\x00JTCom?\x00\x00\x00\x08\x00\x00\x00TypeAssetRefAnalyser.Pair`2[System.String,System.Int32]\x04\x00\x00\x00'+len(VT+(len(VT1+len(VT2+(len(RPL)+4).to_bytes(4,'little')+RPL).to_bytes(4,'little')+VT2[4:]+(len(RPL)+4).to_bytes(4,'little')+RPL)+8).to_bytes(4,'little')+VT1[4:]+len(VT2+(len(RPL)+4).to_bytes(4,'little')+RPL).to_bytes(4,'little')+VT2[4:]+(len(RPL)+4).to_bytes(4,'little')+RPL+Cuoi).to_bytes(4,'little')+VT[4:]+(len(VT1+len(VT2+(len(RPL)+4).to_bytes(4,'little')+RPL).to_bytes(4,'little')+VT2[4:]+(len(RPL)+4).to_bytes(4,'little')+RPL)+8).to_bytes(4,'little')+VT1[4:]+len(VT2+(len(RPL)+4).to_bytes(4,'little')+RPL).to_bytes(4,'little')+VT2[4:]+(len(RPL)+4).to_bytes(4,'little')+RPL+Cuoi).to_bytes(4,'little')+b'\x0b\x00\x00\x00ElementT\x00\x00\x00\x02\x00\x00\x00\r\x00\x00\x00\x06\x00\x00\x00JTCom?\x00\x00\x00\x08\x00\x00\x00TypeAssetRefAnalyser.Pair`2[System.String,System.Int32]\x04\x00\x00\x00'+len(VT+(len(VT1+len(VT2+(len(RPL)+4).to_bytes(4,'little')+RPL).to_bytes(4,'little')+VT2[4:]+(len(RPL)+4).to_bytes(4,'little')+RPL)+8).to_bytes(4,'little')+VT1[4:]+len(VT2+(len(RPL)+4).to_bytes(4,'little')+RPL).to_bytes(4,'little')+VT2[4:]+(len(RPL)+4).to_bytes(4,'little')+RPL+Cuoi).to_bytes(4,'little')+VT[4:]+(len(VT1+len(VT2+(len(RPL)+4).to_bytes(4,'little')+RPL).to_bytes(4,'little')+VT2[4:]+(len(RPL)+4).to_bytes(4,'little')+RPL)+8).to_bytes(4,'little')+VT1[4:]+len(VT2+(len(RPL)+4).to_bytes(4,'little')+RPL).to_bytes(4,'little')+VT2[4:]+(len(RPL)+4).to_bytes(4,'little')+RPL+Cuoi
                            CODE+=RPL
                            VTD=VTD[int.from_bytes((VTD[:4]),'little'):]
                        CODE=len(DAU+len(CODE+VTDAU).to_bytes(4,'little')+VTDAU[4:]+CODE).to_bytes(4,'little')+DAU[4:]+len(CODE+VTDAU).to_bytes(4,'little')+VTDAU[4:]+CODE;CODETONG+=CODE
                    if id in('15704','11107'):
                        VTP=CUOI1[:149]
                        CUOI=CUOI1[149:]
                        ELEMENT=[]
                        while True:
                            VT=CUOI[:4]
                            if CUOI==b'': break
                            ELEMENT.append(CUOI[:int.from_bytes(VT,'little')])
                            CUOI=CUOI[int.from_bytes(VT,'little'):]
                        CUOI1=b''
                        for VTC in ELEMENT:
                            VT=VTC[103:111]
                            VT1=VTC[111:121]
                            VT2=VTC[121:167]
                            Cuoi=VTC[int.from_bytes(VTC[167:171],'little')+167:]
                            VTT=VTC[167:int.from_bytes(VTC[167:171],'little')+167]
                            RPL=VTT[4:]
                            RPL=RPL[:5]+id.encode()+b'/'+RPL[5:]
                            RPL=len(b'\x0b\x00\x00\x00\x0b\x00\x00\x00ElementT\x00\x00\x00\x02\x00\x00\x00\r\x00\x00\x00\x06\x00\x00\x00JTCom?\x00\x00\x00\x08\x00\x00\x00TypeAssetRefAnalyser.Pair`2[System.String,System.Int32]\x04\x00\x00\x00'+len(VT+(len(VT1+len(VT2+(len(RPL)+4).to_bytes(4,'little')+RPL).to_bytes(4,'little')+VT2[4:]+(len(RPL)+4).to_bytes(4,'little')+RPL)+8).to_bytes(4,'little')+VT1[4:]+len(VT2+(len(RPL)+4).to_bytes(4,'little')+RPL).to_bytes(4,'little')+VT2[4:]+(len(RPL)+4).to_bytes(4,'little')+RPL+Cuoi).to_bytes(4,'little')+VT[4:]+(len(VT1+len(VT2+(len(RPL)+4).to_bytes(4,'little')+RPL).to_bytes(4,'little')+VT2[4:]+(len(RPL)+4).to_bytes(4,'little')+RPL)+8).to_bytes(4,'little')+VT1[4:]+len(VT2+(len(RPL)+4).to_bytes(4,'little')+RPL).to_bytes(4,'little')+VT2[4:]+(len(RPL)+4).to_bytes(4,'little')+RPL+Cuoi).to_bytes(4,'little')+b'\x0b\x00\x00\x00ElementT\x00\x00\x00\x02\x00\x00\x00\r\x00\x00\x00\x06\x00\x00\x00JTCom?\x00\x00\x00\x08\x00\x00\x00TypeAssetRefAnalyser.Pair`2[System.String,System.Int32]\x04\x00\x00\x00'+len(VT+(len(VT1+len(VT2+(len(RPL)+4).to_bytes(4,'little')+RPL).to_bytes(4,'little')+VT2[4:]+(len(RPL)+4).to_bytes(4,'little')+RPL)+8).to_bytes(4,'little')+VT1[4:]+len(VT2+(len(RPL)+4).to_bytes(4,'little')+RPL).to_bytes(4,'little')+VT2[4:]+(len(RPL)+4).to_bytes(4,'little')+RPL+Cuoi).to_bytes(4,'little')+VT[4:]+(len(VT1+len(VT2+(len(RPL)+4).to_bytes(4,'little')+RPL).to_bytes(4,'little')+VT2[4:]+(len(RPL)+4).to_bytes(4,'little')+RPL)+8).to_bytes(4,'little')+VT1[4:]+len(VT2+(len(RPL)+4).to_bytes(4,'little')+RPL).to_bytes(4,'little')+VT2[4:]+(len(RPL)+4).to_bytes(4,'little')+RPL+Cuoi
                            CUOI1+=RPL
                        CUOI1=VTP[:141]+(len(CUOI1)+8).to_bytes(4,'little')+VTP[145:]+CUOI1
                    CODETONG=len(DAU1[:83]+len((DAU1[83:91]+(len(DAU1[91:183]+len(DAU1[183:]+CODETONG+CUOI1).to_bytes(4,'little')+DAU1[187:]+CODETONG+CUOI1).to_bytes(4,'little')+DAU1[95:183]+len(DAU1[183:]+CODETONG+CUOI1).to_bytes(4,'little')+DAU1[187:]+CODETONG+CUOI1)+VTF)).to_bytes(4,'little')+DAU1[87:91]+(len(DAU1[91:183]+len(DAU1[183:]+CODETONG+CUOI1).to_bytes(4,'little')+DAU1[187:]+CODETONG+CUOI1).to_bytes(4,'little')+DAU1[95:183]+len(DAU1[183:]+CODETONG+CUOI1).to_bytes(4,'little')+DAU1[187:]+CODETONG+CUOI1)+VTF).to_bytes(4,'little')+DAU1[4:83]+len((DAU1[83:91]+(len(DAU1[91:183]+len(DAU1[183:]+CODETONG+CUOI1).to_bytes(4,'little')+DAU1[187:]+CODETONG+CUOI1).to_bytes(4,'little')+DAU1[95:183]+len(DAU1[183:]+CODETONG+CUOI1).to_bytes(4,'little')+DAU1[187:]+CODETONG+CUOI1)+VTF)).to_bytes(4,'little')+DAU1[87:91]+(len(DAU1[91:183]+len(DAU1[183:]+CODETONG+CUOI1).to_bytes(4,'little')+DAU1[187:]+CODETONG+CUOI1).to_bytes(4,'little')+DAU1[95:183]+len(DAU1[183:]+CODETONG+CUOI1).to_bytes(4,'little')+DAU1[187:]+CODETONG+CUOI1)+VTF
                    #with open('kb1.bytes','wb') as f:f.write(CODETONG)
                    with open(fileasset_mod,'wb') as f:f.write(CODETONG)
                    print(f'  [✓] Fix Lag  {os.path.basename(fileasset_mod)}')







            else:
                with open(fileasset_mod,'rb') as f:rpl=f.read();f.close()
                CACHE=[]
                VTR=rpl[rpl.find(b'particlesInFirstLayer')-8:rpl.find(b'particlesInFirstLayer')-4];VTC=rpl[rpl.find(b'particlesInFirstLayer')-8:rpl.find(b'animationsw')-8]
                DAU1=rpl[:rpl.find(b'particlesInFirstLayer')-8]
                VTF=b''
                if rpl.find(b'skinSubset') != -1:
                    VTF=rpl[rpl.find(b'skinSubset')-8:]
                    CUOI1=rpl[rpl.find(b'animationsw')-8:rpl.find(b'skinSubset')-8]
                else:
                    CUOI1=rpl[rpl.find(b'animationsw')-8:]
                while True:
                    if VTC == b'': break
                    CACHE.append(VTC[:int.from_bytes((VTC[:4]),'little')])
                    VTC=VTC[int.from_bytes((VTC[:4]),'little'):]
                CODETONG=b''
                for i in CACHE:
                    VT=i.find(b'Element')-8
                    VTDAU=i[VT-8:VT]
                    DAU=i[:VT-8]
                    VTD=i[VT:]
                    CODE=b''
                    for ig in range(i.count(b'Element')):
                        VTC=VTD[:int.from_bytes((VTD[:4]),'little')]
                        VT=VTC[103:111]
                        VT1=VTC[111:121]
                        VT2=VTC[121:167]
                        Cuoi=VTC[int.from_bytes(VTC[167:171],'little')+167:]
                        VTT=VTC[167:int.from_bytes(VTC[167:171],'little')+167]
                        if VTT.find(id[:3].encode())!= -1:
                            RPL=VTT[4:].replace(b"hero_skill_effects/"+(VTT[(VTT.find(b'/',VTT.find(id[:3].encode())-1))+1:(VTT.find(b'/',VTT.find(id[:3].encode())))]),b"hero_skill_effects/"+(VTT[(VTT.find(b'/',VTT.find(id[:3].encode())-1))+1:(VTT.find(b'/',VTT.find(id[:3].encode())))])+b'/'+id.encode()).replace(b"Hero_Skill_Effects/"+(VTT[(VTT.find(b'/',VTT.find(id[:3].encode())-1))+1:(VTT.find(b'/',VTT.find(id[:3].encode())))]),b"Hero_Skill_Effects/"+(VTT[(VTT.find(b'/',VTT.find(id[:3].encode())-1))+1:(VTT.find(b'/',VTT.find(id[:3].encode())))])+b'/'+id.encode());RPL=RPL.replace(id.encode()+b'/'+id.encode(),id.encode())
                        else:RPL=VTT[4:]
                        RPL=len(b'\x0b\x00\x00\x00\x0b\x00\x00\x00ElementT\x00\x00\x00\x02\x00\x00\x00\r\x00\x00\x00\x06\x00\x00\x00JTCom?\x00\x00\x00\x08\x00\x00\x00TypeAssetRefAnalyser.Pair`2[System.String,System.Int32]\x04\x00\x00\x00'+len(VT+(len(VT1+len(VT2+(len(RPL)+4).to_bytes(4,'little')+RPL).to_bytes(4,'little')+VT2[4:]+(len(RPL)+4).to_bytes(4,'little')+RPL)+8).to_bytes(4,'little')+VT1[4:]+len(VT2+(len(RPL)+4).to_bytes(4,'little')+RPL).to_bytes(4,'little')+VT2[4:]+(len(RPL)+4).to_bytes(4,'little')+RPL+Cuoi).to_bytes(4,'little')+VT[4:]+(len(VT1+len(VT2+(len(RPL)+4).to_bytes(4,'little')+RPL).to_bytes(4,'little')+VT2[4:]+(len(RPL)+4).to_bytes(4,'little')+RPL)+8).to_bytes(4,'little')+VT1[4:]+len(VT2+(len(RPL)+4).to_bytes(4,'little')+RPL).to_bytes(4,'little')+VT2[4:]+(len(RPL)+4).to_bytes(4,'little')+RPL+Cuoi).to_bytes(4,'little')+b'\x0b\x00\x00\x00ElementT\x00\x00\x00\x02\x00\x00\x00\r\x00\x00\x00\x06\x00\x00\x00JTCom?\x00\x00\x00\x08\x00\x00\x00TypeAssetRefAnalyser.Pair`2[System.String,System.Int32]\x04\x00\x00\x00'+len(VT+(len(VT1+len(VT2+(len(RPL)+4).to_bytes(4,'little')+RPL).to_bytes(4,'little')+VT2[4:]+(len(RPL)+4).to_bytes(4,'little')+RPL)+8).to_bytes(4,'little')+VT1[4:]+len(VT2+(len(RPL)+4).to_bytes(4,'little')+RPL).to_bytes(4,'little')+VT2[4:]+(len(RPL)+4).to_bytes(4,'little')+RPL+Cuoi).to_bytes(4,'little')+VT[4:]+(len(VT1+len(VT2+(len(RPL)+4).to_bytes(4,'little')+RPL).to_bytes(4,'little')+VT2[4:]+(len(RPL)+4).to_bytes(4,'little')+RPL)+8).to_bytes(4,'little')+VT1[4:]+len(VT2+(len(RPL)+4).to_bytes(4,'little')+RPL).to_bytes(4,'little')+VT2[4:]+(len(RPL)+4).to_bytes(4,'little')+RPL+Cuoi
                        CODE+=RPL
                        VTD=VTD[int.from_bytes((VTD[:4]),'little'):]
                    CODE=len(DAU+len(CODE+VTDAU).to_bytes(4,'little')+VTDAU[4:]+CODE).to_bytes(4,'little')+DAU[4:]+len(CODE+VTDAU).to_bytes(4,'little')+VTDAU[4:]+CODE;CODETONG+=CODE
                if id in('15704','11107'):
                    VTP=CUOI1[:149]
                    CUOI=CUOI1[149:]
                    ELEMENT=[]
                    while True:
                        VT=CUOI[:4]
                        if CUOI==b'': break
                        ELEMENT.append(CUOI[:int.from_bytes(VT,'little')])
                        CUOI=CUOI[int.from_bytes(VT,'little'):]
                    CUOI1=b''
                    for VTC in ELEMENT:
                        VT=VTC[103:111]
                        VT1=VTC[111:121]
                        VT2=VTC[121:167]#MODLQ
                        Cuoi=VTC[int.from_bytes(VTC[167:171],'little')+167:]
                        VTT=VTC[167:int.from_bytes(VTC[167:171],'little')+167]
                        RPL=VTT[4:]
                        RPL=RPL[:5]+id.encode()+b'/'+RPL[5:]
                        RPL=len(b'\x0b\x00\x00\x00\x0b\x00\x00\x00ElementT\x00\x00\x00\x02\x00\x00\x00\r\x00\x00\x00\x06\x00\x00\x00JTCom?\x00\x00\x00\x08\x00\x00\x00TypeAssetRefAnalyser.Pair`2[System.String,System.Int32]\x04\x00\x00\x00'+len(VT+(len(VT1+len(VT2+(len(RPL)+4).to_bytes(4,'little')+RPL).to_bytes(4,'little')+VT2[4:]+(len(RPL)+4).to_bytes(4,'little')+RPL)+8).to_bytes(4,'little')+VT1[4:]+len(VT2+(len(RPL)+4).to_bytes(4,'little')+RPL).to_bytes(4,'little')+VT2[4:]+(len(RPL)+4).to_bytes(4,'little')+RPL+Cuoi).to_bytes(4,'little')+VT[4:]+(len(VT1+len(VT2+(len(RPL)+4).to_bytes(4,'little')+RPL).to_bytes(4,'little')+VT2[4:]+(len(RPL)+4).to_bytes(4,'little')+RPL)+8).to_bytes(4,'little')+VT1[4:]+len(VT2+(len(RPL)+4).to_bytes(4,'little')+RPL).to_bytes(4,'little')+VT2[4:]+(len(RPL)+4).to_bytes(4,'little')+RPL+Cuoi).to_bytes(4,'little')+b'\x0b\x00\x00\x00ElementT\x00\x00\x00\x02\x00\x00\x00\r\x00\x00\x00\x06\x00\x00\x00JTCom?\x00\x00\x00\x08\x00\x00\x00TypeAssetRefAnalyser.Pair`2[System.String,System.Int32]\x04\x00\x00\x00'+len(VT+(len(VT1+len(VT2+(len(RPL)+4).to_bytes(4,'little')+RPL).to_bytes(4,'little')+VT2[4:]+(len(RPL)+4).to_bytes(4,'little')+RPL)+8).to_bytes(4,'little')+VT1[4:]+len(VT2+(len(RPL)+4).to_bytes(4,'little')+RPL).to_bytes(4,'little')+VT2[4:]+(len(RPL)+4).to_bytes(4,'little')+RPL+Cuoi).to_bytes(4,'little')+VT[4:]+(len(VT1+len(VT2+(len(RPL)+4).to_bytes(4,'little')+RPL).to_bytes(4,'little')+VT2[4:]+(len(RPL)+4).to_bytes(4,'little')+RPL)+8).to_bytes(4,'little')+VT1[4:]+len(VT2+(len(RPL)+4).to_bytes(4,'little')+RPL).to_bytes(4,'little')+VT2[4:]+(len(RPL)+4).to_bytes(4,'little')+RPL+Cuoi
                        CUOI1+=RPL
                    CUOI1=VTP[:141]+(len(CUOI1)+8).to_bytes(4,'little')+VTP[145:]+CUOI1
                CODETONG=len(DAU1[:83]+len((DAU1[83:91]+(len(DAU1[91:183]+len(DAU1[183:]+CODETONG+CUOI1).to_bytes(4,'little')+DAU1[187:]+CODETONG+CUOI1).to_bytes(4,'little')+DAU1[95:183]+len(DAU1[183:]+CODETONG+CUOI1).to_bytes(4,'little')+DAU1[187:]+CODETONG+CUOI1)+VTF)).to_bytes(4,'little')+DAU1[87:91]+(len(DAU1[91:183]+len(DAU1[183:]+CODETONG+CUOI1).to_bytes(4,'little')+DAU1[187:]+CODETONG+CUOI1).to_bytes(4,'little')+DAU1[95:183]+len(DAU1[183:]+CODETONG+CUOI1).to_bytes(4,'little')+DAU1[187:]+CODETONG+CUOI1)+VTF).to_bytes(4,'little')+DAU1[4:83]+len((DAU1[83:91]+(len(DAU1[91:183]+len(DAU1[183:]+CODETONG+CUOI1).to_bytes(4,'little')+DAU1[187:]+CODETONG+CUOI1).to_bytes(4,'little')+DAU1[95:183]+len(DAU1[183:]+CODETONG+CUOI1).to_bytes(4,'little')+DAU1[187:]+CODETONG+CUOI1)+VTF)).to_bytes(4,'little')+DAU1[87:91]+(len(DAU1[91:183]+len(DAU1[183:]+CODETONG+CUOI1).to_bytes(4,'little')+DAU1[187:]+CODETONG+CUOI1).to_bytes(4,'little')+DAU1[95:183]+len(DAU1[183:]+CODETONG+CUOI1).to_bytes(4,'little')+DAU1[187:]+CODETONG+CUOI1)+VTF
                #with open('kb1.bytes','wb') as f:f.write(CODETONG)
                with open(fileasset_mod,'wb') as f:f.write(CODETONG)
                print(f'{os.path.basename(fileasset_mod)}')
                print("-"*53)
                

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
            if skin_id_input == "11620" and sound_file_name in ['BattleBank.bytes', 'HeroSound.bytes', 'LobbyBank.bytes', 'LobbySound.bytes', 'ChatSound.bytes']:
                sound_data = sound_data.replace(b'\x50\x2d', b'\x30\x30')
                sound_data = sound_data.replace(b'\x64\x2d', b'\x30\x30')
                sound_data = sound_data.replace(b'\x15\xbb\x11', b'\x50\x2d\x00').replace(b'\x16\xbb\x11', b'\x50\x2d\x00')

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

            if sound_file_name != "CoupleSound.bytes":
                for skin_id in all_skin_ids:
                    skin_id += b"\x00" * 8
                    sound_data = sound_data.replace(skin_id, b"\x0000" + b"\x00" * 10)
            else:
                for skin_id in all_skin_ids:
                    skin_id += b"\x02\x00\x00\x00\x01"
                    sound_data = sound_data.replace(skin_id, b"\x0000\x00\x00\x02\x00\x00\x00\x01")

            if selected_skin_id in sound_data:
                if sound_file_name != "CoupleSound.bytes":
                    sound_data = sound_data.replace(initial_skin_id + b"\x00" * 8, b"\x0000" + b"\x00" * 10)
                    sound_data = sound_data.replace(selected_skin_id + b"\x00" * 8, initial_skin_id + b"\x00" * 8)
                else:
                    sound_data = sound_data.replace(initial_skin_id + b"\x02\x00\x00\x00\x01", b"\x0000\x00\x00\x02\x00\x00\x00\x01")
                    sound_data = sound_data.replace(selected_skin_id + b"\x02\x00\x00\x00\x01", initial_skin_id + b"\x02\x00\x00\x00\x01")

            with open(os.path.join(sound_directory, sound_file_name), "wb") as sound_file:
                sound_file.write(sound_data)
            print(f"     Sound: {sound_file_name}  Done")
    print(f"{'+ Trạng Thái Mod':<25}")
#----------------------------------------------
    FixNgoaiHinh = 'y'#input('Fix Yes Or No :').lower()
    if FixNgoaiHinh in ['yes', 'y']:
        if IDCHECK not in ["13008", "52007"]:
            with open(file_mod_Character, 'rb') as f:
                Code = f.read()
    
            user_prefix = IDMODSKIN[:3]
            relevant_patterns = []
    
            for i in range(10500, 20000):
                if str(i).startswith(user_prefix):
                    bcode = i.to_bytes(4, 'little')
                    if bcode in Code:
                        relevant_patterns.append(bcode)
    
            for i in range(50100, 60000):
                if str(i).startswith(user_prefix):
                    bcode = i.to_bytes(4, 'little')
                    if bcode in Code:
                        relevant_patterns.append(bcode)
    
            if relevant_patterns:
                first_pattern = relevant_patterns[0]
                pos = Code.find(first_pattern)
                if pos == -1:
                    print(f"[!] Không tìm thấy pattern đầu.")
                else:
                    start = pos - 155
                    full_code = b''
                    temp_code = Code[start:]
                    cursor = 0
    
                    while cursor + 4 < len(temp_code):
                        len_block = int.from_bytes(temp_code[cursor:cursor+4], 'little')
                        block = temp_code[cursor:cursor+len_block+4]
    
                        if all(pat not in block for pat in relevant_patterns):
                            break
    
                        full_code += block
                        cursor += len_block + 4
    
                    if full_code:
                        new_code = Code.replace(full_code, b'')
                        with open(file_mod_Character, 'wb') as f:
                            f.write(new_code)
                        print(f'Fix Mất Ngoại Hình - {IDMODSKIN}')
#----------------------------------------------
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
                    code_content = code_content.replace(b"prefab_skill_effects/hero_skill_effects/133_direnjie/",
                                                          b"prefab_skill_effects/component_effects/13311/13311_5/")
                with open(file, "wb") as f:
                    f.write(code_content)
                break
            modified_codes = []
            buffer_codes = []
            with open(file, "rb") as f:
                begin_content = f.read(140)
                while True:
                    data_length = f.read(2)
                    if data_length == b"":
                         break
                    section_length = data_length[0] + data_length[1] * 256 + 2
                    code_section = data_length + f.read(section_length)
                    if user_id_bytes in code_section:
                         modified_codes.append(code_section)
            for code_section in modified_codes:
                start_index = code_section.find(user_id_bytes) + 6
                end_index = code_section.find(b"/", start_index) + 1
                hero_name = code_section[start_index:end_index]
                code_section = code_section.replace(b"Prefab_Skill_Effects/Hero_Skill_Effects",
                                                      b"prefab_skill_effects/hero_skill_effects")
                code_section = code_section.replace(b"hero_skill_effects/" + hero_name,
                                                      b"hero_skill_effects/" + hero_name + bytes(user_id + "/", "utf"))
                offset = code_section.find(b"prefab_skill_effects") - 4
                length_change = bytes.fromhex(hex(code_section[offset] + len(user_id) + 1)[2:]) + b"\x00" * 3
                code_section = code_section.replace(code_section[offset:offset + 4], length_change)
                target_length = hex(len(code_section) - 4)[2:]
                if len(target_length) == 3:
                    target_length = target_length[1:3] + "0" + target_length[0]
                elif len(target_length) == 2:
                    target_length += "00"
                target_length = bytes.fromhex(target_length)
                code_section = code_section.replace(code_section[0:2], target_length, 1)
                buffer_codes.append(code_section)
            modified_content = open(file, "rb").read()
            for index in range(len(modified_codes)):
                modified_content = modified_content.replace(modified_codes[index], buffer_codes[index], 1)
            with open(file, "wb") as f:
                f.write(modified_content)
    #print('-'*53)
    print(f"    Mod Skill Effect ID: {user_id}")
    if matching_files:
        for file in matching_files:
            print(f"    [-] {os.path.basename(file):<25} Done!")
    else:
        print("    [x] SkillMark Not Found")
#-----------------------------------------------
    AllID=[]
    for i in range(21):
        if i<10: AllID.append(ID[0:3]+"0"+str(i))
        else: AllID.append(ID[0:3]+str(i))
    All_S=[]
    for i in AllID:
        i=hex(int(i))[2:]
        All_S.append(bytes.fromhex(f"{i[2:4]}{i[0:2]}0000"))
    with open(file_mod_Modtion,"rb") as f:
        begin=f.read(140)
        All_Code=[]
        while True:
            SL=f.read(2)
            if SL==b"": 
                f.close()
                break
            SL0=SL[0]+SL[1]*256+2
            Code=SL+f.read(SL0)
            if All_S[AllID.index(ID)] in Code: All_Code.append(Code)
            elif All_S[0] in Code: All_Code.append(Code)
    CodeDB=[]
    CodeMD=[]
    CodeMD2=[]
    for code in All_Code:
        if code[0:2] in b"6\x00S\x00": CodeDB.append(code)
        else:
            CodeMD.append(code)
            CodeMD2.append(code)
    aw=0
    if len(CodeDB)>1:
        print(f"Choose One Or {len(CodeDB)}: ",end="")
        aw=int(input())-1
    if len(CodeDB)>0:
        CodeR=CodeDB[aw]
        idmod=CodeR[21:25]
        for code in CodeMD:
            vtf=CodeMD.index(code)
            for id in All_S:
                vt=code.find(id)
                if vt!=-1:
                    codet=code[vt+4:vt+8]
                    code=code.replace(codet,idmod,1)
                else: break
            CodeMD[vtf]=code
    else:
        for code in CodeMD:
            vtr=CodeMD.index(code)
            vt=code.find(All_S[AllID.index(ID)])
            idmod=code[vt+4:vt+8]
            for id in All_S:
                vt=code.find(id)
                if vt!=-1:
                    codet=code[vt+4:vt+8]
                    code=code.replace(codet,idmod,1)
                else: break
            CodeMD[vtr]=code
    with open(file_mod_Modtion,"rb") as f:
        y=f.read()
        f.close()
    for i in range(len(CodeMD)): y=y.replace(CodeMD2[i],CodeMD[i],1)
    if len(CodeMD)+len(CodeDB)==0:
        for id in All_S: y=y.replace(id,b"00\x00\x00",1)
    with open(file_mod_Modtion,"wb") as f: f.write(y)
    #print("—" * 53)
    print(f"    Mod Motion ID: {IDMODSKIN}")
#-----------------------------------------------
    Files_Directory_Path = f'{FolderMod}/Resources/1.59.1/Ages/Prefab_Characters/Prefab_Hero/mod4/'
    with zipfile.ZipFile('Resources/1.59.1/Ages/Prefab_Characters/Prefab_Hero/Actor_'+f'{IDMODSKIN[:3]}'+'_Actions.pkg.bytes') as File_Zip:
        File_Zip.extractall(Files_Directory_Path)
        File_Zip.close()
    HERO_NAME_LIST = os.listdir(Files_Directory_Path)
    for HERO_NAME_ITEM in HERO_NAME_LIST:
        NAME_HERO = HERO_NAME_ITEM
    if b"Skin_Icon_Skill" in dieukienmod or b"Skin_Icon_BackToTown" in dieukienmod or IDCHECK == "53702":

        new_folder_path = Files_Directory_Path
        new_files_list = os.listdir(new_folder_path)
        NAME_HERO = new_files_list
        effect_name = NAME_HERO
        for new_file_item in new_files_list:
            effect_name = new_file_item
        for name1 in NAME_HERO:
            NAME_HERO = name1
        directory_path = Files_Directory_Path + f'{NAME_HERO}' + '/skill/'

    Id_Skin = IDMODSKIN.encode()
    Name_Hero = NAME_HERO.encode()
    HD = b'n'
    Skins = b'n'

    FILES_XML = []
    for root, dirs, files in os.walk(Files_Directory_Path):
        for file in files:
            if file.endswith('.xml'):
                FILES_XML.append(os.path.join(root, file))

    for file_path in FILES_XML:
        if IDMODSKIN == '52414':
            continue
 
        giai(file_path)

        with open(file_path, 'rb') as f:
            All = f.read()

        if b'"Jg\x00' not in All:
            ListAll = All.split(b'\r\n')
            CODE_EFF = [x for x in ListAll if b'prefab_skill_effects/hero_skill_effects/' in x.lower()]
            if len(CODE_EFF) == 0:
                continue

            for text in CODE_EFF:
                if b'<String name="prefabName"' in text:
                    continue
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
            if IDMODSKIN[:3] == '173':
                with open(file_path, 'rb') as f:
                    rpl = f.read()

                    rpl = re.sub(
                    b'prefab_skill_effects/hero_skill_effects/173_liyuanfang/' + re.escape(IDMODSKIN.encode()) + b'/Liyuanfang_buff01_spell03', b'prefab_skill_effects/hero_skill_effects/173_liyuanfang/Liyuanfang_buff01_spell03', rpl)

                with open(file_path, 'wb') as f:
                    f.write(rpl)
#---------------—------------———----------------
            if IDMODSKIN == '53802':
                with open(file_path, 'rb') as f:
                    rpl = f.read().replace(
                    b'prefab_skill_effects/hero_skill_effects/538_Iggy/53802/Iggy_Spell3_Circle_01_E',
                    b'prefab_skill_effects/hero_skill_effects/538_Iggy/Iggy_Spell3_Circle_01_E')
                with open(file_path, 'wb') as f:
                    f.write(rpl)
#---------------—------------———----------------
            if IDMODSKIN == '11620':
                with open(file_path, 'rb') as f:
                    rpl = f.read()
            
                if phukienb == 'tim':
                    rpl = re.sub(
                        br'prefab_skill_effects/hero_skill_effects/116_Jingke/11620/',
                        b'prefab_skill_effects/Component_Effects/11620/1162001/',
                        rpl, flags=re.IGNORECASE
                    )
                    rpl = re.sub(br'11620/11620_3/', b'11620/1162001/', rpl, flags=re.IGNORECASE)
                    rpl = re.sub(br'11620/1162001/11607/11607_huijidi_01', b'11607/11607_huijidi_01', rpl, flags=re.IGNORECASE)
            
                elif phukienb == 'do':
                    rpl = re.sub(
                        br'prefab_skill_effects/hero_skill_effects/116_Jingke/11620/',
                        b'Prefab_Skill_Effects/Component_Effects/11620/1162002/',
                        rpl, flags=re.IGNORECASE
                    )
                    rpl = re.sub(br'11620/11620_3/', b'11620/1162002/', rpl, flags=re.IGNORECASE)
                    rpl = re.sub(br'11620/1162002/11607/11607_huijidi_01', b'11607/11607_huijidi_01', rpl, flags=re.IGNORECASE)
            
                else:
                    rpl = re.sub(br'prefab_skill_effects/hero_skill_effects/116_Jingke/11620/', 
                                 b'prefab_skill_effects/component_effects/11620/11620_5/', rpl, flags=re.IGNORECASE)
            
                    rpl = re.sub(br'prefab_skill_effects/hero_skill_effects/116_JingKe/11620/11620_5/11607', 
                                 b'prefab_skill_effects/component_effects/11620/11620_5/', rpl, flags=re.IGNORECASE)
            
                    rpl = re.sub(br'11620/11620_3/', b'11620/11620_5/', rpl, flags=re.IGNORECASE)
            
                    rpl = re.sub(br'11620/11620_5/11607/11607_huijidi_01', b'11607/11607_huijidi_01', rpl, flags=re.IGNORECASE)
            
                rpl = re.sub(br'<SkinOrAvatarList id="11620"\s*/>', b'<SkinOrAvatarList id="99999" />', rpl, flags=re.IGNORECASE)
            
                rpl = re.sub(br'SkinAvatarFilterType="9">', b'__TEMP__>', rpl, flags=re.IGNORECASE)
                rpl = re.sub(br'SkinAvatarFilterType="11">', b'SkinAvatarFilterType="9">', rpl, flags=re.IGNORECASE)
                rpl = re.sub(br'__TEMP__>', b'SkinAvatarFilterType="11">', rpl, flags=re.IGNORECASE)
            
                with open(file_path, 'wb') as f:
                    f.write(rpl)
#---------------—------------———----------------
            if IDMODSKIN =='13613' and 'S1E1.xml' in file_path:
                with open(file_path, 'rb') as f: rpl = f.read().replace(b'</Event>\r\n    </Track>\r\n  </Action>\r\n</Project>',b'</Event>\r\n    </Track>\r\n    <Track trackName="Youtuber_Akira_Mod_Skin" eventType="TriggerParticleTick" guid="daa65ca6-798c-4280-84b3-171fc3a73a82" enabled="true" useRefParam="false" refParamName="" r="0.000" g="0.000" b="0.000" execOnForceStopped="false" execOnActionCompleted="false" stopAfterLastEvent="true">\r\n      <Event eventName="TriggerParticleTick" time="0.000" isDuration="false" guid="5f30bc82-d28a-4b25-b3a6-92fc32eac064">\r\n        <TemplateObject name="targetId" objectName="None" id="-1" isTemp="false" refParamName="" useRefParam="false" />\r\n        <TemplateObject name="objectSpaceId" objectName="target" id="1" isTemp="false" refParamName="" useRefParam="false" />\r\n        <String name="resourceName" value="prefab_skill_effects/hero_skill_effects/136_wuzetian/13613/WuZeTian_hurt02" refParamName="" useRefParam="false" />\r\n        <float name="lifeTime" value="0.600" refParamName="" useRefParam="false" />\r\n        <Vector3 name="bindPosOffset" x="0.000" y="1.000" z="0.000" refParamName="" useRefParam="false" />\r\n      </Event>\r\n    </Track>\r\n  </Action>\r\n</Project>')
                with open(file_path,'wb') as f: f.write(rpl)
#---------------—------------———----------------
            if IDMODSKIN =='13613' and 'S1E2.xml' in file_path:
                with open(file_path, 'rb') as f: rpl = f.read().replace(b'</Event>\r\n    </Track>\r\n  </Action>\r\n</Project>',b'</Event>\r\n    </Track>\r\n    <Track trackName="Youtuber_Akira_Mod_Skin" eventType="TriggerParticleTick" guid="daa65ca6-798c-4280-84b3-171fc3a73a82" enabled="true" useRefParam="false" refParamName="" r="0.000" g="0.000" b="0.000" execOnForceStopped="false" execOnActionCompleted="false" stopAfterLastEvent="true">\r\n      <Event eventName="TriggerParticleTick" time="0.000" isDuration="false" guid="5f30bc82-d28a-4b25-b3a6-92fc32eac064">\r\n        <TemplateObject name="targetId" objectName="None" id="-1" isTemp="false" refParamName="" useRefParam="false" />\r\n        <TemplateObject name="objectSpaceId" objectName="target" id="1" isTemp="false" refParamName="" useRefParam="false" />\r\n        <String name="resourceName" value="prefab_skill_effects/hero_skill_effects/136_wuzetian/13613/WuZeTian_hurt02" refParamName="" useRefParam="false" />\r\n        <float name="lifeTime" value="0.600" refParamName="" useRefParam="false" />\r\n        <Vector3 name="bindPosOffset" x="0.000" y="1.000" z="0.000" refParamName="" useRefParam="false" />\r\n      </Event>\r\n    </Track>\r\n  </Action>\r\n</Project>')
                with open(file_path,'wb') as f: f.write(rpl)
#---------------—------------———----------------
            if IDMODSKIN =='13613' and 'S1E3.xml' in file_path:
                with open(file_path, 'rb') as f: rpl = f.read().replace(b'</Event>\r\n    </Track>\r\n  </Action>\r\n</Project>',b'</Event>\r\n    </Track>\r\n    <Track trackName="Youtuber_Akira_Mod_Skin" eventType="TriggerParticleTick" guid="daa65ca6-798c-4280-84b3-171fc3a73a82" enabled="true" useRefParam="false" refParamName="" r="0.000" g="0.000" b="0.000" execOnForceStopped="false" execOnActionCompleted="false" stopAfterLastEvent="true">\r\n      <Event eventName="TriggerParticleTick" time="0.000" isDuration="false" guid="5f30bc82-d28a-4b25-b3a6-92fc32eac064">\r\n        <TemplateObject name="targetId" objectName="None" id="-1" isTemp="false" refParamName="" useRefParam="false" />\r\n        <TemplateObject name="objectSpaceId" objectName="target" id="1" isTemp="false" refParamName="" useRefParam="false" />\r\n        <String name="resourceName" value="prefab_skill_effects/hero_skill_effects/136_wuzetian/13613/WuZeTian_hurt02" refParamName="" useRefParam="false" />\r\n        <float name="lifeTime" value="0.600" refParamName="" useRefParam="false" />\r\n        <Vector3 name="bindPosOffset" x="0.000" y="1.000" z="0.000" refParamName="" useRefParam="false" />\r\n      </Event>\r\n    </Track>\r\n  </Action>\r\n</Project>')

                with open(file_path,'wb') as f: f.write(rpl)
#---------------—------------———----------------
            if IDMODSKIN == '13613' and 'S1B1.xml' in file_path:
                with open(file_path, 'rb') as f: rpl = f.read().replace(b'<Vector3 name="scaling" x="1.300" y="1.000" z="1.000" refParamName="" useRefParam="false" />', b'<Vector3 name="scaling" x="1.000" y="1.000" z="1.000" refParamName="" useRefParam="false" />')
                with open(file_path,'wb') as f: f.write(rpl)
#---------------—------------———----------------
            if IDMODSKIN == '51015':
                with open(file_path, 'rb') as f:
                    rpl = f.read().replace(
                        b'SkinAvatarFilterType="9">', b'SkinAvatarFilterType="8">'
                    ).replace(
                        b'SkinAvatarFilterType="11">', b'SkinAvatarFilterType="9">'
                    ).replace(
                        b'SkinAvatarFilterType="8">', b'SkinAvatarFilterType="11">'
                    ).replace(
                        b'<String name="prefabName" value="Prefab_Skill_Effects/Hero_Skill_Effects/510_Liliana/5101_Fox" refParamName="" useRefParam="false" />',
                        b'<String name="prefabName" value="Prefab_Skill_Effects/Hero_Skill_Effects/510_Liliana/' +
                        IDMODSKIN.encode() + 
                        b'/5101_Fox" refParamName="" useRefParam="false" />'
                    )
            
                with open(file_path,'wb') as f: f.write(rpl)
#---------------—------------———----------------
            if IDMODSKIN[:3] =='510' and 'U11.xml' in file_path:
                with open(file_path, 'rb') as f: rpl = f.read().replace(b'<Track trackName="ChangeActorMeshTick0" eventType="ChangeActorMeshTick" guid="3b065f40-1044-4f90-a2d5-1be4f1a968ee" enabled="false" useRefParam="false" refParamName="" r="0.000" g="0.000" b="0.000" execOnForceStopped="false" execOnActionCompleted="false" stopAfterLastEvent="true">', b'<Track trackName="ChangeActorMeshTick0" eventType="ChangeActorMeshTick" guid="3b065f40-1044-4f90-a2d5-1be4f1a968ee" enabled="true" useRefParam="false" refParamName="" r="0.000" g="0.000" b="0.000" execOnForceStopped="false" execOnActionCompleted="false" stopAfterLastEvent="true">')
                with open(file_path,'wb') as f: f.write(rpl)
#---------------—------------———----------------
            if IDMODSKIN[:3] =='537' and 'S12.xml' in file_path:
                with open(file_path, 'rb') as f:
                    rpl = f.read().replace(b'prefab_skill_effects/hero_skill_effects/537_Trip/Trip_attack_spell01_1prefab_skill_effects/hero_skill_effects/537_Trip/Trip_attack_spell01_1prefab_skill_effects/hero_skill_effects/537_Trip/Trip_attack_spell01_1_S',b'prefab_skill_effects/hero_skill_effects/537_Trip/Trip_attack_spell01_1_S')
                with open(file_path,'wb') as f: f.write(rpl)
            
#---------------—------------———----------------
            if IDMODSKIN == '59802':                                                                 
                with open(file_path, 'rb') as f:
                    rpl = f.read()

                tracks = rpl.split(b"</Track>")
                modified_tracks = []

                for track in tracks:
                    if not track.strip():  
                        continue
                            
                    if b'SpawnObjectDuration0' in track or b'preCreateRandonNumName' in track:
                        modified_tracks.append(track + b"</Track>")
                    else:    
                        if b'SkinAvatarFilterType="9" nameSpace="">' not in track:
                            track = track.replace(b'SkinAvatarFilterType="9">', b'SkinAvatarFilterType="temp">') \
                                                .replace(b'SkinAvatarFilterType="11">', b'SkinAvatarFilterType="9">') \
                                                .replace(b'SkinAvatarFilterType="temp">', b'SkinAvatarFilterType="11">') \
                                                .replace(b'<SkinOrAvatarList id="59802" />', b'<SkinOrAvatarList id="20802" />')

                            modified_tracks.append(track + b"</Track>")  

                rpl = b"".join(modified_tracks)
                if rpl.endswith(b"</Track>"):
                    rpl = rpl[:-8]  

                with open(file_path, 'wb') as f: f.write(rpl)
#---------------—------------———----------------
            if IDMODSKIN =='59702' and 'P1E01.xml' in file_path:
                    with open(file_path, 'rb') as f:
                        rpl = f.read().replace(b'e40d96061260" enabled="true"',b'e40d96061260" enabled="false"')
                    with open(file_path, 'wb') as f:
                        f.write(rpl)
#---------------—------------———----------------
            if IDMODSKIN =='59702' and 'P2.xml'in file_path:
                with open(file_path, 'rb') as f:
                    rpl = f.read().replace(b'prefab_skill_effects/hero_skill_effects/KuangTie_attack02_spell02A_1',b'prefab_skill_effects/hero_skill_effects/597_kuangtie/59702/KuangTie_attack02_spell02A_1')
                with open(file_path, 'wb') as f:
                    f.write(rpl)
#---------------—------------———----------------
            if IDMODSKIN =='59702' and 'U1.xml'in file_path:
                with open(file_path, 'rb') as f:
                    rpl = f.read().replace(b'<String name="prefab" value="prefab_skill_effects/hero_skill_effects/KuangTie_attack_spell03_1" refParamName="" useRefParam="false" />', b'<String name="prefab" value="prefab_skill_effects/hero_skill_effects/597_kuangtie/59702/KuangTie_attack_spell03_1" refParamName="" useRefParam="false" />')
                with open(file_path, 'wb') as f:
                    f.write(rpl)
#---------------—------------———----------------
            if IDMODSKIN =='59702' and 'U11.xml'in file_path:
                with open(file_path, 'rb') as f:
                    rpl = f.read().replace(b'<String name="prefab" value="prefab_skill_effects/hero_skill_effects/KuangTie_attack02_spell03_1" refParamName="" useRefParam="false" />', b'<String name="prefab" value="prefab_skill_effects/hero_skill_effects/597_kuangtie/59702/KuangTie_attack02_spell03_1" refParamName="" useRefParam="false" />')
                with open(file_path, 'wb') as f:
                    f.write(rpl)
#---------------—------------———----------------
            if IDMODSKIN[:3] == '521':
                with open(file_path, 'rb') as f:
                    rpl = f.read()
                if IDMODSKIN != '52108' and any(x in file_path for x in ['S1B3', 'S1B4']):
                    rpl = rpl.replace(b'Florentino_spell01_bullet03_2"', b'Florentino_spell01_bullet03"')
                    rpl = rpl.replace(b'Florentino_spell01_bullet03_fade_2"', b'Florentino_spell01_bullet03_fade"')
                    rpl = rpl.replace(b'Florentino_spell01_bullet03_2_e"', b'Florentino_spell01_bullet03_e"')
                    rpl = rpl.replace(b'Florentino_spell01_buff01_2"', b'Florentino_spell01_buff01"')
                    rpl = rpl.replace(b'Florentino_spell01_bullet03_3"', b'Florentino_spell01_bullet03"')
                    rpl = rpl.replace(b'Florentino_spell01_bullet03_fade_3"', b'Florentino_spell01_bullet03_fade"')
                    rpl = rpl.replace(b'Florentino_spell01_bullet03_3_e"', b'Florentino_spell01_bullet03_e"')
                    rpl = rpl.replace(b'Florentino_spell01_buff01_3"', b'Florentino_spell01_buff01"')
        
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
            if IDMODSKIN[:3] == '540' and 'U1B1.xml' in file_path:
                with open(file_path, 'rb') as f:
                    rpl = f.read().replace(b'<String name="prefabName" value="prefab_skill_effects/hero_skill_effects/540_Bright/5401_Bright_God" refParamName="" useRefParam="false" />',b'<String name="prefabName" value="prefab_skill_effects/hero_skill_effects/540_Bright/'+ IDMODSKIN.encode() + b'/5401_Bright_God" refParamName="" useRefParam="false" />')
                with open(file_path, 'wb') as f:
                    f.write(rpl)
                print('Godd')
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
            if IDMODSKIN =='13015' and 'A4.xml' in file_path:
                with open(file_path, 'rb') as f: rpl = f.read().replace(b'<bool name="useNegateValue" value="true"', b'<bool name="useNegateValue" value="false"')
                with open(file_path,'wb') as f: f.write(rpl)
#---------------—------------———----------------
            if IDMODSKIN == '15015':
                with open(file_path, 'rb') as f:
                    content = f.read()
            
                text = content.decode('utf-8') 
                lines = text.splitlines(keepends=True)
                new_lines = []
                inside_event = False
                should_add_skin = False
            
                for line in lines:
                    stripped = line.strip()
                    new_lines.append(line)
            
                    if '<Event' in stripped:
                        inside_event = True
                        should_add_skin = False
            
                    if inside_event and 'resourceName' in stripped and 'prefab_skill_effects/hero_skill_effects/' in stripped:
                        should_add_skin = True
            
                    if inside_event and '</Event>' in stripped:
                        inside_event = False
                        if should_add_skin:
                            indent = ' ' * (len(line) - len(line.lstrip()))
                            new_lines.append(f'{indent}<SkinOrAvatarList id="15000" />\n')
            
                with open(file_path, 'wb') as f:
                    f.write(''.join(new_lines).encode('utf-8'))

#---------------—------------———----------------
            if IDMODSKIN == '13011':
                with open(file_path, 'rb') as f:
                    rpl = f.read()
            
                if 'S2.xml' in file_path:
                    rpl = re.sub(
                        rb'<String name="resourceName" value="prefab_skill_effects/hero_skill_effects/130_GongBenWuZang/13011/GongBenWuZang_attack01_spell02" refParamName="" useRefParam="false" />',
                        b'<String name="resourceName" value="prefab_skill_effects/hero_skill_effects/130_GongBenWuZang/13011/GongBenWuZang_attack01_spell01" refParamName="" useRefParam="false" />',
                        rpl,
                        flags=re.IGNORECASE
                    )
                if 'S2B1.xml' in file_path:
                    rpl = re.sub(b'prefab_skill_effects/hero_skill_effects/130_gongbenwuzang/13011/gongbenwuzang_attack01_spell01',b'prefab_skill_effects/hero_skill_effects/130_gongbenwuzang/13011/gongbenwuzang_attack01_spell02', rpl , flags=re.IGNORECASE)
                if 'S22.xml' in file_path:
                    rpl = re.sub(
                        rb'<String name="resourceName" value="prefab_skill_effects/hero_skill_effects/130_gongbenwuzang/13011/gongbenwuzang_attack01_spell02" refParamName="" useRefParam="false" />',
                        b'<String name="resourceName" value="prefab_skill_effects/hero_skill_effects/13011/gongbenwuzang_attack01_spell01_2" refParamName="" useRefParam="false" />',
                        rpl,
                        flags=re.IGNORECASE
                    )
                    rpl = re.sub(
                        rb'<String name="resourceName" value="prefab_skill_effects/hero_skill_effects/130_GongBenWuZang/13011/gongbenwuzang_attack01_spell01" refParamName="" useRefParam="false" />',
                        b'<String name="resourceName" value="prefab_skill_effects/hero_skill_effects/130_GongBenWuZang/13011/gongbenwuzang_attack01_spell02" refParamName="" useRefParam="false" />',
                        rpl,
                        flags=re.IGNORECASE
                    )
                if 'S21.xml' in file_path:
                    rpl = re.sub(
                        rb'<String name="resourceName" value="prefab_skill_effects/hero_skill_effects/130_gongbenwuzang/13011/gongbenwuzang_attack01_spell02" refParamName="" useRefParam="false" />',
                        b'<String name="resourceName" value="prefab_skill_effects/hero_skill_effects/130_gongbenwuzang/gongbenwuzang_attack01_spell01_1" refParamName="" useRefParam="false" />',
                        rpl,
                        flags=re.IGNORECASE
                    )
                    rpl = re.sub(
                        rb'<String name="resourceName" value="prefab_skill_effects/hero_skill_effects/130_GongBenWuZang/13011/gongbenwuzang_attack01_spell01" refParamName="" useRefParam="false" />',
                        b'<String name="resourceName" value="prefab_skill_effects/hero_skill_effects/13011/GongBenWuZang_attack01_spell02" refParamName="" useRefParam="false" />',
                        rpl,
                        flags=re.IGNORECASE
                    )
                with open(file_path, 'wb') as f:
                    f.write(rpl)
#---------------—------------———----------------
            if IDCHECK =='13015' and 'A4.xml' in file_path:
                with open(file_path, 'rb') as f:
                    rpl = f.read().replace(b'\n        <bool name="useNegateValue" value="true" refParamName="" useRefParam="false" />',b'')
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
            if IDMODSKIN == '13112' and 'P1E5.xml'in file_path:
                with open(file_path, 'rb') as f: rpl = f.read().replace(b'Bone_Blade',b'Bip001 Prop1').replace(b'Bone_Weapon01',b'Bip001 Prop1')
                with open(file_path,'wb') as f: f.write(rpl)
#---------------—------------———----------------
            if IDMODSKIN == '13111' and 'P1E5.xml'in file_path:
                with open(file_path, 'rb') as f: rpl = f.read().replace(b'Bone_Blade',b'Bone_Weapon01').replace(b'Bip001 Prop1',b'Bone_Weapon01')
                with open(file_path,'wb') as f: f.write(rpl)
#---------------—------------———----------------
            if IDMODSKIN == '13116' and 'P1E5.xml'in file_path:
                with open(file_path, 'rb') as f: rpl = f.read().replace(b'Bone_Blade',b'Bip001 Prop1').replace(b'Bone_Weapon01',b'Bip001 Prop1')
                with open(file_path,'wb') as f: f.write(rpl)
#-----------------------------------------------
            if IDMODSKIN =='52414':
                with open(file_path, 'rb') as f:
                    rpl = f.read()
                rpl = re.sub(rb'SkinAvatarFilterType="9"', b'SkinAvatarFilterType="__TMP__"', rpl, flags=re.IGNORECASE)
                rpl = re.sub(rb'SkinAvatarFilterType="11"', b'SkinAvatarFilterType="9"', rpl, flags=re.IGNORECASE)
                rpl = re.sub(rb'SkinAvatarFilterType="__TMP__"', b'SkinAvatarFilterType="11"', rpl, flags=re.IGNORECASE)
                with open(file_path, 'wb') as f:
                    f.write(rpl)
                if 'S3_1.xml' in file_path:
                    with open(file_path, 'rb') as f: rpl = f.read().replace(b'      </Event>\r\n    </Track>\r\n  </Action>\r\n</Project>',b'      </Event>\r\n      <SkinOrAvatarList id="52414" />\r\n    </Track>\r\n  </Action>\r\n</Project>')
                    with open(file_path,'wb') as f: f.write(rpl)
                if 'Death.xml' in file_path:
                    with open(file_path, 'rb') as f: rpl = f.read().replace(b'52414_Capheny_death_01',b'52414/52414_Capheny_death_01')
                    with open(file_path,'wb') as f: f.write(rpl)
                if 'S2B1.xml' in file_path:
                    with open(file_path, 'rb') as f: rpl = f.read().replace(b'prefab_skill_effects/hero_skill_effects/524_Capheny/52414/Spell2_Ground',b'prefab_skill_effects/hero_skill_effects/524_capheny/spell2_ground')
                    with open(file_path,'wb') as f: f.write(rpl)
                if 'S1E1.xml' in file_path:
                    with open(file_path, 'rb') as f: rpl = f.read().replace(b'prefab_skill_effects/hero_skill_effects/524_Capheny/52414/Atk1_FireRange',b'prefab_skill_effects/hero_skill_effects/524_Capheny/Atk1_FireRange')
                    with open(file_path,'wb') as f: f.write(rpl)
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
#---------------—------------———----------------
            if IDMODSKIN =='15012' and 'U1.xml' in file_path:
                with open(file_path, 'rb') as f: rpl = f.read().replace(b'<String name="prefab" value="prefab_skill_effects/hero_skill_effects/150_Hanxin_spellC_01"',b'<String name="prefab" value="prefab_skill_effects/hero_skill_effects/150_hanxin/15012/150_Hanxin_spellC_01"')
                with open(file_path, 'wb') as f: f.write(rpl)
#-----------------------------------------------
            if IDMODSKIN == '13210' and 'S1B0.xml' in file_path:
                with open(file_path, 'rb') as f:
                    rpl = f.read()
                    rpl=re.sub(b'  </Action>',b'    <Track trackName="TriggerParticle0" eventType="TriggerParticle" guid="228d3c6e-eeda-4ae7-b216-b72ce72bead4" enabled="true" useRefParam="false" refParamName="" r="0.000" g="0.000" b="0.000" execOnForceStopped="false" execOnActionCompleted="false" stopAfterLastEvent="true">\n      <Event eventName="TriggerParticle" time="0.000" length="1.400" isDuration="true" guid="a7f8755e-6d8e-4bdd-adb6-b6bde9fde445">\n        <TemplateObject name="targetId" id="0" objectName="self" isTemp="false" refParamName="" useRefParam="false"/>\n        <String name="resourceName" value="prefab_skill_effects/hero_skill_effects/132_makeboluo/13210/makeboluo_spell01_attack_01" refParamName="" useRefParam="false"/>\n        <String name="resourceName2" value="prefab_skill_effects/hero_skill_effects/132_makeboluo/13210/makeboluo_spell01_attack_02" refParamName="" useRefParam="false"/>\n        <String name="resourceName3" value="prefab_skill_effects/hero_skill_effects/132_makeboluo/13210/makeboluo_spell01_attack_03" refParamName="" useRefParam="false"/>\n        <Vector3i name="scalingInt" x="10000" y="10000" z="10000" refParamName="" useRefParam="false"/>\n        <String name="syncAnimationName" value="" refParamName="" useRefParam="false"/>\n        <String name="customTagName" value="" refParamName="" useRefParam="false"/>\n      </Event>\n    </Track>\n    <Track trackName="TriggerParticle0" eventType="TriggerParticle" guid="6b6641b2-20e8-40af-80c8-c29f0554b059" enabled="true" useRefParam="false" refParamName="" r="0.000" g="0.000" b="0.000" execOnForceStopped="false" execOnActionCompleted="false" stopAfterLastEvent="true">\n      <Event eventName="TriggerParticle" time="0.000" length="1.400" isDuration="true" guid="26cecf35-7e0f-4334-a1cf-2cb702fd027b">\n        <TemplateObject name="targetId" id="0" objectName="self" isTemp="false" refParamName="" useRefParam="false"/>\n        <TemplateObject name="objectSpaceId" id="0" objectName="self" isTemp="false" refParamName="" useRefParam="false"/>\n        <String name="resourceName" value="prefab_skill_effects/hero_skill_effects/132_makeboluo/13210/makeboluo_spell01_attack_01_1" refParamName="" useRefParam="false"/>\n        <String name="resourceName2" value="prefab_skill_effects/hero_skill_effects/132_makeboluo/13210/makeboluo_spell01_attack_02_1" refParamName="" useRefParam="false"/>\n        <String name="resourceName3" value="prefab_skill_effects/hero_skill_effects/132_makeboluo/13210/makeboluo_spell01_attack_03_1" refParamName="" useRefParam="false"/>\n        <Vector3i name="scalingInt" x="10000" y="10000" z="10000" refParamName="" useRefParam="false"/>\n        <String name="syncAnimationName" value="" refParamName="" useRefParam="false"/>\n        <String name="customTagName" value="" refParamName="" useRefParam="false"/>\n      </Event>\n    </Track>\n  </Action>', rpl)
                with open(file_path, 'wb') as f:
                    f.write(rpl)
#-----------------------------------------------
            if IDMODSKIN == '13210' and 'S1B1.xml' in file_path:
                with open(file_path, 'rb') as f:
                    rpl = f.read()
                    rpl=re.sub(b'  </Action>',b'    <Track trackName="TriggerParticle6" eventType="TriggerParticle" guid="8ba07821-7778-46ad-95fa-eb22bce26e43" enabled="true" useRefParam="false" refParamName="" r="0.000" g="0.000" b="0.000" execOnForceStopped="false" execOnActionCompleted="false" stopAfterLastEvent="true">\n      <Event eventName="TriggerParticle" time="0.000" length="0.700" isDuration="true" guid="3d864e81-f177-4162-87c4-1ec5400aea0e">\n        <TemplateObject name="targetId" id="2" objectName="bullet" isTemp="true" refParamName="" useRefParam="false"/>\n        <String name="resourceName" value="prefab_skill_effects/hero_skill_effects/132_makeboluo/13210/makeboluo_spell01_bullet_01" refParamName="" useRefParam="false"/>\n        <String name="resourceName2" value="prefab_skill_effects/hero_skill_effects/132_makeboluo/13210/makeboluo_spell01_bullet_02" refParamName="" useRefParam="false"/>\n        <String name="resourceName3" value="prefab_skill_effects/hero_skill_effects/132_makeboluo/13210/makeboluo_spell01_bullet_03" refParamName="" useRefParam="false"/>\n        <Vector3i name="scalingInt" x="10000" y="10000" z="10000" refParamName="" useRefParam="false"/>\n        <String name="syncAnimationName" value="" refParamName="" useRefParam="false"/>\n        <String name="customTagName" value="" refParamName="" useRefParam="false"/>\n      </Event>\n    </Track>\n  </Action>', rpl)
                with open(file_path, 'wb') as f:
                    f.write(rpl)
#-----------------------------------------------
            if IDMODSKIN == '13210' and 'S1E1.xml' in file_path:
                with open(file_path, 'rb') as f:
                    rpl = f.read()
                    rpl=re.sub(b'  </Action>',b'\r\n    <Track trackName="TriggerParticleTick0" eventType="TriggerParticleTick" guid="98e5ab03-00d2-4e55-9f5a-fd4456a00b8e" enabled="true" useRefParam="false" refParamName="" r="0.000" g="0.000" b="0.000" execOnForceStopped="false" execOnActionCompleted="false" stopAfterLastEvent="true">\r\n      <Event eventName="TriggerParticleTick" time="0.000" isDuration="false" guid="e8bf2bdb-8df6-4251-b074-9894c4947f58">\r\n        <TemplateObject name="targetId" id="-1" objectName="None" isTemp="false" refParamName="" useRefParam="false"/>\r\n        <TemplateObject name="objectSpaceId" id="1" objectName="target" isTemp="false" refParamName="" useRefParam="false"/>\r\n        <bool name="bForceShowParticle" value="true" refParamName="" useRefParam="false"/>\r\n        <String name="resourceName" value="prefab_skill_effects/hero_skill_effects/132_makeboluo/13210/makeboluo_spell01_hurt_01" refParamName="" useRefParam="false"/>\r\n        <String name="resourceName2" value="prefab_skill_effects/hero_skill_effects/132_makeboluo/13210/makeboluo_spell01_hurt_02" refParamName="" useRefParam="false"/>\r\n        <String name="resourceName3" value="prefab_skill_effects/hero_skill_effects/132_makeboluo/13210/makeboluo_spell01_hurt_03" refParamName="" useRefParam="false"/>\r\n        <float name="lifeTime" value="0.600" refParamName="" useRefParam="false"/>\r\n        <Vector3 name="bindPosOffset" x="0.000" y="1.000" z="0.000" refParamName="" useRefParam="false"/>\r\n        <Vector3i name="scalingInt" x="10000" y="10000" z="10000" refParamName="" useRefParam="false"/>\r\n        <TemplateObject name="lookTargetId" id="0" objectName="self" isTemp="false" refParamName="" useRefParam="false"/>\r\n        <bool name="bOnlyFollowPos" value="true" refParamName="" useRefParam="false"/>\r\n      </Event>\r\n    </Track>\r\n  </Action>', rpl)
                with open(file_path, 'wb') as f:
                    f.write(rpl)
#---------------—------------———----------------
            if IDMODSKIN == '13210' and 'S11B0.xml' in file_path:
                with open(file_path, 'rb') as f:
                    rpl = f.read()
                    rpl=re.sub(b'  </Action>',b'    <Track trackName="TriggerParticle0" eventType="TriggerParticle" guid="228d3c6e-eeda-4ae7-b216-b72ce72bead4" enabled="true" useRefParam="false" refParamName="" r="0.000" g="0.000" b="0.000" execOnForceStopped="false" execOnActionCompleted="false" stopAfterLastEvent="true">\r\n      <Event eventName="TriggerParticle" time="0.000" length="1.400" isDuration="true" guid="a7f8755e-6d8e-4bdd-adb6-b6bde9fde445">\r\n        <TemplateObject name="targetId" id="0" objectName="self" isTemp="false" refParamName="" useRefParam="false"/>\r\n        <String name="resourceName" value="prefab_skill_effects/hero_skill_effects/132_makeboluo/13210/makeboluo_spell01_attack_01" refParamName="" useRefParam="false"/>\r\n        <String name="resourceName2" value="prefab_skill_effects/hero_skill_effects/132_makeboluo/13210/makeboluo_spell01_attack_02" refParamName="" useRefParam="false"/>\r\n        <String name="resourceName3" value="prefab_skill_effects/hero_skill_effects/132_makeboluo/13210/makeboluo_spell01_attack_03" refParamName="" useRefParam="false"/>\r\n        <Vector3i name="scalingInt" x="10000" y="10000" z="10000" refParamName="" useRefParam="false"/>\r\n        <String name="syncAnimationName" value="" refParamName="" useRefParam="false"/>\r\n        <String name="customTagName" value="" refParamName="" useRefParam="false"/>\r\n      </Event>\r\n    </Track>\r\n    <Track trackName="TriggerParticle0" eventType="TriggerParticle" guid="6b6641b2-20e8-40af-80c8-c29f0554b059" enabled="true" useRefParam="false" refParamName="" r="0.000" g="0.000" b="0.000" execOnForceStopped="false" execOnActionCompleted="false" stopAfterLastEvent="true">\r\n      <Event eventName="TriggerParticle" time="0.000" length="1.400" isDuration="true" guid="26cecf35-7e0f-4334-a1cf-2cb702fd027b">\r\n        <TemplateObject name="targetId" id="0" objectName="self" isTemp="false" refParamName="" useRefParam="false"/>\r\n        <TemplateObject name="objectSpaceId" id="0" objectName="self" isTemp="false" refParamName="" useRefParam="false"/>\r\n        <String name="resourceName" value="prefab_skill_effects/hero_skill_effects/132_makeboluo/13210/makeboluo_spell01_attack_01_1" refParamName="" useRefParam="false"/>\r\n        <String name="resourceName2" value="prefab_skill_effects/hero_skill_effects/132_makeboluo/13210/makeboluo_spell01_attack_02_1" refParamName="" useRefParam="false"/>\r\n        <String name="resourceName3" value="prefab_skill_effects/hero_skill_effects/132_makeboluo/13210/makeboluo_spell01_attack_03_1" refParamName="" useRefParam="false"/>\r\n        <Vector3i name="scalingInt" x="10000" y="10000" z="10000" refParamName="" useRefParam="false"/>\r\n        <String name="syncAnimationName" value="" refParamName="" useRefParam="false"/>\r\n        <String name="customTagName" value="" refParamName="" useRefParam="false"/>\r\n      </Event>\r\n    </Track>\r\n  </Action>', rpl)
                with open(file_path, 'wb') as f:
                    f.write(rpl)
#---------------—------------———----------------
            if IDMODSKIN =='13210' and 'S12B0.xml' in file_path:
                with open(file_path, 'rb') as f:
                    rpl = f.read()
                    rpl=re.sub(b'  </Action>',b'    <Track trackName="TriggerParticle0" eventType="TriggerParticle" guid="228d3c6e-eeda-4ae7-b216-b72ce72bead4" enabled="true" useRefParam="false" refParamName="" r="0.000" g="0.000" b="0.000" execOnForceStopped="false" execOnActionCompleted="false" stopAfterLastEvent="true">\r\n      <Event eventName="TriggerParticle" time="0.000" length="1.400" isDuration="true" guid="a7f8755e-6d8e-4bdd-adb6-b6bde9fde445">\r\n        <TemplateObject name="targetId" id="0" objectName="self" isTemp="false" refParamName="" useRefParam="false"/>\r\n        <String name="resourceName" value="prefab_skill_effects/hero_skill_effects/132_makeboluo/13210/makeboluo_spell01_attack_01" refParamName="" useRefParam="false"/>\r\n        <String name="resourceName2" value="prefab_skill_effects/hero_skill_effects/132_makeboluo/13210/makeboluo_spell01_attack_02" refParamName="" useRefParam="false"/>\r\n        <String name="resourceName3" value="prefab_skill_effects/hero_skill_effects/132_makeboluo/13210/makeboluo_spell01_attack_03" refParamName="" useRefParam="false"/>\r\n        <Vector3i name="scalingInt" x="10000" y="10000" z="10000" refParamName="" useRefParam="false"/>\r\n        <String name="syncAnimationName" value="" refParamName="" useRefParam="false"/>\r\n        <String name="customTagName" value="" refParamName="" useRefParam="false"/>\n      </Event>\r\n    </Track>\r\n    <Track trackName="TriggerParticle0" eventType="TriggerParticle" guid="6b6641b2-20e8-40af-80c8-c29f0554b059" enabled="true" useRefParam="false" refParamName="" r="0.000" g="0.000" b="0.000" execOnForceStopped="false" execOnActionCompleted="false" stopAfterLastEvent="true">\r\n      <Event eventName="TriggerParticle" time="0.000" length="1.400" isDuration="true" guid="26cecf35-7e0f-4334-a1cf-2cb702fd027b">\r\n        <TemplateObject name="targetId" id="0" objectName="self" isTemp="false" refParamName="" useRefParam="false"/>\r\n        <TemplateObject name="objectSpaceId" id="0" objectName="self" isTemp="false" refParamName="" useRefParam="false"/>\r\n        <String name="resourceName" value="prefab_skill_effects/hero_skill_effects/132_makeboluo/13210/makeboluo_spell01_attack_01_1" refParamName="" useRefParam="false"/>\r\n        <String name="resourceName2" value="prefab_skill_effects/hero_skill_effects/132_makeboluo/13210/makeboluo_spell01_attack_02_1" refParamName="" useRefParam="false"/>\r\n        <String name="resourceName3" value="prefab_skill_effects/hero_skill_effects/132_makeboluo/13210/makeboluo_spell01_attack_03_1" refParamName="" useRefParam="false"/>\r\n        <Vector3i name="scalingInt" x="10000" y="10000" z="10000" refParamName="" useRefParam="false"/>\r\n        <String name="syncAnimationName" value="" refParamName="" useRefParam="false"/>\r\n        <String name="customTagName" value="" refParamName="" useRefParam="false"/>\r\n      </Event>\r\n    </Track>\r\n  </Action>', rpl)
                with open(file_path, 'wb') as f:
                    f.write(rpl)
#---------------—------------———----------------
            if IDMODSKIN == '52113':
                with open(file_path, 'rb') as f:
                    rpl = f.read()
                    rpl = re.sub(rb'SkinAvatarFilterType="9"', b'SkinAvatarFilterType="__TMP__"', rpl, flags=re.IGNORECASE)
                    rpl = re.sub(rb'SkinAvatarFilterType="11"', b'SkinAvatarFilterType="9"', rpl, flags=re.IGNORECASE)
                    rpl = re.sub(rb'SkinAvatarFilterType="__TMP__"', b'SkinAvatarFilterType="11"', rpl, flags=re.IGNORECASE)
                    rpl = re.sub(b'<String name="prefabName" value="Prefab_Skill_Effects/Hero_Skill_Effects/521_Florentino/52113_Florentino_BianShen" refParamName="" useRefParam="false" />', b'<String name="prefabName" value="Prefab_Skill_Effects/Hero_Skill_Effects/521_Florentino/52113/52113_Florentino_BianShen" refParamName="" useRefParam="false" />', rpl, flags=re.IGNORECASE)
                text = rpl.decode('utf-8')
                lines = text.splitlines()
                new_lines = []
                for line in lines:
                    if '<String name="clipName"' in line:
                        new_lines.append('    <int name="frameRate" value="1.080.000" refParamName="" useRefParam="false" />')
                    new_lines.append(line)
            
                new_text = '\n'.join(new_lines)
                rpl = new_text.encode('utf-8')
            
                with open(file_path, 'wb') as f:
                    f.write(rpl)
    IDNODMODCHECK = ['14111', '13210', '16707', '13011', '52414']
    if IDCHECK not in IDNODMODCHECK:
        directorypath = Files_Directory_Path + f'{NAME_HERO}' + '/skill/'
        files_list = os.listdir(directorypath)
        for filename in files_list:
            filecheck = os.path.join(directorypath, filename)
            with open(filecheck, 'rb') as f:
                All = f.read()
        
            CheckSkinIdTick = (
                '<int name="skinId" value="' + IDMODSKIN + '" refParamName="" useRefParam="false" />'
            ).encode()
        
            CheckSkinIdTick0 = (
                '<int name="skinId" value="' + IDMODSKIN[:3] + '00' + '" refParamName="" useRefParam="false" />'
            ).encode()
        
            if CheckSkinIdTick in All:
                All = All.replace(CheckSkinIdTick, CheckSkinIdTick0)
                print(f'    Đã sửa CheckSkinIdTick trong: {os.path.basename(filecheck)}')
        
            FixSkinAvatar = ('<SkinOrAvatarList id="' + IDMODSKIN + '" />').encode()
            FixSkinAvatar1 = ('<SkinOrAvatarList id="' + IDMODSKIN[:3] + '00" />').encode()
        
            if FixSkinAvatar in All:
                All = All.replace(FixSkinAvatar, FixSkinAvatar1)
                print(f'   Đã sửa FixSkinAvatar trong: {os.path.basename(filecheck)}')
            with open(filecheck, 'wb') as f:
                f.write(All)
    # fix skin
    if IDMODSKIN == '52414':
        codecheck = Files_Directory_Path + f'{NAME_HERO}' + '/skill/'
        for file in os.listdir(codecheck):
            file_path = os.path.join(codecheck, file)
            if file in ['A1E1.xml','A1E3.xml','A2B1.xml','A2B1_1.xml','A2B2.xml','A2E1.xml','A2E14.xml',
                        'S1.xml','S1_1.xml','S1E2.xml','S2.xml','S3B2.xml','S3B1.xml','S3_1.xml',
                        'S14E1.xml','S14E3.xml','S14E4.xml','S14E5.xml','S14E6.xml']:
                with open(file_path, 'rb') as f:
                    strin = f.read()
                    if b'<SkinOrAvatarList id="52400" />' not in strin:  # tránh thêm trùng
                        strin = strin.replace(
                            b'\r\n      <SkinOrAvatarList id="52414" />',
                            b'\r\n      <SkinOrAvatarList id="23714" />'
                        )
                with open(file_path, 'wb') as f:
                    f.write(strin)
        AddGetHolidayResourcePath(directory_path)

#-----------------------------------------------
    if IDCHECK == '53002' or b"Skin_Icon_SoundEffect" in dieukienmod or b"Skin_Icon_Dialogue" in dieukienmod:
        if IDCHECK not in ["13311", "16707"]:
            directory_path = Files_Directory_Path + f'{NAME_HERO}' + '/skill/'
            IDSOUND_S = IDMODSKIN
        
            if IDSOUND_S[3:4] == '0':
                IDSOUND_S = IDSOUND_S[:3] + IDSOUND_S[4:]
        
            IDSOUND1 = IDSOUND_S[3:]
            IDSOUND12 = IDSOUND1.encode()
            IDSOUND = b"_Skin" + IDSOUND12
        
            for file in os.listdir(directory_path):
                filepath = os.path.join(directory_path, file)
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
                    b = b'<String name="eventName" value="' + code + IDSOUND + b'" refParamName="" useRefParam="false" />'
                    if a in content:
                        content = content.replace(a, b)
                        modified = True
        
                if IDMODSKIN == "11620":
                    if b'_Skin20' in content:
                        content = content.replace(b'_Skin20', b'_Skin20_AW5')
                        modified = True
        
                    if b'11620_3' in content:
                        content = content.replace(b'11620_3', b'11620_5')
                        modified = True
        
                    if b'<SkinOrAvatarList id="11620" />' in content:
                        content = content.replace(
                            b'<SkinOrAvatarList id="11620" />',
                            b'<SkinOrAvatarList id="11600" />'
                        )
                        modified = True
        
                    if 'Skin20E1.xml' in file:
                        content = re.sub(
                            br'(\s*)<SkinOrAvatarList id="11600"\s*/>',
                            b'',
                            content,
                            flags=re.IGNORECASE
                        )
                        modified = True
        
                if modified:
                    with open(filepath, 'wb') as f:
                        f.write(content)
            Track_Guid_Skill(directory_path)

#-----------------------------------------------
    if IDCHECK == '15009':
        for file in ["BlueBuff.xml", "RedBuff_Slow.xml"]:
            duongdan = f"{FolderMod}/Resources/1.59.1/Ages/Prefab_Characters/Prefab_Hero/mod1/PassiveResource/{file}"
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
        Youtuber_Name = f'{FolderMod}/Resources/1.59.1/Ages/Prefab_Characters/Prefab_Hero/mod1/PassiveResource/BlueBuff_CD.xml'
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
    if IDCHECK == "11107" or IDCHECK == "10000":
        with zipfile.ZipFile(f'Resources/1.59.1/Ages/Prefab_Characters/Prefab_Organ_Age.pkg.bytes') as f:
            f.extractall(f'{FolderMod}/Resources/1.59.1/Ages/Prefab_Characters/mod2/')
            TRU1 = (f'{FolderMod}/Resources/1.59.1/Ages/Prefab_Characters/mod2/Prefab_Organ/Crystal/New_BlueCrystal/Skill/')
            TRU2 = (f'{FolderMod}/Resources/1.59.1/Ages/Prefab_Characters/mod2/Prefab_Organ/Crystal/New_RedCrystal/Skill/')
            TRU3 = (f'{FolderMod}/Resources/1.59.1/Ages/Prefab_Characters/mod2/Prefab_Organ/Tower/New_BlueTower/Skill/')
            TRU4 = (f'{FolderMod}/Resources/1.59.1/Ages/Prefab_Characters/mod2/Prefab_Organ/Tower/New_BlueTower_High/Skill/')
            TRU5 = (f'{FolderMod}/Resources/1.59.1/Ages/Prefab_Characters/mod2/Prefab_Organ/Tower/New_RedTower/Skill/')
            TRU6 = (f'{FolderMod}/Resources/1.59.1/Ages/Prefab_Characters/mod2/Prefab_Organ/Tower/New_RedTower_High/Skill/')
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
    if IDCHECK in ("50108","14111","11107","15009","13015","13314"):
        organSkin = "Resources/1.59.1/Databin/Client/Actor/organSkin.bytes"
        organSkin_mod = f"{FolderMod}/Resources/1.59.1/Databin/Client/Actor/organSkin.bytes"
        shutil.copy(organSkin, organSkin_mod)
        giai(organSkin_mod)
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
    if IDCHECK == '13706' or b"Skin_Icon_BackToTown" in dieukienmod or b"Skin_Icon_Animation" in dieukienmod:
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
            if IDMODSKIN in ['11620', '16707', '13311']:
                text = text.replace(
                    '<String name="resourceName" value="" refParamName="strReturnCityFall" useRefParam="true" />',
                    '<String name="resourceName" value="prefab_skill_effects/component_effects/' + NAME_HERO + '/' + IDMODSKIN + '/' + IDMODSKIN + '_5/huijidi_01" refParamName="" useRefParam="false" />'
                )
                text = text.replace(
                    '<String name="resourceName" value="" refParamName="strReturnCityEffectPath" useRefParam="true" />',
                    '<String name="resourceName" value="prefab_skill_effects/component_effects/' + NAME_HERO + '/' + IDMODSKIN + '/' + IDMODSKIN + '_5/huicheng_tongyong_01" refParamName="" useRefParam="false" />'
                )
            
            else:
                text = text.replace(
                    '<String name="resourceName" value="" refParamName="strReturnCityFall" useRefParam="true" />',
                    '<String name="resourceName" value="prefab_skill_effects/hero_skill_effects/' + NAME_HERO + '/' + IDMODSKIN + '/huijidi_01" refParamName="" useRefParam="false" />'
                )
                text = text.replace(
                    '<String name="resourceName" value="" refParamName="strReturnCityEffectPath" useRefParam="true" />',
                    '<String name="resourceName" value="prefab_skill_effects/hero_skill_effects/' + NAME_HERO + '/' + IDMODSKIN + '/huicheng_tongyong_01" refParamName="" useRefParam="false" />'
                )
        
            return '\n'.join([
                '<int name="skinId" value="' + IDMODSKIN[:3] + '00" refParamName="" useRefParam="false" />' if '<int name="skinId"' in line else line
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

        NAME_HERO = next((x for x in os.listdir(Files_Directory_Path) if x.startswith(IDMODSKIN[:3] + "_")), None)
        if not NAME_HERO:
            pass
        else:
            back_path = f'{FolderMod}/Resources/1.59.1/Ages/Prefab_Characters/Prefab_Hero/mod1/commonresource/Back.xml'
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
            # ----- Gan Block------
            with open(back_path, "r", encoding="utf-8") as f:
                target_content = f.read()
            modified_count = 0
            for NAME_HERO in os.listdir(Files_Directory_Path):
                Path_Back = os.path.join(Files_Directory_Path, NAME_HERO, "skill")
                expected_name = f"{IDMODSKIN}_Back.xml".lower()
                matched_file = next((f for f in os.listdir(Path_Back) if f.lower() == expected_name), None)
                if not matched_file:
                    continue

                file_path = os.path.join(Path_Back, matched_file)
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
            # --------SkinOrAvatarList-------
            with open(back_path, 'rb') as f:
                SkinOrAvatarList = f.read()
            
            SkinOrAvatarList = SkinOrAvatarList.replace(
                b'<SkinOrAvatarList id="' + IDMODSKIN.encode() + b'" />',
                b'<SkinOrAvatarList id="' + IDMODSKIN[:3].encode() + b'00" />'
            )
            
            with open(back_path, 'wb') as f:
                f.write(SkinOrAvatarList)

            print("    Back.xml hoàn tất")
#-----------------------------------------------
    for haste_file in ['HasteE1.xml', 'HasteE1_leave.xml']:
        duonggia = f'{FolderMod}/Resources/1.59.1/Ages/Prefab_Characters/Prefab_Hero/mod1/commonresource/{haste_file}'
        giai(duonggia)
        
        if IDCHECK in ['13314', '10611', '11620', '16307', '13210', '15012', '13015', '13011', '19007', '52406', '54402', '18906', '11607', '13613', '52414', '12606', '51015', '13118', '10620', '52011', '11113', '15009', '54307', '13116', '12706', '50112', '15412', '50108', '53703', '14111', '14108', '15710', '12304', '54402'] and IDCHECK != '11620':
            try:
                with open(duonggia, 'r', encoding='utf-8') as f:
                    text = f.read()
            except Exception as e:
                pass
            tracks = re.findall(r'<Track[\s\S]*?</Track>', text)
            
            block_skinid = None
            block_effect = None
            
            for block in tracks:
                if block_skinid is None and re.search(r'name=["\']skinId["\']', block):
                    block_skinid = block
                elif block_effect is None and 'jiasu_tongyong_01' in block:
                    block_effect = block
                if block_skinid and block_effect:
                    break
            
            if not block_skinid or not block_effect:
                exit()
            
            block_skinid = re.sub(
                r'<int name="skinId" value="\d+" refParamName="" useRefParam="false" ?/>',
                f'<int name="skinId" value="{IDMODSKIN[:3]}00" refParamName="" useRefParam="false" />',
                block_skinid
            )
            block_effect = re.sub(r'^\s*<Condition[^>]*?\/>\s*?', '', block_effect, flags=re.MULTILINE)
            block_effect = block_effect.replace(
                'common_effects',
                f'hero_skill_effects/{NAME_HERO}/{IDMODSKIN}'
            )
            if IDMODSKIN == '13314':
                block_effect = block_effect.replace('jiasu_tongyong_01', 'EF_13314_DiRenJie_sprint_loop')
            if IDMODSKIN =='11607':
                block_effect = block_effect.replace('jiaSu_tongyong_01',b'jingke_sprint_01')
            if IDMODSKIN == '15009':
                block_effect = block_effect.replace('jiasu_tongyong_01', 'T2_Spint').replace('        <Vector3 name="bindPosOffset" x="0.000" y="0.700" z="-0.600" refParamName="" useRefParam="false" />','')
            if IDMODSKIN == '15015':
                block_effect = block_effect.replace('jiasu_tongyong_01', '15015_HanXin_sprint_01')
            if IDMODSKIN == '52414':
                block_effect = block_effect.replace('jiasu_tongyong_01','52414_Capheny_sprint_loop')
            if IDMODSKIN == '54307':
                block_effect = block_effect.replace('jiasu_tongyong_01','yao_sprint')
            if IDMODSKIN == '13613':
                block_effect = block_effect.replace('jiasu_tongyong_01', '13613_WuZeTian_sprint')
            if IDMODSKIN == '16307':
                block_effect = block_effect.replace('jiasu_tongyong_01', 'JuYouJing_jiasu_01')
            if IDMODSKIN == '13210':
                if haste_file == 'HasteE1.xml':
                    block_effect = block_effect.replace('jiasu_tongyong_01', 'MaKeBoLuo_Buff_Start')
                elif haste_file == 'HasteE1_leave.xml':
                    block_effect = block_effect.replace('jiasu_tongyong_01', 'MaKeBoLuo_Buff_Start')
            if IDMODSKIN =='14111':
                block_effect = block_effect.replace('JiaSu_tongyong_01','14111_luoer_Sprint').replace('        <Vector3 name="bindPosOffset" x="0.000" y="0.700" z="-0.600" refParamName="" useRefParam="false" />','')
            def count_tracks_above_action_name(duonggia, action_name):
                with open(duonggia, 'r', encoding='utf-8') as file:
                    lines = file.readlines()
                count = 0
                for line in lines:
                    if action_name in line:
                        break
                    if 'trackName' in line:
                        count += 1
                return count
            
            action_name = '</Project>'
            track_count = count_tracks_above_action_name(duonggia, action_name)
            effect_lines = block_effect.splitlines()
            insert_line = f'      <Condition id="{track_count}" guid="{str(uuid.uuid4())}" status="true" />'
            if len(effect_lines) >= 2:
                effect_lines.insert(2, insert_line)
            block_effect = '\n'.join(effect_lines)
            block_ghep = f"  {block_skinid.strip()}\n    {block_effect.strip()}\n"
            if IDMODSKIN == '13210' and haste_file == 'HasteE1.xml':
                with open(duonggia, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                track_count = 0
                for line in lines:
                    if '</Project>' in line:
                        break
                    if 'trackName' in line:
                        track_count += 1
                block_ghep += f'    <Track trackName="TriggerParticle0" eventType="TriggerParticle" guid="{str(uuid.uuid4())}" enabled="true" useRefParam="false" refParamName="" r="0.000" g="0.000" b="0.000" execOnForceStopped="false" execOnActionCompleted="false" stopAfterLastEvent="true">\n      <Condition id="{track_count}" guid="{str(uuid.uuid4())}" status="true"/>\n      <Event eventName="TriggerParticle" time="0.000" length="4.000" isDuration="true" guid="{str(uuid.uuid4())}">\n        <TemplateObject name="targetId" id="1" objectName="target" isTemp="false" refParamName="" useRefParam="false"/>\n        <TemplateObject name="objectSpaceId" id="1" objectName="target" isTemp="false" refParamName="" useRefParam="false"/>\n        <String name="resourceName" value="Prefab_Skill_Effects/Hero_Skill_Effects/132_MaKeBoLuo/13210/MaKeBoLuo_Buff_End" refParamName="" useRefParam="false"/>\n        <Vector3 name="bindPosOffset" x="0.000" y="0.000" z="0.000" refParamName="" useRefParam="false"/>\n        <Vector3i name="scalingInt" x="10000" y="10000" z="10000" refParamName="" useRefParam="false"/>\n        <bool name="bUseTargetSkinEffect" value="true" refParamName="" useRefParam="false"/>\n      </Event>\n    </Track>\n'
            pos = text.find('</Action>')
            if pos == -1:
                pass
            
            text_moi = text[:pos] + block_ghep +'  '+ text[pos:]
            
            with open(duonggia, 'w', encoding='utf-8') as f:
                f.write(text_moi)
            
    print(f"[+] Gia Tốc : Done")
#-----------------------------------------------
    try:
        if IDMODSKIN[:3] in ['150']:
            os.makedirs(f'./{FolderMod}/Resources/1.59.1/Databin/Client/Huanhua/', exist_ok=True)
            shutil.copy(
                "Resources/1.59.1/Databin/Client/Huanhua/ResKillBillboardCfg.bytes",
                f"./{FolderMod}/Resources/1.59.1/Databin/Client/Huanhua/ResKillBillboardCfg.bytes"
            )
            giai(f"./{FolderMod}/Resources/1.59.1/Databin/Client/Huanhua/ResKillBillboardCfg.bytes")
            with open(f"./{FolderMod}/Resources/1.59.1/Databin/Client/Huanhua/ResKillBillboardCfg.bytes", 'rb') as f:
                killboard = f.read()
            if IDMODSKIN in ['15015']:
                killboard=killboard.replace(b'/18/',b'/20/')
            elif IDMODSKIN in ['15012']:
                killboard=killboard.replace(b'\x2C\x00\x00\x00\x10\x00\x00\x00\x1E\x00\x00\x00\x55\x49\x33\x44\x2F\x42\x61\x74\x74\x6C\x65\x2F\x42\x72\x6F\x61\x64\x63\x61\x73\x74\x2F\x31\x36\x2F\x7B\x30\x7D\x2F\x00\x01\x00\x00\x00\x00\x01',b'\x2B\x00\x00\x00\x10\x00\x00\x00\x1D\x00\x00\x00\x55\x49\x33\x44\x2F\x42\x61\x74\x74\x6C\x65\x2F\x42\x72\x6F\x61\x64\x63\x61\x73\x74\x2F\x39\x2F\x7B\x30\x7D\x2F\x00\x01\x00\x00\x00\x00\x01')
            else:
                killboard=killboard.replace(b'/18/',b'/16/')
        with open(f'./{FolderMod}/Resources/1.59.1/Databin/Client/Huanhua/ResKillBillboardCfg.bytes','wb') as f:
            f.write(killboard)
    except Exception as bug:
        pass
#-----------------------------------------------
    if IDMODSKIN == '15710':
        SceneBUFF02 = f'{FolderMod}/Resources/1.59.1/Ages/Prefab_Characters/Prefab_Hero/mod1/commonresource/SceneBUFF02.xml'
        giai(SceneBUFF02)

        remove_lines = [
            '<bool name="bSkipLogicCheck" value="true" refParamName="" useRefParam="false" />',
            '<bool name="bEqual" value="false" refParamName="" useRefParam="false" />'
        ]

        effect = "prefab_skill_effects/common_effects/jiasu_tongyong_01"
        effect = f"prefab_skill_effects/hero_skill_effects/{NAME_HERO}/{IDMODSKIN}/jiasu_tongyong_01"

        with open(SceneBUFF02, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        new_lines = []
        count = 0
        for line in lines:
            line = line.replace("CheckSkinIdTick", "CheckHeroIdTick")
            line = line.replace(f'skinId" value="{IDMODSKIN}"', f'heroId" value="{IDMODSKIN[:3]}"')
            if effect_old in line:
                count += 1
                if count == 2:
                    line = line.replace(effect, effect)
            if line.strip() not in remove_lines:
                new_lines.append(line)

        with open(SceneBUFF02, 'w', encoding='utf-8') as f:
            f.writelines(new_lines)
    Antidec ='n' #input('Antidec :')
    if Antidec == 'y':
        File = Files_Directory_Path + NAME_HERO
        enc(File)
#-----------------------------------------------
    if IDCHECK == "54402":
        giapcuongnoyan = input("\033[1;97m[\033[1;92m?\033[1;97m] SPECIAL: 54402 - MOD EFX GIÁP CUỒNG NỘ YAN Y/n \n[\033[1;92m•\033[1;97m] INPUT: ")
        if giapcuongnoyan.lower() == 'y':	
            with zipfile.ZipFile('Resources/1.59.1/Ages/Prefab_Gear.pkg.bytes') as f:
                f.extractall(f'{FolderMod}/Resources/1.59.1/Ages/mod2/')
                file_path=f'{FolderMod}/Resources/1.59.1/Ages/mod2/Prefab_Gear/Defense/1338E1.xml'
                giai(file_path)
                with open (file_path, 'rb') as f:
                    noidung = f.read()
                    noidung = noidung.replace(b"</Action>", b"""  <Track trackName="CheckHeroIdTick" eventType="CheckHeroIdTick" guid="54402-YanTanJiro" enabled="true" refParamName="" useRefParam="false" r="0.667" g="1.000" b="0.000" execOnForceStopped="false" execOnActionCompleted="false" stopAfterLastEvent="true">\r\n      <Event eventName="CheckHeroIdTick" time="0.000" isDuration="false">\r\n        <TemplateObject name="targetId" objectName="target" id="1" isTemp="false" refParamName="" useRefParam="false"/>\r\n        <int name="heroId" value="544" refParamName="" useRefParam="false"/>\r\n      </Event>\r\n    </Track>\r\n    <Track trackName="TriggerParticle0" eventType="TriggerParticle" guid="54402-YanTanJiro" enabled="true" useRefParam="false" refParamName="" r="0.000" g="0.000" b="0.000" execOnForceStopped="false" execOnActionCompleted="false" stopAfterLastEvent="true" lod="0">\r\n      <Condition id="0" guid="54402-YanTanJiro" status="true" />\r\n      <Event eventName="TriggerParticle" time="0.000" length="2.000" isDuration="true" guid="54402-YanTanJiro">\r\n        <TemplateObject name="targetId" id="0" objectName="self" isTemp="false" refParamName="" useRefParam="false" />\r\n        <TemplateObject name="objectSpaceId" id="0" objectName="self" isTemp="false" refParamName="" useRefParam="false" />\r\n        <String name="resourceName" value="prefab_skill_effects/hero_skill_effects/544_Painter/54402/jiasu_tongyong_01" refParamName="" useRefParam="false" />\r\n        <Vector3 name="bindPosOffset" x="0.000" y="0.700" z="-0.600" refParamName="" useRefParam="false" />\r\n        <Vector3i name="scalingInt" x="10000" y="10000" z="10000" refParamName="" useRefParam="false" />\r\n        <String name="syncAnimationName" value="" refParamName="" useRefParam="false" />\r\n        <String name="customTagName" value="" refParamName="" useRefParam="false" />\r\n      </Event>\r\n    </Track>\r\n  </Action>""")
                with open (file_path,'wb') as f : f.write(noidung)          
                  
                try:
                    folder_path = f'{FolderMod}/Resources/1.59.1/Ages/mod2/'
                    output_path = f'{FolderMod}/Resources/1.59.1/Ages/Prefab_Gear.pkg.bytes'
                    zip_folder(folder_path, output_path)
                except Exception as e:
                    print(e)
                shutil.rmtree(f'{FolderMod}/Resources/1.59.1/Ages/mod2/', ignore_errors=True)
#-----------------------------------------------
        if IDCHECK == "13011":
            giapcuongnoyan = 'y'#input("\033[1;97m[\033[1;92m?\033[1;97m] SPECIAL: 54402 - MOD EFX GIÁP CUỒNG NỘ YAN Y/n \n[\033[1;92m•\033[1;97m] INPUT: ")
            if giapcuongnoyan.lower() == 'y':	
                with zipfile.ZipFile('Resources/1.59.1/Ages/Prefab_Gear.pkg.bytes') as f:
                    f.extractall(f'{FolderMod}/Resources/1.59.1/Ages/mod2/')
                    file_path=f'{FolderMod}/Resources/1.59.1/Ages/mod2/Prefab_Gear/Defense/1338E1.xml'
                    giai(file_path)
                    with open (file_path, 'rb') as f:
                        noidung = f.read()
                        noidung = noidung.replace(b"</Action>", b"""  <Track trackName="CheckHeroIdTick" eventType="CheckHeroIdTick" guid="54402-YanTanJiro" enabled="true" refParamName="" useRefParam="false" r="0.667" g="1.000" b="0.000" execOnForceStopped="false" execOnActionCompleted="false" stopAfterLastEvent="true">\r\n      <Event eventName="CheckHeroIdTick" time="0.000" isDuration="false">\r\n        <TemplateObject name="targetId" objectName="target" id="1" isTemp="false" refParamName="" useRefParam="false"/>\r\n        <int name="heroId" value="130" refParamName="" useRefParam="false"/>\r\n      </Event>\r\n    </Track>\r\n    <Track trackName="TriggerParticle0" eventType="TriggerParticle" guid="54402-YanTanJiro" enabled="true" useRefParam="false" refParamName="" r="0.000" g="0.000" b="0.000" execOnForceStopped="false" execOnActionCompleted="false" stopAfterLastEvent="true" lod="0">\r\n      <Condition id="0" guid="54402-YanTanJiro" status="true" />\r\n      <Event eventName="TriggerParticle" time="0.000" length="2.000" isDuration="true" guid="54402-YanTanJiro">\r\n        <TemplateObject name="targetId" id="0" objectName="self" isTemp="false" refParamName="" useRefParam="false" />\r\n        <TemplateObject name="objectSpaceId" id="0" objectName="self" isTemp="false" refParamName="" useRefParam="false" />\r\n        <String name="resourceName" value="prefab_skill_effects/hero_skill_effects/130_GongBenWuZang/13011/jiasu_tongyong_01" refParamName="" useRefParam="false" />\r\n        <Vector3 name="bindPosOffset" x="0.000" y="0.700" z="-0.600" refParamName="" useRefParam="false" />\r\n        <Vector3i name="scalingInt" x="10000" y="10000" z="10000" refParamName="" useRefParam="false" />\r\n        <String name="syncAnimationName" value="" refParamName="" useRefParam="false" />\r\n        <String name="customTagName" value="" refParamName="" useRefParam="false" />\r\n      </Event>\r\n    </Track>\r\n  </Action>""")
                    with open (file_path,'wb') as f : f.write(noidung)          
                      
                    try:
                        folder_path = f'{FolderMod}/Resources/1.59.1/Ages/mod2/'
                        output_path = f'{FolderMod}/Resources/1.59.1/Ages/Prefab_Gear.pkg.bytes'
                        zip_folder(folder_path, output_path)
                    except Exception as e:
                        print(e)
                    shutil.rmtree(f'{FolderMod}/Resources/1.59.1/Ages/mod2/', ignore_errors=True)
#-----------------------------------------------
        if IDCHECK == "19007":
            giapcuongnoyan = 'y'#input("\033[1;97m[\033[1;92m?\033[1;97m] SPECIAL: 54402 - MOD EFX GIÁP CUỒNG NỘ YAN Y/n \n[\033[1;92m•\033[1;97m] INPUT: ")
            if giapcuongnoyan.lower() == 'y':	
                with zipfile.ZipFile('Resources/1.59.1/Ages/Prefab_Gear.pkg.bytes') as f:
                    f.extractall(f'{FolderMod}/Resources/1.59.1/Ages/mod2/')
                    file_path=f'{FolderMod}/Resources/1.59.1/Ages/mod2/Prefab_Gear/Defense/1338E1.xml'
                    giai(file_path)
                    with open (file_path, 'rb') as f:
                        noidung = f.read()
                        noidung = noidung.replace(b"</Action>", b"""  <Track trackName="CheckHeroIdTick" eventType="CheckHeroIdTick" guid="54402-YanTanJiro" enabled="true" refParamName="" useRefParam="false" r="0.667" g="1.000" b="0.000" execOnForceStopped="false" execOnActionCompleted="false" stopAfterLastEvent="true">\r\n      <Event eventName="CheckHeroIdTick" time="0.000" isDuration="false">\r\n        <TemplateObject name="targetId" objectName="target" id="1" isTemp="false" refParamName="" useRefParam="false"/>\r\n        <int name="heroId" value="190" refParamName="" useRefParam="false"/>\r\n      </Event>\r\n    </Track>\r\n    <Track trackName="TriggerParticle0" eventType="TriggerParticle" guid="54402-YanTanJiro" enabled="true" useRefParam="false" refParamName="" r="0.000" g="0.000" b="0.000" execOnForceStopped="false" execOnActionCompleted="false" stopAfterLastEvent="true" lod="0">\r\n      <Condition id="0" guid="54402-YanTanJiro" status="true" />\r\n      <Event eventName="TriggerParticle" time="0.000" length="2.000" isDuration="true" guid="54402-YanTanJiro">\r\n        <TemplateObject name="targetId" id="0" objectName="self" isTemp="false" refParamName="" useRefParam="false" />\r\n        <TemplateObject name="objectSpaceId" id="0" objectName="self" isTemp="false" refParamName="" useRefParam="false" />\r\n        <String name="resourceName" value="prefab_skill_effects/hero_skill_effects/190_ZhuGeLiang/19007/jiasu_tongyong_01" refParamName="" useRefParam="false" />\r\n        <Vector3 name="bindPosOffset" x="0.000" y="0.700" z="-0.600" refParamName="" useRefParam="false" />\r\n        <Vector3i name="scalingInt" x="10000" y="10000" z="10000" refParamName="" useRefParam="false" />\r\n        <String name="syncAnimationName" value="" refParamName="" useRefParam="false" />\r\n        <String name="customTagName" value="" refParamName="" useRefParam="false" />\r\n      </Event>\r\n    </Track>\r\n  </Action>""")
                    with open (file_path,'wb') as f : f.write(noidung)          
                      
                    try:
                        folder_path = f'{FolderMod}/Resources/1.59.1/Ages/mod2/'
                        output_path = f'{FolderMod}/Resources/1.59.1/Ages/Prefab_Gear.pkg.bytes'
                        zip_folder(folder_path, output_path)
                    except Exception as e:
                        print(e)
                    shutil.rmtree(f'{FolderMod}/Resources/1.59.1/Ages/mod2/', ignore_errors=True)
#-----------------------------------------------
        if IDCHECK == "13210":
            giapcuongnoyan =  'y'#input("\033[1;97m[\033[1;92m?\033[1;97m] SPECIAL: 54402 - MOD EFX GIÁP CUỒNG NỘ YAN Y/n \n[\033[1;92m•\033[1;97m] INPUT: ")
            if giapcuongnoyan.lower() == 'y':	
                with zipfile.ZipFile('Resources/1.59.1/Ages/Prefab_Gear.pkg.bytes') as f:
                    f.extractall(f'{FolderMod}/Resources/1.59.1/Ages/mod2/')
                    file_path=f'{FolderMod}/Resources/1.59.1/Ages/mod2/Prefab_Gear/Defense/1338E1.xml'
                    giai(file_path)
                    with open (file_path, 'rb') as f:
                        noidung = f.read()
                        noidung = noidung.replace(b"</Action>", b"""  <Track trackName="CheckHeroIdTick" eventType="CheckHeroIdTick" guid="54402-YanTanJiro" enabled="true" refParamName="" useRefParam="false" r="0.667" g="1.000" b="0.000" execOnForceStopped="false" execOnActionCompleted="false" stopAfterLastEvent="true">\r\n      <Event eventName="CheckHeroIdTick" time="0.000" isDuration="false">\r\n        <TemplateObject name="targetId" objectName="target" id="1" isTemp="false" refParamName="" useRefParam="false"/>\r\n        <int name="heroId" value="132" refParamName="" useRefParam="false"/>\r\n      </Event>\r\n    </Track>\r\n    <Track trackName="TriggerParticle0" eventType="TriggerParticle" guid="54402-YanTanJiro" enabled="true" useRefParam="false" refParamName="" r="0.000" g="0.000" b="0.000" execOnForceStopped="false" execOnActionCompleted="false" stopAfterLastEvent="true" lod="0">\r\n      <Condition id="0" guid="54402-YanTanJiro" status="true" />\r\n      <Event eventName="TriggerParticle" time="0.000" length="2.000" isDuration="true" guid="54402-YanTanJiro">\r\n        <TemplateObject name="targetId" id="0" objectName="self" isTemp="false" refParamName="" useRefParam="false" />\r\n        <TemplateObject name="objectSpaceId" id="0" objectName="self" isTemp="false" refParamName="" useRefParam="false" />\r\n        <String name="resourceName" value="prefab_skill_effects/hero_skill_effects/132_MaKeBoLuo/13210/jiasu_tongyong_01" refParamName="" useRefParam="false" />\r\n        <Vector3 name="bindPosOffset" x="0.000" y="0.700" z="-0.600" refParamName="" useRefParam="false" />\r\n        <Vector3i name="scalingInt" x="10000" y="10000" z="10000" refParamName="" useRefParam="false" />\r\n        <String name="syncAnimationName" value="" refParamName="" useRefParam="false" />\r\n        <String name="customTagName" value="" refParamName="" useRefParam="false" />\r\n      </Event>\r\n    </Track>\r\n  </Action>""")
                    with open (file_path,'wb') as f : f.write(noidung)           
                    try:
                        folder_path = f'{FolderMod}/Resources/1.59.1/Ages/mod2/'
                        output_path = f'{FolderMod}/Resources/1.59.1/Ages/Prefab_Gear.pkg.bytes'
                        zip_folder(folder_path, output_path)
                    except Exception as e:
                        print(e)
                    shutil.rmtree(f'{FolderMod}/Resources/1.59.1/Ages/mod2/', ignore_errors=True)
#-----------------------------------------------
        if IDCHECK == "13210":
            giapcuongnoyan =  'y'#input("\033[1;97m[\033[1;92m?\033[1;97m] SPECIAL: 54402 - MOD EFX GIÁP CUỒNG NỘ YAN Y/n \n[\033[1;92m•\033[1;97m] INPUT: ")
            if giapcuongnoyan.lower() == 'y':	
                with zipfile.ZipFile('Resources/1.59.1/Ages/Prefab_Gear.pkg.bytes') as f:
                    f.extractall(f'{FolderMod}/Resources/1.59.1/Ages/mod2/')
                    file_path=f'{FolderMod}/Resources/1.59.1/Ages/mod2/Prefab_Gear/Defense/1338E1.xml'
                    giai(file_path)
                    with open (file_path, 'rb') as f:
                        noidung = f.read()
                        noidung = noidung.replace(b"</Action>", b"""  <Track trackName="CheckHeroIdTick" eventType="CheckHeroIdTick" guid="54402-YanTanJiro" enabled="true" refParamName="" useRefParam="false" r="0.667" g="1.000" b="0.000" execOnForceStopped="false" execOnActionCompleted="false" stopAfterLastEvent="true">\r\n      <Event eventName="CheckHeroIdTick" time="0.000" isDuration="false">\r\n        <TemplateObject name="targetId" objectName="target" id="1" isTemp="false" refParamName="" useRefParam="false"/>\r\n        <int name="heroId" value="132" refParamName="" useRefParam="false"/>\r\n      </Event>\r\n    </Track>\r\n    <Track trackName="TriggerParticle0" eventType="TriggerParticle" guid="54402-YanTanJiro" enabled="true" useRefParam="false" refParamName="" r="0.000" g="0.000" b="0.000" execOnForceStopped="false" execOnActionCompleted="false" stopAfterLastEvent="true" lod="0">\r\n      <Condition id="0" guid="54402-YanTanJiro" status="true" />\r\n      <Event eventName="TriggerParticle" time="0.000" length="2.000" isDuration="true" guid="54402-YanTanJiro">\r\n        <TemplateObject name="targetId" id="0" objectName="self" isTemp="false" refParamName="" useRefParam="false" />\r\n        <TemplateObject name="objectSpaceId" id="0" objectName="self" isTemp="false" refParamName="" useRefParam="false" />\r\n        <String name="resourceName" value="prefab_skill_effects/hero_skill_effects/157_BuZhiHuoWu/15710/jiasu_tongyong_01" refParamName="" useRefParam="false" />\r\n        <Vector3 name="bindPosOffset" x="0.000" y="0.700" z="-0.600" refParamName="" useRefParam="false" />\r\n        <Vector3i name="scalingInt" x="10000" y="10000" z="10000" refParamName="" useRefParam="false" />\r\n        <String name="syncAnimationName" value="" refParamName="" useRefParam="false" />\r\n        <String name="customTagName" value="" refParamName="" useRefParam="false" />\r\n      </Event>\r\n    </Track>\r\n  </Action>""")
                    with open (file_path,'wb') as f : f.write(noidung)          
                      
                    try:
                        folder_path = f'{FolderMod}/Resources/1.59.1/Ages/mod2/'
                        output_path = f'{FolderMod}/Resources/1.59.1/Ages/Prefab_Gear.pkg.bytes'
                        zip_folder(folder_path, output_path)
                    except Exception as e:
                        print(e)
                    shutil.rmtree(f'{FolderMod}/Resources/1.59.1/Ages/mod2/', ignore_errors=True)
#-----------------------------------------------
    if IDMODSKIN == '59702':
        giapcuongnoyan =  'y'#input("\033[1;97m[\033[1;92m?\033[1;97m] SPECIAL: 54402 - MOD EFX GIÁP CUỒNG NỘ YAN Y/n \n[\033[1;92m•\033[1;97m] INPUT: ")
        if giapcuongnoyan.lower() == 'y':	
            with zipfile.ZipFile('Resources/1.59.1/Ages/Prefab_Gear.pkg.bytes') as f:
                f.extractall(f'{FolderMod}/Resources/1.59.1/Ages/mod2/')
                file_path=f'{FolderMod}/Resources/1.59.1/Ages/mod2/Prefab_Gear/Defense/1338E1.xml'
                giai(file_path)
                with open (file_path, 'rb') as f:
                    noidung = f.read()
                    noidung = noidung.replace(b'</Action>', b'  <Track trackName="CheckHeroIdTick" eventType="CheckHeroIdTick" guid="54402-YanTanJiro" enabled="true" refParamName="" useRefParam="false" r="0.667" g="1.000" b="0.000" execOnForceStopped="false" execOnActionCompleted="false" stopAfterLastEvent="true">\r\n      <Event eventName="CheckHeroIdTick" time="0.000" isDuration="false">\r\n        <TemplateObject name="targetId" objectName="target" id="1" isTemp="false" refParamName="" useRefParam="false"/>\r\n        <int name="heroId" value="597" refParamName="" useRefParam="false"/>\r\n      </Event>\r\n    </Track>\r\n        <Track trackName="TriggerParticle0" eventType="TriggerParticle" guid="3bb07807-0ec8-4d4a-a8fe-385f9e28e4c3" enabled="true" useRefParam="false" refParamName="" r="0.000" g="0.000" b="0.000" execOnForceStopped="false" execOnActionCompleted="false" stopAfterLastEvent="true">\n      <Event eventName="TriggerParticle" time="0.000" length="2.000" isDuration="true" guid="2b3af436-2730-4d8d-bb09-c9c742566e4e">\n        <TemplateObject name="targetId" id="0" objectName="self" isTemp="false" refParamName="" useRefParam="false" />\n        <TemplateObject name="objectSpaceId" id="0" objectName="self" isTemp="false" refParamName="" useRefParam="false" />\n        <String name="resourceName" value="prefab_skill_effects/hero_skill_effects/597_kuangtie/59702/kuangbao_buff_01" refParamName="" useRefParam="false" />\n        <String name="bindPointName" value="Bip001 L Hand" refParamName="" useRefParam="false" />\n        <Vector3i name="scalingInt" x="10000" y="10000" z="10000" refParamName="" useRefParam="false" />\n        <String name="syncAnimationName" value="" refParamName="" useRefParam="false" />\n        <String name="customTagName" value="" refParamName="" useRefParam="false" />\n      <Event>\n    </Track>\n    <Track trackName="TriggerParticle0" eventType="TriggerParticle" guid="ea95a7f5-5cc8-457d-ba3e-11a5e66f1203" enabled="true" useRefParam="false" refParamName="" r="0.000" g="0.000" b="0.000" execOnForceStopped="false" execOnActionCompleted="false" stopAfterLastEvent="true">\n      <Event eventName="TriggerParticle" time="0.000" length="2.000" isDuration="true" guid="018aaa4e-cc46-4269-aaca-595cc79d1b4e">\n        <TemplateObject name="targetId" id="0" objectName="self" isTemp="false" refParamName="" useRefParam="false" />\n        <TemplateObject name="objectSpaceId" id="0" objectName="self" isTemp="false" refParamName="" useRefParam="false" />\n        <String name="resourceName" value="prefab_skill_effects/hero_skill_effects/597_kuangtie/59702/kuangbao_buff_01" refParamName="" useRefParam="false" />\n        <String name="bindPointName" value="Bip001 R Hand" refParamName="" useRefParam="false" />\n        <bool name="dontShowIfNoBindPoint" value="false" refParamName="" useRefParam="true" />\n        <Vector3i name="scalingInt" x="10000" y="10000" z="10000" refParamName="" useRefParam="false" />\n        <String name="syncAnimationName" value="" refParamName="" useRefParam="false" />\n        <String name="customTagName" value="" refParamName="" useRefParam="false" />\r\n      </Event>\r\n    </Track>\r\n  </Action>')
                    with open (file_path,'wb') as f : f.write(noidung)            
                    try:
                        folder_path = f'{FolderMod}/Resources/1.59.1/Ages/mod2/'
                        output_path = f'{FolderMod}/Resources/1.59.1/Ages/Prefab_Gear.pkg.bytes'
                        zip_folder(folder_path, output_path)
                    except Exception as e:
                        print(e)
                    shutil.rmtree(f'{FolderMod}/Resources/1.59.1/Ages/mod2/', ignore_errors=True)
#-----------------------------------------------
    antidec = 'n'#input("ANTI_DECOMP__?: ").strip().lower()
    if antidec == 'y':
        def mahoa(path):
            def is_encoded(data):
                return data.startswith(b"\x22\x4a\x00\xef") or b"\x28\xb5\x2f\xfd" in data

            def add_antidec(data):
                return data if data.endswith(b"ANTI_DECOMP__") else data + b"ANTI_DECOMP__"

            def process_file(filepath):
                try:
                    if not os.path.isfile(filepath):
                        return
                    with open(filepath, "rb") as f:
                        raw = f.read()
                    if is_encoded(raw):
                        return
                    compressed = pyzstd.compress(raw, zstd_dict=pyzstd.ZstdDict(ZSTD_DICT, True))
                    compressed = b"\x22\x4a\x00\xef" + compressed
                    final = add_antidec(compressed)
                    with open(filepath, "wb") as f:
                        f.write(final)
                except Exception as e:
                    pass

            if os.path.isdir(path):
                for root, dirs, files in os.walk(path):
                    for file in files:
                        process_file(os.path.join(root, file))
            else:
                process_file(path)
        mahoa(directory_path)
#-----------------------------------------------
    INFO_MOD = f'{FolderMod}/Resources/1.59.1/Prefab_Characters/mod/'
    with zipfile.ZipFile(f'Resources/1.59.1/Prefab_Characters/Actor_{IDINFO[:3]}_Infos.pkg.bytes') as f:
        f.extractall(INFO_MOD)
        f.close()
    duong_prefab = INFO_MOD + 'Prefab_Hero/'
    name_hero_list = os.listdir(duong_prefab)

    found = False
    for name in name_hero_list:
        path = os.path.join(duong_prefab, name)
        if name.lower().startswith(f"{IDINFO[:3]}_") and os.path.isdir(path):
            files = os.listdir(path)

            actorinfo_file = None
            for f in files:
                if f.lower() == f"{name.lower()}_actorinfo.bytes":
                    actorinfo_file = f
                    break
            if actorinfo_file is None:
                for f in files:
                    if f.lower().endswith('_actorinfo.bytes'):
                        actorinfo_file = f
                        break

            if actorinfo_file:
                newpath = os.path.join(path, actorinfo_file)
                giai(newpath)
                found = True
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
#-----------------------------------------------
    def ArtPrefabLODnew(data):
        a = ab.find(b'\x00ArtPrefabLOD') - 7
        a2 = ab[a:a+4]
        a3 = ab[a:a+5]
        a4 = a3[4:5]  # số 10
        vitri = int.from_bytes(a2, byteorder='little')
        data = ab[a:a+vitri]
        return data

    def ArtPrefabLODExnew(data4):
        a = ab.find(b'\x00ArtPrefabLODEx') - 7
        a2 = ab[a:a+4]
        a3 = ab[a:a+5]
        a4 = a3[4:5]  # số 10
        vitri = int.from_bytes(a2, byteorder='little')
        data4 = ab[a:a+vitri]
        return data4
#-----------------------------------------------
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
#-----------------------------------------------
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
    CodeDayDu=CodeDayDu.replace(b'_LOD2',b'_LOD1').replace(b'_LOD3',b'_LOD1').replace(b'_Show2\x04',b'_Show1\x04').replace(b'_Show3\x04',b'_Show1\x04')
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
    print('   Actor_'+IDINFO[:3]+'_Infos.pkg.bytes'+' Done')
#-----------------------------------------------
    if IDCHECK[:3] == '196' and b"Skin_Icon_Skill" in dieukienmod:
        Directory = f'{FolderMod}/Resources/1.59.1/Prefab_Characters/mod/Prefab_Hero/196_Elsu/196_Elsu_trap_actorinfo.bytes'
        giai(Directory)

        LC = '1'
        process_directory(Directory, LC)

        with open(Directory, 'rb') as code_elsu:
            elsu = code_elsu.read()
            elsu = elsu.replace(
                b'Prefab_Skill_Effects/Hero_Skill_Effects/196_Elsu/BaiLiShouYue_attack02_spell01_LOD',
                b'Prefab_Skill_Effects/Hero_Skill_Effects/196_Elsu/' + IDCHECK.encode() + b'/BaiLiShouYue_attack02_spell01_LOD'
            )

        with open(Directory, 'wb') as f:
            f.write(elsu)

        LC = '2'
        process_directory(Directory, LC)
#-----------------------------------------------
    if IDCHECK == "19015":
        Directory = f'{FolderMod}/Resources/1.59.1/Prefab_Characters/mod/Prefab_Hero/190_ZhuGeLiang/190_ZhuGeLiang_actorinfo.bytes'

        LC = '1'
        process_directory(Directory, LC)
        with open(Directory, 'rb') as code_tulen:
            tulen = code_tulen.read()
            tulen = tulen.replace(
                b'\n  <useMecanim var="String" type="System.Boolean" value="True"/>',
                b''
            )

        with open(Directory, 'wb') as f:
            f.write(tulen)

        LC = '2'
        process_directory(Directory, LC)
    if IDCHECK == '11620':
        player = input('   Phụ Kiện\n   1. Ngân Nguyệt Lưu\n   2. Hồng Quang Chiến Ngọc\n   3. No Component\n >>> ')
        if player == '1':
            Directory = f'{FolderMod}/Resources/1.59.1/Prefab_Characters/mod/Prefab_Hero/116_JingKe/116_JingKe_actorinfo.bytes'
            LC = '1'
            process_directory(Directory, LC)
            with open(Directory, 'rb') as f:
                pk1 = f.read()
                pk1 = pk1.replace(
                    b'AW1', b'AW5').replace(b'<ArtSkinLobbyShowCamera var="String" type="System.String" value="Prefab_Characters/Prefab_Hero/116_JingKe/Awaken/11621_JingKe_AW5_Cam"/>', b'<ArtSkinLobbyShowCamera var="String" type="System.String" value="Prefab_Characters/Prefab_Hero/116_JingKe/Awaken/11621_JingKe_AW5_Cam"/>\n  <ArtSkinLobbyShowMovie var="String" type="System.String" value="Prefab_Characters/Prefab_Hero/116_JingKe/Awaken/11621_JingKe_Movie"/>').replace(b'116_JingKe/11621_JingKe_AW5_LOD', b'116_JingKe/Component/11621_JingKe_RT_3_LOD').replace(b'116_JingKe/11621_JingKe_AW5_Show', b'116_JingKe/Component/11621_JingKe_RT_3_Show')
    
            with open(Directory, 'wb') as f:
                f.write(pk1)
    
            LC = '2'
            process_directory(Directory, LC)
        if player == '2':
            Directory = f'{FolderMod}/Resources/1.59.1/Prefab_Characters/mod/Prefab_Hero/116_JingKe/116_JingKe_actorinfo.bytes'
            LC = '1'
            process_directory(Directory, LC)
            with open(Directory, 'rb') as f:
                pk2 = f.read()
                pk2 = pk2.replace(
                    b'AW1', b'AW5').replace(b'<ArtSkinLobbyShowCamera var="String" type="System.String" value="Prefab_Characters/Prefab_Hero/116_JingKe/Awaken/11621_JingKe_AW5_Cam"/>', b'<ArtSkinLobbyShowCamera var="String" type="System.String" value="Prefab_Characters/Prefab_Hero/116_JingKe/Awaken/11621_JingKe_AW5_Cam"/>\n  <ArtSkinLobbyShowMovie var="String" type="System.String" value="Prefab_Characters/Prefab_Hero/116_JingKe/Awaken/11621_JingKe_Movie"/>').replace(b'116_JingKe/11621_JingKe_AW5_LOD', b'116_JingKe/Component/11621_JingKe_RT_2_LOD').replace(b'116_JingKe/11621_JingKe_AW5_Show', b'116_JingKe/Component/11621_JingKe_RT_2_Show')
    
            with open(Directory, 'wb') as f:
                f.write(pk2)
    
            LC = '2'
            process_directory(Directory, LC)
            
        if player == '3':
            Directory = f'{FolderMod}/Resources/1.59.1/Prefab_Characters/mod/Prefab_Hero/116_JingKe/116_JingKe_actorinfo.bytes'
            LC = '1'
            process_directory(Directory, LC)
            with open(Directory, 'rb') as f:
                nopk = f.read()
                nopk = nopk.replace(
                    b'AW1', b'AW5').replace(b'<ArtSkinLobbyShowCamera var="String" type="System.String" value="Prefab_Characters/Prefab_Hero/116_JingKe/Awaken/11621_JingKe_AW5_Cam"/>', b'<ArtSkinLobbyShowCamera var="String" type="System.String" value="Prefab_Characters/Prefab_Hero/116_JingKe/Awaken/11621_JingKe_AW5_Cam"/>\n  <ArtSkinLobbyShowMovie var="String" type="System.String" value="Prefab_Characters/Prefab_Hero/116_JingKe/Awaken/11621_JingKe_Movie"/>')
    
            with open(Directory, 'wb') as f:
                f.write(nopk)
    
            LC = '2'
            process_directory(Directory, LC)
    if IDCHECK in ['54805','13118']:
        shutil.rmtree(f'{FolderMod}/Resources/1.59.1/Prefab_Characters/mod/')
        idg = IDINFO
        pf = idg[:3]
        ip = f'{FolderMod}/Resources/1.59.1/Prefab_Characters/mod/'
        pkg = f'Resources/1.59.1/Prefab_Characters/Actor_{pf}_Infos.pkg.bytes'
        
        with zipfile.ZipFile(pkg, 'r') as f:
            f.extractall(ip)
        def auto_rename_bytes_xml(folder):
            count = 0
            for root, _, files in os.walk(folder):
                for file in files:
                    old_path = os.path.join(root, file)
        
                    if file.endswith('.bytes'):
                        new_file = file[:-6] + '.xml'
                    elif file.endswith('.xml'):
                        new_file = file[:-4] + '.bytes'
                    else:
                        continue
        
                    new_path = os.path.join(root, new_file)
        
                    if os.path.exists(new_path):
                        continue
        
                    os.rename(old_path, new_path)
                    count += 1
        def is_main(f):
            l = f.lower()
            return (
                l.endswith('_actorinfo.bytes')
                and 'tutorial' not in l
                and 'tutorail' not in l
                and 'xinshou' not in l
                and 'racenpc' not in l
            )
        
        af = None
        for r, _, fs in os.walk(ip):
            vf = [f for f in fs if is_main(f)]
            if vf:
                for f in vf:
                    if f.lower().startswith(idg.lower() + '_'):
                        af = os.path.join(r, f)
                        break
                if not af:
                    af = os.path.join(r, vf[0])
                break
        
        if not af:
            exit()
        
        giai(af)
        giai(f'{FolderMod}/Resources/1.59.1/Prefab_Characters/mod/Prefab_Hero/196_Elsu/196_Elsu_trap_actorinfo.bytes')
        process_directory(af, '1')
        auto_rename_bytes_xml(os.path.dirname(af))
        
        axml = af.replace(".bytes", ".xml")
        if not os.path.exists(axml):
            exit()
        
        if idg == '5486':
            p = f'{FolderMod}/Resources/1.59.1/Prefab_Characters/mod/Prefab_Hero/548_SunCe/548_SunCe_actorinfo.xml'
            with open(p, 'rb') as f:
                b = f.read()
                b = b.replace(b'<useNewMecanim var="String" type="System.Boolean" value="True"/>', b'', 1)
                b = b.replace(b'<oriSkinUseNewMecanim var="String" type="System.Boolean" value="True"/>', b'', 1)
            with open(p, 'wb') as f:
                f.write(b)
    
        def find_skin(txt, sid):
            tg = '<Element var="Com" type="Assets.Scripts.GameLogic.SkinElement">'
            pos = 0
            while True:
                si = txt.find(tg, pos)
                if si == -1:
                    break
                ei, oc = si, 0
                for m in re.finditer(r'<(/?Element\b[^>]*)>', txt[si:]):
                    t = m.group(1)
                    ei = si + m.end()
                    if t.endswith('/'): continue
                    elif t.startswith('/'): oc -= 1
                    else: oc += 1
                    if oc == 0: break
                seg = txt[si:ei]
                if f'/{sid}_' in seg or f'/{sid}' in seg:
                    try:
                        ET.fromstring(f"<Root>{seg}</Root>")
                        return seg
                    except: return None
                pos = ei
            return None
        
        def find_prefab(txt, sid):
            pos = 0
            while True:
                si = txt.find('<ArtPrefabLOD', pos)
                if si == -1: break
                ei = txt.find('<SkinPrefab var="Array" type="Assets.Scripts.GameLogic.SkinElement[]">', si)
                if ei == -1: break
                seg = txt[si:ei]
                print(f"[DEBUG] {seg}")
                if f"/{sid}_" in seg or f"/{sid}" in seg:
                    return seg
                pos = ei + 1
            return None
        
        with open(axml, "r", encoding="utf-8") as f:
            txt = f.read()
        
        new_txt = txt
        src_id = idg
        
        for i in range(1, 31):
            dst_id = f"{pf}{i}"
            if dst_id == src_id:
                continue
            try:
                seg_src = find_prefab(new_txt, src_id) or find_skin(new_txt, src_id)
                seg_dst = find_prefab(new_txt, dst_id) or find_skin(new_txt, dst_id)
                if seg_src and seg_dst:
                    new_txt = new_txt.replace(seg_dst, seg_src)
            except: pass
        
        with open(axml, "w", encoding="utf-8") as f:
            f.write(new_txt)
        
        with open(axml, "rb") as f:
            d = f.read().decode('utf8')
        d = d.replace('<ArtSkinPrefabLOD var="Array" type="System.String[]">', '<ArtPrefabLOD var="Array" type="System.String[]">', 1)
        d = d.replace('</ArtSkinPrefabLOD>', '</ArtPrefabLOD>', 1)
        d = d.replace('<ArtSkinPrefabLODEx', '<ArtPrefabLODEx', 1)
        d = d.replace('</ArtSkinPrefabLODEx>', '</ArtPrefabLODEx>', 1)
        d = d.replace('<ArtSkinLobbyIdleShowLOD var="Array" type="System.String[]">', '<ArtLobbyIdleShowLOD var="Array" type="System.String[]">', 1)
        d = d.replace('</ArtSkinLobbyIdleShowLOD>', '</ArtLobbyIdleShowLOD>', 1)
        d = d.replace('<ArtSkinLobbyShowLOD var="Array" type="System.String[]">', '<ArtLobbyShowLOD var="Array" type="System.String[]">', 1)
        d = d.replace('</ArtSkinLobbyShowLOD>', '</ArtLobbyShowLOD>', 1)
        d = d.replace('<Element var="Com" type="Assets.Scripts.GameLogic.SkinElement">', '', 1)
        d = d.replace('LOD3','LOD1').replace('LOD2','LOD1').replace('Show3','Show1').replace('Show2','Show1')
        d = re.sub(
            r'[ \t]*<ArtSkinLobbyNode var="String" type="System.String" value="Prefab_Characters/Prefab_Hero/531_keera/5312_Keera_Show1_Node"/>\s*\n?',
            '', d, count=1
        )
        d = d.replace('    </Element><SkinPrefab var="Array" type="Assets.Scripts.GameLogic.SkinElement[]">', '  <SkinPrefab var="Array" type="Assets.Scripts.GameLogic.SkinElement[]">')
        
        with open(axml, "w", encoding="utf-8") as f:
            f.write(d)
        print('\t\t'+'Fix Đứng Animation')
        def clean(axml):
            with open(axml, 'r', encoding='utf-8') as f:
                lns = f.readlines()
        
            new = []
            i = 0
            while i < len(lns):
                c = lns[i].strip()
                n = lns[i + 1].strip() if i + 1 < len(lns) else ""
                if c == "</Element>" and (n.startswith('<SkinPrefab') or n.startswith("<CrossFadeTime") or n.startswith("<FallbackSkinId")):
                    i += 1
                    continue
                new.append(lns[i])
                i += 1
        
            with open(axml, 'w', encoding='utf-8') as f:
                f.writelines(new)
        
        clean(axml)
        auto_rename_bytes_xml(os.path.dirname(axml))
        process_directory(af, '2')
    
#-----------------------------------------------
    with zipfile.ZipFile(FolderMod+"/Resources/1.59.1/Prefab_Characters/Actor_"+IDMODSKIN[:3]+"_Infos.pkg.bytes", 'w', zipfile.ZIP_STORED) as z:
        for r, d, f in os.walk(FolderMod+'/Resources/1.59.1/Prefab_Characters/mod/'):
            for file in f:
                p = os.path.join(r, file)
                z.write(p, os.path.relpath(p, FolderMod+'/Resources/1.59.1/Prefab_Characters/mod/'))
        shutil.rmtree(FolderMod+'/Resources/1.59.1/Prefab_Characters/mod/')
    with zipfile.ZipFile(FolderMod+"/Resources/1.59.1/Ages/Prefab_Characters/Prefab_Hero/Actor_"+IDMODSKIN[:3]+"_Actions.pkg.bytes", 'w', zipfile.ZIP_STORED) as z:
        for r, d, f in os.walk(FolderMod+'/Resources/1.59.1/Ages/Prefab_Characters/Prefab_Hero/mod4/'):
            for file in f:
                p = os.path.join(r, file)
                z.write(p, os.path.relpath(p, FolderMod+'/Resources/1.59.1/Ages/Prefab_Characters/Prefab_Hero/mod4/'))
    shutil.rmtree(FolderMod+'/Resources/1.59.1/Ages/Prefab_Characters/Prefab_Hero/mod4/')

mod1_dir = Path(f"{FolderMod}/Resources/1.59.1/Ages/Prefab_Characters/Prefab_Hero/mod1")
with zipfile.ZipFile(mod1_dir.parent / "CommonActions.pkg.bytes", 'w', zipfile.ZIP_STORED) as z:
    [z.write(f, f.relative_to(mod1_dir)) for f in mod1_dir.rglob("*") if f.is_file()]
shutil.rmtree(mod1_dir)
shutil.rmtree("mod5", ignore_errors=True)

#-----------------------------------------------