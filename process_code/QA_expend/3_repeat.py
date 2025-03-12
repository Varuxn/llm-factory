import json
import openai
import random
import os
import yaml
from dotenv import load_dotenv

env_path = "../../model_api/.env"
load_dotenv(env_path)

def load_yaml(file_path):
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)

config = load_yaml('../../model_api/model.yaml')

available_models = []
for model_name, model_info in config.items():
    if isinstance(model_info, dict) and model_info.get("enabled", False):
        available_models.append(model_name)

# 打印可用模型名称
print("可用的模型名称如下：")
for model in available_models:
    print(f"- {model}")

model_name = input("\n请输入要使用的模型名称：")

if model_name not in available_models:
    print(f"错误：模型 '{model_name}' 不可用或未启用。")
    exit(1)

# 获取模型的 API 信息
model_info = config[model_name]
api_key_name = model_info['api_key']
base_url = model_info['base_url']
api_key = os.getenv(api_key_name)

if not api_key:
    print(f"错误：无法找到环境变量 '{api_key_name}'，请检查 .env 文件。")
    exit(1)

# 设置 OpenAI API 参数
# openai.api_key = api_key
openai.api_base = base_url

def chat_with_model(user_input, max_retries=3):
    system_message = {
        "role": "system",
        "content": "我需要你在意思不变的前提下，将这段内容润色一遍。"
    }
    user_message = {"role": "user", "content": user_input}

    for attempt in range(1, max_retries + 1):
        try:
            # 随机选择参数，并限制到小数点后两位
            temperature = round(random.uniform(0.8, 0.95), 2)
            top_p = round(random.uniform(0.6, 0.75), 2)
            
            print(f"尝试 #{attempt}: 发送请求... 使用参数 temperature={temperature}, top_p={top_p}")
            response = openai.ChatCompletion.create(
                model=model_name,
                messages=[system_message, user_message],
                temperature=temperature,
                top_p=top_p,
                api_key=api_key
            )
            assistant_reply = response['choices'][0]['message']['content'].strip()
            print("处理成功")
            return assistant_reply
        except Exception as e:
            print(f"处理问题时出错，尝试次数：{attempt}/{max_retries}。错误信息：{e}")
            if attempt == max_retries:
                return "无法获取回复。"

def modify_json_content(input_file_path, output_file_path, num_iterations):
    # 读取现有数据或初始化空列表
    try:
        with open(output_file_path, 'r', encoding='utf-8') as outfile:
            existing_data = json.load(outfile)
    except FileNotFoundError:
        existing_data = []

    with open(input_file_path, 'r', encoding='utf-8') as infile:
        data = json.load(infile)
        print(f"读取了 {len(data)} 条数据")

    for _ in range(num_iterations):
        modified_data = []
        for index, item in enumerate(data):
            print(f"处理第 {index + 1} 条数据...")
            original_output = item['output']
            modified_output = chat_with_model(original_output)
            item['output'] = modified_output
            modified_data.append(item)

        existing_data.extend(modified_data)  # 将新数据追加到现有数据中

    # 写回全部数据
    with open(output_file_path, 'w', encoding='utf-8') as outfile:
        json.dump(existing_data, outfile, indent=2, ensure_ascii=False)
    print("数据已保存，并成功传送到待训练数据集中")

if __name__ == "__main__":
    num_iterations = int(input("你需要扩充几倍？请输入数据扩充的倍数（1-10）："))
    # input_file_path = "/root/LLaMA-Factory/chuli/数据增强/train.json"
    # output_file_path = "/root/LLaMA-Factory/chuli/数据增强/chongshu.json"

    current_file_path = os.path.abspath(__file__)
    project_path = os.path.dirname(os.path.dirname(os.path.dirname(current_file_path)))
    input_file_path = os.path.join(project_path, "/processed_data/QA_exp.txt")
    output_file_path = os.path.join(project_path, "/processed_data/QA_exp_v2.json")
    modify_json_content(input_file_path, output_file_path, num_iterations)
