import pandas as pd
import numpy as np

# Load the CSV file
df = pd.read_csv("C:\\Project\\BudgeWiser\\budge\\Capital_Equipment_Cost_Database.csv", encoding='ISO-8859-1')

def select_method():

    method_choices = df["Equipment"].unique().tolist()
    print("Choose method: ")

    for idx, method in enumerate(method_choices, 1):
        print(f"{idx}. {method}")
    choice = int(input("Enter choice number: ")) - 1
    method_choice = method_choices[choice]
    print(f"You selected method: {method_choice}")
    return method_choice


def select_plant_type(method_choice):

    type_choices = (
        df[df["Equipment"] == method_choice]["Family_type"].dropna().unique().tolist()
    )
    print("Choose equipmetn specific type: ")
    for idx, typ in enumerate(type_choices, 1):
            print(f"{idx}. {typ}")
    choice = int(input("Enter choice number: ")) - 1
    type_choice = type_choices[choice]
    print(f"You selected equipment type: {type_choice}")

    selected_row = df[(df['Equipment'] == method_choice) & 
                    (df['Family_type'] == type_choice)].iloc[0]
    return selected_row.to_dict()


def purchased_equipment_cost(a, b, S, n, CEPCI):

    return (a * (S / b) ** n) *  800/CEPCI * 1.07


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