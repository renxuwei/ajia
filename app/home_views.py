import os
import uuid
from datetime import datetime

from flask import Blueprint, render_template, session, jsonify, request

from app.models import User, House, db, Facility, HouseImage, Order

home_blue = Blueprint('home', __name__)


@home_blue.route('/myhouse/', methods=['GET'])
def myhouse():
    use = User.query.get(session['user_id'])
    user = use.houses
    return render_template('myhouse.html', users = user)


@home_blue.route('/myhouse_info/', methods=['GET'])
def myhouse_info():
    user = User.query.get(session['user_id'])
    user = user.to_auth_dict()
    return jsonify({'code': 200, 'msg': 'ok', 'user': user})


@home_blue.route('/newhouse/', methods=['GET'])
def newhouse():

    return render_template('newhouse.html')


# 发布房源
@home_blue.route('/my_newhouse/',methods=['POST'])
def my_newhouse():
    title = request.form.get('title')
    price = request.form.get('price')
    area_id = request.form.get('area_id')
    address = request.form.get('address')
    room_count = request.form.get('room_count')
    acreage = request.form.get('acreage')
    unit = request.form.get('unit')
    capacity = request.form.get('capacity')
    beds = request.form.get('beds')
    deposit = request.form.get('deposit')
    min_days = request.form.get('min_days')
    max_days = request.form.get('max_days')
    facility = request.form.getlist('facility')

    house = House()
    user = User.query.get(session['user_id'])

    house.user_id = user.id

    house.title = title
    house.price = price
    house.area_id = area_id
    house.address = address
    house.room_count = room_count
    house.acreage = acreage
    house.unit = unit
    house.capacity = capacity
    house.beds = beds
    house.deposit = deposit
    house.min_days = min_days
    house.max_days = max_days

    for facilit in facility:
        fac = Facility.query.filter_by(id=facilit).first()
        house.facilities.append(fac)
        db.session.commit()

    house.add_update()

    return jsonify({'code': 200, 'msg': 'ok', 'house_id':house.id})


# 圖片上傳
@home_blue.route('/my_newhouse_info/', methods=['POST'])
def my_newhouse_info():
    # 接收图片并保存图片
    house_id = request.form.get('house_id')
    icon = request.files.get('house_image')
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
        image = HouseImage()
        image.house_id = house_id
        image.url = name
        image.add_update()

        house = House.query.get(house_id)
        if not house.index_image_url:
            house.index_image_url = name
            house.add_update()
        return jsonify({'code': 200, 'msg': '请求成功', 'name': name})


# 房源信息
@home_blue.route('/detail/<int:id>/', methods=['GET'])
def detail(id):
    house = House.query.get(id)
    img = house.images
    return render_template('detail.html', img = img, house=house)
    #return jsonify({'code':200, 'msg':'ok', 'img':img})


# 即可预订
@home_blue.route('/booking/<int:id>/', methods=['GET'])
def booking(id):

    house = House.query.get(id)
    img = house.index_image_url
    title = house.title
    price = house.price

    return jsonify({'code':200, 'msg':'ok', 'img':img, 'title':title, 'price':price})


@home_blue.route('/my_booking/', methods=['GET'])
def my_booking():

    return render_template('booking.html')


# 我的订单
@home_blue.route('/orders/', methods=['POST'])
def my_orders():

    if session:
        start = request.form.get('start')
        end = request.form.get('end')
        # span = request.form.get('span')
        house_id = request.form.get('house_id')

        starttime = datetime.strptime(start, '%Y-%m-%d')
        endtime = datetime.strptime(end, '%Y-%m-%d')

        house = House.query.get(house_id)
        order = Order()
        order.user_id = session['user_id']
        order.house_id = house_id
        order.begin_date = starttime
        order.end_date = endtime
        order.days = (endtime - starttime).days + 1
        order.house_price = house.price
        order.amount = order.days * order.house_price
        order.add_update()

        return jsonify({'code':200, 'msg':'ok'})
    else:
        return jsonify({ 'code':1122, 'msg':'未登录' })

@home_blue.route('/my_orders/', methods=['GET'])
def orders():

    return render_template('orders.html')


@home_blue.route('/myorders/', methods=['GET'])
def myorders():
    order = Order.query.filter_by(user_id = session['user_id']).all()
    orders_list = [ord.to_dict() for ord in order ]


    return jsonify({'code':200, 'msg':'ok', 'orders_list':orders_list})


# 客户订单
@home_blue.route('/lorders/', methods=['GET'])
def lorders():

    return render_template('lorders.html')

@home_blue.route('/order_status/', methods=['PATCH'])
def order_status():
    # 订单的状态
    # 获取参数
    order_id = request.form.get('order_id')
    status = request.form.get('status')
    comment = request.form.get('comment')

    order = Order.query.get(order_id)
    order.status = status
    if comment:
        order.comment = comment
    order.add_update()

    return jsonify({'code': 200, 'msg': '请求成功'})







# 主页



@home_blue.route('/search/', methods=['GET'])
def search():

    return render_template('search.html')