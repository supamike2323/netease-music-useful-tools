# 可以把网易云ncm文件转换成mp3格式
import os
import subprocess

# Define the directory containing the .ncm files
# 设置你自己的路径
# 你所有的ncm文件的文件夹
ncm_directory = '/Users/dengjiaming/Music/网易云音乐'

# 你想让mp3 文件下载去哪里
output_directory = '/Users/dengjiaming/Desktop/mp3s'











# Create the output directory if it doesn't exist
if not os.path.exists(output_directory):
    os.makedirs(output_directory)

# List all ncm files in the directory
ncm_files = [f for f in os.listdir(ncm_directory) if f.endswith('.ncm')]

# List all existing mp3 files in the output directory to avoid re-conversion
existing_mp3_files = {f.replace('.mp3', '') for f in os.listdir(output_directory) if f.endswith('.mp3')}

# Process each file
for file in ncm_files:
    file_base_name = file.replace('.ncm', '')
    
    # Check if the mp3 version of the file already exists
    if file_base_name in existing_mp3_files:
        print(f"{file_base_name}.mp3 already exists, skipping conversion.")
        continue
    
    # Full path to the source file
    src_file = os.path.join(ncm_directory, file)
    
    # Convert the file
    command = f"ncmdump -o \"{output_directory}\" \"{src_file}\""
    process = subprocess.run(command, shell=True)
    
    # Check if the command was executed successfully
    if process.returncode == 0:
        print(f"Converted {file} successfully.")
    else:
        print(f"Failed to convert {file}.")

print("Conversion process completed.")