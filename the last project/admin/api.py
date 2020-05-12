from flask import Blueprint, render_template, jsonify, request, redirect, url_for
from modeles.main import Users, db

api = Blueprint("api", __name__, static_folder="static", template_folder="templates_bp")


@api.route("/users/<username>", methods=["GET"])
def get_user(username):
    # return "<h1>hello</h1>"
    return jsonify(Users.query.filter_by(username=username).first().to_dict())


@api.route("/delete/<username>", methods=["GET"])
def delete(username):
    user = Users.query.filter_by(username=username).first()
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for("api.users"))


@api.route("/users", methods=["GET"])
def users():
    data = Users.query.all()
    return render_template("allUsers.html", data=data)


@api.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["nick"]
        password = request.form["password"]
        if username == "admin" and password == "123admin123":
            return redirect(url_for("api.users"))
        else:
            return render_template("login_bp.html")
    else:
        return render_template("login_bp.html")


@api.route("/search", methods=["GET", "POST"])
def search():
    if request.method == "GET":
        return render_template("search_bp.html")
    else:
        username = request.form["userName"]
        first_name = request.form["firstName"]
        last_name = request.form["lastName"]
        if first_name == last_name == "":
            column = "username"
            keyword = username
        elif username == last_name == "":
            column = "first_name"
            keyword = first_name
            # User = Users.query.filter(Users.first_name.like(f'%{first_name[1:]}%')).all()
        elif username == first_name == "":
            column = "last_name"
            keyword = last_name
            # User = Users.query.filter(Users.last_name.like(f'%{last_name[1:]}%')).all()
        else:
            return redirect(url_for("search"))
        return redirect(url_for("api.results", column=column, keyword=keyword))


@api.route("/search/result/<column>/<keyword>", methods=["POST", "GET"])
def results(column, keyword):
    if request.method == "GET":
        if column == "username":
            users = Users.query.filter_by(username=keyword).all()
        elif column == "first_name":
            users = Users.query.filter(Users.first_name.like(f'%{keyword[1:]}%')).all()
        else:
            users = Users.query.filter(Users.last_name.like(f'%{keyword[1:]}%')).all()
        return render_template("result_bp.html", users=users)
    else:
        username = request.form["userName"]
        first_name = request.form["firstName"]
        last_name = request.form["lastName"]
        if first_name == last_name == "":
            column = "username"
            keyword = username
        elif username == last_name == "":
            column = "first_name"
            keyword = first_name
            # User = Users.query.filter(Users.first_name.like(f'%{first_name[1:]}%')).all()
        elif username == first_name == "":
            column = "last_name"
            keyword = last_name
            # User = Users.query.filter(Users.last_name.like(f'%{last_name[1:]}%')).all()
        else:
            return redirect(url_for("api.search"))
        return redirect(url_for("api.results", column=column, keyword=keyword))