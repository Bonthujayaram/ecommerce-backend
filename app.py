from flask import Flask, request, jsonify, session
from flask_cors import CORS
from models import db, Product, User, ChatSession, ChatLog, Users, Address, Orders, OrderItems
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import uuid
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///yourdb.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    'pool_pre_ping': True,
    'pool_recycle': 300,
}
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
app.config['SESSION_COOKIE_SECURE'] = False
CORS(app, supports_credentials=True)

# Initialize the database with the app
db.init_app(app)

# Create tables if they don't exist
with app.app_context():
    db.create_all()

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/signup', methods=['POST'])
def signup():
    data = request.json
    if not data.get('username') or not data.get('email') or not data.get('password'):
        return jsonify({'error': 'Missing required fields'}), 400
    if User.query.filter((User.username == data['username']) | (User.email == data['email'])).first():
        return jsonify({'error': 'Username or email already exists'}), 409
    # Store password as plain text (not secure, for demo only)
    user = User(username=data['username'], email=data['email'], password=data['password'])
    db.session.add(user)
    db.session.commit()
    login_user(user)
    return jsonify({'message': 'Signup successful', 'user': {'id': user.id, 'username': user.username, 'email': user.email}})

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    print("Login attempt with data:", data)  # Debug log
    user = User.query.filter_by(email=data.get('email')).first()
    print("Found user:", user)  # Debug log
    # Compare password as plain text
    if user and user.password == data.get('password'):
        login_user(user)
        return jsonify({'message': 'Login successful', 'user': {'id': user.id, 'username': user.username, 'email': user.email}})
    return jsonify({'error': 'Invalid email or password'}), 401

@app.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return jsonify({'message': 'Logged out'})

@app.route('/me', methods=['GET'])
@login_required
def me():
    user = current_user
    return jsonify({'id': user.id, 'username': user.username, 'email': user.email, 'created_at': user.created_at})

@app.route('/signup', methods=['GET'])
def signup_get():
    return jsonify({"message": "Send a POST request to this endpoint to create a new user."})

@app.route('/login', methods=['GET'])
def login_get():
    return jsonify({"message": "Send a POST request to this endpoint to log in."})

@app.route('/chatsession', methods=['POST'])
@login_required
def create_chatsession():
    data = request.get_json() or {}
    title = data.get('title')
    session = ChatSession(user_id=current_user.id, title=title)
    db.session.add(session)
    db.session.commit()
    return jsonify({'id': session.id, 'created_at': session.created_at.isoformat(), 'title': session.title})

@app.route('/chatsessions', methods=['GET'])
@login_required
def list_chatsessions():
    sessions = ChatSession.query.filter_by(user_id=current_user.id).order_by(ChatSession.created_at.desc()).all()
    return jsonify([
        {'id': s.id, 'created_at': s.created_at.isoformat(), 'title': s.title} for s in sessions
    ])

@app.route('/chatlog', methods=['GET'])
@login_required
def get_chatlog():
    session_id = request.args.get('session_id')
    if not session_id:
        return jsonify({'error': 'session_id required'}), 400
    logs = ChatLog.query.filter_by(user_id=current_user.id, session_id=session_id).order_by(ChatLog.timestamp).all()
    return jsonify([
        {
            'id': log.id,
            'message': log.message,
            'sender': log.sender,
            'timestamp': log.timestamp.isoformat()
        } for log in logs
    ])

@app.route('/chatlog', methods=['POST'])
@login_required
def save_chatlog():
    data = request.get_json()
    session_id = data.get('session_id')
    messages = data.get('messages', [])
    if not session_id:
        return jsonify({'error': 'session_id required'}), 400
    for msg in messages:
        chat = ChatLog(
            session_id=session_id,
            user_id=current_user.id,
            message=msg['content'],
            sender=msg['sender'],
            timestamp=msg.get('timestamp', None) or None
        )
        db.session.add(chat)
    db.session.commit()
    return jsonify({'status': 'success'})

