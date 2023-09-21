import tkinter as tk


class ChameleonTk:

    def __init__(self):
        root = tk.Tk()
        root.title = 'chameleon'

        # 创建标签和输入框控件
        keyword_label = tk.Label(root, text="Keyword text:")
        keyword_label.pack()
        self.keyword_entry = tk.Entry(root)
        self.keyword_entry.pack()

        module_label = tk.Label(root, text="Module Name:")
        module_label.pack()
        self.module_entry = tk.Entry(root)
        self.module_entry.pack()

        submit_button = tk.Button(root, text="Submit", command=self.submit)
        submit_button.pack()

        # 创建输出文本框控件
        result_label = tk.Label(root, text="Result:")
        result_label.pack()
        self.result_text = tk.Text(root, height=10)
        self.result_text.pack()

        root.mainloop()

    def submit(self):
        keyword = self.keyword_entry.get()
        module = self.module_entry.get()
        from auto_chat import a_func
        result = a_func(keyword, module)
        # 在这里可以使用获取到的输入值进行相应的处理逻辑
        self.result_text.delete(1.0, tk.END)  # 清空之前的输出内容
        self.result_text.insert(tk.END, "result:\n {}".format(result))
