# https://www.youtube.com/@MMNAOV
from colorama import init, Fore
from os import listdir
from colorama import Fore, Style
import xml.etree.ElementTree as ET
from xml.dom import minidom
import os,zipfile,colorama,shutil,xml.dom.minidom,xml.sax,os,re,shutil,random,getopt,sys,pyzstd,math
from pathlib import Path
with open("ZSTD_DICT.xml", 'rb') as f:
    ZSTD_DICT = f.read()
ZSTD_LEVEL = 17
def giai(a):
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hcd", ["help", "compress", "decompress"])
    except getopt.GetoptError:
        sys.exit(1)
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            sys.exit()
    if not args:
        args = a
        anti = b''
        input_blob = None
        with open(args, "rb") as f:
            if b'"Jg' in f.read():
                return
        with open(args, "rb") as f:
            input_blob = f.read()
        if opts:
            opt, arg = opts[0]
        else:
            pos = input_blob.find(b"\x28\xb5\x2f\xfd")
            if pos != -1:
                opt = "-d"
                input_blob = input_blob[pos:]
            else:
                opt = "-c"
        zstd_mode = None
        try:
            if opt in ("-c", "--compress"):
                zstd_mode = "compress"
                output_blob = bytearray(pyzstd.compress(input_blob, ZSTD_LEVEL, pyzstd.ZstdDict(ZSTD_DICT, True)))
                output_blob[0:0] = len(input_blob).to_bytes(4, byteorder="little", signed=False)
                output_blob[0:0] = b"\x22\x4a\x00\xef"
                new = random.randbytes(0)
                anti += new
            elif opt in ("-d", "--decompress"):
                input_blob = input_blob[input_blob.find(b"\x28\xb5\x2f\xfd"):]
                zstd_mode = "decompress"
                output_blob = pyzstd.decompress(input_blob, pyzstd.ZstdDict(ZSTD_DICT, True))
            output_path = args
            with open(output_path, "wb") as output_file:
                output_file.write(output_blob)
            with open(output_path, "ab") as output_file:
                output_file.write(anti)
        except pyzstd.ZstdError:
            pass
    return
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
            return b"" if isinstance(self.String, bytes) else ""
        R = self.String[:Int]
        self.String = self.String[Int:]
        return R

class Bytes_XML:
    @staticmethod
    def decode(String):
        def get_int(A):
            return int.from_bytes(A.read(4), 'little')
        def get_str(A, pos=None):
            if pos is not None:
                A.seek(pos, 0)
            ofs = get_int(A)
            return A.read(ofs - 4).decode()
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
            nod[myid] = ET.SubElement(root if fid is None else nod[fid], stri, attrib=attr)
            if ite:
                nod[myid].set("value", text1 if text1 else ' ')
            check_four(A)
            chk = sta + ofs - A.tell()
            if chk > 12:
                A.seek(4, 1)
                for _ in range(get_int(A)):
                    get_node(A, myid, A.tell())
            A.seek(sta + ofs, 0)
        def get_attr(A, pos=None):
            if pos is None:
                pos = A.tell()
            ofs = get_int(A)
            type = get_int(A)
            raw = A.read(ofs - 8).decode()
            if type == 5:
                A.seek(pos + ofs, 0)
                return raw[1:]
            elif type == 6:
                A.seek(pos + ofs, 0)
                return {"var": {'JTArr': 'Array', 'JTPri': 'String'}.get(raw[:5], raw[2:]) if raw[:2] == 'JT' else raw}
            elif type == 8:
                A.seek(pos + ofs, 0)
                return {"type": raw[4:] if raw[:4] == 'Type' else raw}
            else:
                A.seek(pos + ofs, 0)
                return {"raw": raw}
        def check_four(A):
            if get_int(A) != 4:
                A.seek(-4, 1)
        A = StringBytes(String)
        global i, nod, root
        i, nod = 0, {}
        ofs = get_int(A)
        stri = get_str(A)
        A.seek(4, 1)
        aidx = get_int(A)
        attr, ite = {}, False
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
        if ofs - A.tell() > 12:
            A.seek(4, 1)
            for _ in range(get_int(A)):
                get_node(A, None, A.tell())
        try:
            return minidom.parseString(ET.tostring(root, "utf-8").decode()).toprettyxml(indent="  ", newl="\r\n").encode()
        except:
            return ET.tostring(root, "utf-8").decode().encode()

    @staticmethod
    def encode(xmlfile):
        def byteint(num): return num.to_bytes(4, 'little')
        def bytestr(s): return byteint(len(s) + 4) + s.encode()
        def byteattr(k, a):
            if k == 'var':
                stri, aid = {'Array': 'JTArr', 'String': 'JTPri'}.get(a[k], 'JT' + a[k]), 6
            elif k == 'var_Raw': stri, aid = a[k], 6
            elif k == 'type': stri, aid = 'Type' + a[k], 8
            elif k == 'type_Raw': stri, aid = a[k], 8
            elif k == 'value': return b""
            else: stri, aid = a[k], int(k)
            return byteint(len(stri.encode()) + 8) + byteint(aid) + stri.encode()
        def bytenode(n):
            name = bytestr(n.tag)
            attr = b''.join(byteattr(k, n.attrib) for k in n.attrib if k != "value")
            plus, iftex = 8, False
            if "value" in n.attrib and n.attrib["value"].strip() != "":
                v = '' if n.attrib["value"] == ' ' else n.attrib["value"]
                attr += byteint(len(v.encode()) + 9) + byteint(5) + b'V' + v.encode() + byteint(4)
                plus += 4
            attr = byteint(len(attr) + plus) + byteint(len(n.attrib)) + attr + byteint(4)
            children = b''.join(bytenode(c) for c in n)
            if children:
                children = byteint(len(children) + 8) + byteint(len(n)) + children
            else:
                children = byteint(4)
            bnode = name + attr + children
            return byteint(len(bnode) + 4) + bnode
        root = ET.fromstring(xmlfile)
        return bytenode(root)

