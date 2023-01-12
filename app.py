from flask import Flask, session, request, make_response, render_template
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired
from wtforms import SubmitField
from wtforms.validators import InputRequired, DataRequired, Length, Email
from wtforms.fields import StringField, TextAreaField

from flask_bootstrap import Bootstrap

app = Flask(__name__)
app.config['SECRET_KEY'] = 'kjhfdkjhgjkdfhgkjdfhg'
bootstrap = Bootstrap(app)


# app.config['BOOTSTRAP_SERVE_LOCAL'] = True


# ************************* INTRODUCTION *************************
@app.route('/hello_world')
def index():
    return 'Hello world'


@app.route('/hello_Benjamin_static')
def index_popol():
    return 'Hello Benjamin'


@app.route('/user/<name>')
def hello_user(name):
    if len(name) > 10:
        return "Le nom est beaucoup beaucoup trop long", 404
    return f'Hello {name}'


@app.route('/whoareyou')
def who_are_you():
    return render_template('test_user.html')


# ************************* ROUTE DYNAMIQUE *************************
@app.route('/user_limit/<name>')
def hello_user(name):
    if len(name) > 10:
        return "Le nom est beaucoup beaucoup trop long", 404
    return f'Hello {name}'


# ************************* TEMPLATE JINJA2 *************************
@app.route('/welcome_answer')
def welcome_answer():
    namedfsdf = request.args['name']
    email = request.args['email']
    return render_template("welcome_answer.html", name=namedfsdf, email=email)


# ************************* FORMULAIRE AVEC WTF *************************
class NLPForm(FlaskForm):
    text = TextAreaField("Saisir le text: ", validators=[Length(min=10)])
    submit = SubmitField("Submit")


@app.route('/nlp', methods=['GET', 'POST'])
def nlp():
    text = None
    paris_count = None
    form = NLPForm()
    if form.validate_on_submit():
        text = form.text.data
        text_to_analyze = text.lower()
        paris_count = text_to_analyze.count("paris")
        paris_count = paris_count + text_to_analyze.count("ville de lumiere")
    return render_template("npl.html", form=form, text=text, paris_count=paris_count)


# ************************ FORM ET BOOTSTRAP ***************************
class NameForm(FlaskForm):
    name = StringField('Quel est votre nom ?', validators=[DataRequired(), Length(20)])
    email = StringField('Quel est votre email ?', validators=[DataRequired(), Email("Email invalid")])
    text = TextAreaField('Quel est votre text ?', validators=[])
    submit = SubmitField('Submit')


@app.route('/welcome_request', methods=['GET', 'POST'])
def welcome_request():
    name = None
    email = None
    form = NameForm()
    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        ## stocker en db
        # form.name.data = ''
        # form.email.data = ''
    return render_template("welcome.html", form=form, name=name, email=email)


# ************************ FORM ET BOOTSTRAP AVEC LE TEMPLATE ***************************
@app.route('/bootstrap', methods=['GET', 'POST'])
def bootstrap():
    name = None
    email = None
    form = NameForm()
    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        ## stocker en db
        # form.name.data = ''
        # form.email.data = ''
    return render_template("bootstrap.html", form=form, name=name, email=email)


# ************************ FORM AVEC UPLOAD ET BOOTSTRAP ***********************
class FileForm2(FlaskForm):
    file = FileField('File')
    submit = SubmitField("Submit")


@app.route('/file', methods=['GET', 'POST'])
def file_uploader():
    form = FileForm2()
    if form.validate_on_submit():
        uploaded_file = form.file.data
        if uploaded_file.filename != '':
            uploaded_file.save(uploaded_file.filename)
        # Faire le traitement sur le fichier
    return render_template("file.html", form=form)


# ************************ 2 FORMS DANS LA MEME PAGE ***********************
class FileForm(FlaskForm):
    file = FileField("Fichier à traiter", validators=[FileRequired()])
    submit = SubmitField("Traiter")


class TextForm(FlaskForm):
    text = StringField("Texte à traiter", validators=[InputRequired()])
    submit = SubmitField("Traiter")


class WelcomeForm(FlaskForm):
    name = StringField("Quel est votre nom ?", validators=[])
    submit = SubmitField("Submit")


@app.route("/test_bootstrap", methods=['GET', 'POST'])
def test_bootstrap():
    name = None
    form = WelcomeForm()
    if form.validate_on_submit():
        name = form.name.data
    return render_template("test_bootstrap.html", title="Bienvenu", form=form, name=name)


# ************************** SITE INTERNET AVEC NAVIGATION BOOTSTRAP ********************
@app.route("/test_paris", methods=['GET', 'POST'])
def test_paris():
    occurrence_text = None
    occurrence_file = None
    file_form = FileForm()
    text_form = TextForm()

    if file_form.file.data is not None and file_form.validate_on_submit():
        uploaded_file = file_form.file.data
        if uploaded_file and uploaded_file.filename != '':
            occurrence_file = 0
            uploaded_file.save(uploaded_file.filename)
            with open(uploaded_file.filename) as f:
                for line in f.readlines():
                    occurrence_file += paris_detector(line)
    elif text_form.text.data is not None and text_form.validate_on_submit():
        text = text_form.text.data
        occurrence_text = paris_detector(text)

    return render_template("test_paris.html",
                           title="Détection de Paris",
                           file_form=file_form,
                           text_form=text_form,
                           occurrence_text=occurrence_text,
                           occurrence_file=occurrence_file
                           )


def paris_detector(text):
    text_to_analyze = text.lower()
    occurrence = text_to_analyze.lower().count("paris")
    occurrence += text_to_analyze.lower().count("ville de lumiere")
    return occurrence


@app.route("/test_apropos")
def test_apropos():
    return render_template("test_apropos.html", title="A propos de moi")


# ************************* GESTION DES COOKIE (Stockage Mémoire Client) *************************
@app.route('/register_cookie', methods=['GET', 'POST'])
def set_cookie():
    response = make_response("cookie set")
    response.set_cookie("clef", "valeur")
    return response


@app.route('/test_cookie', methods=['GET', 'POST'])
def get_cookie():
    return f'Le cookie clef vaut {request.cookies["clef"]}'


# ************************* GESTION DE LA SESSION (Stockage Mémoire Serveur) *************************
@app.route('/save_in_session', methods=['GET', 'POST'])
def set_session():
    session["data"] = "value session"
    return "Data save in session"


@app.route('/test_session', methods=['GET', 'POST'])
def get_session():
    return f'La session contient la clé data et vaut {session["data"]}'
