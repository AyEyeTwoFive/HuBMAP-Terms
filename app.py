import pandas as pd
from dash import Dash, Input, Output, dcc, html, dash_table
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc

# Load in data containing terms
data = pd.read_csv('input.csv')

# Initialize the Dash app
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Set the page title
app.title = 'HuBMAP to HCA Term'

# Define custom colors based on HubMAP website
custom_colors = {
    'green': '#0F975B',
    'red': '#D43A2B',
    'yellow': '#FFC72C',
    'background': '#F3F4F5',
    'text': '#363636'
}

# Define custom icons
icons = {
    'green': '✔️',
    'red': '❌',
    'yellow': '❓'
}

# Function to determine style and text based on match quality
def get_match_style_and_text(match_quality):
    if match_quality == 'yes':
        return {'background-color': custom_colors['green'], 'color': 'white'}, 'This is a good match'
    elif match_quality == 'no':
        return {'background-color': custom_colors['red'], 'color': 'white'}, 'No match found'
    else:
        return {'background-color': custom_colors['yellow'], 'color': custom_colors['text']}, 'Match quality unknown'

# Define the style of the app
app.layout = dbc.Container(style={'font-family': 'Arial', 'max-width': '800px', 'margin': 'auto'}, children=[
    html.Div(
        children=[
            html.P(children="🦠", className="header-emoji"),
            html.H1(
                children="HuBMAP to HCA Term", className="header-title"
            ),
            html.P(
                children=(
                    "Find HCA terms that best match a given HuBMAP term"
                ),
                className="header-description",
            ),
        ],
        className="header",),
    html.Div([
        html.H4('Select a HuBMAP term: ', style={'margin-bottom': '10px', 'color': custom_colors['text']}),
        dcc.Dropdown(
            id='term-dropdown',
            options=[{'label': term, 'value': term} for term in data.iloc[:, 0]],
            value=None,
            placeholder='Select a term'
        ),
        html.Div(id='output-display', style={'margin-top': '20px'}),
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

    output_display = [
        html.Div([
            html.H4(f'Selected HuBMAP term: {selected_term}', style={'margin-bottom': '5px', 'text-align': 'left', 'color': custom_colors['text']}),
        ], style={'background-color': custom_colors['background'], 'padding': '20px', 'border-radius': '5px'}),
    ]

    if match_quality == 'no':
        output_display.append(
            html.Div([
                html.H4('No match found', style={'margin-bottom': '5px', 'text-align': 'left', 'color': custom_colors['text']}),
            ], style={'background-color': custom_colors['red'], 'padding': '20px', 'border-radius': '5px'})
        )
    elif match_quality != 'no':
        output_display.append(
            html.Div([
                html.H4(f'Best HCA Match: {corresponding_term}', style={'margin-bottom': '5px', 'text-align': 'left', 'color': custom_colors['text']}),
                html.Div([
                    html.Div(
                        icons.get(match_quality, '') + ' ' + match_text,
                        style={**match_style, 'padding': '10px', 'border-radius': '5px', 'margin-top': '5px'}
                    )
                ], style={'display': 'flex', 'flex-direction': 'column', 'align-items': 'center'}),
            ], style={'background-color': custom_colors['background'], 'padding': '20px', 'border-radius': '5px'})
        )

    return [
        output_display,
        dbc.Table.from_dataframe(
            matching_terms_table_data,
            header=False,
            bordered=True,
            responsive=True,
            style={'margin-top': '10px', 'display': 'block' if selected_term else 'none'}  # Show table when selected_term is not None
        )
    ]

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
