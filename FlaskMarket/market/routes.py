from flask import render_template, redirect, url_for, flash
from market import app, db
from market.models import Item, User
from market.forms import RegisterForm, LoginForm

@app.route("/") #decorator
@app.route("/home")
def home_page():
    return render_template("home.html")


@app.route("/about/<username>")
def about_page(username):
    return f"<h1>This is the about page of {username}</h1>"

@app.route("/market")
def market_page():
    item = Item.query.all()
    return render_template("market.html", items=item)


@app.route("/login")
def login():
    return render_template("login.html")
    
@app.route("/lagout")
def logout():
    return render_template("lagout.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    
    if form.validate_on_submit():
        user_to_create = User(username=form.username.data,
                                email_address=form.email_address.data,
                                password_hash=form.password1.data)
        db.session.add(user_to_create)
        db.session.commit()
        return redirect(url_for("market_page"))
    
    if form.errors != {}: # If there are no errors from the validations
        for err_msg in form.errors.values():
            flash(f"There was an error with creating a user: {err_msg}")
            
    return render_template("register.html", form=form)