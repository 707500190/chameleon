import re

from service.file_util import write_file, read_by_path
from service.search_util import search_files

"""
分为几大步：
一、构造自动化任务信息类：AutoTask对象：收集必要属性：     定义构建 不同的 正则表达式， 查找文件根目录，
                                                    |
二、找文件(一批) ->dest_path[]
        1.批量的数组 [] 值为匹配到的 文件路径：根据不同的通配表达式，进入不同的数组，此处可以一分为二： pojo = [](vo,param,result)  mapper = [](.java .xml)；
                                                    |                                                  
三、 获取到目标文件信息[]： 文件名， 后缀， 路径 ，遍历目标文件进入根据条件 进入策略方法，不同的后缀进入不同的处理策略；
                                                    |
四、处理策略（通用）： 读取目标文件（读），找到指定位置（定位），设置值（构造），设值；

"""


def deal_pojo_file(path):
    java_code = read_by_path(path)
    # 定义正则表达式匹配规则
    pattern = r'(private|protected)\s+(Integer)\s+id;'
    # 定义正则表达式匹配规则
    pattern = r'(private|protected)\s+(Integer)\s+id;'

    # 遍历每一行，查找并替换目标行
    for i in range(len(java_code)):
        if re.search(pattern, java_code[i]):
            # 添加新的代码行
            field_type = 'List<Integer>'
            field_name = 'ageList'
            field_str = f"\r\n\tprivate {field_type} {field_name};\n"
            column_name = 'age';
            comment = '注释'
            java_code.insert(i + 1, f'\r\n\t/**\n\t* {comment}\n\t*/')
            java_code.insert(i + 2, f'\r\n\t@Column(name = "{column_name}")')
            java_code.insert(i + 3, field_str)
    write_file(path, java_code)


def get_pojo_pattern(prefix: str):
    prefix = 'PoEvaluate'
    suffix = 'java'
    pattern_str = r'{}(Vo|VO|Param|Result|)\.{}'.format(prefix, suffix)
    pattern = re.compile(pattern_str)
    return pattern


def get_mapper_pattern(prefix: str):
    prefix = 'PoEvaluate'
    suffix = 'xml'
    pattern_str = r'{}Mapper\.{}'.format(prefix, suffix)
    pattern = re.compile(pattern_str)
    return pattern


PROJECT_DIR_INNER = '\pms-manage\src\main'

# import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup as bs


def deal_mapper_file(path, line1, line2):
    with open(path, 'r', encoding='utf-8') as f:
        soup = bs(f.read(), 'lxml-xml')

        # 遍历所有的insert语句
        for insert in soup.select('insert'):
            if insert.get('id') == 'insertSelective':
                # 找到第一个<trim>标签并插入新的<if>标签
                first_trim = insert.find('trim')
                if first_trim:
                    if_element_1 = first_trim.find('if', {'test': 'a != null'})
                    if not if_element_1:
                        new_if_element_1 = soup.new_tag('if', test="a != null")
                        new_if_element_1.string = "\n\t\tcreate_by=#{createBy},\n"
                        first_trim.append(new_if_element_1)

                # 找到第二个<trim>标签并插入新的<if>标签
                second_trim = insert.find_all('trim')[1]
                if second_trim:
                    if_element_2 = second_trim.find('if', {'test': 'a != null'})
                    if not if_element_2:
                        new_if_element_2 = soup.new_tag('if', test="a != null")
                        new_if_element_2.string = "\n\t\ts\n"
                        second_trim.append(new_if_element_2)

            if insert.get('id') == 'updateById':
                # 找到<set>标签并插入新的<if>标签
                set_element = insert.find('set')
                if set_element:
                    if_element = set_element.find('if', {'test': 'createBy != null'})
                    if not if_element:
                        new_if_element = soup.new_tag('if', test="createBy != null")
                        new_if_element.string = "\n\t\tcreate_by=#{createBy},\n"
                        set_element.append(new_if_element)

        # 格式化XML文档
        xml_str = soup.prettify()

    # 将修改后的内容写回到文件中
    with open(path, 'w', encoding='utf-8') as f:
        f.write(xml_str)


if __name__ == '__main__':
    pre_directory = 'D:\developer\workspace'
    prefix = 'PoEvaluate'

    # directory = os.path.join(pre_directory, PROJECT_DIR_INNER)
    directory = pre_directory + PROJECT_DIR_INNER
    pojo_pattern = get_pojo_pattern(prefix)
    file_path_list = search_files(pojo_pattern, directory)
    for path in file_path_list:
        deal_pojo_file(path)
        pass

    mapper_pattern = get_mapper_pattern(prefix)
    file_path_list = search_files(mapper_pattern, directory)
    for mapper_path in file_path_list:
        deal_mapper_file(mapper_path, f"<if test= '{prefix} != null'>\n\t age,\n\r</if>",
                         f"<if test= '{prefix} != null'>\n\t age,\n\r</if>")
        pass
