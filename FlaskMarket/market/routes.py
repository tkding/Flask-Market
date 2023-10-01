from flask import render_template, redirect, url_for, flash, request
from market import app, db
from market.models import Item, User
from market.forms import RegisterForm, LoginForm, PurchaseItemForm, SellItemForm
from flask_login import login_user, logout_user, login_required, current_user

@app.route("/") #decorator
@app.route("/home")
def home_page():
    return render_template("home.html")


@app.route("/about/<username>")
def about_page(username):
    return f"<h1>This is the about page of {username}</h1>"

@app.route("/market", methods=["GET", "POST"])
@login_required
def market_page():
    purchase_form = PurchaseItemForm()
    sell_form = SellItemForm()
    
    if request.method == "POST":
        # purchase item logic
        purchased_item_id = request.form.get("purchased_item")
        p_item_object = Item.query.filter_by(id=purchased_item_id).first()
        
        if p_item_object:
            if current_user.can_purchase(p_item_object):
                current_user.purchase(p_item_object)
                flash(f"Congratulations! You purchased {p_item_object.name} for {p_item_object.price}$", category="success")
            else:
                flash(f"Unfortunately, you don't have enough money to purchase {p_item_object.name}!", category="danger")

        #sell item logic
        sold_item_id = request.form.get("sold_item")
        s_item_object = Item.query.filter_by(id=sold_item_id).first()
        
        if s_item_object:
            if current_user.can_sell(s_item_object):
                current_user.sell(s_item_object)
                flash(f"Congratulations! You sold {s_item_object.name} back to market!", category="success")
            else:
                flash(f"Something went wrong with selling {s_item_object.name}!", category="danger")
        
        return redirect(url_for("market_page"))

    
    if request.method == "GET":
        items = Item.query.filter_by(owner=None)
        owned_items = Item.query.filter_by(owner=current_user.id)
        return render_template("market.html", items=items, purchase_form=purchase_form, owned_items=owned_items, sell_form=sell_form)


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    
    if form.validate_on_submit():
        # does the user exist?
        attempted_user = User.query.filter_by(username=form.username.data).first()
        # does the password match?
        if attempted_user and attempted_user.check_password_correction(attempted_password=form.password.data):
            login_user(attempted_user)
            flash(f"Success! You are logged in as: {attempted_user.username}", category="success")
            return redirect(url_for("market_page"))
        else:
            flash("Username and password are not match! Please try again", category="danger")
    
    if form.errors != {}:
        for err_msg in form.errors.values():
            flash(f"There was an error with creating a user: {err_msg}", category="danger")
            
    return render_template("login.html", form=form)
    
@app.route("/lagout")
def logout():
    logout_user()   
    flash("You have been logged out!", category="info") 
    return redirect(url_for("home_page"))

@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    
    if form.validate_on_submit():
        user_to_create = User(username=form.username.data,
                                email_address=form.email_address.data,
                                password=form.password1.data)
        db.session.add(user_to_create)
        db.session.commit()
        
        # login user
        login_user(user_to_create)
        flash(f"Account created successfully! You are logged in as: {user_to_create.username}", category="success")
        
        return redirect(url_for("market_page"))
    
    if form.errors != {}: # If there are no errors from the validations
        for err_msg in form.errors.values():
            flash(f"There was an error with creating a user: {err_msg}", category="danger")
            
    return render_template("register.html", form=form)
