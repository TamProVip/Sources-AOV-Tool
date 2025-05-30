import os
import zipfile

def zip_folder(folder_path, output_path):
    with zipfile.ZipFile(output_path, "w", zipfile.ZIP_STORED) as zipf:
        for root, _, files in os.walk(folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                # Giữ nguyên đường dẫn từ thư mục gốc (.)
                arcname = os.path.relpath(file_path, start=".")  # hoặc absolute base path nếu cần
                zipf.write(file_path, arcname)

# Đường dẫn thư mục và file đầu ra
folder = 'Prefab_Hero/150_HanXin'
output_path = 'Actor_150_Infos.pkg.bytes'

# Thực hiện nén
zip_folder(folder, output_path)
