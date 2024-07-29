import json

# 读取JSON文件
file_path = 'result.json'  # 替换为你的JSON文件路径

# 使用 utf-8 编码读取文件
with open(file_path, 'r', encoding='utf-8') as file:
    data = json.load(file)

# 提取task并添加为新的key
for item in data:
    image_name_parts = item["image_name"].split('_')
    if len(image_name_parts) > 1:
        item["task"] = image_name_parts[1]
    else:
        item["task"] = ""

# 保存修改后的JSON文件
output_file_path = 'result.json'  # 替换为你想要保存的文件路径
with open(output_file_path, 'w', encoding='utf-8') as file:
    json.dump(data, file, indent=4, ensure_ascii=False)

print(f'Modified JSON file saved to {output_file_path}')
