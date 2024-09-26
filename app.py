from flask import Flask
from bp.admin import admin_bp
from bp.worker import worker_bp

app = Flask(__name__)


app.register_blueprint(admin_bp, url_prefix='/admin')
app.register_blueprint(worker_bp, url_prefix='/worker')

if __name__ == '__main__':
    app.run(debug=True)