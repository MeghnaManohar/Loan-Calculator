from Helper import *
from Loan import *
from LoanPortfolio import *
from LoanImpacts import *
from Tests.Test_Loans import *
import dash
import dash_table
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_html_components as html
import plotly.express as px
import dash_table_experiments as dt
import pandas as pd
from dash.dependencies import Input, Output, State


app = dash.Dash(external_stylesheets=[dbc.themes.FLATLY])
loans = LoanPortfolio()

#Gather Info from User
card = dbc.Card(
    [
        dbc.Col(html.H5(children = "Enter Information for Each Loan")),
        dbc.FormGroup(
            [
                dcc.Input(id="input1", placeholder='Principal', type='number', min = 0),
                dcc.Input(id="input2", placeholder='Rate', type='text'),
                dcc.Input(id="input3", placeholder='Min Payment', type='number', min = 0),
                dcc.Input(id="input4", placeholder='Extra Payment', type='number', min = 0)
            ],
        ),
        dbc.Button(id='buttonSearch', n_clicks=0, children='Submit', color = "primary",),
    ],
     body=True
)

#Results Section
card2 = dbc.Card(
    [
        dbc.Col(html.H5(children = "Amortization Schedules")),
        dbc.FormGroup(
            [
                    html.H6(children="Individual Loan Schedule(s):"),
                    html.Div(id="output-individual"),
                    html.H6(children="Portfolio Schedule:"),
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


##Backend coding
#Created this function to round the numbers during schedule creation 
def roundedDict(schedule):
    rounded = {}
    foo = lambda t: (round(t[0],2), round(t[1],2), round(t[2],2), round(t[3],2), round(t[4],2), round(t[5],2), round(t[6],2))
   
    for k in schedule.keys():
        rounded[k] = foo(schedule[k])
    return rounded

#This is from Loan.py
def compute_schedule(principal, rate, payment, extra_payment):
    loans.schedule = {} #reset schedule of loan portfolio bc professor is not during aggregation
    loan = None
    try:
        loan = Loan(principal=principal, rate=rate, payment=payment, extra_payment=extra_payment)
        loan.check_loan_parameters()
        loan.compute_schedule()
    except ValueError as ex:
        print(ex)
    #Add loans to portfolio
    loans.add_loan(loan)
    #Realized that the loan schedule wasn't reading it when just 1 loan, so now aggregates at all times 
    loans.aggregate()
    # print(round(loan.total_principal_paid, 2), round(loan.total_interest_paid, 2),
          # round(loan.time_to_loan_termination, 0))


def generate_table(dataframe, max_rows=25):
    field_names = ['Payment Number', 'Begin Principal', 'Payment', 'Extra Payment',
                   'Applied Principal', 'Applied Interest', 'End Principal']
    return dash_table.DataTable(
            id='table',
            columns=[{'id': c, 'name': c} for c in field_names],
            data=dataframe.to_dict('records'),
            page_size = max_rows,
            fixed_rows={'headers': True},
            style_cell = {'minWidth': 95, 'maxWidth': 95, 'width': 95},
            style_table={'height': '300px', 'overflowY': 'auto'}
            )

@app.callback(
    [Output("output-individual", "children"),Output("output-portfolio", "children")],
    [Input('buttonSearch', 'n_clicks')],
    [State("input1", "value"), State("input2", "value"),State("input3", "value"),State("input4", "value")]
)

def schedule_creation(n_clicks, input1, input2, input3, input4):
    #print(input1, input2, input3, input4, n_clicks)
    port_table="no table"

    if (input1 == None or input2 == None or input3 == None or input4 == None):
        return None, None
    compute_schedule(round(float(input1),2), round(float(input2),2), round(float(input3),2), round(float(input4),2))
    # Helper.print(loans)

    # For Individual Loan Schedule(s)
    #loans.getloans = list of individual loans and we iterate through that
    indvloans = []
    for l in loans.getloans():
        tempdataframe = pd.DataFrame.from_dict(roundedDict(l.schedule), orient='index', columns=['Payment Number', 'Begin Principal', 'Payment', 'Extra Payment',
                   'Applied Principal', 'Applied Interest', 'End Principal'])
        indvloans.append(generate_table(tempdataframe))
  
    #For Portfolio Schedule   
    dataframe = pd.DataFrame.from_dict(roundedDict(loans.getportfolio()), orient='index', columns=['Payment Number', 'Begin Principal', 'Payment', 'Extra Payment',
                   'Applied Principal', 'Applied Interest', 'End Principal'])
    port_table = generate_table(dataframe)

    return indvloans, port_table


#Contribution look at LoanImpacts.py
#Store the loan termination and interest paid for each individual loan and then use them as inputs??
def compute_impact(principal, rate, payment, extra_payment, contribution):
    loan_all = None
    loan_none = None
    try:
        loan_all = Loan(principal=principal, rate=rate, payment=payment, extra_payment=extra_payment, contribution = contribution)
        loan_none = Loan(principal=principal, rate=rate, payment=payment, extra_payment=extra_payment, contribution = 0)

@app.callback(
    Output("output-contribution", "children"),
    [Input('buttonSearch', 'n_clicks')],
    [State("input1", "value"), State("input2", "value"),State("input3", "value"),State("input4", "value")]
    )
def impact(n_clicks, input1, input2, input3, input4):
    contribution = []
    table = compute_impact(round(float(input1),2), round(float(input2),2), round(float(input3),2), round(float(input4),2), contributions)
    return table

    
# def impact():
#     contributions = [100, 10, 5]
#     person=LoanImpacts(12000.0, 4.0, 70.0, 12.0, contributions) #how to do this?????
#     table=person.compute_impacts()
#     print(table)
#     return table

if __name__ == '__main__':
    app.run_server(debug=True, use_reloader = False)




