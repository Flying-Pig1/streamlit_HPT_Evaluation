import json
import pandas as pd
def read_json(input_json_path):
    try:
        with open(input_json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data
    except FileNotFoundError:
        print(f"File not found: {input_json_path}")
    except json.JSONDecodeError:
        print(f"Error decoding JSON from file: {input_json_path}")
    except Exception as e:
        print(f"An error occurred: {e}")

def write_json(output_json_path, data):
    try:
        with open(output_json_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        print(f'Successfully wrote data to {output_json_path}')
    except IOError as e:
        print(f'Error writing to file {output_json_path}: {e}')
    except Exception as e:
        print(f'An unexpected error occurred: {e}')

def write_csv(output_csv_path, data):
    try:
        df = pd.DataFrame(data)
        df.to_csv(output_csv_path, index=False, encoding='utf-8')
        print(f'Successfully wrote data to {output_csv_path}')
    except Exception as e:
        print(f'An error occurred: {e}')


# 查找函数
def find_item(data, image_name, question):
    for item in data:
        if item["image_name"] == image_name and item["question"] == question:
            return item
    return {'cogvlm2': '', 'hpto1.1': ''}

# data = read_json('result_cogvlm2_glm_4v.json')
# write_json('cogvlm2_glm_4v_formatted.json', data)
# data = read_json('result_hpto1.1.json')
# write_json('hpto1.1_formatted.json', data)
# data = read_json('result_hpto1.2.json')
# write_json('hpto1.2_formatted.json', data)
data = read_json('result_hpto1.3.json')
write_json('hpto1.3_formatted.json', data)

All = list()
data1 = read_json('hpto1.3_formatted.json')
data2 = read_json('result.json')
for i in data1:
    all = dict()
    all['image_name'] = i['image_name']
    all['question'] = i['question']
    # 目标查找条件
    target_image_name = i['image_name']
    target_question = i['question']
    j = find_item(data2, target_image_name, target_question)
    all['difficulty'] = i['difficulty']
    all['hpto1.1'] = j['hpto1.1']
    all['hpto1.3'] = i['hpto1.3_resp']
    all['cogvlm2'] = j['cogvlm2']
    # all['glm4v'] = j['glm4v_resp']
    All.append(all)

write_json('result_hpto1.1_hpto1.3_cogvlm2.json', All)
write_csv('result_hpto1.1_hpto1.3_cogvlm2.csv', All)