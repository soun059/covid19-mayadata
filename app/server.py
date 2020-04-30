import os
from flask import Flask, request, jsonify, Response,render_template 
import pandas as pd
import chart_studio.plotly as py 
import plotly.graph_objs as go
from plotly.offline import download_plotlyjs, init_notebook_mode, iplot, plot ,plot_mpl
import json
import os
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
import io
import plotly
from flask import Markup


def get_fig(region):
    dataset_forecast = pd.read_csv('datasets\\covid19-global-forecasting-week-1\\train.csv')
    data_china = dataset_forecast[dataset_forecast['Date'] == max(dataset_forecast['Date'])][dataset_forecast['Country/Region'] == 'China']
    data_china_to_plot = data_china[['Province/State','ConfirmedCases','Fatalities']]
    data_china_to_plot['Active'] = data_china_to_plot['ConfirmedCases'] - data_china_to_plot['Fatalities']
    with open(os.getcwd()+'\\extras\\china\\geojson_china.json') as f:
        map_china = json.load(f)
    fig = go.Figure(go.Choroplethmapbox(geojson=map_china,locations=data_china_to_plot['Province/State'],z=data_china_to_plot['Active'],
                                    colorscale='sunsetdark',
                                    marker_opacity=0.5, marker_line_width=0,colorbar={'title':"No. of Active Cases"}))
    fig = fig.update_layout(mapbox_style="carto-positron",
                  mapbox_zoom=3, mapbox_center = {"lat": 35.8617, "lon": 104.1954})
    fig = fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    return fig




# init app
app = Flask(__name__,template_folder='templates')
basedir = os.path.abspath(os.path.dirname(__file__))


# india caller
@app.route('/india', methods=['GET'])
def get_india():
    #fig = get_fig('india')
    #fig.savefig('images/china.png')
    return render_template('india.html')

# world caller
@app.route('/world',methods=['GET'])
def get_world():
    #fig = get_fig('world')
    #fig.savefig('images/china.png')
    return render_template('world.html')

@app.route('/',methods=['GET'])
def get_all():
    #fig = get_fig('wor')
    #fig.savefig('images/china.png')
    return render_template('index.html')
    

   
@app.route('/debug',methods=['GET'])
def get_debug():
    return Response('hello')

    
# china caller
@app.route('/china',methods=['GET'])
def get_china():
    #fig = get_fig('china')
    #fig.savefig('images/china.png') 
    return render_template('china.html')




# Run Server
if __name__ == "__main__":
    app.run(debug=True)
