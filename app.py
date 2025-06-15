from flask import Flask, request, jsonify, session, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///loreal_store.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
CORS(app, supports_credentials=True)

# Models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    contact = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    cart_items = db.relationship('CartItem', backref='user', lazy=True, cascade='all, delete-orphan')
    orders = db.relationship('Order', backref='user', lazy=True)

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    slug = db.Column(db.String(50), unique=True, nullable=False)
    
    products = db.relationship('Product', backref='category', lazy=True)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text)
    image_url = db.Column(db.String(300))
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    stock_quantity = db.Column(db.Integer, default=0)
    is_featured = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class CartItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=1)
    added_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    product = db.relationship('Product', backref='cart_items')

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    total_amount = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(20), default='pending')
    customer_name = db.Column(db.String(100), nullable=False)
    customer_phone = db.Column(db.String(20), nullable=False)
    delivery_address = db.Column(db.Text, nullable=False)
    payment_method = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    order_items = db.relationship('OrderItem', backref='order', lazy=True, cascade='all, delete-orphan')

class OrderItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)
    
    product = db.relationship('Product', backref='order_items')

class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    contact = db.Column(db.String(100), nullable=False)
    message = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_read = db.Column(db.Boolean, default=False)

# Frontend Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/products')
def products():
    return render_template('products.html')

@app.route('/product-detail')
def product_detail():
    return render_template('product-detail.html')

@app.route('/cart')
def cart():
    return render_template('cart.html')

@app.route('/checkout')
def checkout():
    return render_template('checkout.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/login')
def login_page():
    return render_template('login.html')

@app.route('/introduce')
def introduce():
    return render_template('introduce.html')

