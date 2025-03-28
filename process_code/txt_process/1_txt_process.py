def process_text(input_file_path, output_file_path, sentences_per_paragraph=15):
    # 读取文件内容并移除换行符
    with open(input_file_path, 'r', encoding='utf-8') as file:
        content = file.read().replace('\n', '')

    # 初始化变量
    paragraph = []
    sentence_count = 0
    paragraphs = []

    # 分割文本为句子并分组成段落
    for sentence in content.split('。'):
        if sentence:  # 忽略空句子
            paragraph.append(sentence + '。')
            sentence_count += 1
            if sentence_count >= sentences_per_paragraph:
                paragraphs.append('《问题》\n' + ''.join(paragraph))
                paragraph = []  # 重置段落
                sentence_count = 0

    # 添加最后一个段落（如果有）
    if paragraph:
        paragraphs.append('《问题》\n' + ''.join(paragraph))

    # 写入处理后的文本到新文件
    with open(output_file_path, 'w', encoding='utf-8') as file:
        for paragraph in paragraphs:
            file.write(paragraph + '\n\n')

    print('文件处理中.....')


# 定义文件路径

# input_file_path = '/root/LLaMA-Factory/数据集全自动处理/受刑文本.txt'
# output_file_path = '/root/LLaMA-Factory/chuli/重生文本.txt'

current_file_path = os.path.abspath(__file__)
project_path = os.path.dirname(os.path.dirname(os.path.dirname(current_file_path)))
input_file_path = os.path.join(project_path, "/init_data/txt_info.txt")
output_file_path = os.path.join(project_path, "/processed_data/txt_info.txt")

# 调用函数
process_text(input_file_path, output_file_path)
