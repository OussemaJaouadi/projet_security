from routes import bp
from flask import Flask
from model import db,Post
import datetime

def create_app():
# Create Flask app
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///example.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize database connection
    db.init_app(app)

# Create database tables
    with app.app_context():
        db.create_all()

    with app.app_context():
        test = Post("UCL Quarter","Sports","Some Details","Tommy",datetime.date.today())
        db.session.add(test)
        db.session.commit()
    app.register_blueprint(bp)
    return app

if __name__ == "__main__":
    front = create_app()
    front.run(debug=True,port=8000)