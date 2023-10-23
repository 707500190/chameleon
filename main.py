import json
import os
import subprocess
import sys
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox

import requests

import gui.module_tk as mt
from auto_field_gui import AddColumnUI
from util.mysql_util import MySQLUtil
# 从文件中读取配置数据
with open('config.json', 'r') as f:
    config_dic = json.load(f)
dev_config = config_dic["env"]["dev"]
mysql_dev = MySQLUtil(dev_config["ip"], dev_config["username"], dev_config["password"], dev_config["schema"])
mysql_dev.connect()
version = 100


def update_application():
    try:
        check_update_sql = f"select * from support_software where code = 'GENERATE_AUTHORITY_SQL'  order by version desc"
        list_result = mysql_dev.execute_query(check_update_sql)
        entity = list_result[0]
        mysql_dev.disconnect()
        latest_version = entity.get("version")
        url = entity.get("url")
        filename = entity.get("filename")
        if version < latest_version:
            root = tk.Tk()
            root.withdraw()
            message_text = '有最新版本，是否更新？'
            result = messagebox.askyesno('版本更新', message_text)
            if result:
                # 下载远程服务器资源
                folder_path = filedialog.askdirectory()
                response = requests.get(url)
                if response.status_code == 200:
                    # 获取文件名
                    # filename = url.split('/')[-1]
                    file_path = os.path.join(folder_path, filename)
                    # 保存文件
                    with open(file_path, 'wb') as file:
                        file.write(response.content)
                    subprocess.run([file_path])
                    sys.exit()
                else:
                    messagebox.showinfo('提示', '更新失败！')
    except Exception as e:
        messagebox.showinfo('提示', '更新失败！')


'''
pyinstaller --onefile --add-data "image.png;." your_script.py

'''
if __name__ == '__main__':
    update_application()
    md = mt.ModuleTK()
    root = tk.Tk()
    AddColumnUI(root)
    root.mainloop()
    mysql_dev.disconnect()
