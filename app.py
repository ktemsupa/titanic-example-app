######### Import your libraries #######
import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly as py
import plotly.graph_objs as go
from plotly.graph_objs import *

###### Define your variables #####
tabtitle = 'Titanic!'
color1='#3486eb'
color2='#eb347a'
sourceurl = 'https://www.kaggle.com/c/titanic'
githublink = 'https://github.com/ktemsupa/titanic-example-app'


###### Import a dataframe #######
df = pd.read_csv("https://raw.githubusercontent.com/austinlasseter/plotly_dash_tutorial/master/00%20resources/titanic.csv")
df['Survival'] = df['Survived'].map({1:'Survived', 0: 'Did Not Survive'})
variables_list=['Pclass', 'Fare', 'Age']

########### Initiate the app
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
app.title=tabtitle

####### Layout of the app ########
app.layout = html.Div([
    html.H3('Choose a continuous variable for summary statistics:'),
    dcc.Dropdown(
        id='dropdown',
        options=[{'label': i, 'value': i} for i in variables_list],
        value=variables_list[0]
    ),
    html.Br(),
    dcc.Graph(id='display-value'),
    html.A('Code on Github', href=githublink),
    html.Br(),
    html.A("Data Source", href=sourceurl),
])


######### Interactive callbacks go here #########
@app.callback(dash.dependencies.Output('display-value', 'figure'),
              [dash.dependencies.Input('dropdown', 'value')])
def display_value(continuous_var):
    results=pd.DataFrame(df.groupby(['Sex', 'Survival'])[continuous_var].mean())
    # Create a grouped bar chart
    mydata1 = go.Bar(
        x=results.loc['male'].index,
        y=results.loc['male'][continuous_var],
        name='Male',
        marker=dict(color=color1)
    )
    mydata2 = go.Bar(
        x=results.loc['female'].index,
        y=results.loc['female'][continuous_var],
        name='Female',
        marker=dict(color=color2)
    )

    mylayout = go.Layout(
        title='Grouped bar chart',
        xaxis = dict(title = 'Survival'), # x-axis label
        yaxis = dict(title = str(continuous_var)), # y-axis label

    )
    fig = go.Figure(data=[mydata1, mydata2], layout=mylayout)
    return fig


######### Run the app #########
if __name__ == '__main__':
    app.run_server(debug=True)
