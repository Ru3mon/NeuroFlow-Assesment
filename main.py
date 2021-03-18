from flask import Flask, url_for, redirect, render_template, request, session, g
from flask_restful import Api, Resource 
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
api = Api(app)


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///moodModel.db'
db = SQLAlchemy(app)

class moodModel(db.Model):
    id = db.Column("id", db.Integer, primary_key= True)
    user = db.Column(db.String, nullable = False)
    mood = db.Column(db.String, nullable = False)
    
def __init__(self, id, user,mood, time):
    self.id = id
    self.user = user
    self.mood = mood
    
    

@app.route("/")
def home():
    return  "<h1>Welcome to the mood rating Journal</h1>"    


@app.route("/login/", methods = ["POST", "GET"])
def login():
        if request.method == "POST":
            session.pop("user", None)
            session['user'] = request.form["usr"]
            return redirect(url_for("mood"))
        return render_template("login.html")

@app.route("/mood", methods = ["POST", "GET"])
def mood():
    if "user" in session:
        return render_template("mood.html")
    else:
        return redirect(url_for("login"))
        
        

@app.route("/journal/", methods = ["POST", "GET"])
def journal():
    if request.method == "POST":    
        old_ratings = ""
        foundUser = moodModel.query.filter_by(user = session["user"]).first()
        tday = date.today()
        if foundUser:
            old_ratings = foundUser.mood
            session["mRating"] = request.form["md"]
            foundUser.mood = session["mRating"] + " |" + f" {old_ratings}"
            db.session.commit()
            return f"{foundUser.user}, You entered {foundUser.mood} into your mood journal {tday.day - tday.day}"
        else:
            session["mRating"] = request.form["md"]
            nRating = session["mRating"]
            mRating = moodModel(user = session["user"], mood = nRating)
            db.session.add(mRating)
            db.session.commit()
            return f"{mRating.user}, You entered {mRating.mood} into your mood journal {tday.day - tday.day}"
    return render_template("mood.html")

@app.route("/logout")
def logout():
    session.pop("user", None)
    session.pop("mRating", None)
    return redirect(url_for("login"))
    

if __name__ == "__main__":
    app.secret_key = 'neuroFlow'
    db.create_all()
    app.run(debug=True)