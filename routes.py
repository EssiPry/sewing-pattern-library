from app import app
from flask import render_template, request, redirect
import users
import sewingpatterns
import reviews
import my_patterns

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if users.login(username, password):
            return redirect("/")
        return render_template("error.html", message="Please check your username and password")
    return render_template("login.html")

@app.route("/logout")
def logout():
    users.logout()
    return redirect("/")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password1 = request.form["password1"]
        password_conf = request.form["password_conf"]
        if password1 != password_conf:
            return render_template("error.html",
            message="Please make sure your passwords match")
        if users.register(username, password1):
            return redirect("/")
        return render_template("error.html", message="The username is already taken. Please choose a different name")
    return render_template("register.html")

@app.route("/search", methods=["GET", "POST"])
def search():
    garments = sewingpatterns.get_garment_types()
    if request.method == "POST":
        pattern_name = request.form["pattern_name"].lower()
        company = request.form["company"].lower()
        fabric = request.form["fabric"]
        garments = request.form.getlist("garment")
        if pattern_name == "":
            pattern_name = "%"
        if company == "":
            company = "%"
        results = sewingpatterns.get_patterns(pattern_name, company, fabric)
        total = sewingpatterns.count_patterns(pattern_name, company, fabric)
        return render_template("result.html", total=total, results=results)
    return render_template("search.html", garments=garments)

@app.route("/add_pattern", methods=["GET", "POST"])
def add_pattern():
    garments = sewingpatterns.get_garment_types()
    if request.method == "POST":
        pattern_name = request.form["pattern_name"].lower()
        company = request.form["company"].lower()
        fabric = request.form["fabric"]
        garment_ids = request.form.getlist("garment")
        if pattern_name and company:
            if sewingpatterns.add_pattern_to_db(pattern_name, company, fabric):
                pattern_id = sewingpatterns.get_pattern_id(pattern_name)
                for garment_id in garment_ids:
                    sewingpatterns.add_garment_type_to_pattern(pattern_id, garment_id)
                return render_template("add_pattern.html", message="Pattern " + pattern_name + " added to the library.", garments=garments)
            return render_template("add_pattern.html", message="Please check that the pattern "+ pattern_name.capitalize() +" is not already in the database.", garments=garments)
        return render_template("add_pattern.html", message="Please fill in all fields!", garments=garments)
    return render_template("add_pattern.html", garments=garments)

@app.route("/pattern/<pattern_name>", methods=["GET", "POST"])
def pattern_page(pattern_name):
    pattern_name = pattern_name.lower()
    sewing_pattern = sewingpatterns.get_pattern_by_name(pattern_name)
    garments = sewingpatterns.get_garments(pattern_name)
    pattern_reviews = reviews.get_reviews(pattern_name)
    if request.method == "POST":
        user_id = users.get_user_id()
        pattern_id = sewingpatterns.get_pattern_id(pattern_name)
        review = request.form["review"]
        if reviews.add_review(user_id, pattern_id, review):
            pattern_reviews = reviews.get_reviews(pattern_name)
            return render_template("pattern.html", pattern_name=sewing_pattern.name, company=sewing_pattern.company, fabric=sewing_pattern.fabric, garments=garments, reviews=pattern_reviews)
        return render_template("error.html", message="Something went wrong, please try again")
    return render_template("pattern.html", pattern_name=sewing_pattern.name, company=sewing_pattern.company, fabric=sewing_pattern.fabric, garments=garments, reviews=pattern_reviews)

@app.route("/add_to_my_patterns", methods=["POST"])
def add_to_my_patterns():
    pattern_name=request.form["pattern_name"]
    pattern_id = sewingpatterns.get_pattern_id(pattern_name)
    user_id = users.get_user_id()
    my_patterns.add_to_my_patterns(user_id, pattern_id)
    return redirect("/")

@app.route("/delete_from_my_patterns", methods=["POST"])
def add_to_my_patterns():
    pattern_name=request.form["pattern_name"]
    pattern_id = sewingpatterns.get_pattern_id(pattern_name)
    user_id = users.get_user_id()
    my_patterns.add_to_my_patterns(user_id, pattern_id)
    return redirect("/")
