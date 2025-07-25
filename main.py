
from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, DecimalField, IntegerField, SelectField, SubmitField
from wtforms.validators import DataRequired, Email, Length, NumberRange
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import os

# Multilingual translations
TRANSLATIONS = {
    'ru': {
        'site_title': 'Цветочный Магазин',
        'home': 'Главная',
        'catalog': 'Каталог',
        'categories': 'Категории',
        'cart': 'Корзина',
        'login': 'Войти',
        'register': 'Регистрация',
        'logout': 'Выйти',
        'my_orders': 'Мои заказы',
        'admin_panel': 'Админ панель',
        'courier_panel': 'Панель курьера',
        'welcome_title': 'Добро пожаловать в FlowerShop',
        'welcome_subtitle': 'Свежие цветы и букеты с доставкой по Ахалцихе',
        'view_catalog': 'Посмотреть каталог',
        'popular_products': 'Популярные товары',
        'add_to_cart': 'Добавить в корзину',
        'continue_shopping': 'Продолжить покупки',
        'roses': 'Розы',
        'tulips': 'Тюльпаны',
        'orchids': 'Орхидеи',
        'bouquets': 'Букеты',
        'potted': 'Горшечные растения',
        'in_stock': 'В наличии',
        'out_of_stock': 'Нет в наличии',
        'price': 'Цена',
        'empty_cart': 'Ваша корзина пуста',
        'total': 'Итого',
        'checkout': 'Оформить заказ',
        'shipping_address': 'Адрес доставки',
        'phone': 'Телефон',
        'username': 'Имя пользователя',
        'password': 'Пароль',
        'email': 'Email',
        'name': 'Название',
        'description': 'Описание',
        'category': 'Категория',
        'quantity': 'Количество',
        'save': 'Сохранить',
        'delete': 'Удалить',
        'edit': 'Редактировать',
        'add': 'Добавить',
        'order_placed': 'Заказ успешно оформлен!',
        'product_added': 'Товар добавлен в корзину!',
        'contacts': 'Контакты',
        'best_flowers': 'Лучшие цветы для ваших близких',
        'address': 'г. Ахалцихе, ул. Руставели, д. 1',
        'newsletter': 'Подписка',
        'newsletter_text': 'Получайте уведомления о новых поступлениях',
        'all_rights': 'Все права защищены',
        'cart_cleared': 'Корзина очищена!',
        'order_not_found': 'Заказ не найден!',
        'invalid_credentials': 'Неверное имя пользователя или пароль!',
        'username_exists': 'Пользователь с таким именем уже существует!',
        'email_exists': 'Пользователь с таким email уже существует!',
        'registration_success': 'Регистрация успешна!',
        'access_denied': 'Доступ запрещен!',
        'product_updated': 'Товар обновлен!',
        'product_deleted': 'Товар удален!',
        'add_product': 'Добавить товар',
        'edit_product': 'Редактировать товар',
        'fast_delivery': 'Быстрая доставка',
        'delivery_text': 'Доставляем свежие цветы в течение 2 часов по Ахалцихе',
        'fresh_flowers': 'Свежие цветы',
        'fresh_text': 'Все цветы доставляются прямо с плантации',
        'pending': 'В ожидании',
        'confirmed': 'Подтвержден',
        'shipped': 'Отправлен',
        'delivered': 'Доставлен',
        'cancelled': 'Отменен',
        'assign_courier': 'Назначить курьера',
        'courier_assigned': 'Курьер назначен',
        'delivery_routes': 'Маршруты доставки',
        'my_deliveries': 'Мои доставки',
        'statistics': 'Статистика',
        'users_management': 'Управление пользователями',
        'make_courier': 'Сделать курьером',
        'remove_courier': 'Убрать курьера',
        'make_admin': 'Сделать админом',
        'remove_admin': 'Убрать админа'
    },
    'en': {
        'site_title': 'Flower Shop',
        'home': 'Home',
        'catalog': 'Catalog',
        'categories': 'Categories',
        'cart': 'Cart',
        'login': 'Login',
        'register': 'Register',
        'logout': 'Logout',
        'my_orders': 'My Orders',
        'admin_panel': 'Admin Panel',
        'courier_panel': 'Courier Panel',
        'welcome_title': 'Welcome to FlowerShop',
        'welcome_subtitle': 'Fresh flowers and bouquets with delivery in Akhaltsikhe',
        'view_catalog': 'View Catalog',
        'popular_products': 'Popular Products',
        'add_to_cart': 'Add to Cart',
        'continue_shopping': 'Continue Shopping',
        'roses': 'Roses',
        'tulips': 'Tulips',
        'orchids': 'Orchids',
        'bouquets': 'Bouquets',
        'potted': 'Potted Plants',
        'in_stock': 'In Stock',
        'out_of_stock': 'Out of Stock',
        'price': 'Price',
        'empty_cart': 'Your cart is empty',
        'total': 'Total',
        'checkout': 'Checkout',
        'shipping_address': 'Shipping Address',
        'phone': 'Phone',
        'username': 'Username',
        'password': 'Password',
        'email': 'Email',
        'name': 'Name',
        'description': 'Description',
        'category': 'Category',
        'quantity': 'Quantity',
        'save': 'Save',
        'delete': 'Delete',
        'edit': 'Edit',
        'add': 'Add',
        'order_placed': 'Order placed successfully!',
        'product_added': 'Product added to cart!',
        'contacts': 'Contacts',
        'best_flowers': 'Best flowers for your loved ones',
        'address': 'Akhaltsikhe, Rustaveli St. 1',
        'newsletter': 'Newsletter',
        'newsletter_text': 'Get notifications about new arrivals',
        'all_rights': 'All rights reserved',
        'cart_cleared': 'Cart cleared!',
        'order_not_found': 'Order not found!',
        'invalid_credentials': 'Invalid username or password!',
        'username_exists': 'User with this username already exists!',
        'email_exists': 'User with this email already exists!',
        'registration_success': 'Registration successful!',
        'access_denied': 'Access denied!',
        'product_updated': 'Product updated!',
        'product_deleted': 'Product deleted!',
        'add_product': 'Add Product',
        'edit_product': 'Edit Product',
        'fast_delivery': 'Fast Delivery',
        'delivery_text': 'We deliver fresh flowers within 2 hours in Akhaltsikhe',
        'fresh_flowers': 'Fresh Flowers',
        'fresh_text': 'All flowers are delivered directly from the plantation',
        'pending': 'Pending',
        'confirmed': 'Confirmed',
        'shipped': 'Shipped',
        'delivered': 'Delivered',
        'cancelled': 'Cancelled',
        'assign_courier': 'Assign Courier',
        'courier_assigned': 'Courier Assigned',
        'delivery_routes': 'Delivery Routes',
        'my_deliveries': 'My Deliveries',
        'statistics': 'Statistics',
        'users_management': 'Users Management',
        'make_courier': 'Make Courier',
        'remove_courier': 'Remove Courier',
        'make_admin': 'Make Admin',
        'remove_admin': 'Remove Admin'
    },
    'ka': {
        'site_title': 'ყვავილების მაღაზია',
        'home': 'მთავარი',
        'catalog': 'კატალოგი',
        'categories': 'კატეგორიები',
        'cart': 'კალათა',
        'login': 'შესვლა',
        'register': 'რეგისტრაცია',
        'logout': 'გასვლა',
        'my_orders': 'ჩემი შეკვეთები',
        'admin_panel': 'ადმინ პანელი',
        'courier_panel': 'კურიერის პანელი',
        'welcome_title': 'კეთილი იყოს თქვენი მობრძანება FlowerShop-ში',
        'welcome_subtitle': 'ახალი ყვავილები და ბუკეტები ახალციხეში მიტანით',
        'view_catalog': 'კატალოგის ნახვა',
        'popular_products': 'პოპულარული პროდუქტები',
        'add_to_cart': 'კალათაში დამატება',
        'continue_shopping': 'საყიდლების გაგრძელება',
        'roses': 'ვარდები',
        'tulips': 'ტიულიპები',
        'orchids': 'ორქიდეები',
        'bouquets': 'ბუკეტები',
        'potted': 'ქოთნიანი მცენარეები',
        'in_stock': 'მარაგშია',
        'out_of_stock': 'არ არის მარაგში',
        'price': 'ფასი',
        'empty_cart': 'თქვენი კალათა ცარიელია',
        'total': 'სულ',
        'checkout': 'შეკვეთის გაფორმება',
        'shipping_address': 'მიტანის მისამართი',
        'phone': 'ტელეფონი',
        'username': 'მომხმარებლის სახელი',
        'password': 'პაროლი',
        'email': 'ელ.ფოსტა',
        'name': 'სახელი',
        'description': 'აღწერა',
        'category': 'კატეგორია',
        'quantity': 'რაოდენობა',
        'save': 'შენახვა',
        'delete': 'წაშლა',
        'edit': 'რედაქტირება',
        'add': 'დამატება',
        'order_placed': 'შეკვეთა წარმატებით გაფორმდა!',
        'product_added': 'პროდუქტი დაემატა კალათაში!',
        'contacts': 'კონტაქტები',
        'best_flowers': 'საუკეთესო ყვავილები თქვენი ახლობლებისთვის',
        'address': 'ახალციხე, რუსთაველის ქ. 1',
        'newsletter': 'ინფორმაციული ბიულეტენი',
        'newsletter_text': 'მიიღეთ შეტყობინებები ახალი მოსვლების შესახებ',
        'all_rights': 'ყველა უფლება დაცულია',
        'cart_cleared': 'კალათა გაიწმინდა!',
        'order_not_found': 'შეკვეთა ვერ მოიძებნა!',
        'invalid_credentials': 'არასწორი მომხმარებლის სახელი ან პაროლი!',
        'username_exists': 'ამ სახელის მქონე მომხმარებელი უკვე არსებობს!',
        'email_exists': 'ამ ელ.ფოსტის მქონე მომხმარებელი უკვე არსებობს!',
        'registration_success': 'რეგისტრაცია წარმატებულია!',
        'access_denied': 'წვდომა აკრძალულია!',
        'product_updated': 'პროდუქტი განახლდა!',
        'product_deleted': 'პროდუქტი წაიშალა!',
        'add_product': 'პროდუქტის დამატება',
        'edit_product': 'პროდუქტის რედაქტირება',
        'fast_delivery': 'სწრაფი მიტანა',
        'delivery_text': 'ვაწვდით ახალ ყვავილებს 2 საათში ახალციხეში',
        'fresh_flowers': 'ახალი ყვავილები',
        'fresh_text': 'ყველა ყვავილი მიეწოდება პირდაპირ პლანტაციიდან',
        'pending': 'მოლოდინში',
        'confirmed': 'დადასტურებული',
        'shipped': 'გაგზავნილი',
        'delivered': 'მიტანილი',
        'cancelled': 'გაუქმებული',
        'assign_courier': 'კურიერის დანიშვნა',
        'courier_assigned': 'კურიერი დანიშნულია',
        'delivery_routes': 'მიტანის მარშრუტები',
        'my_deliveries': 'ჩემი მიტანები',
        'statistics': 'სტატისტიკა',
        'users_management': 'მომხმარებლების მართვა',
        'make_courier': 'კურიერად გაკეთება',
        'remove_courier': 'კურიერის მოხსნა',
        'make_admin': 'ადმინად გაკეთება',
        'remove_admin': 'ადმინის მოხსნა'
    }
}