def process_file(file_path_FL, LC):
    with open(file_path_FL, "rb") as f:
        G = f.read()
    with open(file_path_FL, "wb") as f1:
        try:
            if LC == "1":
                f1.write(Bytes_XML.decode(G))
            elif LC == "2":
                f1.write(Bytes_XML.encode(G.decode()))
        except Exception:
            pass

def process_directory(file_path_FL, LC):
    process_file(file_path_FL, LC)


def extract_name_hero(id_hero):
    source_folder = "Resources/1.58.1/Ages/Prefab_Characters/Prefab_Hero/"
    actor_file_prefix = f"Actor_{id_hero[:3]}_Actions.pkg.bytes"
    actor_file_path = os.path.join(source_folder, actor_file_prefix)
    if not os.path.exists(actor_file_path):
        print(f"Không tìm thấy tệp '{actor_file_prefix}' trong '{source_folder}'.")
        return None
    extracted_folder = os.path.join(source_folder, f"Extracted_{id_hero}")
    try:
        with zipfile.ZipFile(actor_file_path, 'r') as zip_ref:
            zip_ref.extractall(extracted_folder)
        extracted_items = os.listdir(extracted_folder)
        if not extracted_items:
            print(f"Thư mục '{extracted_folder}' trống.")
            return None
        name_hero = extracted_items[0]
        return name_hero
    except FileNotFoundError:
        print("Không tìm thấy file, vui lòng kiểm tra đường dẫn!")
        return None
    except zipfile.BadZipFile:
        print("Tệp nén bị lỗi, không thể giải nén.")
        return None
    finally:
        if os.path.exists(extracted_folder):
            shutil.rmtree(extracted_folder)
def chuan_hoa_skin_id(skin_id):
    # Tách phần prefix và suffix
    id_prefix = skin_id[:-2]  # Lấy tất cả các chữ số ngoại trừ 2 chữ số cuối
    id_suffix = int(skin_id[-2:])  # Lấy 2 chữ số cuối và chuyển thành số

    # Nếu suffix từ 00 đến 08, bỏ số 0 và cộng 1
    if id_suffix < 9:
        new_suffix = id_suffix + 1
        new_id = id_prefix + str(new_suffix)
    else:
        # Nếu không phải, cộng thêm 1 vào toàn bộ ID
        new_id = str(int(skin_id) + 1)

    return new_id

# Đọc các ID từ file Input_Id.txt
with open('Input_Id.txt', 'r', encoding='utf-8') as f:
    id_list = [line.strip() for line in f if line.strip()]

