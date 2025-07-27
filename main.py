from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, logout_user, login_required, current_user, UserMixin
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, SelectField, DecimalField, IntegerField, SubmitField
from wtforms.validators import DataRequired, Length, Email, NumberRange
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import os
import logging
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

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
        'welcome_title': 'Добро пожаловать в FlowerShop',
        'welcome_subtitle': 'Лучший цветочный магазин в Ахалцихе',
        'shop_now': 'Купить сейчас',
        'learn_more': 'Узнать больше',
        'why_choose_us': 'Почему выбирают нас',
        'featured_products': 'Рекомендуемые товары',
        'best_sellers': 'Хиты продаж',
        'view_details': 'Подробнее',
        'featured': 'Рекомендуем',
        'view_all_products': 'Посмотреть все товары',
        'happy_customers': 'довольных клиентов',
        'orders_delivered': 'выполненных заказов',
        'flower_varieties': 'видов цветов',
        'customer_support': 'поддержка клиентов',
        'customer_reviews': 'Отзывы клиентов',
        'what_customers_say': 'Что говорят наши клиенты',
        'guarantee_text': '100% гарантия качества на все цветы',
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
        'remove_admin': 'Убрать админа',
        'details': 'Подробнее',
        'no_account': 'Нет аккаунта?',
        'have_account': 'Уже есть аккаунт?',
        'all_categories': 'Все категории',
        'no_products': 'Товары не найдены',
        'no_products_text': 'В данной категории пока нет товаров',
        'back_to_catalog': 'Вернуться к каталогу',
        'related_products': 'Похожие товары',
        'view': 'Посмотреть',
        'order_summary': 'Итого по заказу',
        'confirm_clear_cart': 'Очистить корзину?',
        'clear_cart': 'Очистить корзину',
        'login_to_checkout': 'Войдите в аккаунт для оформления заказа',
        'empty_cart_text': 'Добавьте товары в корзину, чтобы продолжить покупки',
        'view_all': 'Смотреть все товары',
        'quality_guarantee': 'Гарантия качества',
        'quality_text': 'Возвращаем деньги, если цветы не свежие'
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
        'remove_admin': 'Remove Admin',
        'details': 'Details',
        'no_account': 'No account?',
        'have_account': 'Already have an account?',
        'all_categories': 'All Categories',
        'no_products': 'No products found',
        'no_products_text': 'No products in this category yet',
        'back_to_catalog': 'Back to catalog',
        'related_products': 'Related products',
        'view': 'View',
        'order_summary': 'Order Summary',
        'confirm_clear_cart': 'Clear cart?',
        'clear_cart': 'Clear cart',
        'login_to_checkout': 'Login to checkout',
        'empty_cart_text': 'Add products to cart to continue shopping',
        'view_all': 'View all products',
        'quality_guarantee': 'Quality Guarantee',
        'quality_text': 'Money back if flowers are not fresh'
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
        'remove_admin': 'ადმინის მოხსნა',
        'details': 'დეტალები',
        'no_account': 'არ გაქვთ ანგარიში?',
        'have_account': 'უკვე გაქვთ ანგარიში?',
        'all_categories': 'ყველა კატეგორია',
        'no_products': 'პროდუქტები ვერ მოიძებნა',
        'no_products_text': 'ამ კატეგორიაში ჯერ არ არის პროდუქტები',
        'back_to_catalog': 'კატალოგში დაბრუნება',
        'related_products': 'მსგავსი პროდუქტები',
        'view': 'ნახვა',
        'order_summary': 'შეკვეთის ჯამი',
        'confirm_clear_cart': 'კალათის გაწმენდა?',
        'clear_cart': 'კალათის გაწმენდა',
        'login_to_checkout': 'შეკვეთისთვის შედით სისტემაში',
        'empty_cart_text': 'დაამატეთ პროდუქტები კალათაში საყიდლების გასაგრძელებლად',
        'view_all': 'ყველას ნახვა',
        'quality_guarantee': 'ხარისხის გარანტია',
        'quality_text': 'ფული უბრუნდება თუ ყვავილები არ არის ახალი'
    }
}

def get_language():
    return session.get('language', 'ru')

def get_text(key):
    lang = get_language()
    return TRANSLATIONS.get(lang, TRANSLATIONS['ru']).get(key, key)

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your-secret-key-here')

