from flask import render_template, request, redirect
from forms import ProductForm, CreateUserForm, CommentForm
from table import Users, Products, Comments, db, app
from flask_login import login_required, logout_user, LoginManager, login_user
from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy import create_engine, Table, MetaData, select, exc, desc

login_manager = LoginManager()
login_manager.init_app(app)
main_filter = False


@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(user_id)


# СПИСОК ТОВАРОВ

@app.route('/', methods=['GET', 'POST'])
def home():
    global main_filter

    def check_admin():
        try:
            if admin == True:
                admin_confider = True

                return admin_confider
            else:
                admin_confider = False

                return admin_confider
        except NameError:
            admin_confider = None

            return admin_confider

    global admin_confider
    admin_confider = check_admin()


    if request.method == "POST":
        select = request.form.get('comp_select')
        if select == "to-high":
            products = Products.query.order_by(Products.price).all()

        if select == "to-low":
            products = Products.query.order_by(desc(Products.price)).all()

    else:
        products = Products.query.order_by(Products.id).all()
    return render_template("home.html", products=products, admin_confider=admin_confider, main_filter=main_filter)


# СОЗДАНИЕ ТОВАРА (АДМИН)

@app.route('/add', methods=['GET', 'POST'])
def add():
    global admin_confider
    if request.method == 'POST':
        type = request.form['type']
        name = request.form['name']
        description = request.form['description']
        manufacturer = request.form['manufacturer']
        price = request.form['price']
        photo = request.files['photo']

        price = int(price)

        products = Products(type=type, name=name, description=description, manufacturer=manufacturer, price=price,
                            photo=photo.filename)
        db.session.add(products)
        db.session.commit()
        return redirect('/')
    else:
        return render_template('add.html', form=ProductForm(),admin_confider=admin_confider)


# АВТОРИЗАЦИЯ

@app.route('/login', methods=['GET', 'POST'])
def login():
    global admin

    login = request.form.get("login")
    password = request.form.get("password")

    if login:
        if password:
            user = Users.query.filter_by(login=login).first()

            if user:
                if check_password_hash(user.password, password):
                    login_user(user)
                    user = Users.query.filter_by(login=login).first()
                    admin = user.admin
                    return redirect('/')
    return render_template('login.html')


# РЕГИСТРАЦИЯ

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = CreateUserForm()
    login_error = False

    if form.validate_on_submit():

        username = form.username.data
        password = form.password.data
        email = form.email.data

        try:
            hash_password = generate_password_hash(password)
            new_user = Users(email=email,login=username,password=hash_password)
            db.session.add(new_user)
            db.session.commit()
            email_error=False
            return redirect('/login')
        except exc.IntegrityError:

            email_error = True
            return render_template('register.html', form=form, login_error=login_error)
    else:
        return render_template('register.html', form=form, login_error=login_error)


# ФУНКЦИЯ ВЫХОДА

@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    global admin
    del (admin)
    logout_user()
    return redirect('/')


# СТРАНИЦА ПРОДУКТА

@app.route('/<int:id>', methods=['GET', 'POST'])
def product_page(id):
    global admin
    product = Products.query.get(id)
    comments = Comments.query.filter_by(prod_id=id).all()
    form = CommentForm()

    if form.validate_on_submit():
        like = form.like.data
        comment = form.comment.data


        new_comment = Comments(prod_id=id, like=like, comment=comment)
        db.session.add(new_comment)
        db.session.commit()

    def check_admin():
        try:
            if admin == True:
                admin_confider = True
                return admin_confider
            else:
                admin_confider = False
                return admin_confider
        except NameError:
            admin_confider = None
            return admin_confider

    admin_confider = check_admin()

    return render_template("product.html", admin_confider=admin_confider, product=product, form=form,
                           comments=comments,id=id)


# УДАЛЕНИЕ ТОВАРА (АДМИН)

@app.route('/delete/<int:id>/Hnecfji2ekdme4efjdk4;gJKJnfkdjne4rfkl;dfj;OIPE(o')
def delete(id):
    u = db.session.get(Products, id)
    db.session.delete(u)
    db.session.commit()
    return redirect('/')


# РЕДАКТИРОВАНИЕ ТОВАРА (АДМИН)

@app.route('/add/<int:id>/ed', methods=["GET", "POST"])
def edite(id):
    global admin_confider

    form = ProductForm()
    if request.method == "POST":

        type = request.form['type']
        name = request.form['name']
        description = request.form['description']
        manufacturer = request.form['manufacturer']
        price = request.form['price']
        photo = request.files['photo']

        engine = create_engine("sqlite:///instance/base.db", echo=True)
        meta = MetaData(engine)
        products = Table("Products", meta, autoload=True)
        conn = engine.connect()

        mass_db = []
        column = 0

        s = select(products).where(products.c.id == id)
        result = conn.execute(s)

        for raw in result:
            pass

        for i in (type, name, description, manufacturer, price, photo):
            column += 1
            if i:
                mass_db.append(i)
            else:
                mass_db.append(raw[column])

        try:
            mass_db[5] = (mass_db[5]).filename
        except AttributeError:
            pass

        s = products.update().where(products.c.id == id).values(type=mass_db[0], name=mass_db[1],
                                                                description=mass_db[2], manufacturer=mass_db[3],
                                                                price=mass_db[4], photo=mass_db[5])
        conn.execute(s)

        return redirect('/')

    return render_template('edit.html', form=form,admin_confider=admin_confider)


# Фильтр Для карточек
@app.route("/filter")
def filter():
    global main_filter
    if main_filter == True:
        main_filter = False
    else:
        main_filter = True
    return redirect("/")


if __name__ == '__main__':
    app.run(debug=True)
