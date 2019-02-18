import os
import re
import random
import uuid

from flask import Blueprint, render_template, jsonify, request, session, url_for, redirect


from app.models import User, db, House, Area, Order
from utils import status_code
from utils.function import login_required

user_blue = Blueprint('user', __name__)


@user_blue.route('/register/', methods=['GET'])
def register():

    return render_template('register.html')


# 后端做的
@user_blue.route('/register/', methods=['POST'])
def my_register():

    # 获取参数
    mobile = request.form.get('mobile')
    imagecode = request.form.get('imagecode')
    passwd = request.form.get('passwd')
    passwd2 = request.form.get('passwd2')
    # 1. 验证参数是否都填写了
    if not all([mobile, imagecode, passwd, passwd2]):
        return jsonify({'code': 1001, 'msg': '请填写完整参数'})

    # 2. 验证手机号是否正确
    if not re.match('^1[3456789]\d{9}$', mobile):
        return jsonify({'code': 1002, 'msg': '手机号不正确'})

    # 3. 验证图片验证码
    if session['img_code'] != imagecode:
        return jsonify({'code': 1003, 'msg': '验证码不正确'})

    # 4. 密码和确认密码是否一致
    if passwd != passwd2:
        return jsonify({'code': 1004, 'msg': '密码不一致'})

    # 验证手机号是否被注册
    user = User.query.filter_by(phone=mobile).first()
    if user:
        return jsonify({'code': 1005, 'msg': '手机号已被注册，请重新注册'})

    # 创建注册信息
    user = User()
    user.phone = mobile
    user.name = mobile
    user.password = passwd
    user.add_update()
    return jsonify({'code': 200, 'msg': '请求成功'})


@user_blue.route('/code/', methods=['GET'])
def get_code():
    # 获取验证码
    # 方式1：后端生成图片，并返回验证码图片的地址（不推荐）
    # 方式2：后端只生成随机参数，返回给页面，在页面中再生成图片（前端做）
    s = '1234567890qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM'
    code = ''
    for i in range(4):
        code += random.choice(s)
    session['img_code'] = code
    return jsonify({'code': 200, 'msg': '请求成功', 'data': code})


@user_blue.route('/login/', methods=['GET'])
def login():

    return render_template('login.html')


@user_blue.route('/login/', methods=['POST'])
def my_login():
    mobile = request.form.get('mobile')
    passwd = request.form.get('passwd')
    if not all([mobile, passwd]):
        return jsonify({'code': 1011, 'msg': '请填写完整参数'})

    user = User.query.filter_by(phone=mobile).first()
    if not user:
        return jsonify({'code': 1012, 'msg': '账号错误'})

    if not user.check_pwd(passwd):
        return jsonify({'code': 1013, 'msg': '密码不正确'})

    session['user_id'] = user.id
    return jsonify({'code': 200, 'msg': 'ok'})


@user_blue.route('/my/', methods=['GET'])
@login_required
def my():
    return render_template('my.html')


@user_blue.route('/user_info/', methods=['GET'])
@login_required
def user_info():
    # 获取用户基本信息
    user_id = session['user_id']
    user = User.query.get(user_id)
    return jsonify({'code':200, 'msg': '请求成功', 'data': user.to_basic_dict()})


@user_blue.route('/profile/', methods=['GET'])
def profile():

    return render_template('profile.html')


# 退出，清除session中user_id
@user_blue.route('/logout/', methods=['GET'])
def logout():
    session.pop('user_id')
    return jsonify({ 'code':200, 'msg': '请求成功' })


# 圖片上傳
@user_blue.route('/profile/', methods=['POST'])
def my_profile():
    # 接收图片并保存图片
    icon = request.files.get('avatar')
    nameee = request.form.get('name')
    if icon:
        # 获取项目根路径
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        # 获取媒体文件的路径
        STSTIC_DIR = os.path.join(BASE_DIR, 'static')
        MEDIA_DIR = os.path.join(STSTIC_DIR, 'media')
        # 随机生成图片名称
        filename = str(uuid.uuid4())
        a = icon.mimetype.split('/')[-1:][0]
        name = filename + '.' + a
        # 拼接图片地址，并保存到/static/media/文件家中
        path = os.path.join(MEDIA_DIR, name)
        icon.save(path)
        # print(icon)
        # 修改用户头像icon字段
        user_id = session['user_id']
        user = User.query.get(user_id)

        # 删除原有的图片文件
        os.remove(os.path.join(MEDIA_DIR, user.avatar))

        # 修改数据库中的照片存储
        user.avatar = name
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('user.profile'))

    if nameee:
        user_id = session['user_id']
        user = User.query.get(user_id)
        user.name = nameee
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('user.profile'))