def get_language():
    return session.get('language', 'ru')

def get_text(key):
    lang = get_language()
    return TRANSLATIONS.get(lang, TRANSLATIONS['ru']).get(key, key)

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
    is_courier = db.Column(db.Boolean, default=False)
    orders = db.relationship('Order', foreign_keys='Order.user_id', backref='user', lazy=True)
    courier_orders = db.relationship('Order', foreign_keys='Order.courier_id', backref='courier', lazy=True)

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
    courier_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    total_amount = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(20), default='pending')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    shipping_address = db.Column(db.Text)
    district = db.Column(db.String(100))
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
    district = SelectField('Район', choices=[
        ('center', 'Центр города Ахалцихе'),
        ('rustaveli', 'Район Руставели'),
        ('agmashenebeli', 'Агмашенебели'),
        ('tabatskuri', 'Табацкури'),
        ('vale', 'Вале'),
        ('ahaltsikhe_village', 'Село Ахалциха'),
        ('other_village', 'Другое село (в пределах района)')
    ], validators=[DataRequired()])
    shipping_address = TextAreaField('Точный адрес', validators=[DataRequired()], 
                                   render_kw={"placeholder": "Улица, дом, квартира"})
    phone = StringField('Телефон', validators=[DataRequired()], 
                       render_kw={"placeholder": "+995 XXX XXX XXX"})
    submit = SubmitField('Оформить заказ')

