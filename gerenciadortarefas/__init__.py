from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///gerenciador.db'
app.config['SECRET_KEY'] = '533b382bc1d38aa9afc99b3c163e623a889f5931bbdb9a9df76438d46841e43d'
app.config['UPLOAD_FOLDER'] = 'static/fotos_posts'

database = SQLAlchemy(app)
bcrypt= Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'index'

from gerenciadortarefas import routes, models