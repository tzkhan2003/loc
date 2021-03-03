from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app
from flaskblog import db, login_manager
from flask_login import UserMixin
import json

#    comnt = db.relationship('Comment', backref='author')
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    birth_date = db.Column(db.DateTime, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    type = db.Column(db.String(5), nullable=False, default='user')
    posts = db.relationship('Post', backref='author', lazy=True)
    order = db.relationship('CustomerOrder', backref='author6', lazy=True)
    comnt = db.relationship('Comment', backref='author1', lazy=True)
    product = db.relationship('Product', backref='author5', lazy=True)
    reactor = db.relationship('React', backref='author3', lazy=True)

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"


class Post(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    post_file = db.Column(db.String(20))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    comntt = db.relationship('Comment', backref='author2', lazy=True)
    post_react = db.relationship('React', backref='author4', lazy=True)
    

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"

class Product(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.String(100), nullable=False)
    discount = db.Column(db.String(100), nullable=False)
    stock = db.Column(db.String(100), nullable=False)
    colors = db.Column(db.String(100), nullable=False)
    desc = db.Column(db.String(100), nullable=False)
    brand = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    image_1 = db.Column(db.String(20), nullable=False, default='default.jpg')
    image_2 = db.Column(db.String(20), nullable=False, default='default.jpg')
    image_3 = db.Column(db.String(20), nullable=False, default='default.jpg')

class Comment(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    comment_content = db.Column(db.String(200), nullable=False)
    date_comment = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    comm_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
    	
    def __repr__(self):
        return f"Comment('{self.comment_content}', '{self.date_comment}')"

class React(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    react_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)

    def __repr__(self):
        return f"React('{self.react_id}', '{self.post_id}')"

class Brandname(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    brand_name= db.Column(db.String(200), nullable=False)
    brand_det = db.Column(db.String(200), nullable=False)
        
    def __repr__(self):
        return f"Comment('{self.brand_name}', '{self.brand_det}')"

class Catagoryname(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    catagory_name= db.Column(db.String(200), nullable=False)
    catagory_det = db.Column(db.String(200), nullable=False)
        
    def __repr__(self):
        return f"Comment('{self.catagory_name}', '{self.catagory_det}')"

class SellerId(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    birth_date = db.Column(db.DateTime, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    trade = db.Column(db.String(60), nullable=False)
    nid = db.Column(db.String(60), nullable=False)
    address = db.Column(db.String(60), nullable=False)
    phone = db.Column(db.String(60), nullable=False)
    shopname = db.Column(db.String(60), nullable=False)

    def __repr__(self):
        return f"Comment('{self.username}', '{self.email}', '{self.birth_date}', '{self.password}', '{self.address}', '{self.phone}', '{self.shopname}')"

class JsonEcodedDict(db.TypeDecorator):
    impl = db.Text
    def process_bind_param(self, value, dialect):
        if value is None:
            return '{}'
        else:
            return json.dumps(value)
    def process_result_value(self, value, dialect):
        if value is None:
            return {}
        else:
            return json.loads(value)

class CustomerOrder(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    invoice = db.Column(db.String(20), unique=True, nullable=False)
    status = db.Column(db.String(20), default='Pending', nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    orders = db.Column(JsonEcodedDict)

    def __repr__(self):
        return'<CustomerOrder %r>' % self.invoice