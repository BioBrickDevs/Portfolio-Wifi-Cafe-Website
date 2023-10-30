from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap5
from wtforms import StringField, BooleanField, SubmitField
from flask_wtf import FlaskForm
from wtforms.validators import input_required, URL

app = Flask(__name__)
bootstrap = Bootstrap5(app)
app.config["SQLALCHEMY_DATABASE_URI"] = r"""sqlite:///C:\Users\blast\OneDrive\Desktop\Portfolio - 100 days of code\Portfolio - Wifi Cafe website\cafes.db"""
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['BOOTSTRAP_BOOTSWATCH_THEME'] = 'minty'
app.config['SECRET_KEY'] = '32X32X32lajfljfa;fj;'
db = SQLAlchemy(app)


class InputNewForm(FlaskForm):
    name = StringField("Cafe name", validators=[input_required()])
    map_url = StringField(
        "Cafe location on Google Maps (URL)", validators=[input_required(),
                                                          URL()])
    img_url = StringField("Cafe image (URL)", validators=[
                          input_required(), URL()])
    location = StringField("Cafe location", validators=[input_required()])
    seats = StringField("Number of seats", validators=[input_required()])
    has_toilet = BooleanField("Has toilet?", validators=[])
    has_wifi = BooleanField("Has wifi?", validators=[])
    has_sockets = BooleanField("Has sockets?", validators=[])
    can_take_calls = BooleanField("Can take calls?", validators=[])
    coffee_price = StringField(
        "Coffee price", validators=[input_required()])
    submit = SubmitField()


class Cafe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    map_url = db.Column(db.String(500), nullable=False)
    img_url = db.Column(db.String(500), nullable=False)
    location = db.Column(db.String(250), nullable=False)
    seats = db.Column(db.String(250), nullable=False)
    has_toilet = db.Column(db.Boolean, nullable=False)
    has_wifi = db.Column(db.Boolean, nullable=False)
    has_sockets = db.Column(db.Boolean, nullable=False)
    can_take_calls = db.Column(db.Boolean, nullable=False)
    coffee_price = db.Column(db.String(250), nullable=True)


with app.app_context():
    db.create_all()


@app.route("/")
def get_all_cafes():
    cafes = {"cafes": []}
    all_cafes = Cafe.query.all()
    for cafe in all_cafes:
        cafe = dict(cafe.__dict__)
        del cafe["_sa_instance_state"]
        cafes["cafes"].append(cafe)
    return render_template("index.html", cafes=cafes)


@app.route("/add", methods=["GET", "POST"])
def add_cafe():
    form = InputNewForm()
    if form.validate_on_submit():
        try:
            new_cafe = Cafe(
                name=request.form["name"],
                map_url=request.form["map_url"],
                img_url=request.form["img_url"],
                location=request.form["location"],
                seats=request.form["seats"],
                has_toilet=bool(form.has_toilet.data),
                has_wifi=bool(form.has_wifi.data),
                has_sockets=bool(form.has_sockets.data),
                can_take_calls=bool(form.can_take_calls.data),
                coffee_price=request.form["coffee_price"],
            )
            db.session.add(new_cafe)
            db.session.commit()
            return redirect(url_for("get_all_cafes"))

        except Exception as e:
            flash("""Error adding new cafe to database.
                Maybe the cafe already exists?""")
            return render_template("add.html", form=form, success=False)
    else:
        return render_template("add.html", form=form)


@app.route("/cafe/<int:id>")
def cafe_details(id):
    try:
        cafe = Cafe.query.get(id)
        cafe = dict(cafe.__dict__)
        del cafe["_sa_instance_state"]
        return render_template("cafe_details.html", cafe=cafe)
    except Exception as e:
        return redirect(url_for("get_all_cafes"))


app.run(debug=True)