# Xử lý mỗi ID và in ra kết quả
for skin_id in id_list:
    new_skin_id = chuan_hoa_skin_id(skin_id)
    print(f'{skin_id} → {new_skin_id}')
    
    # Cập nhật giá trị cho IDINFO và IDCHECK
    IDINFO = new_skin_id
    IDCHECK = IDINFO
    print(f'IDINFO: {IDINFO}, IDCHECK: {IDCHECK}')
NAME_HERO = extract_name_hero(IDINFO)
if NAME_HERO is None:
    exit("Không thể lấy NAME_HERO, dừng chương trình.")
INFO_MOD = 'Files_Mod/Resources/1.58.1/Prefab_Characters/mod/'
zip_path = f'Resources/1.58.1/Prefab_Characters/Actor_{IDINFO[:3]}_Infos.pkg.bytes'
with zipfile.ZipFile(zip_path) as f:
    f.extractall(INFO_MOD)
đuongan = os.path.join(INFO_MOD, 'Prefab_Hero', NAME_HERO)
all_files = os.listdir(đuongan)
for f in all_files:
    if f.lower() == f'{NAME_HERO.lower()}_actorinfo.bytes':
        newpath = os.path.join(đuongan, f)
        break
else:
    print("Không tìm thấy file actorinfo phù hợp.")
    exit()
giai(newpath)
def skincanmod(data):
    trc1=r.find(timtrc,r.find(b'SkinPrefabG'))
    vt1=r.find(b'JTCom0',trc1-300)
    a1=r[vt1-31:]
    a3=vt1 - 31
    skin1=a1[:4]
    skin2=int.from_bytes(skin1,byteorder='little')
    data=r[a3:a3+skin2]
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
#=========================================================================================================================                        
if new1.find(b'prefab_skill_effects/hero_skill_effects/')!= -1:
    FIND=new1.find(b'PreloadAnimatorEffects')-8
    VT1=new1[FIND:FIND+4]
    VTR=int.from_bytes(VT1,byteorder='little')
    VTM=new1[FIND:FIND+VTR]
    VTM9=VTM
    VTM=(VTR+12).to_bytes(4,byteorder='little')+VTM[4:]
    ELe=VTM.find(b'Element')-8
    ELe1=VTM.find(b'Element')-16
    VTRCM=VTM[:ELe-8]
    DAU=VTM[ELe:ELe+4]
    VTR=int.from_bytes(DAU,byteorder='little')
    VTM1=VTM[ELe:ELe+VTR]
    VTM1=(VTR+6).to_bytes(4,byteorder='little')+VTM1[4:]
    VTCUOI=VTM[ELe:]
    VTCUOI1=VTM[ELe1:ELe1+8]
    tinh=VTM.count(b'Element')
    VTM=VTCUOI
    KB=0
    CODEFULL=b''
#=========================================================================================================================                        
    for i in range(tinh):
        ELe=VTM.find(b'Element')-8
        DAU=VTM[ELe:ELe+4]
        VTR=int.from_bytes(DAU,byteorder='little')
        VTM1=VTM[ELe:ELe+VTR]
        if VTM1.find(b'Vprefab_skill_effects/hero_skill_effects/') == -1:
            CODEFULL+=VTM1
            break
        VTM1=(VTR+6).to_bytes(4,byteorder='little')+VTM1[4:]
        VTCUOI=VTM[VTR:]
        ELe1=VTM.find(b'Element')+7
        DAU1=VTM[ELe1:ELe1+4]
        VTR=int.from_bytes(DAU1,byteorder='little')
        VTM2=VTM[ELe1:ELe1+VTR]
        VTM2=(VTR+6).to_bytes(4,byteorder='little')+VTM2[4:]
        newvt=VTM1.find(b'Vprefab_skill_effects/')-8
        MOI=VTM1[newvt:newvt+4]
        VTR=int.from_bytes(MOI,byteorder='little')
        VTR3=VTM1[newvt:newvt+VTR]
        VTM3=(VTR+6).to_bytes(4,byteorder='little')+VTR3[4:]
        CODE=VTM1[:15]+VTM2[:46]+VTM3+b'\x04\x00\x00\x00\x04\x00\x00\x00'
        VTM=VTCUOI
        CODEFULL+=CODE
    
    CODEFULL=CODEFULL.replace(str1,str1+ idnew).replace(str2,str2 + idnew)
    CODEFULL=len(VTRCM+VTCUOI1+CODEFULL).to_bytes(4,byteorder='little')+VTRCM[4:]+(len(VTCUOI1+CODEFULL)).to_bytes(4,byteorder='little')+VTCUOI1[4:]+CODEFULL
    new1=new1.replace(VTM9,CODEFULL)
    new1=len(new1).to_bytes(4,byteorder='little')+new1[4:]
    mkcam = b'\x05'

