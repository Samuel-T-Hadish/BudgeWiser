import pandas as pd
from InquirerPy import inquirer
import math

df = pd.read_csv("C:\\Project\\BudgeWiser\\vesseldata.csv")

def equipment_choice(df):
    """
    Function to prompt user to select an equipment from the dataframe using InquirerPy.

    Parameters:
    -----------
    df : pandas.DataFrame
        The input dataframe containing equipment data.

    Returns:
    --------
    str
        Selected equipment name.
    """
    equipment_list = df['Equipment'].unique()
    
    selected_equipment = inquirer.select(
        message="Select equipment:",
        choices=equipment_list,
    ).execute()
    
    return selected_equipment

def get_all_components(df, selected_equipment):
    """
    Function to get all types (components) for the chosen equipment.

    Parameters:
    -----------
    df : pandas.DataFrame
        The input dataframe containing equipment data.
    selected_equipment : str
        The chosen equipment name.

    Returns:
    --------
    list
        List of all components (types) for the selected equipment.
    """
    components = df[df['Equipment'] == selected_equipment]['type'].unique()
    return components

def calculate_thickness_and_weight(df, selected_equipment, selected_type):
    """
    Function to calculate the thickness based on the formula defined in the dataset.

    Parameters:
    -----------
    df : pandas.DataFrame
        The input dataframe containing equipment data.
    selected_equipment : str
        The chosen equipment name.
    selected_type : str
        The chosen type of equipment component.

    Returns:
    --------
    tuple
        Calculated thickness and weight of the vessel component.
    """
    row = df[(df['Equipment'] == selected_equipment) & (df['type'] == selected_type)].iloc[0]
    
    ID = row['ID']
    L = row['Length']
    design_P = row['Internal_design_pressure']
    S = row['Maximum_allowable_stress']
    E = row['Joint_efficiency']
    formula = row['Formula']
    Density = row['Density_of_material']
    
    if formula == 1:
        thickness = (design_P * ID) / (2 * S * E - 0.2 * design_P)
        weight = (math.pi / 24) * ((ID + 2 * thickness)**3 - (ID)**3) * Density    
    elif formula == 2:
        thickness = (design_P * ID) / (2 * S * E - 1.2 * design_P)
        weight = math.pi * (ID + 2 * thickness) * L * thickness * Density
    return thickness, weight

selected_equipment = equipment_choice(df)
components = get_all_components(df, selected_equipment)

total_weight = 0

for component in components:
    thickness, weight = calculate_thickness_and_weight(df, selected_equipment, component)
    print(f"Component: {component} | Thickness: {thickness:.6f} meters | Weight: {weight:.4f} kg")
    total_weight += weight

weight_including_multiplier = total_weight * 1.2
print(f"\nWeight of Vessel with 1.2 multiplier: {selected_equipment}: {weight_including_multiplier:.2f} kg\n")


