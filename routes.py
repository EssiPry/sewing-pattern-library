from app import app
from flask import render_template, request, redirect, url_for
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
        
@app.route("/logout")
def logout():
    users.logout()
    return redirect ("/")

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

@app.route("/search", methods=["GET", "POST"])
def search(): 
    if "pattern_name" in request.args:
        pattern_name = request.args["pattern_name"].lower()
        results = sewingpatterns.get_pattern_by_name(pattern_name)
        total = sewingpatterns.count_by_name(pattern_name)
        return render_template("result.html", total = total, results = results)
    return render_template("search.html")


@app.route("/add_pattern", methods=["GET", "POST"])
def add_pattern(): 
    if request.method == "POST": 
        pattern_name = request.form["pattern_name"].lower()
        company = request.form["company"].lower()
        fabric = request.form["fabric"]
        if pattern_name and company:
            if sewingpatterns.add_pattern_to_db(pattern_name, company, fabric): 
                return render_template("add_pattern.html", message="Pattern " + pattern_name + " added to the library.")
            else: 
                return render_template("add_pattern.html", message="Please check that the pattern "+ pattern_name.capitalize() +" is not already in the database.")
        else: 
            return render_template("add_pattern.html", message="Please fill in all the fields!") 
    return render_template("add_pattern.html") 

@app.route("/pattern/<pattern_name>")
def pattern_page(pattern_name):
    # hae pattern-tiedot kannasta
    return render_template("pattern.html", pattern_name = pattern_name)
