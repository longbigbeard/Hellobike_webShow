from flask import Flask, render_template, request, jsonify
import pymysql

app = Flask(__name__)


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/index', methods=['GET', 'POST'])
def hello_world():
    # if request.method = 'GET'
    data = request.form
    data = data.to_dict()
    time = data["datas"]

    sql_time = deal_time(time)

    db = mysql_link()  # 打开数据库连接
    cursor = db.cursor()  # 使用 cursor() 方法创建一个游标对象 cursor

    sql_1 = "select * from whereis where time LIKE '%" + sql_time + "%';"
    sql_2 = "select * from whereis where time LIKE '%" + time + "%';"

    my_list = []
    try:
        # 执行SQL语句
        cursor.execute(sql_1)
        result = cursor.fetchall()
        if not result:
            cursor.execute(sql_2)
            result = cursor.fetchall()
        for line in result:
            values = [eval(line[4]), eval(line[3])]
            my_list.append(values)
    except:
        print("Error: unable to fetch data")
    db.close()

    return jsonify({"result": my_list})


# 处理前台传过来的时间
def deal_time(time):
    int_time = int(time[14:16])

    int_time = int_time + 1
    str_time = str(int_time)
    if len(str_time) < 2:
        sql_time = time[0:14] + '0' + str_time
    else:
        sql_time = time[0:14] + str_time

    return sql_time


# 连接数据库
def mysql_link():
    try:
        db = pymysql.connect(host="127.0.0.1", user="root",
                             passwd="*******",
                             db="db_bikes",
                             charset='utf8')
        return db
    except:
        print("could not connect to mysql server")


if __name__ == '__main__':
    app.run(debug=True)
