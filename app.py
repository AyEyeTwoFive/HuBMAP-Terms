import pandas as pd
from dash import Dash, Input, Output, dcc, html, dash_table
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc

# Load in data containing terms
data = pd.read_csv('input.csv')

# Initialize the Dash app
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Set the page title
app.title = 'HuBMAP to HCA term'


# Function to determine style and text based on match quality
def get_match_style_and_text(match_quality):
    if match_quality == 'yes':
        return {'background-color': '#3bb54a', 'color': 'white'}, 'This is a good match'
    elif match_quality == 'no':
        return {'background-color': '#d9534f', 'color': 'white'}, 'This is a bad match'
    else:
        return {'background-color': '#f0ad4e'}, 'Match quality unknown'


# Define custom icons
icons = {
    'green': '✔️',
    'red': '❌',
    'yellow': '❓'
}

# Define the style of the app
app.layout = dbc.Container(style={'font-family': 'Arial', 'max-width': '800px', 'margin': 'auto'}, children=[
    html.H1('HuBMAP to HCA term', style={'text-align': 'center'}),
    html.Div([
        dcc.Dropdown(
            id='term-dropdown',
            options=[{'label': term, 'value': term} for term in data.iloc[:, 0]],  # Populate dropdown with first column
            value=None,
            placeholder='Select a term'
        ),
        html.Div(id='output-display', style={'margin-top': '20px'}),
        html.H4('Top 10 matching HCA terms', style={'margin-top': '20px'}),
        html.Div(id='matching-terms-table')  # Empty div for table display
    ])
])


# Define the callback to update the output-display and matching-terms-table
@app.callback(
    [Output('output-display', 'children'),
     Output('matching-terms-table', 'children')],
    Input('term-dropdown', 'value')
)
def update_output(selected_term):
    if selected_term is None:
        return [], []  # Return empty lists

    corresponding_term = data[data.iloc[:, 0] == selected_term].iloc[0, 1]
    match_quality = data[data.iloc[:, 0] == selected_term].iloc[0, 11]

    match_style, match_text = get_match_style_and_text(match_quality)

    matching_terms_table_data = data[data.iloc[:, 0] == selected_term].iloc[0, 1:11].to_frame(name='Matching Terms')
    matching_terms_table_data.reset_index(drop=True, inplace=True)

    return [
        html.Div([
            html.H4(f'Selected HuBMAP term: {selected_term}', style={'margin-bottom': '5px', 'text-align': 'left'}),
            html.Div([
                html.Div('Best HCA Match: ' + corresponding_term, style={'padding': '10px', 'text-align': 'left'}),
                html.Div(
                    icons.get(match_quality, '') + ' ' + match_text,
                    style={**match_style, 'padding': '10px', 'border-radius': '5px', 'margin-top': '5px'}
                )
            ], style={'display': 'flex', 'flex-direction': 'column', 'align-items': 'center'}),
        ], style={'background-color': '#f4f4f4', 'padding': '20px', 'border-radius': '5px'}),

        dbc.Table.from_dataframe(
            matching_terms_table_data,
            header=False,
            bordered=True,
            responsive=True,
            style={'margin-top': '10px'}
        )
    ]


# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