# Routes
@app.route('/set_language/<language>')
def set_language(language):
    if language in ['ru', 'en', 'ka']:
        session['language'] = language
    return redirect(request.referrer or url_for('index'))

def get_product(product_id):
    return Product.query.get(int(product_id))

def get_couriers():
    return User.query.filter_by(is_courier=True).all()

@app.context_processor
def inject_globals():
    return dict(get_language=get_language, get_text=get_text, get_product=get_product, Product=Product, get_couriers=get_couriers)

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
    flash(get_text('product_added'), 'success')
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

@app.route('/clear_cart')
def clear_cart():
    if 'cart' in session:
        session.pop('cart', None)
        session.modified = True
        flash(get_text('cart_cleared') if get_text('cart_cleared') != 'cart_cleared' else 'Корзина очищена!', 'success')
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
            district=form.district.data,
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
        flash(get_text('order_not_found') if get_text('order_not_found') != 'order_not_found' else 'Заказ не найден!', 'error')
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
        flash(get_text('invalid_credentials') if get_text('invalid_credentials') != 'invalid_credentials' else 'Неверное имя пользователя или пароль!', 'error')
    return render_template('login.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        existing_user = User.query.filter_by(username=form.username.data).first()
        existing_email = User.query.filter_by(email=form.email.data).first()
        
        if existing_user:
            flash(get_text('username_exists') if get_text('username_exists') != 'username_exists' else 'Пользователь с таким именем уже существует!', 'error')
        elif existing_email:
            flash(get_text('email_exists') if get_text('email_exists') != 'email_exists' else 'Пользователь с таким email уже существует!', 'error')
        else:
            user = User(
                username=form.username.data,
                email=form.email.data,
                password_hash=generate_password_hash(form.password.data)
            )
            db.session.add(user)
            db.session.commit()
            login_user(user)
            flash(get_text('registration_success') if get_text('registration_success') != 'registration_success' else 'Регистрация успешна!', 'success')
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
        flash(get_text('access_denied') if get_text('access_denied') != 'access_denied' else 'Доступ запрещен!', 'error')
        return redirect(url_for('index'))
    
    products = Product.query.all()
    orders = Order.query.order_by(Order.created_at.desc()).limit(10).all()
    return render_template('admin/dashboard.html', products=products, orders=orders)

@app.route('/admin/products')
@login_required
def admin_products():
    if not current_user.is_admin:
        flash(get_text('access_denied') if get_text('access_denied') != 'access_denied' else 'Доступ запрещен!', 'error')
        return redirect(url_for('index'))
    
    products = Product.query.all()
    return render_template('admin/products.html', products=products)

@app.route('/admin/product/add', methods=['GET', 'POST'])
@login_required
def admin_add_product():
    if not current_user.is_admin:
        flash(get_text('access_denied') if get_text('access_denied') != 'access_denied' else 'Доступ запрещен!', 'error')
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
        flash(get_text('product_added') if get_text('product_added') != 'product_added' else 'Товар добавлен!', 'success')
        return redirect(url_for('admin_products'))
    
    return render_template('admin/product_form.html', form=form, title=get_text('add_product') if get_text('add_product') != 'add_product' else 'Добавить товар')

@app.route('/admin/product/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def admin_edit_product(id):
    if not current_user.is_admin:
        flash(get_text('access_denied') if get_text('access_denied') != 'access_denied' else 'Доступ запрещен!', 'error')
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
        flash(get_text('product_updated') if get_text('product_updated') != 'product_updated' else 'Товар обновлен!', 'success')
        return redirect(url_for('admin_products'))
    
    return render_template('admin/product_form.html', form=form, title=get_text('edit_product') if get_text('edit_product') != 'edit_product' else 'Редактировать товар')

@app.route('/admin/product/<int:id>/delete')
@login_required
def admin_delete_product(id):
    if not current_user.is_admin:
        flash(get_text('access_denied') if get_text('access_denied') != 'access_denied' else 'Доступ запрещен!', 'error')
        return redirect(url_for('index'))
    
    product = Product.query.get_or_404(id)
    db.session.delete(product)
    db.session.commit()
    flash(get_text('product_deleted') if get_text('product_deleted') != 'product_deleted' else 'Товар удален!', 'success')
    return redirect(url_for('admin_products'))

@app.route('/admin/orders')
@login_required
def admin_orders():
    if not current_user.is_admin:
        flash(get_text('access_denied') if get_text('access_denied') != 'access_denied' else 'Доступ запрещен!', 'error')
        return redirect(url_for('index'))
    
    orders = Order.query.order_by(Order.created_at.desc()).all()
    return render_template('admin/orders.html', orders=orders)

@app.route('/admin/order/<int:id>/update_status', methods=['POST'])
@login_required
def admin_update_order_status(id):
    if not current_user.is_admin:
        flash(get_text('access_denied'), 'error')
        return redirect(url_for('index'))
    
    order = Order.query.get_or_404(id)
    status = request.form.get('status')
    courier_id = request.form.get('courier_id')
    
    order.status = status
    if courier_id:
        order.courier_id = int(courier_id) if courier_id != '' else None
    
    db.session.commit()
    flash(get_text('order_updated') if get_text('order_updated') != 'order_updated' else 'Заказ обновлен!', 'success')
    return redirect(url_for('admin_orders'))

# Courier routes
@app.route('/courier')
@login_required
def courier_dashboard():
    if not current_user.is_courier and not current_user.is_admin:
        flash(get_text('access_denied'), 'error')
        return redirect(url_for('index'))
    
    my_orders = Order.query.filter_by(courier_id=current_user.id).order_by(Order.created_at.desc()).all()
    return render_template('courier/dashboard.html', orders=my_orders)

@app.route('/courier/order/<int:id>/update_status', methods=['POST'])
@login_required
def courier_update_status(id):
    if not current_user.is_courier and not current_user.is_admin:
        flash(get_text('access_denied'), 'error')
        return redirect(url_for('index'))
    
    order = Order.query.get_or_404(id)
    if order.courier_id != current_user.id and not current_user.is_admin:
        flash(get_text('access_denied'), 'error')
        return redirect(url_for('courier_dashboard'))
    
    status = request.form.get('status')
    order.status = status
    db.session.commit()
    flash(get_text('order_updated') if get_text('order_updated') != 'order_updated' else 'Статус заказа обновлен!', 'success')
    return redirect(url_for('courier_dashboard'))

# Admin user management
@app.route('/admin/users')
@login_required
def admin_users():
    if not current_user.is_admin:
        flash(get_text('access_denied'), 'error')
        return redirect(url_for('index'))
    
    users = User.query.all()
    return render_template('admin/users.html', users=users)

@app.route('/admin/user/<int:id>/toggle_role', methods=['POST'])
@login_required
def admin_toggle_user_role(id):
    if not current_user.is_admin:
        flash(get_text('access_denied'), 'error')
        return redirect(url_for('index'))
    
    user = User.query.get_or_404(id)
    role = request.form.get('role')
    
    if role == 'courier':
        user.is_courier = not user.is_courier
        message = get_text('courier_assigned') if user.is_courier else get_text('courier_removed') if get_text('courier_removed') != 'courier_removed' else 'Курьер удален'
    elif role == 'admin':
        user.is_admin = not user.is_admin
        message = get_text('admin_assigned') if get_text('admin_assigned') != 'admin_assigned' else 'Админ назначен' if user.is_admin else get_text('admin_removed') if get_text('admin_removed') != 'admin_removed' else 'Админ удален'
    
    db.session.commit()
    flash(message, 'success')
    return redirect(url_for('admin_users'))

# Statistics route
@app.route('/admin/statistics')
@login_required
def admin_statistics():
    if not current_user.is_admin:
        flash(get_text('access_denied'), 'error')
        return redirect(url_for('index'))
    
    total_orders = Order.query.count()
    total_revenue = db.session.query(db.func.sum(Order.total_amount)).scalar() or 0
    total_products = Product.query.count()
    total_users = User.query.count()
    
    # Orders by district
    district_stats = db.session.query(Order.district, db.func.count(Order.id)).group_by(Order.district).all()
    
    # Orders by status
    status_stats = db.session.query(Order.status, db.func.count(Order.id)).group_by(Order.status).all()
    
    return render_template('admin/statistics.html', 
                         total_orders=total_orders,
                         total_revenue=total_revenue,
                         total_products=total_products,
                         total_users=total_users,
                         district_stats=district_stats,
                         status_stats=status_stats)

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
            
        # Создаем курьера по умолчанию
        courier = User.query.filter_by(username='courier').first()
        if not courier:
            courier = User(
                username='courier',
                email='courier@example.com',
                password_hash=generate_password_hash('courier123'),
                is_courier=True
            )
            db.session.add(courier)
            
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
