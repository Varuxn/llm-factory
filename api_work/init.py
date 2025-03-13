import os
import subprocess

def get_user_input():
    # 获取模型的绝对路径
    model_path = input("请输入模型的绝对路径: ").strip()
    if not os.path.isabs(model_path):
        print("错误：请输入绝对路径！")
        return None

    # 获取显卡数量
    gpu_count = input("请输入使用的显卡数量（默认为 1）: ").strip()
    gpu_count = int(gpu_count) if gpu_count.isdigit() else 1

    # 获取端口号
    port = input("请输入 API 端口号（默认为 8000）: ").strip()
    port = int(port) if port.isdigit() else 8000

    prompt = input("请输入 prompt 的名称（默认为 llama3 ）: ").strip()
    if prompt == "":
        prompt = "llama3"


    return model_path, gpu_count, port, prompt

def construct_command(model_path, gpu_count, port, prompt):
    # 构造 CUDA_VISIBLE_DEVICES 的值
    cuda_devices = ",".join(str(i) for i in range(gpu_count))

    # 构造命令
    command = (
        f"CUDA_VISIBLE_DEVICES={cuda_devices} "
        f"API_PORT={port} "
        f"python src/api.py "
        f"--model_name_or_path {model_path} "
        f"--template {prompt}"
    )
    return command

def main():
    # 获取用户输入
    user_input = get_user_input()
    if not user_input:
        return

    model_path, gpu_count, port, prompt = user_input

    # 构造命令
    command = construct_command(model_path, gpu_count, port,prompt)
    print(f"即将执行的命令: {command}")

    # 确认是否执行
    confirm = input("是否执行命令？(y/n): ").strip().lower()
    if confirm != 'y':
        print("命令已取消。")
        return

    # 执行命令
    try:
        subprocess.run(command, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"命令执行失败: {e}")
    except Exception as e:
        print(f"发生错误: {e}")

if __name__ == "__main__":
    main()