@app.route('/products', methods=['GET'])
def get_products():
    products = Product.query.all()
    return jsonify([p.to_dict() for p in products])

@app.route('/product/<int:product_id>', methods=['GET'])
def get_product(product_id):
    product = Product.query.get(product_id)
    if product:
        return jsonify(product.to_dict())
    return jsonify({'error': 'Product not found'}), 404

@app.route('/products/search')
def search_products():
    query = request.args.get('q', '').lower()
    products = Product.query.filter(
        (Product.name.ilike(f'%{query}%')) |
        (Product.description.ilike(f'%{query}%')) |
        (Product.category.ilike(f'%{query}%')) |
        (Product.brand.ilike(f'%{query}%'))
    ).all()
    return jsonify([p.to_dict() for p in products])

@app.route('/products/category/<category>')
def get_products_by_category(category):
    products = Product.query.filter(Product.category.ilike(category)).all()
    return jsonify([p.to_dict() for p in products])

@app.route('/')
def index():
    return 'Hello, World!'

@app.route('/debug/users', methods=['GET'])
def debug_users():
    users = User.query.all()
    return jsonify([{
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'created_at': user.created_at
    } for user in users])

@app.route('/users/<user_id>', methods=['GET'])
def get_profile(user_id):
    try:
        # First try to find an existing user profile
        user = Users.query.filter_by(user_id=int(user_id)).first()
        
        if not user:
            # If no profile exists, create one with a new UUID
            user = Users(
                id=str(uuid.uuid4()),
                user_id=int(user_id)
            )
            db.session.add(user)
            db.session.commit()
        
        return jsonify({
            'id': user.id,
            'user_id': user.user_id,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'gender': user.gender,
            'mail': user.mail,
            'phone': user.phone
        })
    except Exception as e:
        print(f"Error getting/creating user profile: {str(e)}")
        return jsonify({'error': 'Failed to get user profile'}), 500

@app.route('/users/<user_id>', methods=['PUT'])
def upsert_profile(user_id):
    data = request.json
    user = Users.query.filter_by(user_id=user_id).first()
    if user:
        # Update existing
        user.first_name = data.get('first_name')
        user.last_name = data.get('last_name')
        user.gender = data.get('gender')
        user.mail = data.get('mail')
        user.phone = data.get('phone')
    else:
        # Insert new
        user = Users(
            id=str(uuid.uuid4()),
            user_id=int(user_id),
            first_name=data.get('first_name'),
            last_name=data.get('last_name'),
            gender=data.get('gender'),
            mail=data.get('mail'),
            phone=data.get('phone')
        )
        db.session.add(user)
    db.session.commit()
    return jsonify({'message': 'Profile saved'})

@app.route('/users/<int:user_id>/addresses/<int:address_id>', methods=['PUT', 'OPTIONS'])
def update_address(user_id, address_id):
    if request.method == 'OPTIONS':
        return '', 200
    data = request.json
    address = Address.query.filter_by(id=address_id, user_id=user_id).first_or_404()
    address.label = data['label']
    address.name = data['name']
    address.phone = data['phone']
    address.address = data['address']
    db.session.commit()
    return jsonify({'message': 'Address updated'})

@app.route('/users/<int:user_id>/addresses/<int:address_id>', methods=['DELETE', 'OPTIONS'])
def delete_address(user_id, address_id):
    if request.method == 'OPTIONS':
        return '', 200
    address = Address.query.filter_by(id=address_id, user_id=user_id).first_or_404()
    db.session.delete(address)
    db.session.commit()
    return jsonify({'message': 'Address deleted'})

@app.route('/users/<int:user_id>/addresses', methods=['GET'])
def get_addresses(user_id):
    addresses = Address.query.filter_by(user_id=user_id).all()
    return jsonify([
        {
            'id': addr.id,
            'label': addr.label,
            'name': addr.name,
            'phone': addr.phone,
            'address': addr.address
        } for addr in addresses
    ])

