import os
from flask import Flask, render_template, request, session, redirect
import userdata as ud
from os import path
import time

app = Flask(__name__)
# 设置秘钥
app.secret_key = 'weruihjsighwajkabiu123'
app.config['uploads'] = 'static/uploads'
#app.config.from_object('c')


# 默认界面设置为登录界面
@app.route('/')
def login1():
    return redirect('/login')


# 主界面接口(显示用户登录的用户名即个人信息)
@app.route('/index', methods=['GET', 'POST'])  # 这里写入的是接口名称，即URL地址
def main_interface():
    # 从用户会话中获取到用户名
    username = session.get('username')
    # 获取用户在前端输入的课程号
    course_id = request.form.get('course_id')
    # 获取用户在前端输入的课程名
    course_name = request.form.get('course_name')
    # 创建实例化对象user
    user = ud.User(username, '')
    # 调用方法，获取用户的班级号
    class_id = user.show_user()
    # 创建Course_class类中的实例化对象
    course_class = ud.Course_class(username, '', class_id)
    # 对班级号进行判断，如果班级号为空，并且是POST请求，则将前端数据赋值给该用户
    if class_id == None:
        if request.method == 'POST':
            class_id1 = request.form.get('class-id')
            # 赋值完成后，重新创建Course_class类实例化对象
            course_class1 = ud.Course_class(username, '', class_id1)
            # 调用方法，将班级号加到数据库中
            course_class1.add_class()
            return redirect('/index')
    # 调用展示班级成员的方法
    class_member = course_class.show_class_member()
    # 创建Course类中的实例化对象
    course = ud.Course(username, '', course_id, course_name)
    if request.method == 'POST':
        course.add_course()
    course_list = course.search_course()
    # 将用户名 班级号 班级成员 课程列表传入前端
    return render_template('index.html', username=username, class_id=class_id, class_member=class_member,
                           course_list=course_list)


# 登录接口
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    if request.method == 'POST':
        username = request.form.get('username')  # 接收来自前台的账号
        password = request.form.get('password')  # 接收来自前台的密码
        user = ud.User(username, password)
        logins = user.login()
        if logins == 1:
            # 将用户名存储至用户会话中，用户会话是一种私有存储，默认情况下，会保存在cookie中。
            session['username'] = username
            return redirect('/index')

        else:
            return '账户密码错误，请重新登录'
# 注册接口
@app.route('/register', methods=['GET', 'POST'])
def register():
    # 判断是get请求还是post请求
    if request.method == 'GET':
        return render_template('register.html')
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = ud.User(username, password)
        user.register()
        return redirect('/login')


# 主页跳转至资源库页面的接口
@app.route('/upload')
def show_upload():
    username = session.get('username')
    user = ud.User(username, '')
    class_id = ''.join(user.show_user())
    return render_template('upload.html', username=username, class_id=class_id)


@app.route('/upload', methods=['POST'])
def upload_file():
    file_list = []
    file_time = []
    if request.method == 'POST':
        # 获得前端上传的文件
        f = request.files['file']
        # 将其保存在static下的uploads文件夹中
        f.save(path.join(app.config['uploads'], f.filename))
        # 对uploads文件夹下所有的文件进行遍历
        for item in os.walk(app.config['uploads']):
            # os.walk函数执行后，会产生(root,dirs,files)的三元组
            # root所指的是当前正在遍历的这个文件夹的本身的地址
            # dirs是一个 list,内容是该文件夹中所有的目录的名字(不包括子目录)
            # files 同样是 list,内容是该文件夹中所有的文件(不包括子目录)
            for items in item[2]:
                file_list.append(items)
        for items1 in file_list:
            # 获取上传文件时的时间，并对其格式化
            a = os.path.getctime(app.config['uploads'] + f'/{items1}')
            b = time.localtime(a)
            c = time.strftime("%Y-%m-%d %H:%M:%S", b)
            file_time.append(c)
        # 将两个列表打包，方便前端遍历展示
        zip_list = zip(file_list, file_time)
        return render_template('upload.html', zip_list=zip_list, file_list=file_list)


# 删除上传的文件
@app.route("/delete/<file>")
def delete_file(file):
    file_list = []
    file_time = []
    # 需要删除的文件路径
    path = app.config['uploads'] + f"/{file}"
    # 删除文件
    os.remove(path)
    for item in os.walk(app.config['uploads']):
        for items in item[2]:
            file_list.append(items)
    for items1 in file_list:
        a = os.path.getctime(app.config['uploads'] + f'/{items1}')
        b = time.localtime(a)
        c = time.strftime("%Y-%m-%d %H:%M:%S", b)
        file_time.append(c)
    zip_list = zip(file_list, file_time)
    return render_template('upload.html', zip_list=zip_list, file_list=file_list)


if __name__ == '__main__':
    app.run()
