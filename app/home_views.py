
import os

from flask import Blueprint, render_template, session, jsonify, request, Config

from app.models import User, Facility, Area, HouseImage, House
from utils import status_code
from utils.setting import MEDIA_PATH

home_blue = Blueprint('home', __name__)


@home_blue.route('/index/', methods=['GET'])
def house():
    return render_template('index.html')


@home_blue.route('/hindex/', methods=['GET'])
def index():
    if 'user_id' in session:
        user = User.query.filter_by(id=session['user_id']).first()
        user_name = user.name
        code = status_code.OK
        return jsonify(code=code, name=user_name)


@home_blue.route('/myhouse/', methods=['GET'])
def myhouse():
    return render_template('myhouse.html')


@home_blue.route('/house_info/', methods=['GET'])
def house_info():
    user = User.query.get(session['user_id'])
    if user.id_card:
        # 实名认证成功
        houses = House.query.filter(House.user_id == session['user_id'])
        houses_list = [house.to_dict() for house in houses]
        return jsonify(code=status_code.OK, houses_list=houses_list)
    else:
        return jsonify({'code': 1016, 'msg': '错误'})


@home_blue.route('/imyhouse/', methods=['GET'])
def imyhouse():
    user_id = User.query.get(session['user_id'])
    user = user_id.to_auth_dict()
    return jsonify({'code': 200, 'msg': '请求成功', 'user': user})


@home_blue.route('/newhouse/', methods=['GET'])
def newhouse():
    return render_template('newhouse.html')


@home_blue.route('/newhouse/', methods=['POST'])
def newihouse():
    facility_ids = request.form.getlist('facility')
    house = House()
    house.user_id = session['user_id']
    house.area_id = request.form.get('area_id')
    house.title = request.form.get('title')
    house.price = request.form.get('price')
    house.address = request.form.get('address')
    house.room_count = request.form.get('room_count')
    house.acreage = request.form.get('acreage')
    house.beds = request.form.get('beds')
    house.unit = request.form.get('unit')
    house.capacity = request.form.get('capacity')
    house.deposit = request.form.get('deposit')
    house.min_days = request.form.get('min_days')
    house.max_days = request.form.get('max_days')
    if facility_ids:
        facility_list = Facility.query.filter(Facility.id.in_(facility_ids)).all()
        house.facilities = facility_list
    house.add_update()
    return jsonify({'code': 200, 'msg': '请求成功', 'house_id': house.id})


@home_blue.route('/area_facility/', methods=['GET'])
def area_facility():
    areas = Area.query.all()
    facilitys = Facility.query.all()
    areas_json = [area.to_dict() for area in areas]
    facilitys_json = [facility.to_dict() for facility in facilitys]
    return jsonify(code=status_code.OK, area=areas_json, facilitys=facilitys_json)


@home_blue.route('/image/', methods=['POST'])
def newhouse_image():
    house_id = request.form.get('house_id')
    f = request.files.get('house_image')
    url = os.path.join(MEDIA_PATH, f.filename)
    f.save(url)
    image = HouseImage()
    image.house_id = house_id
    image_url = os.path.join(f.filename)
    image.url = image_url
    image.add_update()
    house = House.query.get(house_id)
    if not house.index_image_url:
        house.index_image_url = os.path.join('/static/media/', f.filename)
        house.add_update()
    return jsonify(code='200', url=image_url)


@home_blue.route('/detail/', methods=['GET'])
def detail():
    return render_template('detail.html')


@home_blue.route('/user_house/', methods=['GET'])
def user_house():
    houses = House.query.filter(House.user_id == session['user_id']).all()
    houses_list = [house.to_dict() for house in houses]
    return jsonify({'code': 200, 'houses_list': houses_list})