import re

from service.read_util import read_by_path
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
if __name__ == '__main__':

    prefix = 'PoEvaluate'
    suffix = 'java'
    pattern_str = r'{}(Vo|VO|Param|Result|)\.{}'.format(prefix, suffix)
    pattern = re.compile(pattern_str)
    directory = 'D:\workspace\pms-manage\src\main'
    file_path_list = search_files(pattern, directory)
    for path in file_path_list:
        read_by_path(path)
        pass

