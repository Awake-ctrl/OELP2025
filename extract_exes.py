import os
import zipfile
import shutil

def extract_exe_from_zips(base_dir="theZoo/malware/Binaries", output_dir="malware", password=b'infected'):
    os.makedirs(output_dir, exist_ok=True)
    k=0
    for root, _, files in os.walk(base_dir):
        for file in files:
            if file.endswith(".zip"):
                zip_path = os.path.join(root, file)
                try:
                    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                        for member in zip_ref.namelist():
                            if member.endswith((".exe", ".dll", ".scr", ".com")):
                                extracted_path = zip_ref.extract(member, path="temp_extract", pwd=password)
                                new_name = os.path.basename(root) + "_" + os.path.basename(member)
                                dest_path = os.path.join(output_dir, new_name)
                                shutil.move(extracted_path, dest_path)
                                k=k+1
                                print(f"[✓] Extracted: {new_name}" ,k)
                except (RuntimeError, zipfile.BadZipFile, zipfile.LargeZipFile) as e:
                    print(f"[✗] Failed {zip_path}: {e}")

    if os.path.exists("temp_extract"):
        print("in temp_extract ____\n")
        shutil.rmtree("temp_extract")


if __name__ == "__main__":
    extract_exe_from_zips()
