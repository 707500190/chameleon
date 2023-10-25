import tkinter as tk

root = tk.Tk()

# 创建一个标签控件，跨越两列
label = tk.Label(root, text="This is a label", padx=10, pady=10)
label.grid(row=0, column=0, columnspan=2)

# 创建两个按钮控件
button1 = tk.Button(root, text="Button 1")
button2 = tk.Button(root, text="Button 2")

# 将按钮控件放置在第一列和第二列
button1.grid(row=1, column=0)
button2.grid(row=1, column=1)

root.mainloop()