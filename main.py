
from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, DecimalField, IntegerField, SelectField, SubmitField
from wtforms.validators import DataRequired, Email, Length, NumberRange
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///flower_shop.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Models
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    orders = db.relationship('Order', backref='user', lazy=True)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, default=0)
    category = db.Column(db.String(50))
    image_url = db.Column(db.String(200))

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    total_amount = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(20), default='pending')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    shipping_address = db.Column(db.Text)
    phone = db.Column(db.String(20))
    items = db.relationship('OrderItem', backref='order', lazy=True)

class OrderItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)
    product = db.relationship('Product', backref='order_items')

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Forms
class LoginForm(FlaskForm):
    username = StringField('Имя пользователя', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    submit = SubmitField('Войти')

class RegisterForm(FlaskForm):
    username = StringField('Имя пользователя', validators=[DataRequired(), Length(min=4, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Пароль', validators=[DataRequired(), Length(min=6)])
    submit = SubmitField('Зарегистрироваться')

class ProductForm(FlaskForm):
    name = StringField('Название', validators=[DataRequired()])
    description = TextAreaField('Описание')
    price = DecimalField('Цена', validators=[DataRequired(), NumberRange(min=0)])
    stock = IntegerField('Количество', validators=[DataRequired(), NumberRange(min=0)])
    category = SelectField('Категория', choices=[
        ('roses', 'Розы'),
        ('tulips', 'Тюльпаны'),
        ('orchids', 'Орхидеи'),
        ('bouquets', 'Букеты'),
        ('potted', 'Горшечные растения')
    ])
    image_url = StringField('URL изображения')
    submit = SubmitField('Сохранить')

class CheckoutForm(FlaskForm):
    shipping_address = TextAreaField('Адрес доставки', validators=[DataRequired()])
    phone = StringField('Телефон', validators=[DataRequired()])
    submit = SubmitField('Оформить заказ')

# Routes
@app.route('/')
def index():
    products = Product.query.limit(8).all()
    return render_template('index.html', products=products)

@app.route('/catalog')
def catalog():
    category = request.args.get('category')
    if category:
        products = Product.query.filter_by(category=category).all()
    else:
        products = Product.query.all()
    return render_template('catalog.html', products=products, category=category)

@app.route('/product/<int:id>')
def product_detail(id):
    product = Product.query.get_or_404(id)
    return render_template('product_detail.html', product=product)

@app.route('/add_to_cart/<int:product_id>')
def add_to_cart(product_id):
    if 'cart' not in session:
        session['cart'] = {}
    
    cart = session['cart']
    product_id_str = str(product_id)
    
    if product_id_str in cart:
        cart[product_id_str] += 1
    else:
        cart[product_id_str] = 1
    
    session['cart'] = cart
    flash('Товар добавлен в корзину!', 'success')
    return redirect(url_for('catalog'))

@app.route('/cart')
def cart():
    if 'cart' not in session or not session['cart']:
        return render_template('cart.html', cart_items=[], total=0)
    
    cart = session['cart']
    cart_items = []
    total = 0
    
    for product_id, quantity in cart.items():
        product = Product.query.get(int(product_id))
        if product:
            item_total = product.price * quantity
            cart_items.append({
                'product': product,
                'quantity': quantity,
                'total': item_total
            })
            total += item_total
    
    return render_template('cart.html', cart_items=cart_items, total=total)

@app.route('/update_cart', methods=['POST'])
def update_cart():
    product_id = request.form.get('product_id')
    quantity = int(request.form.get('quantity'))
    
    if 'cart' in session:
        if quantity > 0:
            session['cart'][product_id] = quantity
        else:
            session['cart'].pop(product_id, None)
        session.modified = True
    
    return redirect(url_for('cart'))

@app.route('/remove_from_cart/<int:product_id>')
def remove_from_cart(product_id):
    if 'cart' in session:
        session['cart'].pop(str(product_id), None)
        session.modified = True
    return redirect(url_for('cart'))

@app.route('/checkout', methods=['GET', 'POST'])
@login_required
def checkout():
    if 'cart' not in session or not session['cart']:
        flash('Ваша корзина пуста!', 'warning')
        return redirect(url_for('cart'))
    
    form = CheckoutForm()
    if form.validate_on_submit():
        # Создаем заказ
        total = 0
        cart = session['cart']
        
        for product_id, quantity in cart.items():
            product = Product.query.get(int(product_id))
            if product:
                total += product.price * quantity
        
        order = Order(
            user_id=current_user.id,
            total_amount=total,
            shipping_address=form.shipping_address.data,
            phone=form.phone.data
        )
        db.session.add(order)
        db.session.flush()
        
        # Добавляем товары в заказ
        for product_id, quantity in cart.items():
            product = Product.query.get(int(product_id))
            if product:
                order_item = OrderItem(
                    order_id=order.id,
                    product_id=product.id,
                    quantity=quantity,
                    price=product.price
                )
                db.session.add(order_item)
                # Уменьшаем количество на складе
                product.stock -= quantity
        
        db.session.commit()
        session.pop('cart', None)
        flash('Заказ успешно оформлен!', 'success')
        return redirect(url_for('order_success', order_id=order.id))
    
    return render_template('checkout.html', form=form)

@app.route('/order_success/<int:order_id>')
@login_required
def order_success(order_id):
    order = Order.query.get_or_404(order_id)
    if order.user_id != current_user.id:
        flash('Заказ не найден!', 'error')
        return redirect(url_for('index'))
    return render_template('order_success.html', order=order)

@app.route('/my_orders')
@login_required
def my_orders():
    orders = Order.query.filter_by(user_id=current_user.id).order_by(Order.created_at.desc()).all()
    return render_template('my_orders.html', orders=orders)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and check_password_hash(user.password_hash, form.password.data):
            login_user(user)
            return redirect(url_for('index'))
        flash('Неверное имя пользователя или пароль!', 'error')
    return render_template('login.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        existing_user = User.query.filter_by(username=form.username.data).first()
        existing_email = User.query.filter_by(email=form.email.data).first()
        
        if existing_user:
            flash('Пользователь с таким именем уже существует!', 'error')
        elif existing_email:
            flash('Пользователь с таким email уже существует!', 'error')
        else:
            user = User(
                username=form.username.data,
                email=form.email.data,
                password_hash=generate_password_hash(form.password.data)
            )
            db.session.add(user)
            db.session.commit()
            login_user(user)
            flash('Регистрация успешна!', 'success')
            return redirect(url_for('index'))
    return render_template('register.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

# Admin routes
@app.route('/admin')
@login_required
def admin():
    if not current_user.is_admin:
        flash('Доступ запрещен!', 'error')
        return redirect(url_for('index'))
    
    products = Product.query.all()
    orders = Order.query.order_by(Order.created_at.desc()).limit(10).all()
    return render_template('admin/dashboard.html', products=products, orders=orders)

@app.route('/admin/products')
@login_required
def admin_products():
    if not current_user.is_admin:
        flash('Доступ запрещен!', 'error')
        return redirect(url_for('index'))
    
    products = Product.query.all()
    return render_template('admin/products.html', products=products)

@app.route('/admin/product/add', methods=['GET', 'POST'])
@login_required
def admin_add_product():
    if not current_user.is_admin:
        flash('Доступ запрещен!', 'error')
        return redirect(url_for('index'))
    
    form = ProductForm()
    if form.validate_on_submit():
        product = Product(
            name=form.name.data,
            description=form.description.data,
            price=float(form.price.data),
            stock=form.stock.data,
            category=form.category.data,
            image_url=form.image_url.data
        )
        db.session.add(product)
        db.session.commit()
        flash('Товар добавлен!', 'success')
        return redirect(url_for('admin_products'))
    
    return render_template('admin/product_form.html', form=form, title='Добавить товар')

@app.route('/admin/product/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def admin_edit_product(id):
    if not current_user.is_admin:
        flash('Доступ запрещен!', 'error')
        return redirect(url_for('index'))
    
    product = Product.query.get_or_404(id)
    form = ProductForm(obj=product)
    
    if form.validate_on_submit():
        product.name = form.name.data
        product.description = form.description.data
        product.price = float(form.price.data)
        product.stock = form.stock.data
        product.category = form.category.data
        product.image_url = form.image_url.data
        db.session.commit()
        flash('Товар обновлен!', 'success')
        return redirect(url_for('admin_products'))
    
    return render_template('admin/product_form.html', form=form, title='Редактировать товар')

@app.route('/admin/product/<int:id>/delete')
@login_required
def admin_delete_product(id):
    if not current_user.is_admin:
        flash('Доступ запрещен!', 'error')
        return redirect(url_for('index'))
    
    product = Product.query.get_or_404(id)
    db.session.delete(product)
    db.session.commit()
    flash('Товар удален!', 'success')
    return redirect(url_for('admin_products'))

@app.route('/admin/orders')
@login_required
def admin_orders():
    if not current_user.is_admin:
        flash('Доступ запрещен!', 'error')
        return redirect(url_for('index'))
    
    orders = Order.query.order_by(Order.created_at.desc()).all()
    return render_template('admin/orders.html', orders=orders)

@app.route('/admin/order/<int:id>/update_status', methods=['POST'])
@login_required
def admin_update_order_status(id):
    if not current_user.is_admin:
        flash('Доступ запрещен!', 'error')
        return redirect(url_for('index'))
    
    order = Order.query.get_or_404(id)
    status = request.form.get('status')
    order.status = status
    db.session.commit()
    flash('Статус заказа обновлен!', 'success')
    return redirect(url_for('admin_orders'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        # Создаем админа по умолчанию
        admin = User.query.filter_by(username='admin').first()
        if not admin:
            admin = User(
                username='admin',
                email='admin@example.com',
                password_hash=generate_password_hash('admin123'),
                is_admin=True
            )
            db.session.add(admin)
            db.session.commit()
            
        # Добавляем товары по умолчанию
        if Product.query.count() == 0:
            sample_products = [
                Product(name='Красные розы', description='Букет из 11 красных роз', price=2500, stock=50, category='roses', image_url='https://via.placeholder.com/300x300'),
                Product(name='Белые тюльпаны', description='Букет из 15 белых тюльпанов', price=1800, stock=30, category='tulips', image_url='https://via.placeholder.com/300x300'),
                Product(name='Орхидея фаленопсис', description='Белая орхидея в горшке', price=3500, stock=20, category='orchids', image_url='https://via.placeholder.com/300x300'),
                Product(name='Свадебный букет', description='Роскошный свадебный букет', price=8000, stock=10, category='bouquets', image_url='https://via.placeholder.com/300x300'),
                Product(name='Фикус Бенджамина', description='Красивое комнатное растение', price=1200, stock=25, category='potted', image_url='https://via.placeholder.com/300x300'),
            ]
            for product in sample_products:
                db.session.add(product)
            db.session.commit()
    
    app.run(host='0.0.0.0', port=5000, debug=True)
