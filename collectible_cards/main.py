import datetime
from dash import Dash, dash_table, dcc, html
from dash.dependencies import Input, Output, State
from plotly.graph_objs import Scatter, Bar

language_coefficients = {
    "Українська": 0.1,
    "Англійська": 0.05,
    "Японська": 0.25,
    "Італійська": 0.2
}

condition_coefficients = {
    "ідеальний": 0,
    "трохи пошкоджений": -0.25,
    "пошкоджений": -0.5,
    "сильно пошкоджений": -0.75
}

foil_alternate_coefficient = 0.5

app = Dash(title='Калькулятор ціни колекційної картки', prevent_initial_callbacks=True, serve_locally=True)

app.layout = html.Div(style={'textAlign': 'center', 'maxWidth': '600px', 'margin': 'auto'}, children=[
    html.H1("Калькулятор ціни колекційної картки"),
    html.Div(style={'margin-top': '50px', 'border': '2px solid #ccc', 'border-radius': '10px', 'padding': '20px'}, children=[
        html.Div([
            html.Label("Базова ціна карти:"),
            dcc.Input(id='base-price', type='number', value=100, debounce=True, style={'width': '150px', 'margin-bottom': '10px', 'margin-top': '10px'}),
        ]),
        html.Div([
            html.Label("Мова:", style={'margin-right': '10px'}),
            dcc.Dropdown(id='language', options=[{'label': lang, 'value': lang} for lang in language_coefficients.keys()], placeholder="Оберіть мову", style={'margin-bottom': '10px'}),
        ]),
        html.Div([
            html.Label("Стан:"),
            dcc.Dropdown(id='condition', options=[{'label': cond, 'value': cond} for cond in condition_coefficients.keys()], placeholder="Оберіть стан", style={'margin-bottom': '10px'}),
        ]),
        html.Div([
            html.Label("Фольговане покриття:"),
            dcc.RadioItems(
                id='foil',
                options=[{'label': 'Так', 'value': 'yes'}, {'label': 'Ні', 'value': 'no'}],
                value='no',
                labelStyle={'display': 'inline-block', 'margin-right': '10px'}
            ),
        ]),
        html.Div([
            html.Label("Альтернативний малюнок:"),
            dcc.RadioItems(
                id='alternate',
                options=[{'label': 'Так', 'value': 'yes'}, {'label': 'Ні', 'value': 'no'}],
                value='no',
                labelStyle={'display': 'inline-block', 'margin-right': '10px'}
            ),
        ]),
        html.Button('Розрахувати вартість', id='submit-val', n_clicks=0, style={'margin-top': '20px', 'margin-bottom': '10px', 'padding': '10px 20px', 'font-size': '16px', 'background-color': 'red', 'color': 'white'}),
        html.Div(id='output-price')
    ])
])

@app.callback(
    Output('output-price', 'children'),
    [Input('submit-val', 'n_clicks')],
    [State('base-price', 'value'),
     State('language', 'value'),
     State('condition', 'value'),
     State('foil', 'value'),
     State('alternate', 'value')]
)
def update_output(n_clicks, base_price, language, condition, foil, alternate):
    if n_clicks > 0:
        try:
            base_price = float(base_price)
            if base_price < 0:
                raise ValueError
        except ValueError:
            return "Базова ціна карти повинна бути додатнім числом."

        if not language and not condition:
            return "Оберіть, будь ласка, мову і стан карти."
        if not language:
            return "Оберіть, будь ласка, мову"
        if not condition:
            return "Оберіть, будь ласка, стан карти."
        
        if language == "Японська" and foil == 'yes':
            return "Японські фольговані карти не існують."
        if language == "Італійська" and (foil == 'yes' or alternate == 'yes'):
            return "Італійські фольговані і альтернативні карти не існують."

    language_coef = language_coefficients[language]
    condition_coef = condition_coefficients[condition]
    foil_coef = foil_alternate_coefficient if 'yes' in foil else 0
    alternate_coef = foil_alternate_coefficient if 'yes' in alternate else 0
    
    total_price = base_price * (1 + language_coef + condition_coef + foil_coef + alternate_coef)
    
    return f"Ціна карти: {total_price:.2f}"

if __name__ == '__main__':
    app.run_server(debug=True)
