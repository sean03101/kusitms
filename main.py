from flask import Flask, session, app, request, render_template
from connection import mysql_info, mysql_connect
from exts import db

app = Flask(__name__, template_folder='view', static_url_path='', static_folder='static')
app.secret_key = 'horangsecrettt'
mysql = mysql_info.info

app.config['SECRET_KEY'] = 'horangsecrettt'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://'+mysql['user']+':'+mysql['password']+'@'+mysql['host']+'/'+mysql['db']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['POST_FILE'] = './static/images/post_file'

db.init_app(app)

from user import user
from product import product


app.register_blueprint(product.product_blue)
app.register_blueprint(user.user_blue)

app.run(host='0.0.0.0', port=5000)

