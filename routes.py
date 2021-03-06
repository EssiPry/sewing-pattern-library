from functools import wraps
from app import app
from flask import render_template, request, redirect, url_for, session
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
    patterns_total = sewingpatterns.count_patterns("", "", "%", "")
    companies_total = sewingpatterns.count_companies()
    reviews_total = reviews.count_reviews()
    reviewers_total = reviews.count_reviewers()
    top_three_reviewed = reviews.top_three_reviewed()
    return render_template(
        "index.html", patterns=patterns_total, companies=companies_total, reviews=reviews_total,
        reviewers=reviewers_total, top_three=top_three_reviewed)

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if users.login(username, password):
            return redirect("/")
        return render_template("login.html", error_message="Incorrect username or password. Please try again.")
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
        if len(username) < 3 or len(username) > 20:
            return render_template("register.html", error_message="Your username needs to be between 3-20 characters.")
        password = request.form["password"]
        if len(password) < 3 or len(password) > 20:
            return render_template("register.html", error_message="Your password needs to be between 3-20 characters.")
        password_confirmation = request.form["password_confirmation"]
        if password != password_confirmation:
            return render_template("register.html", error_message="Please make sure your passwords match")
        if users.register(username, password):
            return redirect("/login")
        return render_template(
            "register.html", error_message="The username is already in use. Please choose a different username.")
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
        garment_id = request.form["garment"]
        results = sewingpatterns.get_patterns(pattern_name, company, fabric, garment_id)
        total = sewingpatterns.count_patterns(pattern_name, company, fabric, garment_id)
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
                user_id = users.get_user_id()
                my_patterns.add_to_my_patterns(user_id, pattern_id)
                return render_template(
                    "add_pattern.html", error_message="Pattern "
                    + pattern_name.capitalize() +
                    " added to the library & your patterns.", garments=garments)
            return render_template(
                "add_pattern.html", error_message="The pattern " + pattern_name.capitalize() +
                " is already in the database. Please use a unique name or code", garments=garments)
        return render_template(
            "add_pattern.html",
            error_message="Please fill in all fields and select at least one garment type.",
            garments=garments)
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
            return render_template(
                "pattern.html", pattern_id=pattern_id, pattern_name=sewing_pattern.name,
                company=sewing_pattern.company, fabric=sewing_pattern.fabric, garments=garments,
                reviews=pattern_reviews, in_my_patterns=in_my_patterns,
                error_message="Please don't leave a blank review.")
        if reviews.add_review(user_id, pattern_id, review):
            pattern_reviews = reviews.get_reviews(pattern_id)
            return render_template(
                "pattern.html", pattern_id=pattern_id, pattern_name=sewing_pattern.name,
                company=sewing_pattern.company, fabric=sewing_pattern.fabric, garments=garments,
                reviews=pattern_reviews, in_my_patterns=in_my_patterns)
        return render_template("error.html", message="Something went wrong, please try again")
    return render_template(
        "pattern.html", pattern_id=pattern_id, pattern_name=sewing_pattern.name,
        company=sewing_pattern.company, fabric=sewing_pattern.fabric, garments=garments,
        reviews=pattern_reviews, in_my_patterns=in_my_patterns)

@app.route("/my_patternlibrary")
@login_required
def my_patternlibrary():
    user_id = users.get_user_id()
    my_sewingpatterns = my_patterns.get_my_patterns(user_id)
    total = my_patterns.count_my_patterns(user_id)
    return render_template("my_patternlibrary.html", my_patterns=my_sewingpatterns, total=total)

@app.route("/add_to_my_patterns", methods=["POST"])
def add_to_my_patterns():
    users.check_csrf(request.form["csrf_token"])
    pattern_id = request.form["pattern_id"]
    user_id = users.get_user_id()
    if my_patterns.add_to_my_patterns(user_id, pattern_id):
        return redirect("/my_patternlibrary")
    return render_template("error.html", message="Something went wrong, please try again")

@app.route("/delete_from_my_patterns", methods=["POST"])
def delete_from_my_patterns():
    users.check_csrf(request.form["csrf_token"])
    pattern_id = request.form["pattern_id"]
    user_id = users.get_user_id()
    if my_patterns.delete_from_my_patterns(user_id, pattern_id):
        return redirect("/")
    return render_template("error.html", message="Something went wrong, please try again")

@app.route("/delete_review", methods=["POST"])
def delete_review():
    users.check_csrf(request.form["csrf_token"])
    review_id = request.form["review_id"]
    reviews.delete_review(review_id)
    return redirect(request.referrer)

@app.route("/edit_review", methods=["POST"])
@login_required
def edit_review():
    users.check_csrf(request.form["csrf_token"])
    review_id = request.form["review_id"]
    pattern_id = request.form["pattern_id"]
    review = reviews.get_review_text(review_id)
    return render_template("edit_review.html", review_id=review_id, review=review, pattern_id=pattern_id)

@app.route("/update_review", methods=["POST"])
def update_review():
    users.check_csrf(request.form["csrf_token"])
    review_id = request.form["review_id"]
    review = request.form["review"]
    if not review:
        return render_template(
            "edit_review.html", review_id=review_id, review=review,
            error_message="Please don't leave a blank review")
    reviews.update_review(review_id, review)
    pattern_id = request.form["pattern_id"]
    return redirect(url_for('pattern_page', pattern_id=pattern_id))
