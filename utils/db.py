import pymysql
import os

DB_CONF = {
    'host': os.getenv('MYSQL_HOST'),
    'port': int(os.getenv('MYSQL_PORT')),
    'db': os.getenv('MYSQL_DB'),
    'user': os.getenv('MYSQL_USER'),
    'password': os.getenv('MYSQL_PWD'),
    'charset': 'utf8',
    'autocommit': True
}

class DB(object):
    def __init__(self):
        # print("建立数据库连接")
        self.conn = pymysql.connect(**DB_CONF)
        self.cur = self.conn.cursor()  # 建立游标

    def execute(self, sql):
        # print(f"执行sql: {sql}")
        self.cur.execute(sql)
        result = self.cur.fetchall()
        # print(f"执行结果: {result}")
        return result

    def close(self):
        # print("关闭数据库连接")
        self.conn.close()


class LongTengServer(DB):
    """该项目数据库的常用业务操作封装"""
    def del_card(self, card_number):
        if self.check_card(card_number):
            # print(f"数据库删除加油卡: {card_number}")
            sql = f'DELETE FROM cardinfo WHERE cardNumber="{card_number}"'
            self.execute(sql)

    def check_card(self, card_number):
        # print(f"数据库查询加油卡: {card_number}")
        sql = f'SELECT cardNumber FROM cardinfo WHERE cardNumber="{card_number}"'
        result = self.execute(sql)
        return True if result else False  # 如果result为真(非()),返回True, 否则返回False

    def add_card(self, card_number):
        if not self.check_card(card_number):
            print(f'数据库插入加油卡: {card_number}')
            sql = f'INSERT INTO cardinfo (`cardNumber`) VALUES ("{card_number}")'
            result = self.execute(sql)



# 模块私有代码
if __name__ == '__main__': # 一般用来调试当前模块, 只有从当前模块运行时才执行
    # db = DB()
    # # r = db.execute('select cardNumber from cardInfo where cardNumber="123456abc"')
    # # print(r)
    #
    # db.close()
    db = LongTengServer()
    db.add_card('12345')
    db.check_card('12345')

    db.close()
