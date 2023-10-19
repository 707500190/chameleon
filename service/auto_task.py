"""
服务于Java 文件 一键新增字段 条件：
1.目标实体或者 表名称 ep: EmployeeSupply  / employee_supply；
2.实体类，新增一行的 字符串值；可以分解为  设置访问类型（public protected private）
3.后缀集合（哪些类需要更改）[Vo, Result, Param, DTO, Dto]
4.本地项目路径（）  比如项目 PMS-manage 路径：D:\workspace\pms-manage
5.通用命名空间前缀：BASE_NAMESPACE_PREFIX = 'com.d1mgroup.pms'
"""

from enum import Enum


class ExecutionType(Enum):
    ADD = "新增"
    REPLACE = "替换"
    DELETE = "删除"


class AutoTaskInfo:

    def __init__(self,
                 execute_type: ExecutionType = ExecutionType.ADD,
                 table_name: str = None,
                 field_name: str = '',
                 project_directory: str = 'D:\workspace\pms-manage',
                 base_namespace: str = 'com.d1mgroup.pms'
                 ):
        # 文件基本命名空间
        self.base_namespace = base_namespace
        # 项目根路径
        self.project_directory = project_directory
        # 目标属性
        self.field_name = field_name

        self.execute_type = execute_type

        self.table_name = table_name

    @property
    def base_namespace(self):
        return self._base_namespace

    @base_namespace.setter
    def base_namespace(self, value):
        if not isinstance(value, str):
            raise TypeError("base_namespace must be a string")
        self._base_namespace = value

    @property
    def project_directory(self):
        return self._project_directory

    @project_directory.setter
    def project_directory(self, value):
        if not isinstance(value, str):
            raise TypeError("project_directory must be a string")
        self._project_directory = value

    @property
    def property_str(self):
        return self._property_str

    @property_str.setter
    def property_str(self, value):
        if not isinstance(value, str):
            raise TypeError("property_str must be a string")
        self._property_str = value

    @property
    def execute_type(self):
        return self._execute_type

    @execute_type.setter
    def execute_type(self, value):
        if not isinstance(value, ExecutionType):
            raise TypeError("execute_type must be an instance of ExecutionType enum")
        self._execute_type = value

    @property
    def table_name(self):
        return self._table_name

    @table_name.setter
    def table_name(self, value):
        if not isinstance(value, str):
            raise TypeError("table_name must be a string")
        self._table_name = value
