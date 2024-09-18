from flask import Flask, render_template
import pandas as pd
import plotly.graph_objs as go
import plotly
import json

app = Flask(__name__)

# Load the dataset
df = pd.read_csv('CrimesOnWomenData.csv')

# Helper functions to generate charts
def get_growth_rate_data():
    growth_rate = df.groupby('Year').sum().pct_change() * 100
    trace = go.Bar(x=growth_rate.index, y=growth_rate['Total Crimes'], name='Annual Growth Rate')
    return json.dumps([trace], cls=plotly.utils.PlotlyJSONEncoder)

def get_total_cases_data():
    total_cases = df.groupby('Year').sum()
    trace = go.Scatter(x=total_cases.index, y=total_cases['Total Crimes'], mode='lines+markers', name='Total Cases')
    return json.dumps([trace], cls=plotly.utils.PlotlyJSONEncoder)

def get_average_cases_by_state():
    avg_cases_by_state = df.groupby('State').mean()
    trace = go.Pie(labels=avg_cases_by_state.index, values=avg_cases_by_state['Total Crimes'], name='Average Cases by State')
    return json.dumps([trace], cls=plotly.utils.PlotlyJSONEncoder)

def get_rape_cases_data():
    avg_rape_cases = df.groupby('Year')['Rape'].mean()
    trace = go.Scatter(x=avg_rape_cases.index, y=avg_rape_cases.values, mode='lines+markers', name='Average Rape Cases')
    return json.dumps([trace], cls=plotly.utils.PlotlyJSONEncoder)

def get_other_crimes_data():
    avg_other_crimes = df.groupby('Year').mean()
    trace = go.Bar(x=avg_other_crimes.index, y=avg_other_crimes['Other Crimes'], name='Average Other Crimes')
    return json.dumps([trace], cls=plotly.utils.PlotlyJSONEncoder)

def get_highest_rape_cases_data():
    highest_rape_cases = df.groupby('Year')['Rape'].max()
    trace = go.Bar(x=highest_rape_cases.index, y=highest_rape_cases.values, name='Highest Rape Cases Each Year')
    return json.dumps([trace], cls=plotly.utils.PlotlyJSONEncoder)

def get_lowest_rape_cases_data():
    lowest_rape_cases = df.groupby('Year')['Rape'].min()
    trace = go.Bar(x=lowest_rape_cases.index, y=lowest_rape_cases.values, name='Lowest Rape Cases Each Year')
    return json.dumps([trace], cls=plotly.utils.PlotlyJSONEncoder)

def get_highest_lowest_other_crimes_data():
    highest_lowest_other = df.groupby('Year').agg({'Other Crimes': ['min', 'max']})
    trace = go.Bar(x=highest_lowest_other.index, y=highest_lowest_other['Other Crimes']['max'], name='Highest Other Crimes')
    trace2 = go.Bar(x=highest_lowest_other.index, y=highest_lowest_other['Other Crimes']['min'], name='Lowest Other Crimes')
    return json.dumps([trace, trace2], cls=plotly.utils.PlotlyJSONEncoder)

# Route for Home Page
@app.route('/')
def home():
    # growth_rate_data = get_growth_rate_data()
    # total_cases_data = get_total_cases_data()
    # return render_template('home.html', growth_rate_data=growth_rate_data, total_cases_data=total_cases_data)
    return render_template('index.html')
# Route for Crime Distribution Page
@app.route('/crime-distribution')
def crime_distribution():
    average_cases_data = get_average_cases_by_state()
    return render_template('crime_distribution.html', average_cases_data=average_cases_data)

# Route for Crime Categories Page
@app.route('/crime-categories')
def crime_categories():
    rape_cases_data = get_rape_cases_data()
    other_crimes_data = get_other_crimes_data()
    return render_template('crime_categories.html', rape_cases_data=rape_cases_data, other_crimes_data=other_crimes_data)

# Route for Yearly Comparison Page
@app.route('/yearly-comparison')
def yearly_comparison():
    highest_rape_cases_data = get_highest_rape_cases_data()
    lowest_rape_cases_data = get_lowest_rape_cases_data()
    highest_lowest_other_crimes_data = get_highest_lowest_other_crimes_data()
    return render_template('yearly_comparison.html', highest_rape_cases_data=highest_rape_cases_data,
                           lowest_rape_cases_data=lowest_rape_cases_data,
                           highest_lowest_other_crimes_data=highest_lowest_other_crimes_data)

if __name__ == '__main__':
    app.run(debug=True)