# 实名认证
@user_blue.route('/auth/', methods=['GET'])
def auth():

    return render_template('auth.html')


# 渲染页面时，如果以实名认证（数据库中有身份信息，就返回到前段）
@user_blue.route('/auth_info/', methods=['GET'])
def auth_info():
    user = User.query.get(session['user_id'])
    user = user.to_auth_dict()
    return jsonify({'code':200, 'msg':'ok', 'user':user})


@user_blue.route('/auth/', methods=['POST'])
def my_auth():
    name = request.form.get('name')

    num = request.form.get('num')
    if not all([name, num]):
        return jsonify({'code': 1101, 'msg': '请填写完整信息'})
    if len(name) < 2 or len(name) > 4:
        return jsonify({ 'code':1102, 'msg': '姓名有误，在2~4个字符之间' })
    if not re.match('(^[1-9]\d{5}(18|19|([23]\d))\d{2}((0[1-9])|(10|11|12))(([0-2][1-9])|10|20|30|31)\d{3}[0-9Xx]$)|(^[1-9]\d{5}\d{2}((0[1-9])|(10|11|12))(([0-2][1-9])|10|20|30|31)\d{2}$)', num):
        return jsonify({'code': 1103, 'msg': '身份证号有误'})

    user_id = session['user_id']
    user = User.query.get(user_id)
    user.id_name = name
    user.id_card = num
    db.session.add(user)
    db.session.commit()

    return jsonify({'code': 200, 'msg':'ok'})


# 主页
@user_blue.route('/index/', methods=['GET'])
def index():
    house = House.query.order_by('-id').all()[0:3]
    return render_template('index.html', house=house)


@user_blue.route('/my_index/', methods=['GET'])
def my_index():
    if 'user_id' in session:
        user = User.query.filter_by(id=session['user_id']).first()
        nem = user.name
        return jsonify({'code':200, 'msg':'ok', 'name':nem})


@user_blue.route('/search/', methods=['GET'])
def search():

    return render_template('search.html')


@user_blue.route('/my_search/', methods=['GET'])
def my_search():
    sort_key = request.args.get('sk')  # 排序
    a_id = request.args.get('aid')  # 区域
    begin_date = request.args.get('sd')  # 入住时间
    end_date = request.args.get('ed')  # 离店时间

    houses = House.query.filter_by(area_id=a_id)
    # 不能查询自己发布的房源，排除当前用户发布的房屋
    if 'user_id' in session:
        hlist = houses.filter(House.user_id != (session['user_id']))

    # 满足时间条件，查询入住时间和退房时间在首页选择时间内的房间，并排除掉这些房间
    order_list = Order.query.filter(Order.status != 'REJECTED')
    # 情况一：
    order_list1 = Order.query.filter(Order.begin_date >= begin_date, Order.end_date <= end_date)
    # 情况二：
    order_list2 = order_list.filter(Order.begin_date < begin_date, Order.end_date > end_date)
    # 情况三：
    order_list3 = order_list.filter(Order.end_date >= begin_date, Order.end_date <= end_date)
    # 情况四：
    order_list4 = order_list.filter(Order.begin_date >= begin_date, Order.begin_date <= end_date)
    # 获取订单中的房屋编号
    house_ids = [order.house_id for order in order_list2]
    for order in order_list3:
        house_ids.append(order.house_id)
    for order in order_list4:
        if order.house_id not in house_ids:
            house_ids.append(order.house_id)
    # 查询排除入住时间和离店时间在预约订单内的房屋信息
    hlist = hlist.filter(House.id.notin_(house_ids))

    # 排序规则,默认根据最新排列
    sort = House.id.desc()
    if sort_key == 'booking':
        sort = House.order_count.desc()
    elif sort_key == 'price-inc':
        sort = House.price.asc()
    elif sort_key == 'price-des':
        sort = House.price.desc()
    hlist = hlist.order_by(sort)
    hlist = [house.to_dict() for house in hlist]

    # 获取区域信息
    area_list = Area.query.all()
    area_dict_list = [area.to_dict() for area in area_list]

    return jsonify(code=status_code.OK, houses=hlist, areas=area_dict_list)
    return jsonify({'code':200, 'msg':'ok'})


