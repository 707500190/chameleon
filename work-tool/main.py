import os
import subprocess
import sys
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox

import requests

import gui.general_sql_gui as mt
from gui.auto_field_gui import AddColumnUI
from util.mysql_util import MySQLUtil

# # 从文件中读取配置数据
# with open('config.json', 'r') as f:
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

dev_config = config_dic["env"]["dev"]
mysql_dev = MySQLUtil(dev_config["ip"], dev_config["username"], dev_config["password"], dev_config["schema"])
mysql_dev.connect()
version = 103


def get_platform_type():
    import platform
    system_type = platform.system()
    if system_type == 'Windows':
        return 'Windows'
    elif system_type == 'Linux':
        return 'Linux'
    elif system_type == 'Darwin':
        return 'macOS'
    else:
        return 'Windows'


def update_application():
    """
   检查更新
    """
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
        mysql_dev.disconnect()
        print("更新失败！", e)
        messagebox.showinfo('提示', '更新失败！')


def generate_authority_sql(root):
    mt.GeneralSqlUI(root)


def add_column(root2):
    AddColumnUI(root2)


'''
pyinstaller --onefile --window --icon=img/1.ico main.py

'''
if __name__ == '__main__':
    update_application()

    root = tk.Tk()
    root.title("工具")
    root.geometry("300x200")

    button1 = tk.Button(root, text="生成权限 SQL", command=lambda: generate_authority_sql(root))
    button1.pack(pady=20)

    button2 = tk.Button(root, text="一键新增字段", command=lambda: add_column(root))
    button2.pack()
    root.mainloop()
