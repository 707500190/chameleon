import re

import const.constant as ct
from util.file_util import write_file, read_by_path
from util.mysql_util import MySQLUtil
from util.search_util import search_files

# # 获取当前脚本所在的目录
# script_dir = os.path.dirname(os.path.abspath(__file__))
# # 构建配置文件的路径
# config_file_path = os.path.join(script_dir, '../config.json')
# with open(config_file_path, 'r') as f:
#     config_dic = json.load(f)
config_dic = {
    "project_dir": "\\pms-manage\\src\\main",
    "env": {
        "dev": {
            "ip": "10.60.22.139",
            "username": "pms_rw",
            "password": "d1m_pms_dev",
            "schema": "pms_dev"
        }
    }
}
PROJECT_DIR_INNER = config_dic["project_dir"]


def convert_type(field_type) -> tuple:
    """
    数据库类型和Java类型转换
    :param field_type: 数据库类型
    :return: Java类型
    """
    type_mapping = ct.type_mapping
    return type_mapping.get(field_type.lower())


def deal_pojo_file(path1, column_name, db_type1, field_pojo_name, comment1):
    """
    处理POJO Java的实体类； 导包，插入指定字段

    :param path1:  Java的实体类所在路径；
    :param column_name: 数据库字段
    :param db_type1: 数据库类型
    :param field_pojo_name: Java类字段
    :param comment1: 注释；
    """
    java_code = read_by_path(path1)
    # 定义正则表达式匹配规则
    pattern = r'(private|protected)\s+(Integer|Long|int|long)\s+id;'

    java_type, package_name = convert_type(db_type1)
    insert_line = f'\tprotected {java_type} {field_pojo_name};\n'
    # 判断文件中是否已经包含此包  True：包含
    import_flag = java_code.__str__().__contains__(java_type)
    column_flag = java_code.__str__().__contains__("@Column")

    for i in range(len(java_code)):
        # 导包
        if java_code[i].__contains__("import") and not import_flag and package_name:
            import_str = f'import {package_name}.{java_type};\n'
            java_code.insert(i + 1, import_str)
            import_flag = True
        if re.search(pattern, java_code[i]):
            # 添加新的代码行

            java_code.insert(i + 1, f'\n\t/**\n \t * {comment1}\n\t */')
            # 非实体类不加此注释
            if column_flag:
                java_code.insert(i + 2, f'\n\t@Column(name = "{column_name}")\n')
                java_code.insert(i + 3, insert_line)
            else:
                java_code.insert(i + 3, insert_line + '\n')
    write_file(path1, java_code)


def get_pojo_pattern(prefix: str):
    suffix = 'java'
    pattern_str = r'{}(Vo|VO|Param|Result|)\.{}'.format(prefix, suffix)
    pattern = re.compile(pattern_str)
    return pattern


def get_mapper_pattern(prefix: str):
    suffix = 'xml'
    pattern_str = r'{}Mapper\.{}'.format(prefix, suffix)
    pattern = re.compile(pattern_str)
    return pattern


def insert_create_by(content, column_name, pojo_field):
    # 查找 <insert id="insertSelective" 的位置
    index = content.find('<insert id="insertSelective"')
    if index != -1:
        # 在 <insert id="insertSelective" 后查找第一个 </trim> 的位置
        trim_index = content.find('</trim>', index)
        if trim_index != -1:
            # 插入 <if> 标签
            insert_text = f'\t<if test="{pojo_field}!= null">\n\t\t\t\t{column_name},\n\t\t\t</if>\n\t\t'
            content = content[:trim_index] + insert_text + content[trim_index:]
            trim2_index = content.find('</trim>', trim_index)
            trim2_index = content.find('</trim>', trim2_index + 1)
            if trim2_index != -1:
                # 插入 <if> 标签
                insert_text = f'\t<if test="{pojo_field}!= null">\n' + '\t\t\t\t#{' + pojo_field + '},\n\t\t\t</if>\n\t\t'
                content = content[:trim2_index] + insert_text + content[trim2_index:]
    return content


