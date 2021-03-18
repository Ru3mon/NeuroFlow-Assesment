from flask import Flask, url_for, redirect, render_template, request, session, g
from flask_restful import Api, Resource 
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
api = Api(app)


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///moodModel.db'
db = SQLAlchemy(app)

#Creates the database 

class moodModel(db.Model):
    id = db.Column("id", db.Integer, primary_key= True)
    user = db.Column(db.String, nullable = False)
    mood = db.Column(db.String, nullable = False)

#Constructor for database    
def __init__(self, id, user,mood, time):
    self.id = id
    self.user = user
    self.mood = mood
    
    
#Homepage
@app.route("/")
def home():
    return  "<h1>Welcome to the Mood Rating Journal</h1>"    

#Login method
@app.route("/login/", methods = ["POST", "GET"])
def login():
        if request.method == "POST":
            session.pop("user", None)
            session['user'] = request.form["usr"]
            return redirect(url_for("mood"))
        return render_template("login.html")

#Connector to the journal template
@app.route("/mood", methods = ["POST", "GET"])
def mood():
    if "user" in session:
        return render_template("mood.html") #Submitting the form on mood.html redirect you to journal 
    else:
        return redirect(url_for("login"))
        
        
#Displays the users Mood Ratings
@app.route("/journal/", methods = ["POST", "GET"])
def journal():
    if request.method == "POST":    
        old_ratings = ""
        foundUser = moodModel.query.filter_by(user = session["user"]).first() #Searchs the database for a user
        if foundUser:
            old_ratings = foundUser.mood
            session["mRating"] = request.form["md"]
            foundUser.mood = session["mRating"] + " |" + f" {old_ratings}" #String concatenation to add the old user rating to the new rating separted by a |
            db.session.commit()
            return f"{foundUser.user}, You entered {foundUser.mood} into your mood journal "
        else:
            session["mRating"] = request.form["md"]
            nRating = session["mRating"]
            mRating = moodModel(user = session["user"], mood = nRating)
            db.session.add(mRating)
            db.session.commit()
            return f"{mRating.user}, You entered {mRating.mood} into your mood journal"
    return render_template("mood.html")

#logs the user out
@app.route("/logout")
def logout():
    session.pop("user", None)
    session.pop("mRating", None)
    return redirect(url_for("login"))
    

if __name__ == "__main__":
    app.secret_key = 'neuroFlow'
    db.create_all()
    app.run(debug=True)