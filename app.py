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
    crimes = ['Rape', 'K&A', 'DD', 'AoW', 'AoM', 'DV', 'WT']
    growth_rate = df.groupby('Year')[crimes].sum().pct_change() * 100
    traces = [go.Scatter(x=growth_rate.index, y=growth_rate[crime], mode='lines+markers', name=crime) for crime in crimes]
    return json.dumps(traces, cls=plotly.utils.PlotlyJSONEncoder)

def get_total_cases_data():
    crimes = ['Rape', 'K&A', 'DD', 'AoW', 'AoM', 'DV', 'WT']
    total_cases = df.groupby('Year')[crimes].sum()
    traces = [go.Bar(x=total_cases.index, y=total_cases[crime], name=crime) for crime in crimes]
    return json.dumps(traces, cls=plotly.utils.PlotlyJSONEncoder)

def get_average_cases_by_state():
    avg_cases_by_state = df.groupby('State')[['Rape', 'K&A', 'DD', 'AoW', 'AoM', 'DV', 'WT']].mean()
    traces = [go.Pie(labels=avg_cases_by_state.index, values=avg_cases_by_state[crime], name=crime) for crime in avg_cases_by_state]
    return json.dumps(traces, cls=plotly.utils.PlotlyJSONEncoder)

def get_rape_cases_data():
    avg_rape_cases = df.groupby('Year')['Rape'].mean()
    trace = go.Scatter(x=avg_rape_cases.index, y=avg_rape_cases.values, mode='lines+markers', name='Average Rape Cases')
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
    crimes = ['K&A', 'DD', 'AoW', 'AoM', 'DV', 'WT']
    highest_lowest_other = df.groupby('Year').agg({crime: ['min', 'max'] for crime in crimes})
    
    traces = []
    for crime in crimes:
        traces.append(go.Scatter(x=highest_lowest_other.index, y=highest_lowest_other[crime]['max'], mode='lines+markers', name=f'Highest {crime}'))
        traces.append(go.Scatter(x=highest_lowest_other.index, y=highest_lowest_other[crime]['min'], mode='lines+markers', name=f'Lowest {crime}'))
    
    return json.dumps(traces, cls=plotly.utils.PlotlyJSONEncoder)

# Route for Home Page
@app.route('/')
def home():
    growth_rate_data = get_growth_rate_data()
    total_cases_data = get_total_cases_data()
    return render_template('index.html', growth_rate_data=growth_rate_data, total_cases_data=total_cases_data)

@app.route('/overview')
def overview():
    growth_rate_data = get_growth_rate_data()
    total_cases_data = get_total_cases_data()
    return render_template('overview.html', growth_rate_data=growth_rate_data, total_cases_data=total_cases_data)

# Route for Crime Distribution Page
@app.route('/crime-distribution')
def crime_distribution():
    average_cases_data = get_average_cases_by_state()
    return render_template('crime_distribution.html', average_cases_data=average_cases_data)

# Route for Crime Categories Page
@app.route('/crime-categories')
def crime_categories():
    rape_cases_data = get_rape_cases_data()
    return render_template('crime_categories.html', rape_cases_data=rape_cases_data)

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