# API Routes
@app.route('/api/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        name = data.get('name')
        contact = data.get('contact')
        password = data.get('password')
        
        if not all([name, contact, password]):
            return jsonify({'error': 'Vui lòng điền đầy đủ thông tin'}), 400
        
        if User.query.filter_by(contact=contact).first():
            return jsonify({'error': 'Tài khoản đã tồn tại'}), 400
        
        password_hash = generate_password_hash(password)
        user = User(name=name, contact=contact, password_hash=password_hash)
        
        db.session.add(user)
        db.session.commit()
        
        return jsonify({'message': 'Đăng ký thành công', 'user_id': user.id}), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/login', methods=['POST'])
def api_login():
    try:
        data = request.get_json()
        contact = data.get('contact')
        password = data.get('password')
        
        if not all([contact, password]):
            return jsonify({'error': 'Vui lòng điền đầy đủ thông tin'}), 400
        
        user = User.query.filter_by(contact=contact).first()
        
        if not user or not check_password_hash(user.password_hash, password):
            return jsonify({'error': 'Sai thông tin đăng nhập'}), 401
        
        session['user_id'] = user.id
        session['user_name'] = user.name
        session['is_admin'] = user.is_admin
        
        print(f"User logged in: {user.id}, session: {session}")
        
        return jsonify({
            'message': 'Đăng nhập thành công',
            'user': {
                'id': user.id,
                'name': user.name,
                'contact': user.contact,
                'is_admin': user.is_admin
            }
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/logout', methods=['POST'])
def logout():
    session.clear()
    return jsonify({'message': 'Đăng xuất thành công'}), 200

@app.route('/api/forgot-password', methods=['POST'])
def forgot_password():
    try:
        data = request.get_json()
        contact = data.get('contact')
        new_password = data.get('new_password')
        
        if not all([contact, new_password]):
            return jsonify({'error': 'Vui lòng điền đầy đủ thông tin'}), 400
        
        user = User.query.filter_by(contact=contact).first()
        if not user:
            return jsonify({'error': 'Không tìm thấy tài khoản'}), 404
        
        user.password_hash = generate_password_hash(new_password)
        db.session.commit()
        
        return jsonify({'message': 'Cập nhật mật khẩu thành công'}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/products', methods=['GET'])
def get_products():
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 8, type=int)
        category = request.args.get('category')
        search = request.args.get('search')
        price_range = request.args.get('price_range')
        
        query = Product.query
        
        if category and category != 'tat-ca':
            category_obj = Category.query.filter_by(slug=category).first()
            if category_obj:
                query = query.filter_by(category_id=category_obj.id)
        
        if search:
            query = query.filter(Product.name.contains(search))
        
        if price_range:
            if price_range == 'low':
                query = query.filter(Product.price < 300000)
            elif price_range == 'medium':
                query = query.filter(Product.price.between(300000, 600000))
            elif price_range == 'high':
                query = query.filter(Product.price > 600000)
        
        products = query.paginate(page=page, per_page=per_page, error_out=False)
        
        return jsonify({
            'products': [{
                'id': p.id,
                'name': p.name,
                'price': p.price,
                'description': p.description,
                'image_url': p.image_url,
                'category': p.category.slug,
                'stock_quantity': p.stock_quantity,
                'is_featured': p.is_featured
            } for p in products.items],
            'total': products.total,
            'pages': products.pages,
            'current_page': page
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    try:
        product = Product.query.get_or_404(product_id)
        return jsonify({
            'id': product.id,
            'name': product.name,
            'price': product.price,
            'description': product.description,
            'image_url': product.image_url,
            'category': product.category.slug,
            'category_id': product.category_id,
            'stock_quantity': product.stock_quantity,
            'is_featured': product.is_featured
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/products/featured', methods=['GET'])
def get_featured_products():
    try:
        products = Product.query.filter_by(is_featured=True).limit(10).all()
        return jsonify([{
            'id': p.id,
            'name': p.name,
            'price': p.price,
            'description': p.description,
            'image_url': p.image_url,
            'category': p.category.slug
        } for p in products]), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/cart', methods=['GET'])
def get_cart():
    try:
        print(f"Getting cart for session: {session}")
        
        if 'user_id' not in session:
            print("No user_id in session")
            return jsonify({'error': 'Vui lòng đăng nhập'}), 401
        
        user_id = session['user_id']
        print(f"Getting cart for user_id: {user_id}")
        
        # Use eager loading to ensure product data is available
        cart_items = CartItem.query.options(db.joinedload(CartItem.product)).filter_by(user_id=user_id).all()
        
        print(f"Found {len(cart_items)} cart items")
        
        result = []
        for item in cart_items:
            if item.product:  # Ensure product exists
                print(f"Processing cart item: {item.id}, product: {item.product.name}, quantity: {item.quantity}")
                result.append({
                    'id': item.id,
                    'product': {
                        'id': item.product.id,
                        'name': item.product.name,
                        'price': float(item.product.price),  # Ensure it's a number
                        'image_url': item.product.image_url
                    },
                    'quantity': item.quantity
                })
            else:
                print(f"Cart item {item.id} has no associated product")
        
        print(f"Returning cart data: {result}")
        return jsonify(result), 200
        
    except Exception as e:
        print(f"Error in get_cart: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

@app.route('/api/cart/add', methods=['POST'])
def add_to_cart():
    try:
        print(f"Adding to cart, session: {session}")
        
        if 'user_id' not in session:
            print("No user_id in session for add_to_cart")
            return jsonify({'error': 'Vui lòng đăng nhập'}), 401
        
        data = request.get_json()
        product_id = data.get('product_id')
        quantity = data.get('quantity', 1)
        
        print(f"Adding product {product_id} with quantity {quantity} for user {session['user_id']}")
        
        if not product_id:
            return jsonify({'error': 'Thiếu thông tin sản phẩm'}), 400
        
        product = Product.query.get_or_404(product_id)
        print(f"Found product: {product.name}")
        
        cart_item = CartItem.query.filter_by(
            user_id=session['user_id'], 
            product_id=product_id
        ).first()
        
        if cart_item:
            print(f"Updating existing cart item, old quantity: {cart_item.quantity}")
            cart_item.quantity += quantity
            print(f"New quantity: {cart_item.quantity}")
        else:
            print("Creating new cart item")
            cart_item = CartItem(
                user_id=session['user_id'],
                product_id=product_id,
                quantity=quantity
            )
            db.session.add(cart_item)
        
        db.session.commit()
        print("Cart item saved successfully")
        
        # Verify the item was saved
        verify_item = CartItem.query.filter_by(
            user_id=session['user_id'], 
            product_id=product_id
        ).first()
        print(f"Verification - item exists: {verify_item is not None}")
        if verify_item:
            print(f"Verification - quantity: {verify_item.quantity}")
        
        return jsonify({'message': 'Đã thêm vào giỏ hàng'}), 200
        
    except Exception as e:
        print(f"Error in add_to_cart: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

@app.route('/api/cart/update/<int:item_id>', methods=['PUT'])
def update_cart_item(item_id):
    try:
        if 'user_id' not in session:
            return jsonify({'error': 'Vui lòng đăng nhập'}), 401
        
        data = request.get_json()
        quantity = data.get('quantity')
        
        if not quantity or quantity < 1:
            return jsonify({'error': 'Số lượng không hợp lệ'}), 400
        
        cart_item = CartItem.query.filter_by(
            id=item_id, 
            user_id=session['user_id']
        ).first_or_404()
        
        cart_item.quantity = quantity
        db.session.commit()
        
        return jsonify({'message': 'Cập nhật thành công'}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/cart/remove/<int:item_id>', methods=['DELETE'])
def remove_cart_item(item_id):
    try:
        if 'user_id' not in session:
            return jsonify({'error': 'Vui lòng đăng nhập'}), 401
        
        cart_item = CartItem.query.filter_by(
            id=item_id, 
            user_id=session['user_id']
        ).first_or_404()
        
        db.session.delete(cart_item)
        db.session.commit()
        
        return jsonify({'message': 'Đã xóa khỏi giỏ hàng'}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/orders', methods=['POST'])
def create_order():
    try:
        if 'user_id' not in session:
            return jsonify({'error': 'Vui lòng đăng nhập'}), 401
        
        data = request.get_json()
        customer_name = data.get('customer_name')
        customer_phone = data.get('customer_phone')
        delivery_address = data.get('delivery_address')
        payment_method = data.get('payment_method')
        
        if not all([customer_name, customer_phone, delivery_address, payment_method]):
            return jsonify({'error': 'Vui lòng điền đầy đủ thông tin'}), 400
        
        cart_items = CartItem.query.filter_by(user_id=session['user_id']).all()
        
        if not cart_items:
            return jsonify({'error': 'Giỏ hàng trống'}), 400
        
        total_amount = sum(item.product.price * item.quantity for item in cart_items)
        
        order = Order(
            user_id=session['user_id'],
            total_amount=total_amount,
            customer_name=customer_name,
            customer_phone=customer_phone,
            delivery_address=delivery_address,
            payment_method=payment_method
        )
        
        db.session.add(order)
        db.session.flush()
        
        for cart_item in cart_items:
            order_item = OrderItem(
                order_id=order.id,
                product_id=cart_item.product_id,
                quantity=cart_item.quantity,
                price=cart_item.product.price
            )
            db.session.add(order_item)
        
        CartItem.query.filter_by(user_id=session['user_id']).delete()
        
        db.session.commit()
        
        return jsonify({
            'message': 'Đặt hàng thành công',
            'order_id': order.id
        }), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/contact', methods=['POST'])
def submit_contact():
    try:
        data = request.get_json()
        name = data.get('name')
        contact = data.get('contact')
        message = data.get('message')
        
        if not all([name, contact, message]):
            return jsonify({'error': 'Vui lòng điền đầy đủ thông tin'}), 400
        
        contact_msg = Contact(name=name, contact=contact, message=message)
        db.session.add(contact_msg)
        db.session.commit()
        
        return jsonify({'message': 'Gửi tin nhắn thành công'}), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/categories', methods=['GET'])
def get_categories():
    try:
        categories = Category.query.all()
        return jsonify([{
            'id': cat.id,
            'name': cat.name,
            'slug': cat.slug
        } for cat in categories]), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/user', methods=['GET'])
def get_user_info():
    print(f"Getting user info, session: {session}")
    
    if 'user_id' not in session:
        return jsonify({'error': 'Chưa đăng nhập'}), 401
    
    user = User.query.get(session['user_id'])
    if not user:
        return jsonify({'error': 'Người dùng không tồn tại'}), 404
    
    return jsonify({
        'id': user.id,
        'name': user.name,
        'contact': user.contact,
        'is_admin': user.is_admin
    }), 200

# Admin Routes
@app.route('/admin')
def admin_panel():
    return render_template('admin.html')

# Admin API Routes
@app.route('/api/admin/stats/products', methods=['GET'])
def admin_stats_products():
    if 'user_id' not in session or not session.get('is_admin'):
        return jsonify({'error': 'Không có quyền truy cập'}), 403
    
    count = Product.query.count()
    return jsonify({'count': count}), 200

@app.route('/api/admin/stats/users', methods=['GET'])
def admin_stats_users():
    if 'user_id' not in session or not session.get('is_admin'):
        return jsonify({'error': 'Không có quyền truy cập'}), 403
    
    count = User.query.count()
    return jsonify({'count': count}), 200

@app.route('/api/admin/stats/orders', methods=['GET'])
def admin_stats_orders():
    if 'user_id' not in session or not session.get('is_admin'):
        return jsonify({'error': 'Không có quyền truy cập'}), 403
    
    count = Order.query.count()
    return jsonify({'count': count}), 200

@app.route('/api/admin/stats/contacts', methods=['GET'])
def admin_stats_contacts():
    if 'user_id' not in session or not session.get('is_admin'):
        return jsonify({'error': 'Không có quyền truy cập'}), 403
    
    count = Contact.query.filter_by(is_read=False).count()
    return jsonify({'count': count}), 200

@app.route('/api/admin/products', methods=['GET'])
def admin_get_products():
    if 'user_id' not in session or not session.get('is_admin'):
        return jsonify({'error': 'Không có quyền truy cập'}), 403
    
    try:
        products = db.session.query(Product, Category.name.label('category_name')).join(Category).all()
        return jsonify([{
            'id': p.Product.id,
            'name': p.Product.name,
            'price': p.Product.price,
            'description': p.Product.description,
            'image_url': p.Product.image_url,
            'category_id': p.Product.category_id,
            'category_name': p.category_name,
            'stock_quantity': p.Product.stock_quantity,
            'is_featured': p.Product.is_featured,
            'created_at': p.Product.created_at.isoformat()
        } for p in products]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/admin/products', methods=['POST'])
def admin_create_product():
    if 'user_id' not in session or not session.get('is_admin'):
        return jsonify({'error': 'Không có quyền truy cập'}), 403
    
    try:
        data = request.get_json()
        product = Product(
            name=data['name'],
            price=data['price'],
            description=data.get('description', ''),
            image_url=data['image_url'],
            category_id=data['category_id'],
            stock_quantity=data['stock_quantity'],
            is_featured=data.get('is_featured', False)
        )
        
        db.session.add(product)
        db.session.commit()
        
        return jsonify({'message': 'Tạo sản phẩm thành công', 'id': product.id}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/admin/products/<int:product_id>', methods=['PUT'])
def admin_update_product(product_id):
    if 'user_id' not in session or not session.get('is_admin'):
        return jsonify({'error': 'Không có quyền truy cập'}), 403
    
    try:
        product = Product.query.get_or_404(product_id)
        data = request.get_json()
        
        product.name = data['name']
        product.price = data['price']
        product.description = data.get('description', '')
        product.image_url = data['image_url']
        product.category_id = data['category_id']
        product.stock_quantity = data['stock_quantity']
        product.is_featured = data.get('is_featured', False)
        
        db.session.commit()
        
        return jsonify({'message': 'Cập nhật sản phẩm thành công'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/admin/products/<int:product_id>', methods=['DELETE'])
def admin_delete_product(product_id):
    if 'user_id' not in session or not session.get('is_admin'):
        return jsonify({'error': 'Không có quyền truy cập'}), 403
    
    try:
        product = Product.query.get_or_404(product_id)
        db.session.delete(product)
        db.session.commit()
        
        return jsonify({'message': 'Xóa sản phẩm thành công'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/admin/users', methods=['GET'])
def admin_get_users():
    if 'user_id' not in session or not session.get('is_admin'):
        return jsonify({'error': 'Không có quyền truy cập'}), 403
    
    try:
        users = User.query.all()
        return jsonify([{
            'id': u.id,
            'name': u.name,
            'contact': u.contact,
            'is_admin': u.is_admin,
            'created_at': u.created_at.isoformat()
        } for u in users]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/admin/users/<int:user_id>', methods=['GET'])
def admin_get_user(user_id):
    if 'user_id' not in session or not session.get('is_admin'):
        return jsonify({'error': 'Không có quyền truy cập'}), 403
    
    try:
        user = User.query.get_or_404(user_id)
        return jsonify({
            'id': user.id,
            'name': user.name,
            'contact': user.contact,
            'is_admin': user.is_admin
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/admin/users', methods=['POST'])
def admin_create_user():
    if 'user_id' not in session or not session.get('is_admin'):
        return jsonify({'error': 'Không có quyền truy cập'}), 403
    
    try:
        data = request.get_json()
        
        if User.query.filter_by(contact=data['contact']).first():
            return jsonify({'error': 'Tài khoản đã tồn tại'}), 400
        
        user = User(
            name=data['name'],
            contact=data['contact'],
            password_hash=generate_password_hash(data['password']),
            is_admin=data.get('is_admin', False)
        )
        
        db.session.add(user)
        db.session.commit()
        
        return jsonify({'message': 'Tạo người dùng thành công', 'id': user.id}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/admin/users/<int:user_id>', methods=['PUT'])
def admin_update_user(user_id):
    if 'user_id' not in session or not session.get('is_admin'):
        return jsonify({'error': 'Không có quyền truy cập'}), 403
    
    try:
        user = User.query.get_or_404(user_id)
        data = request.get_json()
        
        # Check if contact is already used by another user
        existing_user = User.query.filter_by(contact=data['contact']).first()
        if existing_user and existing_user.id != user_id:
            return jsonify({'error': 'Email/SĐT đã được sử dụng'}), 400
        
        user.name = data['name']
        user.contact = data['contact']
        if data['password']:
            user.password_hash = generate_password_hash(data['password'])
        user.is_admin = data.get('is_admin', False)
        
        db.session.commit()
        
        return jsonify({'message': 'Cập nhật người dùng thành công'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/admin/users/<int:user_id>', methods=['DELETE'])
def admin_delete_user(user_id):
    if 'user_id' not in session or not session.get('is_admin'):
        return jsonify({'error': 'Không có quyền truy cập'}), 403
    
    try:
        user = User.query.get_or_404(user_id)
        
        if user.is_admin:
            return jsonify({'error': 'Không thể xóa tài khoản admin'}), 400
        
        db.session.delete(user)
        db.session.commit()
        
        return jsonify({'message': 'Xóa người dùng thành công'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/admin/orders', methods=['GET'])
def admin_get_orders():
    if 'user_id' not in session or not session.get('is_admin'):
        return jsonify({'error': 'Không có quyền truy cập'}), 403
    
    try:
        orders = Order.query.order_by(Order.created_at.desc()).all()
        return jsonify([{
            'id': o.id,
            'customer_name': o.customer_name,
            'customer_phone': o.customer_phone,
            'delivery_address': o.delivery_address,
            'payment_method': o.payment_method,
            'total_amount': o.total_amount,
            'status': o.status,
            'created_at': o.created_at.isoformat()
        } for o in orders]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/admin/orders/<int:order_id>', methods=['PUT'])
def admin_update_order(order_id):
    if 'user_id' not in session or not session.get('is_admin'):
        return jsonify({'error': 'Không có quyền truy cập'}), 403
    
    try:
        order = Order.query.get_or_404(order_id)
        data = request.get_json()
        
        order.status = data['status']
        db.session.commit()
        
        return jsonify({'message': 'Cập nhật trạng thái đơn hàng thành công'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/admin/orders/<int:order_id>/details', methods=['GET'])
def admin_get_order_details(order_id):
    if 'user_id' not in session or not session.get('is_admin'):
        return jsonify({'error': 'Không có quyền truy cập'}), 403
    
    try:
        order = Order.query.get_or_404(order_id)
        order_items = db.session.query(OrderItem, Product.name.label('product_name')).join(Product).filter(OrderItem.order_id == order_id).all()
        
        return jsonify({
            'id': order.id,
            'customer_name': order.customer_name,
            'customer_phone': order.customer_phone,
            'delivery_address': order.delivery_address,
            'payment_method': order.payment_method,
            'total_amount': order.total_amount,
            'status': order.status,
            'created_at': order.created_at.isoformat(),
            'items': [{
                'product_name': item.product_name,
                'quantity': item.OrderItem.quantity,
                'price': item.OrderItem.price
            } for item in order_items]
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/admin/contacts', methods=['GET'])
def admin_get_contacts():
    if 'user_id' not in session or not session.get('is_admin'):
        return jsonify({'error': 'Không có quyền truy cập'}), 403
    
    try:
        contacts = Contact.query.order_by(Contact.created_at.desc()).all()
        return jsonify([{
            'id': c.id,
            'name': c.name,
            'contact': c.contact,
            'message': c.message,
            'is_read': c.is_read,
            'created_at': c.created_at.isoformat()
        } for c in contacts]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/admin/contacts/<int:contact_id>', methods=['PUT'])
def admin_update_contact(contact_id):
    if 'user_id' not in session or not session.get('is_admin'):
        return jsonify({'error': 'Không có quyền truy cập'}), 403
    
    try:
        contact = Contact.query.get_or_404(contact_id)
        data = request.get_json()
        
        contact.is_read = data.get('is_read', True)
        db.session.commit()
        
        return jsonify({'message': 'Cập nhật trạng thái tin nhắn thành công'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
