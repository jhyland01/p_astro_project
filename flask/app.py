from flask import *
from P_astro_project import select_hyperposterior
import pandas as pd
import json
import plotly
import plotly.express as px
import plotly.graph_objects as go
import subprocess

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/run")
def search():
    data = request.args # gather form input data
    keyword = data["Nhyp"] # select from the id
    value = int(keyword) # convert to int
    PP_params = select_hyperposterior.select_hyper(value) # use the form input value as input to function
    df = pd.DataFrame(PP_params) # create df from function
    table = go.Figure(data=[go.Table(header=dict(values=list(df.columns),
                                        fill_color='paleturquoise',
                                        align='left'),
                                        cells=dict(values=df.transpose().values.tolist(),
                                        fill_color='lavender',
                                        align='left'))])
    table.update_layout(height=350)
    tableJSON = json.dumps(table, cls=plotly.utils.PlotlyJSONEncoder)
    #PP_params_html = pd.DataFrame.to_html(df, classes="table") # convert to html

    # run the gibbs sampling
    subprocess.run(["../P_astro_project/run_analysis.sh", keyword], shell=True, capture_output=True)
    samples = pd.read_csv('../outputs/params_for_SNR.csv')
    fig = px.scatter_matrix(samples, dimensions=['mass_1', 'mass_ratio']) # create a figure
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder) # json the figure

    return render_template("results.html", hyp=value, table=tableJSON, graphJSON=graphJSON) # include all in render

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
