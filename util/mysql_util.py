import mysql.connector


class MySQLUtil:
    def __init__(self, host, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.connection = None

    def connect(self):
        self.connection = mysql.connector.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database
        )

    def disconnect(self):
        if self.connection.is_connected():
            self.connection.close()

    def execute_query(self, query):
        cursor = self.connection.cursor()
        cursor.execute(query)
        result = cursor.fetchall()
        cursor.close()
        return result

    def execute_update(self, query):
        cursor = self.connection.cursor()
        cursor.execute(query)
        self.connection.commit()
        cursor.close()


# 使用示例
if __name__ == "__main__":
    util = MySQLUtil("localhost", "root", "password", "mydatabase")
    util.connect()

    # 执行查询
    query = "SELECT * FROM users"
    result = util.execute_query(query)
    for row in result:
        print(row)

    # 执行更新
    update_query = "UPDATE users SET name = 'Alice' WHERE id = 1"
    util.execute_update(update_query)

    util.disconnect()
