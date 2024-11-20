import pandas as pd
from InquirerPy import inquirer
import numpy as np

# Load the CSV file
df = pd.read_csv(
    "C:\\Project\\BudgeWiser\\budge\\Capital_Equipment_Cost_Database.csv",
    encoding="ISO-8859-1",
)


def select_method():

    method_choices = df["Equipment"].unique().tolist()
    method_choice = inquirer.select(
        message="Choose Equipment:", choices=method_choices
    ).execute()
    print(f"You selected: {method_choice}")
    return method_choice


def select_plant_type(method_choice):

    plant_choices = (
        df[df["Equipment"] == method_choice]["Family_type"].dropna().unique().tolist()
    )
    plant_choice = inquirer.select(
        message="Choose Equipment specific type:", choices=plant_choices
    ).execute()
    print(f"You selected: {plant_choice}")

    selected_row = df[
        (df["Equipment"] == method_choice) & (df["Family_type"] == plant_choice)
    ].iloc[0]

    return {
        "Scaling_quantity": selected_row["Scaling_quantity"],
        "Unit": selected_row["Unit"],
        "Min_Scale": selected_row["Min_Scale"],
        "Max_Scale": selected_row["Max_Scale"],
        "Min_Cost": selected_row["Min_Cost"],
        "Scaling_Factor": selected_row["Scaling_Factor"],
        "CEPCI": selected_row["CEPCI"],
    }


def purchased_equipment_cost(a, b, S, n, CEPCI):

    return (a * (S / b) ** (n)) * 800/CEPCI * 1.07


def get_valid_sizing_input(s_lower, s_upper, sizing_quantity, units):

    while True:
        try:
            s = float(
                input(
                    f"Enter a value for {sizing_quantity} in {units} between {s_lower} and {s_upper}: "
                )
            )
            if s_lower <= s <= s_upper:
                return s
            else:
                print(
                    f"Error: The input value must be between {s_lower} and {s_upper}. Please try again."
                )
        except ValueError:
            print("Error: Please enter a numeric value. Try again.")


method_choice = select_method()
type_info = select_plant_type(method_choice)
s = get_valid_sizing_input(
    type_info["Min_Scale"],
    type_info["Max_Scale"],
    type_info["Scaling_quantity"],
    type_info["Unit"],
)
Purchased_equipment_cost = purchased_equipment_cost(
    type_info["Min_Cost"],
    type_info["Min_Scale"],
    s,
    type_info["Scaling_Factor"],
    type_info["CEPCI"],
)
print(f"\nThe Purchased equipment cost is: ${int(Purchased_equipment_cost): ,}")
