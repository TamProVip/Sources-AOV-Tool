import os
import struct
import xml.etree.ElementTree as ET

HEADER_BYTES = bytes.fromhex(
'4D5345530700000049000000AB0500006161616161616161616161616161616161616161616161616161616161616161000000000000000000000000000000005554462D380000000000000000000000000000000000000000000000000000003731316532366134653861643165656333323839376238643863396336386132000000008C00000000000000'
)

def bytes_to_xml_battlebank(byte_data):
    xml_elements = []
    i = 0
    while i < len(byte_data):
        total_length, track_id = struct.unpack_from('<I4s', byte_data, i)
        track_id = int.from_bytes(track_id, byteorder='little')

        skin_id = struct.unpack_from('<I', byte_data, i + 13)[0]
        if skin_id == 0:
            monster_id = struct.unpack_from('<I', byte_data, i + 17)[0]
            skin_id = None

        sound_name_length = struct.unpack_from('<I', byte_data, i + 35)[0] - 1
        sound_name = byte_data[i + 39:i + 39 + sound_name_length].decode('utf-8')

        if skin_id is None:
            track = ET.Element('Track', MonsterId=str(monster_id), SoundName=sound_name, Id=str(track_id))
        else:
            track = ET.Element('Track', SkinId=str(skin_id), SoundName=sound_name, Id=str(track_id))
        xml_elements.append(ET.tostring(track, encoding='unicode'))

        i += total_length + 4

    return '\n\n'.join(xml_elements)

def bytes_to_xml_lobbysound(byte_data):
    xml_elements = []
    i = 0
    while i < len(byte_data):
        total_length, track_id = struct.unpack_from('<I4s', byte_data, i)
        track_id = int.from_bytes(track_id, byteorder='little')

        action_name_length = struct.unpack_from('<I', byte_data, i + 8)[0]
        action_name_end = i + 12 + action_name_length - 1
        action_name = byte_data[i + 12:action_name_end].decode('utf-8', errors='ignore').rstrip('\x00')

        skin_id_start = action_name_end + 1
        skin_id = int.from_bytes(byte_data[skin_id_start:skin_id_start + 4], byteorder='little')

        cu_name_length = struct.unpack_from('<I', byte_data, skin_id_start + 22)[0]
        cu_name_end = skin_id_start + 26 + cu_name_length - 1
        cu_name = byte_data[skin_id_start + 26:cu_name_end].decode('utf-8', errors='ignore').rstrip('\x00\x01')

        track = ET.Element('Track', Skin=str(skin_id), Name=action_name, ID=str(track_id), Status=str(cu_name))
        xml_elements.append(ET.tostring(track, encoding='unicode'))

        i += total_length + 4

    return '\n\n'.join(xml_elements)

def bytes_to_xml_lobbybank(byte_data):
    xml_elements = []
    i = 0
    while i < len(byte_data):
        total_length, track_id = struct.unpack_from('<I4s', byte_data, i)
        track_id = int.from_bytes(track_id, byteorder='little')

        skin_id = struct.unpack_from('<I', byte_data, i + 13)[0]

        action_name_length = struct.unpack_from('<I', byte_data, i + 35)[0]
        action_name_end = i + 39 + action_name_length - 1
        action_name = byte_data[i + 39:action_name_end].decode('utf-8', errors='ignore').rstrip('\x00\x01')

        track = ET.Element('Track', Skin=str(skin_id), Name=action_name, ID=str(track_id))
        xml_elements.append(ET.tostring(track, encoding='unicode'))

        i += total_length + 4

    return '\n\n'.join(xml_elements)

