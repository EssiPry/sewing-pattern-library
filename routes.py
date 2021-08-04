from app import app
from flask import render_template, request, redirect
import users, sewingpatterns

@app.route("/")
def index(): 
    return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET": 
        return render_template("login.html")

    if request.method == "POST": 
        username = request.form["username"]
        password = request.form["password"]
        
        if users.login(username, password): 
            return redirect("/")
        else: 
            return render_template("error.html", message="Please check your username and password")
        
@app.route("/register", methods=["GET", "POST"])
def register(): 
    if request.method == "GET": 
        return render_template("register.html")
    if request.method == "POST": 
        username = request.form["username"]
        password1 = request.form["password1"]
        password_conf = request.form["password_conf"]
        if password1 != password_conf: 
            return render_template("error.html", message="Please make sure your passwords match")
        if users.register(username, password1):
            return redirect("/")
        else: 
            return render_template("error.html", message="The username is already taken. Please choose a different name")

@app.route("/logout")
def logout():
    users.logout()
    return redirect ("/")