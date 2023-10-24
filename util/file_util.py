import re


def read_by_path(file_path: str):
    # 读取Java文件内容
    with open(file_path, 'r', encoding='utf-8') as file:
        java_code = file.readlines()
    return java_code


def write_file(file_path: str, java_code):
    with open(file_path, 'w', encoding='utf-8') as file:
        file.writelines(java_code)
