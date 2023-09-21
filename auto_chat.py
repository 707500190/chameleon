import pyperclip
from playwright.sync_api import Playwright, sync_playwright
from gui.chat_tk import ChameleonTk
import time

from util.mysql_util import MySQLUtil

mysql = MySQLUtil("localhost", "root", "root", "lock")
mysql.connect()


def run(pw: Playwright, keyword, module) -> None:
    browser = pw.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://chat.yqcloud.top/#/chat/")
    page.get_by_placeholder("Ask me anything...(Shift + Enter = line break)").click()
    page.get_by_placeholder("Ask me anything...(Shift + Enter = line break)").fill(keyword)
    page.get_by_placeholder("Ask me anything...(Shift + Enter = line break)").press("Enter")
    time.sleep(10)
    page.get_by_text("Copy Code").click()
    # 从剪贴板中获取值
    value = pyperclip.paste()
    # 打印获取到的值
    res = mysql.execute_query(value)
    print(res)
    context.close()
    browser.close()
    return res


def a_func(keyword, module):
    with sync_playwright() as playwright:
        return run(playwright, keyword, module)


if __name__ == '__main__':
    c_tk = ChameleonTk()