@app.route('/users/<int:user_id>/addresses', methods=['POST'])
def add_address(user_id):
    data = request.get_json()
    new_address = Address(
        user_id=user_id,
        label=data['label'],
        name=data['name'],
        phone=data['phone'],
        address=data['address']
    )
    db.session.add(new_address)
    db.session.commit()
    return jsonify({'id': new_address.id}), 201

@app.route('/orders', methods=['POST'])
def create_order():
    data = request.json
    
    # Create order in orders table
    order = Orders(
        user_id=data['user_id'],
        total_amount=data['total_amount'],
        payment_method=data['payment_method'],
        payment_details=data['payment_details'],
        status=data['status'],
        address_id=data['address_id']
    )
    db.session.add(order)
    db.session.flush()  # To get the order_id
    
    # Create order items
    for item in data['order_items']:
        order_item = OrderItems(
            order_id=order.id,
            product_id=item['product_id'],
            quantity=item['quantity'],
            price=item['price']
        )
        db.session.add(order_item)
    
    db.session.commit()
    return jsonify({'message': 'Order created successfully', 'order_id': order.id})

@app.route('/users/<user_id>/orders', methods=['GET', 'OPTIONS'])
def get_user_orders(user_id):
    if request.method == 'OPTIONS':
        return '', 200
        
    try:
        # First get the user profile to get the correct ID type
        user = Users.query.filter_by(id=user_id).first()
        if not user:
            # If UUID not found, try with integer user_id
            user = Users.query.filter_by(user_id=int(user_id)).first()
            if not user:
                return jsonify({'error': 'User not found'}), 404
        
        # Now fetch orders using the integer user_id
        orders = Orders.query.filter_by(user_id=str(user.user_id)).order_by(Orders.order_date.desc()).all()
        print(f"Found {len(orders)} orders for user_id {user.user_id}")  # Debug log
        
        order_list = []
        for order in orders:
            order_dict = {
                'id': order.id,
                'user_id': order.user_id,
                'total_amount': float(order.total_amount),
                'payment_method': order.payment_method,
                'payment_details': order.payment_details,
                'status': order.status,
                'order_date': order.order_date.isoformat() if order.order_date else None,
                'address_id': order.address_id,
                'items': [{
                    'id': item.id,
                    'product_id': item.product_id,
                    'quantity': item.quantity,
                    'price': float(item.price)
                } for item in order.order_items]
            }
            print(f"Processing order: {order_dict}")  # Debug log
            order_list.append(order_dict)
            
        print(f"Returning {len(order_list)} orders")  # Debug log
        return jsonify(order_list)
    except Exception as e:
        print(f"Error fetching orders: {str(e)}")
        return jsonify({'error': 'Failed to fetch orders'}), 500

@app.route('/users/<user_id>/orders/<order_id>', methods=['GET'])
def get_order_details(user_id, order_id):
    try:
        # Convert order_id to int
        order_id = int(order_id)
        
        # Get the user's integer ID
        try:
            user_id_int = int(user_id)
        except ValueError:
            # If user_id is not an integer (UUID), find the user first
            user = Users.query.filter_by(id=user_id).first()
            if user:
                user_id_int = user.user_id
            else:
                return jsonify({'error': 'User not found'}), 404

        # Get the order directly with both user_id and order_id
        order = Orders.query.filter_by(id=order_id, user_id=user_id_int).first()
        
        if not order:
            return jsonify({'error': 'Order not found'}), 404

        # Convert to dictionary using the model's to_dict method
        response = order.to_dict()
        
        # Add address details
        address = Address.query.get(order.address_id)
        if address:
            response['address'] = {
                'id': address.id,
                'label': address.label,
                'name': address.name,
                'phone': address.phone,
                'address': address.address
            }
        
        return jsonify(response)
        
    except Exception as e:
        print(f"Error fetching order details: {str(e)}")
        return jsonify({'error': 'Failed to fetch order details'}), 500

if __name__ == "__main__":
    # Use environment variables with fallback values
    port = int(os.environ.get("PORT", 8000))
    app.run(host="0.0.0.0", port=port)

