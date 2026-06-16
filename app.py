from flask import Flask, render_template
import pandas as pd

app = Flask(__name__)


@app.route("/")
def home():

    return render_template("index.html")


@app.route("/teams")
def teams():

    teams = pd.read_csv("data/teams.csv")

    teams = teams.to_dict(orient="records")

    return render_template(
        "teams.html",
        teams=teams
    )


app.run(debug=True)