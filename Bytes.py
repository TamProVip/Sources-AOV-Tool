import xml.etree.ElementTree as ET
import os
from xml.dom import minidom
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
        
#=========================================================================================================================                        

def process_file(file_path, LC):
    base, ext = os.path.splitext(file_path)

    try:
        if LC == "1" and ext == ".bytes":
            # Giải mã: .bytes -> .xml
            with open(file_path, "rb") as f:
                data = f.read()
            xml_data = Bytes_XML.decode(data)
            with open(base + ".xml", "wb") as f:
                f.write(xml_data)
            print(f"Đã giải mã: {file_path} -> {base}.xml")

        elif LC == "2" and ext == ".xml":
            # Mã hóa: .xml -> .bytes
            with open(file_path, "r", encoding="utf-8") as f:
                xml_content = f.read()
            bin_data = Bytes_XML.encode(xml_content)
            with open(base + ".bytes", "wb") as f:
                f.write(bin_data)
            print(f"Đã mã hóa: {file_path} -> {base}.bytes")

    except Exception as e:
        print(f"Lỗi xử lý file {file_path}: {e}")

def process_directory(directory_path, LC):
    for root, _, files in os.walk(directory_path):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            process_file(file_path, LC)

def main():
    directory_path = input("Nhập đường dẫn thư mục cần xử lý: ").strip()
    
    if not os.path.isdir(directory_path):
        print("Đường dẫn không hợp lệ!")
        return
    
    LC = input("Nhập 1 để giải mã (.bytes -> .xml), 2 để mã hóa (.xml -> .bytes): ").strip()
    if LC in ["1", "2"]:
        process_directory(directory_path, LC)
    else:
        print("Lựa chọn không hợp lệ!")

# Chạy chương trình
main()

import os
import re

# Nhập ID skin và ID hero tương ứng (cách nhau dấu cách)
id_skins = input("ID Skin : ").split()
id_heros = input("ID Hero : ").split()

if len(id_skins) != len(id_heros):
    print("Số lượng ID Skin và ID Hero không khớp.")
    exit()

path = input("Nhập Thư Mục")  # Thư mục chứa file cần xử lý

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
        # Xoá toàn bộ dòng <SkinOrAvatarList id="..." />
        track = re.sub(r'^[ \t]*<SkinOrAvatarList id="\d+"(?: heroId="\d+")? ?/>\n?', '', track, flags=re.MULTILINE)

        # Thay SkinAvatarFilterType="11" thành "9", hoặc thêm SkinAvatarFilterType="9" nếu chưa có
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

        # Kiểm tra track thuộc prefab hay sound
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

            for skin_id, hero_id in zip(id_skins, id_heros):
                mod_track = track
                if is_sound:
                    mod_track = re.sub(
                        r'(eventName" value="[^"]+?)(")',
                        lambda m: m.group(1) + f"_Skin{int(skin_id[-2:])}" + m.group(2),
                        mod_track
                    )
                mod_track = re.sub(
                    r'(</Event>)',
                    r'\1\n' + indent_event + f'<SkinOrAvatarList id="{hero_id}"',
                    mod_track
                )

                new_tracks.append(mod_track)

    if new_tracks:
        print(f"----- Xử lý file: {filename} -----")
        insert_block = '\n'.join(new_tracks) + '\n'

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

# Xoá dòng trắng thừa
for filename in os.listdir(path):
    filepath = os.path.join(path, filename)
    if not os.path.isfile(filepath):
        continue
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            lines = [line for line in f if line.strip()]
        with open(filepath, 'w', encoding='utf-8') as f:
            f.writelines(lines)
        print(f"Đã xử lý xóa dòng trắng: {filename}")
    except UnicodeDecodeError:
        print(f"Bỏ qua file không đọc được utf-8 khi xóa dòng trắng: {filename}")
    except PermissionError:
        print(f"Không có quyền xử lý file: {filename}")