def insert_create_by_update(content, column_name, pojo_field):
    # 查找 <update id="updateById" 的位置
    index = content.find('<update id="updateById"')
    if index != -1:
        # 在 <update id="updateById" 后查找第一个 </set> 的位置
        set_index = content.find('</set>', index)
        if set_index != -1:
            # 插入 <if> 标签
            insert_text = f'\t<if test="{pojo_field}!= null">\n\t\t\t\t{column_name}=#' + '{' + pojo_field + '},\n\t\t\t</if>\n\t\t'
            content = content[:set_index] + insert_text + content[set_index:]

    return content


def deal_mapper_file(path1, column_name, field_pojo):
    """
    处理 Mapper.xml 在指定地方插入代码 insert | update
    :param column_name: 数据库字段 age_first
    :param path1: Mapper.xml文件所在路径；
    :param field_pojo: ageFirst
    """
    # 解析XML文件
    # 打开文件并读取内容
    with open(path1, 'r', encoding='utf-8') as f:
        file_content = f.read()

    # 插入 <if> 标签
    file_content = insert_create_by(file_content, column_name, field_pojo)
    file_content = insert_create_by_update(file_content, column_name, field_pojo)

    # 将结果写回到原文件
    with open(path1, 'w', encoding='utf-8') as f:
        f.write(file_content)


#
#
# def deal_mapper_file(path1, field_source, field_pojo):
#     """
#     处理 Mapper.xml 在指定地方插入代码 insert | update
#     :param path1: Mapper.xml文件所在路径；
#     :param field_source: 数据库字段 age_first
#     :param field_pojo: ageFirst
#     """
#     # 解析XML文件
#     parser = etree.XMLParser(resolve_entities=False)
#     tree = etree.parse(path1, parser=parser)
#     root = tree.getroot()
#
#     # 遍历所有的insert语句 xpath
#     for insert in root.xpath('.//*[starts-with(name(), "insert")] | .//*[starts-with(name(), "update")]'):
#         if insert.get('id') == 'insertSelective':
#             # 找到第一个<trim>标签并插入新的<if>标签
#             first_trim = insert.find('trim')
#             if first_trim is not None:
#                 new_if_element = etree.SubElement(first_trim, 'if', test=f"{field_pojo} != null")
#                 new_if_element.text = f'\n\t\t\t\t{field_source},\n\t\t'
#                 new_if_element.tail = '\n\t\t'
#             else:
#                 print("No first trim tag found")
#
#                 # 找到第二个<trim>标签并插入新的<if>标签
#             second_trim = insert.findall('trim')[1]
#             if second_trim is not None:
#                 new_if_element = etree.SubElement(second_trim, 'if', test=f"{field_pojo} != null")
#                 new_if_element.text = '\n\t\t\t#{' + field_pojo + '},\n\t\t'
#                 new_if_element.tail = '\n\t\t'
#
#         if insert.get('id') == 'updateById':
#             # 找到<set>标签并插入新的<if>标签
#             set_element = insert.find('set')
#             if set_element is not None:
#                 new_if_element = etree.SubElement(set_element, 'if', test=f"{field_pojo} != null")
#                 new_if_element.text = f'\n\t\t\t\t{field_source}=' + '#{' + field_pojo + '},\n\t\t\t'
#                 new_if_element.tail = '\n\t\t\t'
#
#     # 将修改后的元素树写回到文件中
#     tree.write(path1, encoding='utf-8', xml_declaration=True)


def get_class_name_by_tb(s: str):
    words = s.split('_')
    result = ''.join(word.capitalize() for word in words)
    return result


