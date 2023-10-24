import tkinter as tk

import const.constant as ct
from func.add_field import execute_auto


class AddColumnUI:
    def __init__(self, master):
        self.master = master
        self.master.title("一键新增字段")
        self.master.geometry("500x450")

        self.pre_directory = tk.StringVar()
        self.table_name_source = tk.StringVar()
        self.column_name = tk.StringVar()
        self.env = tk.StringVar(value='dev')
        self.comment1 = tk.StringVar()
        self.default = tk.StringVar()
        self.db_type = tk.StringVar(value='int')
        self.length = tk.StringVar(value='')

        # 定义字段类型下拉列表
        self.type_mapping = ct.type_mapping
        self.db_type_list = sorted([k for k in self.type_mapping.keys()])

        self.create_widgets()

    def create_widgets(self):
        # 项目路径
        tk.Label(self.master, text="项目路径:").grid(row=0, column=0)
        tk.Entry(self.master, width=25, textvariable=self.pre_directory).grid(row=0, column=1, columnspan=2)

        # 表名
        tk.Label(self.master, text="表名:").grid(row=1, column=0)
        tk.Entry(self.master, width=25, textvariable=self.table_name_source).grid(row=1, column=1, columnspan=2)

        # 字段名
        tk.Label(self.master, text="字段名:").grid(row=2, column=0)
        tk.Entry(self.master, width=25, textvariable=self.column_name).grid(row=2, column=1, columnspan=2)

        # 环境
        tk.Label(self.master, text="环境:").grid(row=3, column=0)
        tk.OptionMenu(self.master, self.env, "dev", "test").grid(row=3, column=1, columnspan=2)

        # 注释
        tk.Label(self.master, text="注释:").grid(row=4, column=0)
        tk.Entry(self.master, width=25, textvariable=self.comment1).grid(row=4, column=1, columnspan=2)

        # 默认值
        tk.Label(self.master, text="默认值:").grid(row=5, column=0)
        tk.Entry(self.master, width=25, textvariable=self.default).grid(row=5, column=1, columnspan=2)

        # 字段类型
        tk.Label(self.master, text="字段类型:").grid(row=6, column=0)
        tk.OptionMenu(self.master, self.db_type, *self.db_type_list).grid(row=6, column=1)

        # 长度
        tk.Label(self.master, text="长度:").grid(row=6, column=2)
        tk.Entry(self.master, width=10, textvariable=self.length).grid(row=6, column=2)

        # 提交按钮
        tk.Button(self.master, text="提交", command=self.add_column).grid(row=7, column=1, columnspan=2, pady=10)

        # 输出框
        tk.Label(self.master, text="输出:").grid(row=8, column=0, sticky="w")
        self.output_text = tk.Text(self.master, height=7, width=50)
        self.output_text.grid(row=8, column=1, sticky="w")

    def add_column(self):
        project_dir = self.pre_directory.get()
        table_name = self.table_name_source.get()
        column_name = self.column_name.get()
        env = self.env.get()
        db_type = f"{self.db_type.get()}({self.length.get()})"
        default_value = self.default.get()
        if default_value.__contains__('null') or default_value.__contains__('NULL') and db_type.__contains__(
                "timestamp"):
            default_value = 'now()'
        if len(default_value) < 1:
            default_value = 'null'
            if db_type.__contains__("timestamp"):
                default_value = 'now()'
        comment = self.comment1.get()
        # TODO: 可供选择的 执行部分
        # TODO: 自动搜索pms项目路径
        # TODO: 接受的值去除空格
        res = execute_auto(project_dir, table_name, column_name, env, comment, default_value, db_type)

        self.output_text.delete("1.0", tk.END)
        self.output_text.insert(tk.END, res)


'''
D:\workspace
po_evaluate
zhao_he
这是一个注释
'''
if __name__ == '__main__':
    a = list()
    root = tk.Tk()
    AddColumnUI(root)
    root.mainloop()
