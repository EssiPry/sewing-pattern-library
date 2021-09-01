from app import app
from flask import render_template, request, redirect, session
from functools import wraps
import users
import sewingpatterns
import reviews
import my_patterns

def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if "logged_in" in session:
            return f(*args, **kwargs)
        else:
            return redirect("/login")
    return wrap

@app.route("/")
def index():
    patterns_total = sewingpatterns.count_patterns("", "", "%")
    companies_total = sewingpatterns.count_companies()
    reviews_total = reviews.count_reviews()
    reviewers_total = reviews.count_reviewers()
    return render_template("index.html", patterns=patterns_total, companies=companies_total, reviews=reviews_total, reviewers=reviewers_total)

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
@login_required
def logout():
    users.logout()
    return redirect("/")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        password_confirmation = request.form["password_confirmation"]
        if password != password_confirmation:
            return render_template("error.html", message="Please make sure your passwords match")
        if users.register(username, password):
            return redirect("/login")
        return render_template("error.html", message="The username is already in use.  Please choose a different name")
    return render_template("register.html")

@app.route("/search", methods=["GET", "POST"])
@login_required
def search():
    garments = sewingpatterns.get_garment_types()
    if request.method == "POST":
        users.check_csrf(request.form["csrf_token"])
        pattern_name = request.form["pattern_name"].lower()
        company = request.form["company"].lower()
        fabric = request.form["fabric"]
        garments = request.form.getlist("garment")
        results = sewingpatterns.get_patterns(pattern_name, company, fabric)
        total = sewingpatterns.count_patterns(pattern_name, company, fabric)
        return render_template("result.html", total=total, results=results)
    return render_template("search.html", garments=garments)

@app.route("/add_pattern", methods=["GET", "POST"])
@login_required
def add_pattern():
    garments = sewingpatterns.get_garment_types()
    if request.method == "POST":
        users.check_csrf(request.form["csrf_token"])
        pattern_name = request.form["pattern_name"].lower()
        company = request.form["company"].lower()
        fabric = request.form["fabric"]
        garment_ids = request.form.getlist("garment")
        if pattern_name and company and garment_ids:
            if sewingpatterns.add_pattern_to_db(pattern_name, company, fabric):
                pattern_id = sewingpatterns.get_pattern_id(pattern_name)
                for garment_id in garment_ids:
                    sewingpatterns.add_garment_type_to_pattern(pattern_id, garment_id)
                user_id=users.get_user_id()
                my_patterns.add_to_my_patterns(user_id, pattern_id)
                return render_template("add_pattern.html", message="Pattern " + pattern_name + " added to the library & your patterns.", garments=garments)
            return render_template("add_pattern.html", message="Please check that the pattern "+ pattern_name.capitalize() +" is not already in the database.", garments=garments)
        return render_template("add_pattern.html", message="Please fill in all fields and select at least one garment type", garments=garments)
    return render_template("add_pattern.html", garments=garments)

@app.route("/pattern/<pattern_id>", methods=["GET", "POST"])
@login_required
def pattern_page(pattern_id):
    sewing_pattern = sewingpatterns.get_pattern_by_id(pattern_id)
    garments = sewingpatterns.get_garments(pattern_id)
    pattern_reviews = reviews.get_reviews(pattern_id)
    user_id = users.get_user_id()
    in_my_patterns = my_patterns.in_db(user_id, pattern_id)
    if request.method == "POST":
        users.check_csrf(request.form["csrf_token"])
        review = request.form["review"].strip()
        if not review:
            return render_template("pattern.html", pattern_id=pattern_id, pattern_name=sewing_pattern.name, company=sewing_pattern.company, fabric=sewing_pattern.fabric, garments=garments, reviews=pattern_reviews, in_my_patterns=in_my_patterns,
            error_message="Please don't leave a blank review.")
        if reviews.add_review(user_id, pattern_id, review):
            pattern_reviews = reviews.get_reviews(pattern_id)
            return render_template("pattern.html", pattern_id=pattern_id, pattern_name=sewing_pattern.name, company=sewing_pattern.company, fabric=sewing_pattern.fabric, garments=garments, reviews=pattern_reviews, in_my_patterns=in_my_patterns)
        return render_template("error.html", message="Something went wrong, please try again")
    return render_template("pattern.html", pattern_id=pattern_id, pattern_name=sewing_pattern.name, company=sewing_pattern.company, fabric=sewing_pattern.fabric, garments=garments, reviews=pattern_reviews, in_my_patterns=in_my_patterns)

@app.route("/my_patternlibrary")
@login_required
def my_patternlibrary():
    user_id=users.get_user_id()
    my_sewingpatterns = my_patterns.get_my_patterns(user_id)
    total = my_patterns.count_my_patterns(user_id)
    return render_template("my_patternlibrary.html", my_patterns=my_sewingpatterns, total = total)

@app.route("/add_to_my_patterns", methods=["POST"])
def add_to_my_patterns():
    users.check_csrf(request.form["csrf_token"])
    pattern_id=request.form["pattern_id"]
    user_id = users.get_user_id()
    if my_patterns.add_to_my_patterns(user_id, pattern_id):
        return redirect("/my_patternlibrary")
    return render_template("error.html", message="Something went wrong, please try again")

@app.route("/delete_from_my_patterns", methods=["POST"])
def delete_from_my_patterns():
    users.check_csrf(request.form["csrf_token"])
    pattern_id=request.form["pattern_id"]
    user_id = users.get_user_id()
    if my_patterns.delete_from_my_patterns(user_id, pattern_id):
        return redirect("/")
    return render_template("error.html", message="Something went wrong, please try again")