def get_pojo_field_by_name(s: str):
    """
    获取类字段名称
    获取 Params|VO|Result 或者实体类中字段的名称
    :param s:  数据库字段 ep:age_first
    :return:  POJO 字段 ep:ageFirst
    """
    words = s.split('_')
    result = words[0] + ''.join(word.capitalize() for word in words[1:])
    print(result)
    return result


# 调用函数进行检查
def check_column_exists(table_name, column_name, util):
    try:
        # 执行查询语句
        query = f"SHOW COLUMNS FROM {table_name} LIKE '{column_name}'"
        result = util.execute_query(query)

        # 检查结果是否为空
        if len(result) == 0:
            print(f"Column '{column_name}' does not exist in table '{table_name}'")
            return False
        else:
            print(f"Column '{column_name}' exists in table '{table_name}'")
            return True
    except Exception as e1:
        print(e1)
        return True


def execute_auto(pre_directory, table_name_source, column_name, env, comment1, default='null', db_type='',
                 task_list=None):
    """
    1、mysql获取连接；
    2、校验：字段是否存在，表名是否不存在；
    3、处理参数，拼接 DDL SQL，拼接绝对路，字段驼峰和类命名转换；
    2、根据任务项处理文件，1.正则多线程找文件 pojo = [](vo,param,result)  mapper = [](.java .xml)；2.流读入处理
    """

    # 获取连接读取指定环境的配置
    mysql_dic = config_dic["env"][env]
    util = MySQLUtil(mysql_dic['ip'], mysql_dic["username"], mysql_dic["password"], mysql_dic["schema"])
    util.connect()
    # 检查重复字段；
    exists = check_column_exists(table_name_source, column_name, util)
    if exists:
        util.disconnect()
        return '字段已存在或表不存在！'

    # 参数预处理
    if task_list is None:
        task_list = ['POJO', 'XML', 'DB']
    # 字段类型和长度分离： db_type_full varchar(1000) db_type: varchar
    print(db_type)
    # sql concat
    concat_ddl = f"alter table `{table_name_source}` " \
                 f"add column `{column_name}` {db_type} default {default} comment '{comment1}';"
    print("DDL - SQL: ", concat_ddl)
    # 转换大小写，驼峰命名，拼接路径
    pojo_name = get_class_name_by_tb(table_name_source)
    field_name = get_pojo_field_by_name(column_name)
    directory = pre_directory + PROJECT_DIR_INNER

    # 处理入库
    if 'DB' in task_list:
        try:
            pass
            util.execute_update(concat_ddl)
        except Exception as e2:
            msg = "请检查sql" + e2.__str__()
            print(f"-----------------------{msg}---------------------")
            util.disconnect()
            return msg + f'\n sql语句：{concat_ddl}'

    # 处理 param vo result
    if 'POJO' in task_list:
        try:
            pojo_pattern = get_pojo_pattern(pojo_name)
            file_path_list = search_files(pojo_pattern, directory)
            # 处理 pojo类
            for path in file_path_list:
                deal_pojo_file(path, column_name, db_type, field_name, comment1)
                pass
        except Exception as e2:
            msg = "处理POJO类（param vo result...）异常：" + e2.__str__()
            print(f"-----------------------{msg}---------------------")
            util.disconnect()
            return msg
    # 处理 mapper.xml文件（insert update）
    if 'XML' in task_list:
        try:
            mapper_pattern = get_mapper_pattern(pojo_name)
            file_path_list = search_files(mapper_pattern, directory)
            for mapper_path in file_path_list:
                deal_mapper_file(mapper_path, column_name, field_name)
                pass
        except Exception as e2:
            msg = "处理 mapper.xml文件（insert update）异常：" + e2.__str__()
            print(f"-----------------------{msg}---------------------")
            util.disconnect()
            return msg
    util.disconnect()
    return concat_ddl


if __name__ == '__main__':
    deal_mapper_file('D:/workspace/pms-manage/src/main/resources/mapper/PoEvaluateMapper.xml', 'column', 'field')
