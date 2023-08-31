import pandas as pd
from dash import Dash, Input, Output, dcc, html, dash_table
from dash.dependencies import Input, Output

# Load in data containing terms
data = pd.read_csv('input.csv')

# Initialize the Dash app
app = Dash(__name__)

# Set the page title
app.title = 'HuBMAP to HCA term'


# Function to determine style and text based on match quality
def get_match_style_and_text(match_quality):
    if match_quality == 'yes':
        return {'background-color': 'green', 'color': 'white'}, 'This is a good match'
    elif match_quality == 'no':
        return {'background-color': 'red', 'color': 'white'}, 'This is a bad match'
    else:
        return {'background-color': 'yellow'}, 'Match quality unknown'


# Define the style of the app
app.layout = html.Div(style={'font-family': 'Arial', 'max-width': '800px', 'margin': 'auto'}, children=[
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
                html.Div(match_text,
                         style={**match_style, 'padding': '10px', 'border-radius': '5px', 'margin-top': '5px'})
            ], style={'display': 'flex', 'flex-direction': 'column', 'align-items': 'center'}),
        ], style={'background-color': '#f4f4f4', 'padding': '20px', 'border-radius': '5px'}),

        dash_table.DataTable(
            id='matching-terms-table-display',
            columns=[{'name': 'Matching Terms', 'id': 'Matching Terms'}],
            data=matching_terms_table_data.to_dict('records'),
            style_table={'margin-top': '10px'},
            style_cell={'textAlign': 'left', 'padding': '8px'}
        )
    ]


# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
