import dash_table
from Helper import *
from Loan import *
from LoanPortfolio import *
from LoanImpacts import *
import dash
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
import plotly.express as px
import plotly.express as px
import dash_table_experiments as dt
import pandas as pd
from dash.dependencies import Input, Output, State
from Tests.Test_Loans import *

app = dash.Dash(external_stylesheets=[dbc.themes.FLATLY])
loans = LoanPortfolio()

#Gather Info from User
card = dbc.Card(
    [
        dbc.Col(html.H5(children = "Enter Information")),
        dbc.FormGroup(
            [
                dcc.Input(id="input1", placeholder='principal', type='number', min = 0),
                dcc.Input(id="input2", placeholder='rate', type='text'),
                dcc.Input(id="input3", placeholder='payment', type='number', min = 0),
                dcc.Input(id="input4", placeholder='extra payment', type='number', min = 0)
            ],
        ),
        dbc.Button(id='buttonSearch', n_clicks=0, children='Submit', color = "primary",),
    ],
     body=True
)

#Results Section
card2 = dbc.Card(
    [
        dbc.Col(html.H5(children = "Results")),
        dbc.FormGroup(
            [
                    html.H6(children="Individual:"),
                    html.Div(id="output-individual"),
                    html.H6(children="Portfolio:"),
                    html.Div(id="output-portfolio"),
                    html.H6(children="Contribution:"),
                    html.Div(id="output-contribution"),
                    html.Div(id="tt")
            ],
        )
    ],
    body=True
)

#App Layout
app.layout = dbc.Container(
    [
        #Title
        dbc.Row(
            dbc.Col(
                html.H2(children = "Loan Calculator")
            )
        ), 
        #Info from User
        dbc.Row(
            [
                dbc.Col(card, md=5),
            ],
            align="left",
        ),
        #Results Section
        dbc.Row(
            [
                dbc.Col(card2, md =8),
            ],
        align="left",
        ),
    ],
    id="main-container",
    style={"display": "flex", "flex-direction": "column"},
    fluid=True
)


#Backend coding
#This is from Loan.py
def compute_schedule(principal, rate, payment, extra_payment):
    loan = None
    try:
        loan = Loan(principal=principal, rate=rate, payment=payment, extra_payment=extra_payment)
        loan.check_loan_parameters()
        loan.compute_schedule()
    except ValueError as ex:
        print(ex)
    loans.add_loan(loan)
    #Helper.plot(loan)
    #Helper.print(loan)
    #loans.aggregate()
    print(round(loan.total_principal_paid, 2), round(loan.total_interest_paid, 2),
          round(loan.time_to_loan_termination, 0))

    if loans.get_loan_count() > 1:
        loans.aggregate()
        #Helper.plot(loans)
        Helper.print(loans)
        

# def generate_table(dataframe, max_rows=26):
#     field_names = ['Payment Number', 'Begin Principal', 'Payment', 'Extra Payment',
#                    'Applied Principal', 'Applied Interest', 'End Principal']
#     return html.Table(
#         # Header
#         [html.Tr([html.Th(col) for col in field_names]) ] +
#         # Body
#         [html.Tr([
#             html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
#         ]) for i in range(len(dataframe))]
#     )
#use datatable / dcb
#USING DCB....
# df = pd.DataFrame(
#     {
#         "First Name": ["Arthur", "Ford", "Zaphod", "Trillian"],
#         "Last Name": ["Dent", "Prefect", "Beeblebrox", "Astra"],
#     }
# )

# table = dbc.Table.from_dataframe(df, striped=True, bordered=True)



def generate_table1(dataframe, max_rows=26):
    field_names = ['Payment Number', 'Begin Principal', 'Payment', 'Extra Payment',
                   'Applied Principal', 'Applied Interest', 'End Principal']
    return dash_table.DataTable(
            id='table',
            columns=[{'id': c, 'name': c} for c in field_names],
            data=dataframe.to_dict('records'),
            style_table={
                'overflowY': 'scroll'
            })

@app.callback(
    [Output("output-individual", "children"),Output("output-portfolio", "children")],
    [Input('buttonSearch', 'n_clicks')],
    [State("input1", "value"), State("input2", "value"),State("input3", "value"),State("input4", "value")]
)
def route_line(n_clicks, input1, input2, input3, input4):
    print(input1, input2, input3, input4, n_clicks)
    table2="no table"

    if (input1 == None or input2 == None or input3 == None or input4 == None):
        return None, None
    schdl = compute_schedule(int(input1), int(input2), int(input3), int(input4))
    print("****")

    #dataframe1 = pd.DataFrame.from_dict(individual, orient='index')
    #table1 = generate_table(dataframe1)

    Helper.print(loans)
    dataframe2 = pd.DataFrame.from_dict(loans.getportfolio(), orient='index')
    table2 = generate_table1(dataframe2)

    print(schdl)
    print(dataframe2)
    #print(port)

    return "", table2 #what difference btwn individual and portfolio?????


# @app.callback(
#     Output("output-contribution", "children")
# )
# def impact():
#     contributions = [100, 10, 5]
#     person=LoanImpacts(12000.0, 4.0, 70.0, 12.0, contributions) #how to do this?????
#     table=person.compute_impacts()
#     print(table)
#     return table

if __name__ == '__main__':
    #compute_schedule(12000.0, 4.0, 70.0, 12.0)
    #compute_schedule(5000.0, 2.0, 20.0, 6.0)
    #compute_schedule(10000.0, 3.0, 60.0, 7.0)
    app.run_server(debug=True, use_reloader = False)




