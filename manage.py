
from flask import Flask
from flask_script import Manager

from app.home_views import home_blue
from app.models import db
from app.user_views import user_blue


app = Flask(__name__)

app.register_blueprint(blueprint=user_blue, url_prefix='/user')
app.register_blueprint(blueprint=home_blue, url_prefix='/home')


app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:123456@127.0.0.1:3306/aijia'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

app.secret_key = '1220faslfj2002342lalf232-42'


manage = Manager(app)

if __name__ == '__main__':
    manage.run()