skinmoi=new1
skinprefag=r.find(b'SkinPrefabG')-8
tinhskinpre=r[skinprefag:skinprefag+4]
tinhskinpre1=int.from_bytes(tinhskinpre,byteorder='little')
tinhskinpre2=r[skinprefag:skinprefag+tinhskinpre1]
JTCom0 = tinhskinpre2.count(b"JTCom0")
beginskin=tinhskinpre2[:101]
CodeSkinNew=beginskin+new1*JTCom0
tinhCodeSkinNew1=CodeSkinNew[:93]
tinhCodeSkinNew=CodeSkinNew[93:]
Elenmen=len(tinhCodeSkinNew).to_bytes(4,byteorder='little')+tinhCodeSkinNew[4:]
SkinPrefag1=tinhCodeSkinNew1+Elenmen
SkinPrefag=len(SkinPrefag1).to_bytes(4,byteorder='little')+SkinPrefag1[4:]
codeskinnew=r1.replace(tinhskinpre2,SkinPrefag)
#=========================================================================================================================                        
def ArtSkinLobbyIdleShowLOD(data4):
    a=camSkin.find(b'\x00ArtSkinLobbyIdleShowLOD')-7
    a10=camSkin.find(b'\x00ArtSkinLobbyIdleShowLOD')-3
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

#=========================================================================================================================                        
def ArtPrefabLODnew(data):
    a=ab.find(b'\x00ArtPrefabLOD')-7
    a2=ab[a:a+4]
    a3=ab[a:a+5]
    a4=a3[4:5]#so 10
    vitri=int.from_bytes(a2,byteorder='little')
    data=ab[a:a+vitri]
    return data

#=========================================================================================================================                        
def ArtPrefabLODExnew(data4):
    a=ab.find(b'\x00ArtPrefabLODEx')-7
    a2=ab[a:a+4]
    a3=ab[a:a+5]
    a4=a3[4:5]#so 10
    vitri=int.from_bytes(a2,byteorder='little')
    data4=ab[a:a+vitri]
    return data4

#=========================================================================================================================                        
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

#=========================================================================================================================                        
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
#=========================================================================================================================                        
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
#=========================================================================================================================                        
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

SkinMD=r[:skinprefag]
Art=SkinMD.find(b'ArtPrefabLOD')-8
tinhskinpre=SkinMD[Art:Art+4]
tinhskinpre1=int.from_bytes(tinhskinpre,byteorder='little')
tinhskinpre2=SkinMD[Art:Art+tinhskinpre1]
ArtLobby=SkinMD.find(b'ArtLobbyShowLOD')-8
tinhArtLobby=SkinMD[ArtLobby:ArtLobby+4]
tinhArtLobby1=int.from_bytes(tinhArtLobby,byteorder='little')
tinhArtLobby2=SkinMD[ArtLobby:ArtLobby+tinhArtLobby1]
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
#=========================================================================================================================                        
if mkcam == b'\x05':
    camSkin=camSkin.replace(CODEFULL,b'')

CodeNewMD=CodeNewMD.replace(cammd,camSkin)
CodeFull=codeskinnew.replace(SkinMD,CodeNewMD)
RootDtrc=CodeFull[:84]
RootDsau=CodeFull[84:]
RootD1=RootDsau[8:12]
VTR=int.from_bytes(RootD1,byteorder='little')
m=RootDsau.find(b'ArtPrefabLOD')-8
tinhRootDsau=len(RootDsau).to_bytes(4,byteorder='little')+RootDsau[4:]
tinhRootDtrc=RootDtrc+tinhRootDsau
CodeDayDu=len(tinhRootDtrc).to_bytes(4,byteorder='little')+tinhRootDtrc[4:]
CodeDayDu=CodeDayDu.replace(b"Light<",b"00000<")
CodeDayDu=CodeDayDu.replace(b'_LOD2',b'_LOD1').replace(b'_LOD3',b'_LOD1').replace(b'_Show2\x04',b'_Show1\x04').replace(b'_Show3\x04',b'_Show1\x04')
tinhcam=CodeDayDu[:89]

