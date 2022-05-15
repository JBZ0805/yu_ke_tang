'''
定义用户类,课程班级类和课程类
用户必须先登录或者账号，再以自己的账号的身份输入班级号，加入班级
班级类和课程类都是用户类的子类
'''
import pymysql

# 连接数据库，此前在数据库中创建数据库yuketang
db = pymysql.connect(host="localhost", user="root", password="123456", db="yuketang")
# 使用cursor()方法获取操作游标
cursor = db.cursor()


# 定义用户类
class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password

    # 登录账号
    def login(self):
        # ping()使用该方法 ping(reconnect=True) ，那么可以在每次连接之前，会检查当前连接是否已关闭，如果连接关闭则会重新进行连接。
        db.ping(reconnect=True)
        # 编写sql语句，用来查询前端输入的用户名与数据库中user表对应的密码
        sql = "select password from user where username='" + self.username + "'"
        # 执行sql语句
        cursor.execute(sql)
        # 将数据从数据库读出 类型为元组类型
        results = cursor.fetchone()
        # 判断前端输入的密码是否与数据库密码一致，一致则返回1
        if self.password in results:
            return 1
        # 关闭数据库
        db.close()

    # 注册账号
    def register(self):
        # ping()使用该方法 ping(reconnect=True) ，那么可以在每次连接之前，会检查当前连接是否已关闭，如果连接关闭则会重新进行连接。
        db.ping(reconnect=True)
        # 插入sql语句
        sql_0 = "INSERT INTO user(username,password) VALUES(%s,%s)"
        sql = sql_0 % (repr(self.username), repr(self.password))
        # 执行sql语句
        cursor.execute(sql)
        # 提交到数据库执行
        db.commit()
        # 关闭数据库
        db.close()

    # 查询用户所在班级的方法
    def show_user(self):
        # ping()使用该方法 ping(reconnect=True) ，那么可以在每次连接之前，会检查当前连接是否已关闭，如果连接关闭则会重新进行连接。
        db.ping(reconnect=True)
        # 插入sql语句
        sql = "SELECT classid FROM class WHERE username='" + self.username + "'"
        #执行sql语句，对该用户在class表中没有记录抛出异常，并将返回的结果赋值为None
        try:
            # 执行sql语句
            cursor.execute(sql)
            # 将数据从数据库读出 类型为元组类型 转成字符串
            results = ''.join(cursor.fetchone())
            #关闭数据库
            db.close()
            return results
        except:
            results=None
            db.close()
            return results

# 定义课程班级类 班级类继承用户类
class Course_class(User):
    def __init__(self, username, password, class_id):
        super().__init__(username, password)
        self.class_id = class_id

    # 查询用户所在的班级成员的方法
    def show_class_member(self):
        # ping()使用该方法 ping(reconnect=True) ，那么可以在每次连接之前，会检查当前连接是否已关闭，如果连接关闭则会重新进行连接。
        db.ping(reconnect=True)
        if self.class_id==None:
            results1=[]
        else:
            # 插入sql语句
            sql = "SELECT username FROM class WHERE classid='" + self.class_id + "'"
            # 执行sql语句
            cursor.execute(sql)
            # 将数据从数据库读出 类型为多个元组
            results = cursor.fetchall()
            # 定义一个空列表
            results1 = []
            # 遍历元组中每个元素，将每个元素转化为字符串并添加至列表中
            for item in results:
                results1.append(''.join(item))
            # 关闭数据库
            db.close()
        # 返回结果
        return results1
    #加入班级
    def add_class(self):
        # ping()使用该方法 ping(reconnect=True)
        db.ping(reconnect=True)
        #编写sql语句
        sql_0 = "INSERT INTO class(username,classid) VALUES(%s,%s)"
        sql = sql_0 % (repr(self.username), repr(self.class_id))
        cursor.execute(sql)
        # 提交到数据库执行
        db.commit()
        # 关闭数据库
        db.close()



# 定义课程类 课程类继承于用户类
class Course(User):
    def __init__(self, username, password, course_id, course_name):
        super().__init__(username, password)
        self.course_id = course_id
        self.course_name = course_name

    # 定义查询课程的方法
    def search_course(self):
        # ping()使用该方法 ping(reconnect=True) ，那么可以在每次连接之前，会检查当前连接是否已关闭，如果连接关闭则会重新进行连接。
        db.ping(reconnect=True)
        # 插入sql语句
        sql = "SELECT courseid,coursename FROM course WHERE username='" + self.username + "'"
        # 执行sql语句
        cursor.execute(sql)
        # 将数据从数据库读出 类型为多个元组
        results = cursor.fetchall()
        # 定义一个空列表
        course_list = []
        # 将返回的元组通过遍历转成字典，最后再将字典存入列表中
        for items in results:
            results1 = [items]
            for item in results1:
                course_dict = {item[0]: item[1]}
                course_list.append(course_dict)
        # 关闭数据库
        db.close()
        return course_list

    # 添加课程并加入到数据库
    def add_course(self):
        # ping()使用该方法 ping(reconnect=True)
        db.ping(reconnect=True)
        # 插入sql语句
        sql_0 = "INSERT INTO course(username,courseid,coursename) VALUES(%s,%s,%s)"
        sql = sql_0 % (repr(self.username), repr(self.course_id), repr(self.course_name))
        # 执行sql语句
        cursor.execute(sql)
        # 提交到数据库执行
        db.commit()
        # 关闭数据库
        db.close()
