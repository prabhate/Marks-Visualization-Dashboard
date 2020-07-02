import dash
import dash_auth
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import plotly.graph_objs as go

import pymongo
from pymongo import MongoClient

import pandas as pd
import numpy as np

VALID_USERNAME_PASSWORD_PAIRS = {
    'NoSql': 'Project'
}
app = dash.Dash()
auth = dash_auth.BasicAuth(
	app,
	VALID_USERNAME_PASSWORD_PAIRS
)


MONGODB_HOST = 'localhost'
MONGODB_PORT = 27017
DBS_NAME = 'YOUR_DATABASE_NAME'
COLLECTION_NAME = 'YOUR_COLLECTION_NAME'
FIELDS = {'gender': True,'parental_level_of_education': True, 'lunch': True, 'test_preparation_course': True, 'math_score': True,'reading_score' : True,'writing_score': True,'_id': False}
connection = MongoClient(MONGODB_HOST, MONGODB_PORT)
collection = connection[DBS_NAME][COLLECTION_NAME]
required = collection.find(projection=FIELDS)

df = pd.DataFrame(required)
df['id'] = df.index


trace1 = go.Scatter(
	y = df['math_score'],
	x = df['id'],
	mode = "markers",
	name = "math score",
	marker = dict(color = 'rgba(16,112,2,0.8)'),
	text = df.index)

trace2 = go.Scatter(
	y = df['reading_score'],
	x = df['id'],
	mode = "markers",
	name = "reading score",
	marker = dict(color = 'rgba(105,168,181,1)'),
	text = df.index)
trace3 = go.Scatter(
	y = df['writing_score'],
	x = df['id'],
	mode = "markers",
	name = "writing score",
	marker = dict(color = 'rgba(232, 116, 33, 1)'),
	text = df.index)

trace7 = go.Histogram(
    x=df['parental_level_of_education'],
    opacity=0.75,
    name = "parental level of education",
    marker=dict(color='rgba(171, 50, 96, 0.6)'))

trace8 = go.Scatter3d(
    x=df['math_score'],
	y=df['reading_score'],
	z=df['writing_score'],
    mode='markers',
    marker=dict(size=10,color='rgba(255, 0, 0)'),
    text = df.index)

data = [trace1]
layout1 = dict(title = 'math score',
xaxis = dict(title ='children roll number',ticklen=1,zeroline = False)
)

data2 = [trace2]
layout2 = dict(title = 'reading score',
xaxis = dict(title ='children roll number',ticklen=1,zeroline = False)
)

data3 = [trace3]
layout3 = dict(title = 'writing score',
xaxis = dict(title ='children roll number',ticklen=1,zeroline = False)
)


data5 = [trace7]
layout5 = dict(barmode='overlay',title = 'parental level of study histogram',
xaxis = dict(title ='parental_level_of_education',ticklen=1,zeroline = False),
yaxis = dict(title='count')
)

data6 = [trace8]
layout = go.Layout(margin = dict(l=0,r=0,b=0,t=0))

colors = {
    'background': '#329da8',
    'text': '#ffffff'
}

app.layout = html.Div(style={'backgroundColor': colors['background']},children = [
	html.H1('WELCOME, NoSQL Project',style={
            'textAlign': 'center',
            'color': colors['text']
        }),
	html.H2('DASHBOARD',style={
            'textAlign': 'center',
            'color': colors['text']
        }),

	dcc.Input(id='input-1-state', type='text'),
    dcc.Input(id='input-2-state', type='text'),
	dcc.Input(id='input-3-state', type='text'),
	dcc.Input(id='input-4-state', type='number'),
	dcc.Input(id='input-5-state', type='text'),
	dcc.Input(id='input-6-state', type='number',),
	dcc.Input(id='input-7-state', type='number'),
    html.Button(id='submit-button-state', n_clicks=0, children='Submit'),
    html.Div(id='output-state'),
	dcc.Graph(
        id='math_scores',
        figure = dict(data = data, layout = layout1)
    ),
	dcc.Graph(
        id='reading_scores',
        figure = dict(data = data2, layout = layout2)
    ),
	dcc.Graph(
        id='writing_scores',
        figure = dict(data = data3, layout = layout3)
    ),
	dcc.Graph(
        id='parental level of education',
        figure = dict(data = data5, layout = layout5)
    ),
	dcc.Graph(
        id='3d',
        figure = dict(data = data6, layout = layout)
    )
	])


@app.callback(Output('output-state', 'children'),
              [Input('submit-button-state', 'n_clicks')],
              [State('input-1-state', 'value'),
               State('input-2-state', 'value'),
			   State('input-3-state', 'value'),
			   State('input-4-state', 'value'),
			   State('input-5-state', 'value'),
			   State('input-6-state', 'value'),
			   State('input-7-state', 'value')]
			  )
def update_output(n_clicks, input1, input2,input3,input4,input5,input6,input7):
	new_user_input = dict(gender=input1,lunch=input2,test_preparation_course=input3,math_score=input4,parental_level_of_education=input5,reading_score=input6,writing_score=input7)
	res = all(x == None for x in new_user_input.values())
	if res is True:
		pass

	collection.insert_one(new_user_input)
	return u'''
		The submit Button has been pressed {} times.
		gender is "{}",\n
		lunch is "{}",\n
		test preparation course is "{}",\n
		math score is "{}",\n
		parental level of education is \n
		reading score is "{}",\n
		writing score is "{}"
	'''.format(n_clicks,input1,input2,input3,input4,input5,input6,input7)

	
if __name__ == '__main__':
    app.run_server(debug=True)
