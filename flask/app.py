from flask import *
from P_astro_project import select_hyperposterior
import pandas as pd

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/run")
def search():
    data = request.args
    keyword = data["Nhyp"]
    value = int(keyword) # output here is the string "you input:"
    PP_params = select_hyperposterior.select_hyper(value)
    df = pd.DataFrame([PP_params[0]])
    PP_params_html = pd.DataFrame.to_html(df, classes="table")
    return render_template("results.html", hyp=value, table=PP_params_html)

# New functions
@app.route("/about/")
def about():
    return render_template("about.html")

@app.route("/contact/")
def contact():
    return render_template("contact.html")

@app.route("/api/data")
def get_data():
    return app.send_static_file("data.json")
