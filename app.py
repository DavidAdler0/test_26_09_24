from flask import Flask
from db import db
from bp import mission_bp



app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:da7104@localhost:5432/wwii_missions'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# db.init_app(app)
# with app.app_context():
#     db.create_all()


app.register_blueprint(mission_bp, url_prefix='/mission')


if __name__ == '__main__':
    app.run(debug=True)