def bytes_to_xml_herosound(byte_data):
    xml_elements = []
    i = 0
    while i < len(byte_data):
        total_length, track_id = struct.unpack_from('<I4s', byte_data, i)
        track_id = int.from_bytes(track_id, byteorder='little')

        action_name_length = struct.unpack_from('<I', byte_data, i + 8)[0]
        action_name_end = i + 12 + action_name_length - 1
        action_name = byte_data[i + 12:action_name_end].decode('utf-8').rstrip('\x00')

        skin_id_start = action_name_end + 1
        skin_id = int.from_bytes(byte_data[skin_id_start:skin_id_start + 4], byteorder='little')

        input_start = skin_id_start + 12
        input_value = int(byte_data[input_start:input_start + 1].hex(), 16)

        output_start = input_start + 1
        output_value = int(byte_data[output_start:output_start + 1].hex(), 16)

        track = ET.Element('Track', Skin=str(skin_id), Name=action_name, ID=str(track_id), In=str(input_value), Out=str(output_value))
        xml_elements.append(ET.tostring(track, encoding='unicode'))

        i += total_length + 4

    return '\n\n'.join(xml_elements)

def save_xml_from_bytes(file_path, converter_func):
    with open(file_path, 'rb') as file:
        byte_content = file.read()

    xml_content = converter_func(byte_content[140:])
    new_file_path = file_path.replace('.bytes', '.xml')
    with open(new_file_path, 'w', encoding='utf-8') as file:
        file.write(xml_content)
    os.remove(file_path)
    print(f"\033[92m{file_path} đã chuyển đổi thành {new_file_path}")

def xml_to_bytes_battlebank(xml_str):
    byte_data = bytearray()
    root = ET.ElementTree(ET.fromstring(f'<root>{xml_str}</root>')).getroot()

    for track in root:
        track_id = int(track.attrib['Id'])
        sound_name = track.attrib['SoundName']

        if 'SkinId' in track.attrib:
            skin_id = int(track.attrib['SkinId'])
            monster_id = None
        elif 'MonsterId' in track.attrib:
            skin_id = 0
            monster_id = int(track.attrib['MonsterId'])

        sound_name_length = len(sound_name) + 1
        total_length = 39 + sound_name_length + 1

        byte_data.extend(int_to_bytes(total_length, 4))
        byte_data.extend(int_to_bytes(track_id, 4))
        byte_data.append(1)
        byte_data.extend(b'\x00\x00\x00\x00')

        if monster_id is None:
            byte_data.extend(int_to_bytes(skin_id, 4))
            byte_data.extend(b'\x00\x00\x00\x00\x00\x00\x00\x00')
        else:
            byte_data.extend(int_to_bytes(skin_id, 4))
            byte_data.extend(int_to_bytes(monster_id, 4))
            byte_data.extend(b'\x00\x00\x00\x00')

        byte_data.extend(b'\x02\x00\x00\x00\x00\x00\x00\x00\x00\x00')
        byte_data.extend(int_to_bytes(sound_name_length, 4))
        byte_data.extend(sound_name.encode('utf-8'))
        byte_data.append(0)
        byte_data.append(1)
        byte_data.extend(b'\x00\x00\x00\x00')

    return bytes(byte_data)

def xml_to_bytes_lobbysound(xml_str):
    byte_data = bytearray()
    root = ET.ElementTree(ET.fromstring(f'<root>{xml_str}</root>')).getroot()

    for track in root:
        track_id = int(track.attrib['ID'])
        action_name = track.attrib['Name']
        skin_id = int(track.attrib['Skin'])
        cu_name = track.attrib['Status']

        cu_name_length = len(cu_name) + 1
        action_name_length = len(action_name) + 1
        total_length = 12 + action_name_length + 26 + cu_name_length + 1

        byte_data.extend(int_to_bytes(total_length, 4))
        byte_data.extend(int_to_bytes(track_id, 4))
        byte_data.extend(int_to_bytes(action_name_length, 4))
        byte_data.extend(action_name.encode('utf-8'))
        byte_data.append(0)
        byte_data.extend(int_to_bytes(skin_id, 4))
        byte_data.extend(b'\x00\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00')
        byte_data.extend(int_to_bytes(cu_name_length, 4))
        byte_data.extend(cu_name.encode('utf-8'))
        byte_data.append(0)
        byte_data.append(1)
        byte_data.extend(b'\x00\x00\x00\x00')

    return bytes(byte_data)

