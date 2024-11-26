from flask import Flask, render_template
import requests
import plotly.graph_objs as go

app = Flask(__name__)

# Code to fetch COVID-19 data from the API
def fetch_data(api_key):
    url = f"https://api.covidactnow.org/v2/states.json?apiKey={api_key}"
    response = requests.get(url)
    data = response.json()
    return data

# Route for the dashboard
@app.route('/')
def dashboard():
    api_key = "5d8378493a754735a4e955394d003967"
    data = fetch_data(api_key)
    
    table_data = []
    for entry in data:
        state = entry['state']
        cases = entry['actuals']['cases']
        new_cases = entry['actuals']['newCases']
        deaths = entry['actuals']['deaths']
        positive_tests = entry['actuals']['positiveTests']
        case_density = entry['metrics']['caseDensity']
        hospital_beds = entry['actuals']['hospitalBeds']['capacity']
        vaccination_completed = entry['actuals']['vaccinationsCompleted']
        table_data.append({'state': state, 'cases': cases, 'new_cases': new_cases, 'deaths': deaths,
                           'positive_tests': positive_tests, 'case_density': case_density,
                           'hospital_beds': hospital_beds, 'vaccination_completed': vaccination_completed})

    # Bar Plot: New Cases Per State
    states = [entry['state'] for entry in table_data]
    new_cases = [entry['new_cases'] for entry in table_data]
    
    bar_plot = go.Bar(x=states, y=new_cases, name='New Cases', marker=dict(color='blue'))
    bar_layout = go.Layout(title='COVID-19 Cases by State', xaxis_title='State', yaxis_title='New Cases')
    bar_fig = go.Figure(data=[bar_plot], layout=bar_layout)

    # Pie Chart: Percentage of Deaths by State
    deaths = [entry['deaths'] for entry in table_data]
    pie_chart = go.Pie(labels=states, values=deaths, name='Deaths')
    pie_layout = go.Layout(title='Death percentage by State')
    pie_layout = go.Layout(
        title='Death percentage by State',
        width=800,  # Increase the width
        height=600  # Increase the height
    )
    pie_fig = go.Figure(data=[pie_chart], layout=pie_layout)

    # Generate HTML for the plots
    bar_graph = bar_fig.to_html(full_html=False)
    pie_graph = pie_fig.to_html(full_html=False)

    return render_template('index.html', new_case_graph=bar_graph, starebcase_graph=pie_graph, table_data=table_data)

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=False)
