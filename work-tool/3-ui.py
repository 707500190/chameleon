import tkinter as tk


class SearchApp:
    def __init__(self, master):
        self.master = master
        master.title("搜索应用")

        # 创建搜索框和搜索按钮
        self.search_label = tk.Label(master, text="输入关键字：")
        self.search_label.pack(side=tk.LEFT)
        self.search_entry = tk.Entry(master, width=30)
        self.search_entry.pack(side=tk.LEFT)
        self.search_button = tk.Button(master, text="搜索", command=self.search)
        self.search_button.pack(side=tk.LEFT)

        # 创建输出框
        self.output_text = tk.Text(master, height=20, width=50)
        self.output_text.pack()

    def search(self):
        # 获取搜索关键字
        keyword = self.search_entry.get()

        # 调用自定义的搜索函数进行搜索
        # result = my_search_func.search(keyword)
        result = 'my_search_func.search(keyword)'

        # 清空输出框并显示搜索结果
        self.output_text.delete('1.0', tk.END)
        self.output_text.insert(tk.END, result)


root = tk.Tk()
app = SearchApp(root)
root.mainloop()
