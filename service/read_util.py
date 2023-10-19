import re


def read_by_path(file_path: str):
    # 读取Java文件内容
    with open(file_path, 'r', encoding='utf-8') as file:
        java_code = file.readlines()

    # 定义正则表达式匹配规则
    pattern = r'(private|protected)\s+(Integer)\s+id;'

    # 定义正则表达式匹配规则
    pattern = r'(private|protected)\s+(Integer)\s+id;'

    # 遍历每一行，查找并替换目标行
    for i in range(len(java_code)):
        if re.search(pattern, java_code[i]):
            # 添加新的代码行
            dest_field_type = 'List<Integer>'
            dest_field_name = 'ageList'
            dest_str = f"\r\n\tprivate {dest_field_type} {dest_field_name};\n"
            column_name = 'age';
            comment = '注释'
            java_code.insert(i + 1, f'\r\n\t/**\n\t* {comment}\n\t*/')
            java_code.insert(i + 2, f'\r\n\t@Column(name = "{column_name}")')
            java_code.insert(i + 3, dest_str)

            # 将修改后的代码写回文件
    with open(file_path, 'w', encoding='utf-8') as file:
        file.writelines(java_code)
