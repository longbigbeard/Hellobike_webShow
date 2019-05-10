import pymysql
import sys

'''
    连接数据库
    args：db_name（数据库名称）
    returns:db
'''


def mysql_link():
    try:
        db = pymysql.connect(host="127.0.0.1", user="root",
                             passwd="******",
                             db="db_bikes",
                             charset='utf8')
        return db
    except:
        print("could not connect to mysql server")


'''
    执行插入操作
    args:db_name（数据库名称）
         table_name(表名称）
         excel_file（excel文件名，把文件与py文件放在同一目录下）

'''


def store_to():
    db = mysql_link()  # 打开数据库连接
    cursor = db.cursor()  # 使用 cursor() 方法创建一个游标对象 cursor
    mylist = []  # 定义列表用来存放数据
    num = 0  # 用来控制每次插入的数量

    with open("bick.txt") as fp:
        data = fp.readlines()
    print("数据总量：%s" % len(data))
    for da in data:
        da = da.strip()
        dd = da.split("\t")

        value = (dd[0], dd[1], dd[2], dd[3])
        mylist.append(value)  # 将数据暂存在列表

        num += 1
        if (num >= 10000):  # 每一万条数据执行一次插入
            print("执行插入一万条")
            sql = "INSERT INTO whereis (time, user, longitude, latitude) VALUES(%s,%s,%s,%s)"
            cursor.executemany(sql, mylist)  # 执行sql语句

            num = 0  # 计数归零
            mylist.clear()  # 清空list
    sql = "INSERT INTO whereis (time, user, longitude, latitude) VALUES(%s,%s,%s,%s)"
    cursor.executemany(sql, mylist)  # 执行sql语句
    mylist.clear()  # 清空list
    print("插入结束")
    db.commit()  # 提交
    cursor.close()  # 关闭连接
    db.close()


if __name__ == '__main__':
    store_to()
