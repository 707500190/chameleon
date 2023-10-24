import re

from lxml import etree

import const.constant as ct
from util.file_util import write_file, read_by_path
from util.search_util import search_files
from util.mysql_util import MySQLUtil

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
    pattern = r'(private|protected)\s+(Integer)\s+id;'

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


def deal_mapper_file(path1, field_source, field_pojo):
    """
    处理 Mapper.xml 在指定地方插入代码 insert | update
    :param path1: Mapper.xml文件所在路径；
    :param field_source: 数据库字段 age_first
    :param field_pojo: ageFirst
    """
    # 解析XML文件
    parser = etree.XMLParser(resolve_entities=False)
    tree = etree.parse(path1, parser=parser)
    root = tree.getroot()

    # 遍历所有的insert语句 xpath
    for insert in root.xpath('.//*[starts-with(name(), "insert")] | .//*[starts-with(name(), "update")]'):
        if insert.get('id') == 'insertSelective':
            # 找到第一个<trim>标签并插入新的<if>标签
            first_trim = insert.find('trim')
            if first_trim is not None:
                new_if_element = etree.SubElement(first_trim, 'if', test=f"{field_pojo} != null")
                new_if_element.text = f'\n\t\t\t\t{field_source},\n\t\t'
                new_if_element.tail = '\n\t\t'
            else:
                print("No first trim tag found")

                # 找到第二个<trim>标签并插入新的<if>标签
            second_trim = insert.findall('trim')[1]
            if second_trim is not None:
                new_if_element = etree.SubElement(second_trim, 'if', test=f"{field_pojo} != null")
                new_if_element.text = '\n\t\t\t#{' + field_pojo + '},\n\t\t'
                new_if_element.tail = '\n\t\t'

        if insert.get('id') == 'updateById':
            # 找到<set>标签并插入新的<if>标签
            set_element = insert.find('set')
            if set_element is not None:
                new_if_element = etree.SubElement(set_element, 'if', test=f"{field_pojo} != null")
                new_if_element.text = f'\n\t\t\t\t{field_source}=' + '#{' + field_pojo + '},\n\t\t\t'
                new_if_element.tail = '\n\t\t\t'

    # 将修改后的元素树写回到文件中
    tree.write(path1, encoding='utf-8', xml_declaration=True)


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


def execute_auto(pre_directory, table_name_source, column_name, env, comment1, default='null', db_type='dev'):
    """
    分为几大步：
    一、入库
    二、找文件(一批) ->dest_path[]
            1.批量的数组 [] 值为匹配到的 文件路径：根据不同的通配表达式，进入不同的数组，此处可以一分为二： pojo = [](vo,param,result)  mapper = [](.java .xml)；
    三、 处理实体类；
    四、处理xml
    """
    # 去除 类型后面的数值
    db_type = db_type[:db_type.find('(')]
    print(db_type)

    concat_ddl = f"alter table {table_name_source} " \
                 f"add column {column_name} {db_type} default {default} comment '{comment1}';"
    print("DDL - SQL: ", concat_ddl)
    # 读取指定环境的配置
    mysql_dic = config_dic["env"][env]
    util = MySQLUtil(mysql_dic['ip'], mysql_dic["username"], mysql_dic["password"], mysql_dic["schema"])
    util.connect()

    try:
        # TODO:此处新增 查询表是否存在
        pass
        util.execute_update(concat_ddl)

    except Exception as e2:
        msg = "请检查sql" + e2.__str__()
        if e2.__str__().__contains__("Duplicate"):
            msg = "重复字段：" + column_name + e2.__str__()
        print(f"-----------------------{msg}---------------------")
        return msg
    # 获取类名， 获取属性名
    pojo_name = get_class_name_by_tb(table_name_source)
    field_name = get_pojo_field_by_name(column_name)
    directory = pre_directory + PROJECT_DIR_INNER
    # 处理 param vo result
    pojo_pattern = get_pojo_pattern(pojo_name)
    file_path_list = search_files(pojo_pattern, directory)
    # 处理 pojo类
    for path in file_path_list:
        deal_pojo_file(path, column_name, db_type, field_name, comment1)
        pass
    # 处理 mapper.xml文件（insert update）
    mapper_pattern = get_mapper_pattern(pojo_name)
    file_path_list = search_files(mapper_pattern, directory)
    for mapper_path in file_path_list:
        deal_mapper_file(mapper_path, column_name, field_name)
        pass
    util.disconnect()
    return concat_ddl
