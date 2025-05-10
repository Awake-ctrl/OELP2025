
import numpy as np
import os
from PIL import Image

def file_to_rgb_image(file_path, image_size=(128, 128)):
    with open(file_path, 'rb') as f:
        byte_data = f.read()
    byte_array = np.frombuffer(byte_data, dtype=np.uint8)

    pad_len = (-len(byte_array)) % 3
    byte_array = np.pad(byte_array, (0, pad_len), 'constant', constant_values=0)
    rgb_array = byte_array.reshape((-1, 3))

    square_len = int(np.ceil(np.sqrt(len(rgb_array))))
    padded_len = square_len * square_len
    pad_pixels = padded_len - len(rgb_array)
    rgb_array = np.pad(rgb_array, ((0, pad_pixels), (0, 0)), 'constant', constant_values=0)

    rgb_image = rgb_array.reshape((square_len, square_len, 3))
    img = Image.fromarray(rgb_image.astype(np.uint8), mode='RGB')
    img = img.resize(image_size)
    return img

def process_directory(input_dir, output_dir, label):
    count =0
    os.makedirs(output_dir, exist_ok=True)
    for file in os.listdir(input_dir):
        if file.endswith(('.exe', '.elf', '.pdf')):
            try:
                image = file_to_rgb_image(os.path.join(input_dir, file))
                image.save(os.path.join(output_dir, f"{label}_{file}.png"))
                count +=1
                print(f"[✓] Processed {file}")
            except Exception as e:
                print(f"[✗] Failed {file}: {e}")
    print("_______________________________________",count)
if __name__ == "__main__":
    benign_dir = "dataset/benign"
    malware_dir = "dataset/malware"
    output_dir = "dataset/images"
    
    process_directory(benign_dir, os.path.join(output_dir, "benign"), "benign")
    process_directory(malware_dir, os.path.join(output_dir, "malware"), "malware")
