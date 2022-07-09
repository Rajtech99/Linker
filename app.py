# Import Statements
from flask import Flask, redirect, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy

# Initialization
app = Flask(__name__)

# All App Configuration
app.config['SECRET_KEY'] = '''You Secret Key'''
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///linker.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] =  False
db = SQLAlchemy(app)

# Create Database
class  Myapp(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(300), nullable=False)
    url = db.Column(db.String(300), nullable=False)
    msg = db.Column(db.String(600), nullable=False)
    def __repr__(self) -> str:
        return f"{self.name} -- {self.url} -- {self.msg}"

# Home Page Route
@app.route("/", methods=['GET', 'POST'])
@app.route("/home", methods=['GET', 'POST'])
def home():
    if request.method == "POST":
        if not request.form['name'] or not request.form['url'] or not request.form['msg']:
            return render_template('error.html')
        else:
            name = request.form['name']
            url = request.form['url']
            msg = request.form['msg']
            fav_app = Myapp(name=name.capitalize(), url=url, msg=msg.capitalize())
            db.session.add(fav_app)
            db.session.commit()
    allmsg = Myapp.query.all()
    return render_template("index.html", allmsg=allmsg)

# Error Page Route
@app.route('/errorpage')
def error():
    return render_template("error.html")

# About Page Route
@app.route('/about')
def about():
    return render_template("about.html")

# Contact Page Route
@app.route('/contact')
def contact():
    return render_template("contact.html")

# Error Handling
@app.errorhandler(404)
def page_not_found(e):
    return render_template('400.html'), 404

# App Run Code
if __name__ == '__main__':
    app.run(debug=True, port=9999)