import pandas as pd
import numpy as np
from dash import Dash, dcc, html, Output, Input

# Load the CSV file
df = pd.read_csv("data.csv", encoding='ISO-8859-1')

# Initialize the Dash app
app = Dash(__name__)

# Define the app layout
app.layout = html.Div([
    html.H1("Capital Cost Calculator"),

    # Dropdown to select method
    html.Label("Select Method"),
    dcc.Dropdown(
        id='method-dropdown',
        options=[{'label': method, 'value': method} for method in df['method'].unique()],
        placeholder="Choose method",
    ),

    # Dropdown to select plant type
    html.Label("Select Plant Type"),
    dcc.Dropdown(id='plant-dropdown', placeholder="Choose plant type"),

    # Dropdown to select equipment
    html.Label("Select Equipment"),
    dcc.Dropdown(id='equipment-dropdown', placeholder="Choose equipment type"),

    # Dropdown to select equipment type
    html.Label("Select Equipment Type"),
    dcc.Dropdown(id='type-dropdown', placeholder="Choose specific type for the equipment"),

    # Input for sizing quantity
    html.Label(id='sizing-quantity-label', children="Enter Sizing Quantity"),
    dcc.Input(id='sizing-quantity-input', type='number', placeholder="Enter sizing quantity"),

    # Button to calculate costs
    html.Button("Calculate Cost", id='calculate-button', n_clicks=0),

    # Output for purchased equipment cost
    html.Div(id='purchased-equipment-cost-output'),

    # Output for installed equipment or total fixed capital cost
    html.Div(id='total-cost-output')
])


# Update plant type options based on selected method
@app.callback(
    Output('plant-dropdown', 'options'),
    Input('method-dropdown', 'value')
)
def update_plant_options(selected_method):
    if selected_method:
        plant_choices = df[df['method'] == selected_method]['plant_type'].dropna().unique()
        return [{'label': plant, 'value': plant} for plant in plant_choices]
    return []


# Update equipment options based on selected plant type
@app.callback(
    Output('equipment-dropdown', 'options'),
    Input('plant-dropdown', 'value')
)
def update_equipment_options(selected_plant):
    if selected_plant:
        equipment_choices = df[df['plant_type'] == selected_plant]['equipment'].dropna().unique()
        return [{'label': eq, 'value': eq} for eq in equipment_choices]
    return []


# Update equipment type options based on selected equipment
@app.callback(
    Output('type-dropdown', 'options'),
    Input('equipment-dropdown', 'value')
)
def update_type_options(selected_equipment):
    if selected_equipment:
        type_choices = df[df['equipment'] == selected_equipment]['type'].dropna().unique()
        return [{'label': typ, 'value': typ} for typ in type_choices]
    return []

# Update sizing quantity label based on selected equipment type
@app.callback(
    Output('sizing-quantity-label', 'children'),
    Input('type-dropdown', 'value')
)
def update_sizing_quantity_label(selected_type):
    if selected_type:
        row = df[df['type'] == selected_type].iloc[0]
        sizing_quantity_label = f"Enter {row['sizing_quantity']} in {row['units']} (Range: {row['s_lower']} - {row['s_upper']})"
        return sizing_quantity_label, ""
    return "Enter Sizing Quantity", ""


# Perform calculations and update outputs
@app.callback(
    Output('purchased-equipment-cost-output', 'children'),
    Output('total-cost-output', 'children'),
    Input('calculate-button', 'n_clicks'),
    Input('method-dropdown', 'value'),
    Input('plant-dropdown', 'value'),
    Input('equipment-dropdown', 'value'),
    Input('type-dropdown', 'value'),
    Input('sizing-quantity-input', 'value')
)
def calculate_costs(n_clicks, method, plant, equipment, equipment_type, S):
    if n_clicks > 0 and method and plant and equipment and equipment_type and S:
        # Retrieve selected row
        selected_row = df[(df['method'] == method) &
                          (df['plant_type'] == plant) &
                          (df['equipment'] == equipment) &
                          (df['type'] == equipment_type)].iloc[0]

        # Retrieve necessary values from row
        a, b, n = selected_row['a'], selected_row['b'], selected_row['n']
        
        # Calculate purchased equipment cost
        Purchased_equipment_cost = a + b * (S ** n)
        purchased_cost_output = f"Purchased Equipment Cost: ${Purchased_equipment_cost:,.2f}"

        # Calculate installed cost or total fixed capital cost based on method
        if method == "Hand":
            installation_factor = selected_row['installation_factor']
            Installed_equipment_cost = Purchased_equipment_cost * installation_factor
            total_cost_output = f"Installed Equipment Cost: ${Installed_equipment_cost:,.2f}"
        else:
            # Using other factors for total fixed capital cost calculation
            fm = selected_row['material_factor']
            fer = selected_row['equipment_erection_factor']
            fp = selected_row['piping_factor']
            fi = selected_row['instrumentation_and_control_factor']
            fel = selected_row['electrical_factor']
            fc = selected_row['civil_factor']
            fs = selected_row['structures_and_buildings_factor']
            fl = selected_row['lagging_and_paint_factor']
            OS = selected_row['Offsites_factor']
            DE = selected_row['design_and_engineering_factor']
            X = selected_row['contingency']
            location_factor = selected_row['location_factor']

            ISBL_cost = Purchased_equipment_cost * ((1 + fp) * fm + (fer + fel + fi + fc + fs + fl))
            Total_fixed_capital_cost = ISBL_cost * (1 + OS) * (1 + DE + X) * location_factor
            total_cost_output = f"Total Fixed Capital Cost: ${Total_fixed_capital_cost:,.2f}"

        return purchased_cost_output, total_cost_output
    return "", ""

# Run the Dash app
if __name__ == '__main__':
    app.run_server(debug=True)
