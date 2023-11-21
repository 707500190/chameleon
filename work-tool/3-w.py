import sqlite3

from docx import Document

# 模拟入库操作的函数


# 连接数据库
conn = sqlite3.connect('s.db')
c = conn.cursor()


def save_to_database(data):
    for item in data:
        c.execute("INSERT INTO questions (content) VALUES (?)", (item,))
    conn.commit()
    # 这里可以编写将数据存入数据库的代码


def parse_docx_file(docx_file):
    document = Document(docx_file)

    content_array = []
    content = ""
    start_extraction = False
    count = 0

    for paragraph in document.paragraphs:
        text = paragraph.text.strip()

        if start_extraction:
            if "题目解析" in text:
                # 如果遇到下一个题目解析，将内容存入数组并清空content
                content_array.append(content)
                content = ""
                count += 1
                # 当数组大小达到50时执行入库操作
                if count == 50:
                    save_to_database(content_array)
                    content_array = []
                    count = 0
                start_extraction = False
            else:
                content += text + "\n"
        if "题目解析" in text:
            start_extraction = True

    # 处理最后一部分未入库的内容
    if content:
        content_array.append(content)
        if len(content_array) > 0:
            save_to_database(content_array)


# 指定docx文件路径
docx_file = "dest.docx"
# 调用函数解析docx文件
parse_docx_file(docx_file)

conn.close()
