from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

db = SQLAlchemy()

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)  # hashed
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text, nullable=True)
    image_url = db.Column(db.String(255), nullable=True)
    rating = db.Column(db.Float, nullable=True)
    stock_quantity = db.Column(db.Integer, default=0)
    brand = db.Column(db.String(100), nullable=True)

    @property
    def in_stock(self):
        return self.stock_quantity > 0

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "category": self.category,
            "price": self.price,
            "description": self.description,
            "image": self.image_url,
            "rating": self.rating,
            "inStock": self.in_stock,
            "stock_quantity": self.stock_quantity,
            "brand": self.brand
        }

class ChatSession(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    title = db.Column(db.String(255), nullable=True)
    user = db.relationship('User', backref=db.backref('chat_sessions', lazy=True))

class ChatLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.Integer, db.ForeignKey('chat_session.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    message = db.Column(db.Text, nullable=False)
    sender = db.Column(db.String(20), nullable=False)  # 'user' or 'bot'
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    session = db.relationship('ChatSession', backref=db.backref('messages', lazy=True))
    user = db.relationship('User')

class Users(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.String(36), primary_key=True)  # UUID as string
    user_id = db.Column(db.Integer, unique=True)  # Link to user table if needed
    first_name = db.Column(db.String(255))
    last_name = db.Column(db.String(255))
    gender = db.Column(db.String(10))
    mail = db.Column(db.String(255))
    phone = db.Column(db.String(20))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Address(db.Model):
    __tablename__ = 'addresses'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, nullable=False)
    label = db.Column(db.String(20), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    address = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Orders(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, nullable=False)  # Changed from String to Integer
    total_amount = db.Column(db.Float, nullable=False)
    payment_method = db.Column(db.String(10), nullable=False)  # 'UPI' or 'QR'
    payment_details = db.Column(db.Text, nullable=True)
    status = db.Column(db.String(20), nullable=False)  # 'PENDING', 'PAID', 'PROCESSING', 'SHIPPED', 'DELIVERED', 'CANCELLED'
    order_date = db.Column(db.DateTime, default=datetime.utcnow)
    address_id = db.Column(db.Integer, db.ForeignKey('addresses.id'), nullable=False)
    
    # Relationships
    address = db.relationship('Address', backref=db.backref('orders', lazy=True))
    order_items = db.relationship('OrderItems', backref='order', lazy=True, cascade='all, delete-orphan')

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'total_amount': float(self.total_amount),
            'payment_method': self.payment_method,
            'payment_details': self.payment_details,
            'status': self.status,
            'order_date': self.order_date.isoformat() if self.order_date else None,
            'address_id': self.address_id,
            'items': [item.to_dict() for item in self.order_items]
        }

class OrderItems(db.Model):
    __tablename__ = 'order_items'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    product_id = db.Column(db.String(36), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'order_id': self.order_id,
            'product_id': self.product_id,
            'quantity': self.quantity,
            'price': self.price
        }
