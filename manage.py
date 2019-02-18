
from flask import Flask
from flask_script import Manager

from app.user_views import user_blue
from app.home_views import home_blue
from app.order_views import order_blue
from app.models import db
from utils.setting import STATIC_PATH, TEMPLATE_PATH

app = Flask(__name__, static_folder=STATIC_PATH, template_folder=TEMPLATE_PATH)

app.register_blueprint(blueprint=user_blue, url_prefix='/user')
app.register_blueprint(blueprint=home_blue, url_prefix='/home')
app.register_blueprint(blueprint=order_blue, url_prefix='/order')

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:123456@127.0.0.1:3306/ihome8'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

app.secret_key = '23erg5hy54er89fg5hju'

manage = Manager(app)

if __name__ == '__main__':
    manage.run()