import tkinter as tk
from tkinter import ttk

from func import concat_sql


class GeneralSqlUI:
    def __init__(self, root):
        root.title("pms-权限sql生成")
        new_toplevel = tk.Toplevel(root)
        # 创建顶层容器
        main_frame = ttk.Frame(new_toplevel, padding="20")
        main_frame.pack(expand=True, fill=tk.BOTH)

        # 创建上部分输入框
        self.nb = ttk.Notebook(main_frame)
        self.nb.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)

        # 新增模块tab
        module_frame = ttk.Frame(self.nb)
        module_frame.pack(fill=tk.BOTH)

        parent_module_name_label = ttk.Label(module_frame, text="Parent Module Name:")
        parent_module_name_label.pack(pady=(10, 5))

        self.parent_module_name_entry = ttk.Entry(module_frame)
        self.parent_module_name_entry.pack(pady=(0, 10))

        module_name_label = ttk.Label(module_frame, text="Module Name:")
        module_name_label.pack(pady=(10, 5))

        self.module_name_entry = ttk.Entry(module_frame)
        self.module_name_entry.pack(pady=(0, 10))

        new_module_url_label = ttk.Label(module_frame, text="Module URL:")
        new_module_url_label.pack(pady=(10, 5))

        self.new_module_url_entry = ttk.Entry(module_frame)
        self.new_module_url_entry.pack(pady=(0, 10))

        # 新增button tab
        button_frame = ttk.Frame(self.nb)
        button_frame.pack(fill=tk.BOTH)

        module_name_label2 = ttk.Label(button_frame, text="Module Name:")
        module_name_label2.pack(pady=(10, 5))

        self.module_name_entry2 = ttk.Entry(button_frame)
        self.module_name_entry2.pack(pady=(0, 10))

        but_url_label = ttk.Label(button_frame, text="But URL:")
        but_url_label.pack(pady=(10, 5))

        self.but_url_entry = ttk.Entry(button_frame)
        self.but_url_entry.pack(pady=(0, 10))

        self.but_number_label = ttk.Label(button_frame, text="But Number:")
        self.but_number_label.pack(pady=(10, 5))

        self.but_number_entry = ttk.Entry(button_frame)
        self.but_number_entry.pack(pady=(0, 10))

        but_name_label2 = ttk.Label(button_frame, text="But Name:")
        but_name_label2.pack(pady=(10, 5))

        self.but_name_entry2 = ttk.Entry(button_frame)
        self.but_name_entry2.pack(pady=(0, 10))

        # 新增URL tab
        url_frame = ttk.Frame(self.nb)
        url_frame.pack(fill=tk.BOTH)

        module_name_label3 = ttk.Label(url_frame, text="Module Name:")
        module_name_label3.pack(pady=(10, 5))

        self.module_name_entry3 = ttk.Entry(url_frame)
        self.module_name_entry3.pack(pady=(0, 10))

        but_number_label3 = ttk.Label(url_frame, text="But Number")
        but_number_label3.pack(pady=(10, 5))

        self.but_number_entry3 = ttk.Entry(url_frame)
        self.but_number_entry3.pack(pady=(0, 10))

        new_but_url_label3 = ttk.Label(url_frame, text="New But URL:")
        new_but_url_label3.pack(pady=(10, 5))

        self.new_but_url_entry3 = ttk.Entry(url_frame)
        self.new_but_url_entry3.pack(pady=(0, 10))

        # 将三个tab加入Notebook中
        self.nb.add(module_frame, text="新增模块")
        self.nb.add(button_frame, text="新增button")
        self.nb.add(url_frame, text="新增URL")

        # 创建提交按钮
        submit_button = ttk.Button(main_frame, text="提交", command=self.submit)
        submit_button.pack(pady=10)

        # 创建下方的结果展示区域
        result_frame = ttk.LabelFrame(main_frame, text="结果")
        result_frame.pack(expand=True, fill=tk.BOTH, padx=10, pady=5)

        self.result_text = tk.Text(result_frame)
        self.result_text.pack(expand=True, fill=tk.BOTH, padx=5, pady=5)

        new_toplevel.mainloop()

    def submit(self):
        current_tab = self.nb.index("current")

        if current_tab == 0:
            parent_module_name = self.parent_module_name_entry.get()
            module_name = self.module_name_entry.get()
            new_module_url = self.new_module_url_entry.get()

            self.result_text.delete("1.0", tk.END)
            res = concat_sql.add_module(parent_module_name, module_name, new_module_url)
            self.result_text.insert(tk.END, f" {res.get('parent_id_sql')}\n")
            self.result_text.insert(tk.END, f" {res.get('max_rank_sql')}\n")
            self.result_text.insert(tk.END, f" {res.get('insert_module_sql')}\n")
        elif current_tab == 1:
            module_name = self.module_name_entry2.get()
            but_url = self.but_url_entry.get()
            but_number = self.but_number_entry.get()
            but_name = self.but_name_entry2.get()

            self.result_text.delete("1.0", tk.END)
            res = concat_sql.module_exists_add_but(module_name, but_url, but_number, but_name)
            self.result_text.insert(tk.END, f" {res.get('module_sql')}\n")
            self.result_text.insert(tk.END, f" {res.get('but_sql')}\n")
        elif current_tab == 2:
            module_name = self.module_name_entry3.get()
            but_number = self.but_number_entry3.get()
            new_but_url = self.new_but_url_entry3.get()

            self.result_text.delete("1.0", tk.END)
            res = concat_sql.but_exists_add_url(module_name, but_number, new_but_url)
            self.result_text.insert(tk.END, f" {res.get('module_sql')}\n")
            self.result_text.insert(tk.END, f" {res.get('module_but_sql')}\n")
            self.result_text.insert(tk.END, f" {res.get('update_but_sql')}\n")