def xml_to_bytes_lobbybank(xml_str):
    byte_data = bytearray()
    root = ET.ElementTree(ET.fromstring(f'<root>{xml_str}</root>')).getroot()

    for track in root:
        track_id = int(track.attrib['ID'])
        action_name = track.attrib['Name']
        skin_id = int(track.attrib['Skin'])

        action_name_length = len(action_name) + 1
        total_length = 39 + action_name_length + 1

        byte_data.extend(int_to_bytes(total_length, 4))
        byte_data.extend(int_to_bytes(track_id, 4))
        byte_data.extend(b'\x01\x00\x00\x00\x00')
        byte_data.extend(int_to_bytes(skin_id, 4))
        byte_data.extend(b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00')
        byte_data.extend(int_to_bytes(action_name_length, 4))
        byte_data.extend(action_name.encode('utf-8'))
        byte_data.append(0)
        byte_data.append(1)
        byte_data.extend(b'\x00\x00\x00\x00')

    return bytes(byte_data)

def xml_to_bytes_herosound(xml_str):
    byte_data = bytearray()
    root = ET.ElementTree(ET.fromstring(f'<root>{xml_str}</root>')).getroot()

    for track in root:
        track_id = int(track.attrib['ID'])
        action_name = track.attrib['Name']
        skin_id = int(track.attrib['Skin'])
        input_value = int(track.attrib['In'])
        output_value = int(track.attrib['Out'])

        action_name_length = len(action_name) + 1
        total_length = 12 + action_name_length + 12 + 1 + 1 + 14

        byte_data.extend(int_to_bytes(total_length, 4))
        byte_data.extend(int_to_bytes(track_id, 4))
        byte_data.extend(int_to_bytes(action_name_length, 4))
        byte_data.extend(action_name.encode('utf-8'))
        byte_data.append(0)
        byte_data.extend(int_to_bytes(skin_id, 4))
        byte_data.extend(b'\x00\x00\x00\x00\x00\x00\x00\x00')
        byte_data.extend(int_to_bytes(input_value, 1))
        byte_data.extend(int_to_bytes(output_value, 1))
        byte_data.extend(b'\x00\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\x01')

        byte_data.extend(b'\x00\x00\x00\x00')

    return bytes(byte_data)

def int_to_bytes(value, length):
    return value.to_bytes(length, byteorder='little')

def is_utf8(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            file.read()
        return True
    except UnicodeDecodeError:
        return False

def process_file(file_path, option):
    if option == 1:  # Bytes to XML
        if "BattleBank" in file_path:
            save_xml_from_bytes(file_path, bytes_to_xml_battlebank)
        elif "LobbySound" in file_path:
            save_xml_from_bytes(file_path, bytes_to_xml_lobbysound)
        elif "LobbyBank" in file_path:
            save_xml_from_bytes(file_path, bytes_to_xml_lobbybank)
        elif "HeroSound" in file_path:
            save_xml_from_bytes(file_path, bytes_to_xml_herosound)
    elif option == 2:  # XML to Bytes
        if is_utf8(file_path):
            with open(file_path, 'r', encoding='utf-8') as file:
                xml_content = file.read()
            if "BattleBank" in file_path:
                byte_content = xml_to_bytes_battlebank(xml_content)
            elif "LobbySound" in file_path:
                byte_content = xml_to_bytes_lobbysound(xml_content)
            elif "LobbyBank" in file_path:
                byte_content = xml_to_bytes_lobbybank(xml_content)
            elif "HeroSound" in file_path:
                byte_content = xml_to_bytes_herosound(xml_content)
            new_file_path = file_path.replace('.xml', '.bytes')
            with open(new_file_path, 'wb') as file:
                file.write(HEADER_BYTES + byte_content)
            os.remove(file_path)
            print(f"\033[92m{file_path} đã chuyển đổi thành {new_file_path}.")

def main():
    while True:
        directory = input("\033[93mNHẬP THƯ MỤC: \033[0m")
        option = int(input("1. Bytes➤XML \n2. XML➤Bytes \nNhập 1 hoặc 2:  "))

        for filename in os.listdir(directory):
            if option == 1 and filename.endswith('.bytes'):
                file_path = os.path.join(directory, filename)
                process_file(file_path, option)
            elif option == 2 and filename.endswith('.xml'):
                file_path = os.path.join(directory, filename)
                process_file(file_path, option)

if __name__ == "__main__":
    main()