# Supabase PostgreSQL configuration
DATABASE_URL = os.environ.get('DATABASE_URL')
if DATABASE_URL:
    # Use Supabase PostgreSQL
    app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
else:
    # Fallback to SQLite for local development
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///flower_shop.db'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    'pool_pre_ping': True,
    'pool_recycle': 300,
}

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Models
class SiteSettings(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    site_name = db.Column(db.String(100), default='FlowerShop')
    site_description = db.Column(db.Text, default='Лучший цветочный магазин в Ахалцихе')
    contact_phone = db.Column(db.String(20), default='+995 XXX XXX XXX')
    contact_email = db.Column(db.String(100), default='info@flowershop.com')
    contact_address = db.Column(db.Text, default='г. Ахалцихе, ул. Руставели, д. 1')
    delivery_cost_city = db.Column(db.Float, default=5.0)
    delivery_cost_village = db.Column(db.Float, default=10.0)
    currency = db.Column(db.String(10), default='₾')
    logo_url = db.Column(db.String(200))
    hero_title = db.Column(db.String(200), default='Добро пожаловать в FlowerShop')
    hero_subtitle = db.Column(db.Text, default='Свежие цветы и букеты с доставкой по Ахалцихе')
    
    @staticmethod
    def get_settings():
        settings = SiteSettings.query.first()
        if not settings:
            settings = SiteSettings()
            db.session.add(settings)
            db.session.commit()
        return settings

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    slug = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.Text)
    image_url = db.Column(db.String(200))
    is_active = db.Column(db.Boolean, default=True)
    sort_order = db.Column(db.Integer, default=0)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(20))
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
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    image_url = db.Column(db.String(200))
    is_visible = db.Column(db.Boolean, default=True)
    is_featured = db.Column(db.Boolean, default=False)
    category_obj = db.relationship('Category', backref='products')

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
    payment_method = db.Column(db.String(20), default='cash')
    bank = db.Column(db.String(50))
    payment_status = db.Column(db.String(20), default='pending')
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
    return db.session.get(User, int(user_id))