with open(op, 'wb') as f:
    f.write(CodeDayDu)

with open(op, 'rb') as o:
    o.seek(92)  # Bỏ qua phần header (92 byte đầu)
    k = 0
    while True:
        # Đọc 4 byte để biết kích thước block
        r1 = o.read(4)
        if len(r1) < 4:
            break  # Không đủ dữ liệu => kết thúc

        KB = int.from_bytes(r1, byteorder='little')

        # Chỉ kiểm tra KB có hợp lệ không (>=4), không giới hạn max
        if KB < 4:
            break  # Kích thước block không hợp lệ

        # Đọc nội dung block (trừ 4 byte đã đọc)
        block_data = o.read(KB - 4)
        if len(block_data) < KB - 4:
            break  # Không đủ dữ liệu => bỏ qua block này

        k += 1  # Tăng số block đọc được

# Ghi lại số block (k) vào vị trí byte 88 (dùng 4 byte để hỗ trợ số lớn)
k_bytes = k.to_bytes(4, byteorder='little')

# Đảm bảo CodeDayDu đủ dài để chèn k_bytes
if len(CodeDayDu) >= 92:
    CodeDayDu = CodeDayDu[:88] + k_bytes + CodeDayDu[92:]
else:
    raise ValueError("File không hợp lệ: không đủ 92 byte header")

# Ghi lại toàn bộ dữ liệu
with open(op, 'wb') as f:
    f.write(CodeDayDu)
# Xử lý tiếp
#giai(newpath)
#print("INFOS [DONE!]")
def process_elsu(IDCHECK):
    if IDCHECK[:3] != '196':
        return
    path = 'Files_Mod/Resources/1.58.1/Prefab_Characters/mod/Prefab_Hero/196_Elsu/196_Elsu_trap_actorinfo.bytes'
    giai(path)
    process_directory(path, "1")
    with open(path, 'rb') as f:
        data = f.read()
    data = data.replace(
        b'Prefab_Skill_Effects/Hero_Skill_Effects/196_Elsu/BaiLiShouYue_attack02_spell01_LOD',
        b'Prefab_Skill_Effects/Hero_Skill_Effects/196_Elsu/' + IDCHECK.encode() + b'/BaiLiShouYue_attack02_spell01_LOD'
    )
    with open(path, 'wb') as f:
        f.write(data)
    process_directory(path, "2")
def process_tulen(IDCHECK):
    if IDCHECK != "19015":
        return
    path = 'Files_Mod/Resources/1.58.1/Prefab_Characters/mod/Prefab_Hero/190_ZhuGeLiang/190_ZhuGeLiang_actorinfo.bytes'
    process_directory(path, "1")  # Giải mã
    with open(path, 'rb') as code_tulen:
        tulen = code_tulen.read()
        tulen = tulen.replace(
            b'\n  <useMecanim var="String" type="System.Boolean" value="True"/>',
            b''
        )
    with open(path, 'wb') as f:
        f.write(tulen)
    process_directory(path, "2")  # Mã hóa lại
    
def butterfly(IDCHECK):
    if IDCHECK != '11621':
        return
    path = 'Files_Mod/Resources/1.58.1/Prefab_Characters/mod/Prefab_Hero/116_JingKe/116_JingKe_actorinfo.bytes'
    process_directory(path, '1')
    with open(path, 'rb') as code_butter:
        nd = code_butter.read()
        nd = nd.replace(
        b'<ArtSkinLobbyShowCamera var="String" type="System.String" value="Prefab_Characters/Prefab_Hero/116_JingKe/Awaken/11621_JingKe_AW1_Cam"/>',
        b'<ArtSkinLobbyShowCamera var="String" type="System.String" value="Prefab_Characters/Prefab_Hero/116_JingKe/Awaken/11621_JingKe_AW1_Cam"/>\n  <ArtSkinLobbyShowMovie var="String" type="System.String" value="Prefab_Characters/Prefab_Hero/116_JingKe/Awaken/11621_JingKe_Movie"/>').replace(b'AW1',b'AW5')
    with open(path, 'wb') as f:
        f.write(nd)
    process_directory(path, "2")
process_elsu(IDCHECK)
process_tulen(IDCHECK)
butterfly(IDCHECK)
