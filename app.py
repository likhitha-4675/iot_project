from flask import Flask
from flask_mysqldb import MySQL
from models import user_models, connected_models
from routes.user_routes import user_router
from routes.connected_routes import connected_router


app = Flask(__name__)
app.secret_key = 'your_secret_key'
app.config.from_pyfile('config.py')

mysql = MySQL(app)
user_models.init_mysql(mysql)
connected_models.init_mysql(mysql)
app.register_blueprint(user_router)
app.register_blueprint(connected_router)

if __name__ == '__main__':
    app.run(debug=True)