# Forms
class LoginForm(FlaskForm):
    username = StringField('Имя пользователя', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    submit = SubmitField('Войти')

class RegisterForm(FlaskForm):
    username = StringField('Имя пользователя', validators=[DataRequired(), Length(min=4, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    phone = StringField('Телефон', validators=[DataRequired()], render_kw={"placeholder": "+995 XXX XXX XXX"})
    password = PasswordField('Пароль', validators=[DataRequired(), Length(min=6)])
    submit = SubmitField('Зарегистрироваться')

class SiteSettingsForm(FlaskForm):
    site_name = StringField('Название сайта', validators=[DataRequired()])
    site_description = TextAreaField('Описание сайта')
    contact_phone = StringField('Телефон')
    contact_email = StringField('Email')
    contact_address = TextAreaField('Адрес')
    delivery_cost_city = DecimalField('Стоимость доставки по городу', validators=[NumberRange(min=0)])
    delivery_cost_village = DecimalField('Стоимость доставки по деревням', validators=[NumberRange(min=0)])
    currency = StringField('Валюта')
    logo_url = StringField('URL логотипа')
    hero_title = StringField('Заголовок главной страницы')
    hero_subtitle = TextAreaField('Подзаголовок главной страницы')
    submit = SubmitField('Сохранить настройки')

class CategoryForm(FlaskForm):
    name = StringField('Название категории', validators=[DataRequired()])
    slug = StringField('Slug (URL)', validators=[DataRequired()])
    description = TextAreaField('Описание')
    image_url = StringField('URL изображения')
    is_active = SelectField('Активность', choices=[('True', 'Активная'), ('False', 'Неактивная')], default='True')
    sort_order = IntegerField('Порядок сортировки', default=0)
    submit = SubmitField('Сохранить')

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
    is_visible = SelectField('Видимость', choices=[
        ('True', 'Видимый'),
        ('False', 'Скрытый')
    ], default='True')
    is_featured = SelectField('Рекомендуемый', choices=[
        ('True', 'Да'),
        ('False', 'Нет')
    ], default='False')
    submit = SubmitField('Сохранить')

class CheckoutForm(FlaskForm):
    district = SelectField('Район', choices=[
        ('center', 'Центр Ахалцихе - 5₾'),
        ('rustaveli', 'Руставели - 5₾'),
        ('agmashenebeli', 'Агмашенебели - 5₾'),
        ('rabat', 'Рабат - 5₾'),
        ('tabatskuri', 'Табацкури - 10₾'),
        ('vale', 'Вале - 10₾'),
        ('okami', 'Окаме - 10₾'),
        ('akhalkalaki_road', 'Ахалкалакская дорога - 10₾')
    ], validators=[DataRequired()])
    shipping_address = TextAreaField('Точный адрес', validators=[DataRequired()], 
                                   render_kw={"placeholder": "Улица, дом, квартира"})
    phone = StringField('Телефон', validators=[DataRequired()], 
                       render_kw={"placeholder": "+995 XXX XXX XXX"})
    payment_method = SelectField('Способ оплаты', choices=[
        ('cash', 'Наличными при получении'),
        ('online', 'Онлайн оплата')
    ], default='cash')
    bank = SelectField('Банк', choices=[
        ('', 'Выберите банк'),
        ('tbc', 'TBC Bank'),
        ('liberty', 'Liberty Bank'),
        ('georgia', 'საქართველოს ბანკი')
    ])
    submit = SubmitField('Оформить заказ')

# Routes
@app.route('/set_language/<language>')
def set_language(language):
    if language in ['ru', 'en', 'ka']:
        session['language'] = language
    return redirect(request.referrer or url_for('index'))

def get_product(product_id):
    return db.session.get(Product, int(product_id))

def get_couriers():
    return User.query.filter_by(is_courier=True).all()

def get_delivery_cost(district):
    """Calculate delivery cost based on district"""
    # Ахалцихе (5 лари)
    city_districts = ['center', 'rustaveli', 'agmashenebeli', 'rabat']
    # Деревни возле Ахалцихе (10 лари)  
    village_districts = ['tabatskuri', 'vale', 'okami', 'akhalkalaki_road']

    if district in city_districts:
        return 5
    elif district in village_districts:
        return 10
    else:
        return 10  # default for any other areas

@app.context_processor
def inject_globals():
    settings = SiteSettings.get_settings()
    categories = Category.query.filter_by(is_active=True).order_by(Category.sort_order).all()
    return dict(
        get_language=get_language, 
        get_text=get_text, 
        get_product=get_product, 
        Product=Product, 
        get_couriers=get_couriers, 
        get_delivery_cost=get_delivery_cost,
        site_settings=settings,
        categories=categories
    )

@app.route('/')
def index():
    featured_products = Product.query.filter_by(is_featured=True, is_visible=True).limit(4).all()
    products = Product.query.filter_by(is_visible=True).limit(8).all()
    return render_template('index.html', products=products, featured_products=featured_products)

@app.route('/catalog')
def catalog():
    category = request.args.get('category')
    if category:
        products = Product.query.filter_by(category=category, is_visible=True).all()
    else:
        products = Product.query.filter_by(is_visible=True).all()
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

    if request.method == 'POST':
        # Manual form validation
        district = request.form.get('district')
        shipping_address = request.form.get('shipping_address', '').strip()
        phone = request.form.get('phone', '').strip()
        payment_method = request.form.get('payment', 'cash')
        bank = request.form.get('bank', '') if payment_method == 'online' else None
        delivery_method = request.form.get('delivery', 'standard')

        # Validation
        errors = []
        if not district:
            errors.append('Выберите район доставки')
        if not shipping_address:
            errors.append('Укажите адрес доставки')
        if not phone:
            errors.append('Укажите номер телефона')
        if payment_method == 'online' and not bank:
            errors.append('Выберите банк для онлайн-оплаты')

        if not errors:
            # Создаем заказ
            total = 0
            cart = session['cart']

            for product_id, quantity in cart.items():
                product = Product.query.get(int(product_id))
                if product:
                    total += product.price * quantity

            # Calculate delivery cost
            delivery_cost = 0
            if delivery_method != 'pickup':
                delivery_cost = get_delivery_cost(district)

            # Add delivery cost to total
            final_total = total + delivery_cost

            order = Order(
                user_id=current_user.id,
                total_amount=final_total,
                shipping_address=shipping_address,
                district=district,
                phone=phone,
                payment_method=payment_method,
                bank=bank,
                payment_status='pending' if payment_method == 'online' else 'not_required',
                status='confirmed'  # Автоматически подтверждаем заказ для курьеров
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

            # Handle payment method
            if payment_method == 'online' and bank:
                flash(f'Заказ оформлен! Перенаправляем на оплату через {bank.upper()}...', 'info')
                return redirect(url_for('payment_redirect', order_id=order.id, bank=bank))
            else:
                flash('Заказ успешно оформлен!', 'success')
                return redirect(url_for('order_success', order_id=order.id))
        else:
            # Show validation errors
            for error in errors:
                flash(error, 'error')

    return render_template('checkout.html', form=form)

@app.route('/payment_redirect/<int:order_id>/<bank>')
@login_required
def payment_redirect(order_id, bank):
    order = Order.query.get_or_404(order_id)
    if order.user_id != current_user.id:
        flash('Заказ не найден!', 'error')
        return redirect(url_for('index'))

    # Simulate bank redirect URLs (в реальном проекте здесь будут настоящие API банков)
    bank_urls = {
        'tbc': f'https://ecommerce.tbc.ge/payment?amount={order.total_amount}&order_id={order.id}',
        'liberty': f'https://pay.libertybank.ge/payment?amount={order.total_amount}&order_id={order.id}',
        'georgia': f'https://ipay.bog.ge/payment?amount={order.total_amount}&order_id={order.id}'
    }

    bank_names = {
        'tbc': 'TBC Bank',
        'liberty': 'Liberty Bank', 
        'georgia': 'საქართველოს ბანკი'
    }

    if bank not in bank_urls:
        flash('Неподдерживаемый банк!', 'error')
        return redirect(url_for('order_success', order_id=order.id))

    return render_template('payment_redirect.html', 
                         order=order, 
                         bank_url=bank_urls[bank],
                         bank_name=bank_names[bank])

@app.route('/payment_success/<int:order_id>')
@login_required  
def payment_success(order_id):
    order = Order.query.get_or_404(order_id)
    if order.user_id != current_user.id:
        flash('Заказ не найден!', 'error')
        return redirect(url_for('index'))

    # Update payment status
    order.payment_status = 'completed'
    order.status = 'confirmed'
    db.session.commit()

    flash('Оплата прошла успешно! Ваш заказ подтвержден.', 'success')
    return redirect(url_for('order_success', order_id=order.id))

@app.route('/payment_failed/<int:order_id>')
@login_required
def payment_failed(order_id):
    order = Order.query.get_or_404(order_id)
    if order.user_id != current_user.id:
        flash('Заказ не найден!', 'error')
        return redirect(url_for('index'))

    order.payment_status = 'failed'
    db.session.commit()

    flash('Оплата не прошла. Вы можете попробовать еще раз или выбрать другой способ оплаты.', 'warning')
    return redirect(url_for('order_success', order_id=order.id))

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
                phone=form.phone.data,
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
            image_url=form.image_url.data,
            is_visible=form.is_visible.data == 'True',
            is_featured=form.is_featured.data == 'True'
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

    product = db.get_or_404(Product, id)
    form = ProductForm(obj=product)

    if form.validate_on_submit():
        product.name = form.name.data
        product.description = form.description.data
        product.price = float(form.price.data)
        product.stock = form.stock.data
        product.category = form.category.data
        product.image_url = form.image_url.data
        product.is_visible = form.is_visible.data == 'True'
        product.is_featured = form.is_featured.data == 'True'
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

    product = db.get_or_404(Product, id)
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

    order = db.get_or_404(Order, id)
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

    # My assigned orders
    my_orders = Order.query.filter_by(courier_id=current_user.id).order_by(Order.created_at.desc()).all()

    # Available orders (not assigned to any courier and confirmed)
    available_orders = Order.query.filter_by(courier_id=None).filter(
        Order.status.in_(['confirmed', 'pending'])
    ).order_by(Order.created_at.desc()).all()

    # Statistics for courier
    total_deliveries = Order.query.filter_by(courier_id=current_user.id, status='delivered').count()
    pending_deliveries = Order.query.filter_by(courier_id=current_user.id).filter(
        Order.status.in_(['confirmed', 'shipped'])
    ).count()

    return render_template('courier/dashboard.html', 
                         orders=my_orders,
                         available_orders=available_orders,
                         total_deliveries=total_deliveries,
                         pending_deliveries=pending_deliveries)

# Take order by courier
@app.route('/courier/take_order/<int:order_id>')
@login_required
def courier_take_order(order_id):
    if not current_user.is_courier and not current_user.is_admin:
        flash(get_text('access_denied'), 'error')
        return redirect(url_for('index'))

    order = Order.query.get_or_404(order_id)
    if order.courier_id is None and order.status in ['confirmed', 'pending']:
        order.courier_id = current_user.id
        order.status = 'shipped'
        db.session.commit()
        flash('Заказ взят в работу!', 'success')
    else:
        flash('Заказ уже назначен или недоступен', 'warning')

    return redirect(url_for('courier_dashboard'))

@app.route('/courier/order/<int:id>/update_status', methods=['POST'])
@login_required
def courier_update_status(id):
    if not current_user.is_courier and not current_user.is_admin:
        flash(get_text('access_denied'), 'error')
        return redirect(url_for('index'))

    order = db.get_or_404(Order, id)
    if order.courier_id != current_user.id and not current_user.is_admin:
        flash(get_text('access_denied'), 'error')
        return redirect(url_for('courier_dashboard'))

    status = request.form.get('status')
    order.status = status
    db.session.commit()
    flash(get_text('order_updated') if get_text('order_updated') != 'order_updated' else 'Статус заказа обновлен!', 'success')
    return redirect(url_for('courier_dashboard'))

# Admin settings
@app.route('/admin/settings', methods=['GET', 'POST'])
@login_required
def admin_settings():
    if not current_user.is_admin:
        flash(get_text('access_denied'), 'error')
        return redirect(url_for('index'))

    settings = SiteSettings.get_settings()
    form = SiteSettingsForm(obj=settings)

    if form.validate_on_submit():
        settings.site_name = form.site_name.data
        settings.site_description = form.site_description.data
        settings.contact_phone = form.contact_phone.data
        settings.contact_email = form.contact_email.data
        settings.contact_address = form.contact_address.data
        settings.delivery_cost_city = float(form.delivery_cost_city.data)
        settings.delivery_cost_village = float(form.delivery_cost_village.data)
        settings.currency = form.currency.data
        settings.logo_url = form.logo_url.data
        settings.hero_title = form.hero_title.data
        settings.hero_subtitle = form.hero_subtitle.data
        db.session.commit()
        flash('Настройки сайта обновлены!', 'success')
        return redirect(url_for('admin_settings'))

    return render_template('admin/settings.html', form=form, settings=settings)

# Admin categories
@app.route('/admin/categories')
@login_required
def admin_categories():
    if not current_user.is_admin:
        flash(get_text('access_denied'), 'error')
        return redirect(url_for('index'))

    categories = Category.query.order_by(Category.sort_order).all()
    return render_template('admin/categories.html', categories=categories)

@app.route('/admin/category/add', methods=['GET', 'POST'])
@login_required
def admin_add_category():
    if not current_user.is_admin:
        flash(get_text('access_denied'), 'error')
        return redirect(url_for('index'))

    form = CategoryForm()
    if form.validate_on_submit():
        category = Category(
            name=form.name.data,
            slug=form.slug.data,
            description=form.description.data,
            image_url=form.image_url.data,
            is_active=form.is_active.data == 'True',
            sort_order=form.sort_order.data
        )
        db.session.add(category)
        db.session.commit()
        flash('Категория добавлена!', 'success')
        return redirect(url_for('admin_categories'))

    return render_template('admin/category_form.html', form=form, title='Добавить категорию')

@app.route('/admin/category/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def admin_edit_category(id):
    if not current_user.is_admin:
        flash(get_text('access_denied'), 'error')
        return redirect(url_for('index'))

    category = Category.query.get_or_404(id)
    form = CategoryForm(obj=category)

    if form.validate_on_submit():
        category.name = form.name.data
        category.slug = form.slug.data
        category.description = form.description.data
        category.image_url = form.image_url.data
        category.is_active = form.is_active.data == 'True'
        category.sort_order = form.sort_order.data
        db.session.commit()
        flash('Категория обновлена!', 'success')
        return redirect(url_for('admin_categories'))

    return render_template('admin/category_form.html', form=form, title='Редактировать категорию')

@app.route('/admin/category/<int:id>/delete')
@login_required
def admin_delete_category(id):
    if not current_user.is_admin:
        flash(get_text('access_denied'), 'error')
        return redirect(url_for('index'))

    category = Category.query.get_or_404(id)
    # Update products to remove category reference
    Product.query.filter_by(category_id=category.id).update({'category_id': None})
    db.session.delete(category)
    db.session.commit()
    flash('Категория удалена!', 'success')
    return redirect(url_for('admin_categories'))

# Admin user management
@app.route('/admin/users')
@login_required
def admin_users():
    if not current_user.is_admin:
        flash(get_text('access_denied'), 'error')
        return redirect(url_for('index'))

    users = User.query.all()
    total_users = User.query.count()
    total_admins = User.query.filter_by(is_admin=True).count()
    total_couriers = User.query.filter_by(is_courier=True).count()

    return render_template('admin/users.html', 
                         users=users,
                         total_users=total_users,
                         total_admins=total_admins,
                         total_couriers=total_couriers)

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

# API Routes
@app.route('/api/product/<int:id>')
def api_product(id):
    product = Product.query.get_or_404(id)
    return jsonify({
        'id': product.id,
        'name': product.name,
        'description': product.description,
        'price': product.price,
        'stock': product.stock,
        'category': product.category,
        'image_url': product.image_url,
        'is_visible': product.is_visible
    })

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

    # Recent orders
    recent_orders = Order.query.order_by(Order.created_at.desc()).limit(5).all()

    # Low stock products
    low_stock_products = Product.query.filter(Product.stock <= 5).all()

    # Best selling products
    best_products = db.session.query(
        Product.name, 
        db.func.sum(OrderItem.quantity).label('total_sold')
    ).join(OrderItem).group_by(Product.id).order_by(db.desc('total_sold')).limit(5).all()

    # Orders by district
    district_stats = db.session.query(Order.district, db.func.count(Order.id)).group_by(Order.district).all()

    # Orders by status
    status_stats = db.session.query(Order.status, db.func.count(Order.id)).group_by(Order.status).all()

    # Monthly revenue
    from datetime import datetime, timedelta
    last_30_days = datetime.utcnow() - timedelta(days=30)
    monthly_revenue = db.session.query(db.func.sum(Order.total_amount)).filter(
        Order.created_at >= last_30_days
    ).scalar() or 0

    return render_template('admin/statistics.html', 
                         total_orders=total_orders,
                         total_revenue=total_revenue,
                         total_products=total_products,
                         total_users=total_users,
                         district_stats=district_stats,
                         status_stats=status_stats,
                         recent_orders=recent_orders,
                         low_stock_products=low_stock_products,
                         best_products=best_products,
                         monthly_revenue=monthly_revenue)

# Bulk operations for admin
@app.route('/admin/products/bulk_update', methods=['POST'])
@login_required
def admin_bulk_update_products():
    if not current_user.is_admin:
        flash(get_text('access_denied'), 'error')
        return redirect(url_for('index'))

    action = request.form.get('action')
    product_ids = request.form.getlist('product_ids')

    if not product_ids:
        flash('Выберите товары для операции', 'warning')
        return redirect(url_for('admin_products'))

    if action == 'delete':
        Product.query.filter(Product.id.in_(product_ids)).delete(synchronize_session=False)
        flash(f'Удалено товаров: {len(product_ids)}', 'success')
    elif action == 'update_stock':
        new_stock = int(request.form.get('new_stock', 0))
        Product.query.filter(Product.id.in_(product_ids)).update(
            {'stock': new_stock}, synchronize_session=False
        )
        flash(f'Обновлен склад для {len(product_ids)} товаров', 'success')

    db.session.commit()
    return redirect(url_for('admin_products'))

# Enhanced order management
@app.route('/admin/orders/bulk_update', methods=['POST'])
@login_required
def admin_bulk_update_orders():
    if not current_user.is_admin:
        flash(get_text('access_denied'), 'error')
        return redirect(url_for('index'))

    action = request.form.get('action')
    order_ids = request.form.getlist('order_ids')

    if not order_ids:
        flash('Выберите заказы для операции', 'warning')
        return redirect(url_for('admin_orders'))

    if action == 'confirm':
        Order.query.filter(Order.id.in_(order_ids)).update(
            {'status': 'confirmed'}, synchronize_session=False
        )
        flash(f'Подтверждено заказов: {len(order_ids)}', 'success')
    elif action == 'cancel':
        Order.query.filter(Order.id.in_(order_ids)).update(
            {'status': 'cancelled'}, synchronize_session=False
        )
        flash(f'Отменено заказов: {len(order_ids)}', 'success')

    db.session.commit()
    return redirect(url_for('admin_orders'))

if __name__ == '__main__':
    with app.app_context():
        try:
            # Create all tables
            db.create_all()
            print("Database tables created successfully")

            # Создаем админа по умолчанию если его нет
            admin = User.query.filter_by(username='admin').first()
        if not admin:
            admin = User(
                username='admin',
                email='admin@flowershop.com',
                phone='+995 555 123 456',
                password_hash=generate_password_hash('admin123'),
                is_admin=True
            )
            db.session.add(admin)
            db.session.commit()
            print("Админ создан: admin/admin123")

        # Создаем курьера по умолчанию если его нет
        courier = User.query.filter_by(username='courier').first()
        if not courier:
            courier = User(
                username='courier',
                email='courier@flowershop.com',
                phone='+995 555 654 321',
                password_hash=generate_password_hash('courier123'),
                is_courier=True
            )
            db.session.add(courier)
            db.session.commit()
            print("Курьер создан: courier/courier123")

        # Создаем базовые настройки сайта
        if not SiteSettings.query.first():
            settings = SiteSettings()
            db.session.add(settings)
            db.session.commit()
            print("Базовые настройки созданы")

        # Создаем базовые категории если их нет
        if Category.query.count() == 0:
            categories = [
                Category(name='Розы', slug='roses', description='Красивые розы разных сортов', sort_order=1),
                Category(name='Тюльпаны', slug='tulips', description='Свежие тюльпаны', sort_order=2),
                Category(name='Орхидеи', slug='orchids', description='Экзотические орхидеи', sort_order=3),
                Category(name='Букеты', slug='bouquets', description='Готовые букеты', sort_order=4),
                Category(name='Горшечные растения', slug='potted', description='Растения в горшках', sort_order=5)
            ]
            for category in categories:
                db.session.add(category)
            db.session.commit()
            print("Базовые категории созданы")

        # Добавляем тестовые товары если их нет
        if Product.query.count() == 0:
            roses_cat = Category.query.filter_by(slug='roses').first()
            tulips_cat = Category.query.filter_by(slug='tulips').first()
            orchids_cat = Category.query.filter_by(slug='orchids').first()
            
            sample_products = [
                Product(name='Красные розы', description='Букет из 25 красных роз', price=50, stock=20, category='roses', category_id=roses_cat.id if roses_cat else None, image_url='https://images.unsplash.com/photo-1518895949257-7621c3c786d7?w=400', is_visible=True, is_featured=True),
                Product(name='Белые лилии', description='Элегантный букет белых лилий', price=35, stock=15, category='roses', category_id=roses_cat.id if roses_cat else None, image_url='https://images.unsplash.com/photo-1490750967868-88aa4486c946?w=400', is_visible=True, is_featured=True),
                Product(name='Тюльпаны микс', description='Яркий букет разноцветных тюльпанов', price=30, stock=30, category='tulips', category_id=tulips_cat.id if tulips_cat else None, image_url='https://images.unsplash.com/photo-1520763185298-1b434c919102?w=400', is_visible=True),
                Product(name='Пионы', description='Нежные розовые пионы', price=60, stock=10, category='roses', category_id=roses_cat.id if roses_cat else None, image_url='https://images.unsplash.com/photo-1588017341958-ce36aa0fb6d3?w=400', is_visible=True, is_featured=True),
                Product(name='Орхидеи', description='Экзотические орхидеи', price=90, stock=8, category='orchids', category_id=orchids_cat.id if orchids_cat else None, image_url='https://images.unsplash.com/photo-1557804506-669a67965ba0?w=400', is_visible=True),
                Product(name='Хризантемы', description='Осенние хризантемы', price=25, stock=25, category='roses', category_id=roses_cat.id if roses_cat else None, image_url='https://images.unsplash.com/photo-1544735716-392fe2489ffa?w=400', is_visible=True)
            ]
            for product in sample_products:
                db.session.add(product)
            db.session.commit()
            print("Добавлены тестовые товары")
            
        except Exception as e:
            print(f"Database initialization error: {e}")
            # For PostgreSQL, we might need to handle specific connection issues
            if "does not exist" in str(e):
                print("Database connection issue. Please check your Supabase credentials.")
            
    app.run(host='0.0.0.0', port=5000, debug=True)