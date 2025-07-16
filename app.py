from flask import Flask
from flask_mysqldb import MySQL
from models import user_models
from routes.user_routes import user_router

app = Flask(__name__)
app.secret_key = 'your_secret_key'
app.config.from_pyfile('config.py')

mysql = MySQL(app)
user_models.init_mysql(mysql)

app.register_blueprint(user_router)

if __name__ == '__main__':
    app.run(debug=True)
