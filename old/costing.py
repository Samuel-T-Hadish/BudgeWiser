import json
import pandas as pd
from rich.console import Console
from rich.table import Table
from InquirerPy import inquirer

def calculate_direct_cost(material_cost, direct_percentages):
    """
    Calculate the direct cost from the material cost using provided percentages
    and return both the total direct cost and a DataFrame with the cost breakdown.

    Args:
        material_cost (float): The base material cost.
        direct_percentages (dict): A dictionary of percentages for different cost elements.

    Returns:
        float: The total direct cost.
        pd.DataFrame: A DataFrame containing the breakdown of costs.
    """
    # Extract the relevant percentages from the dictionary
    piping_percent = direct_percentages["piping_percent"]
    instrumentation_percent = direct_percentages["instrumentation_percent"]
    electrical_percent = direct_percentages["electrical_percent"]
    structural_percent = direct_percentages["structural_percent"]
    others_percent = direct_percentages["others_percent"]
    operational_spares_percent = direct_percentages["operational_spares_percent"]
    installation_percent = direct_percentages["installation_percent"]
    construction_percent = direct_percentages["construction_percent"]
    commissioning_percent = direct_percentages["commissioning_percent"]

    # Calculate the costs based on percentages
    piping_cost = material_cost * piping_percent / 100
    instrumentation_cost = material_cost * instrumentation_percent / 100
    electrical_cost = material_cost * electrical_percent / 100
    structural_cost = material_cost * structural_percent / 100
    others_cost = material_cost * others_percent / 100
    operational_spares_cost = material_cost * operational_spares_percent / 100
    installation_cost = material_cost * installation_percent / 100
    construction_cost = material_cost * construction_percent / 100
    commissioning_cost = material_cost * commissioning_percent / 100

    # Total direct cost is the sum of all the calculated costs
    total_direct_cost = (material_cost + piping_cost + instrumentation_cost +
                         electrical_cost + structural_cost + others_cost +
                         operational_spares_cost + installation_cost + construction_cost +
                         commissioning_cost)

    # Create a DataFrame with the breakdown of costs and percentages where applicable
    cost_breakdown = {
        "Category": ["Material", "Piping", "Instrumentation", "Electrical", "Structural", "Others", "Operational Spares", "Installation", "Construction", "Commissioning"],
        "Percentage (%)": ["-", direct_percentages["piping_percent"], direct_percentages["instrumentation_percent"],
                           direct_percentages["electrical_percent"], direct_percentages["structural_percent"],
                           direct_percentages["others_percent"], direct_percentages["operational_spares_percent"],
                           direct_percentages["installation_percent"], direct_percentages["construction_percent"],
                           direct_percentages["commissioning_percent"]],
        "Cost (USD)": [material_cost, piping_cost, instrumentation_cost, electrical_cost, structural_cost, others_cost,
                       operational_spares_cost, installation_cost, construction_cost, commissioning_cost]
    }

    df_breakdown = pd.DataFrame(cost_breakdown)

    # Set Category as index
    df_breakdown.set_index("Category", inplace=True)

    # Add a final row for the total direct cost
    total_row = pd.DataFrame([["-", total_direct_cost]], columns=["Percentage (%)", "Cost (USD)"], index=["Total Direct Cost"])
    df_breakdown = pd.concat([df_breakdown, total_row], ignore_index=False)

    return total_direct_cost, df_breakdown

def calculate_epc_cost(direct_cost, contractor_indirects):
    """
    Calculate the EPC (Engineering, Procurement, and Construction) cost by adding
    contractor indirect costs to the direct cost, and return the total cost with a breakdown.

    Args:
        direct_cost (float): The total direct cost (sum of material, installation, etc.).
        contractor_indirects (dict): A dictionary of percentages for contractor indirect costs.

    Returns:
        float: The total EPC cost.
        pd.DataFrame: A DataFrame containing the breakdown of contractor indirect costs.
    """
    # Extract the relevant percentages for contractor indirects
    detailed_engineering_percent = contractor_indirects["detailed_engineering_percent"]
    freight_percent = contractor_indirects["freight_percent"]
    tpia_percent = contractor_indirects["tpia_percent"]
    supervision_percent = contractor_indirects["supervision_percent"]

    # Calculate the contractor indirect costs
    detailed_engineering_cost = direct_cost * detailed_engineering_percent / 100
    freight_cost = direct_cost * freight_percent / 100
    tpia_cost = direct_cost * tpia_percent / 100
    supervision_cost = direct_cost * supervision_percent / 100

    # Sum up all contractor indirect costs
    contractor_indirect_cost = (detailed_engineering_cost + freight_cost +
                                tpia_cost + supervision_cost)

    # Total EPC cost is the sum of direct cost and contractor indirect cost
    epc_cost = direct_cost + contractor_indirect_cost

    # Create a DataFrame with the breakdown of contractor indirect costs
    cost_breakdown = {
        "Category": ["Direct Cost", "Detailed Engineering", "Freight", "TPIA", "Supervision"],
        "Percentage (%)": ["-", detailed_engineering_percent, freight_percent, tpia_percent, supervision_percent],
        "Cost (USD)": [direct_cost, detailed_engineering_cost, freight_cost, tpia_cost, supervision_cost]
    }

    df_breakdown = pd.DataFrame(cost_breakdown)
    df_breakdown.set_index("Category", inplace=True)

    # Add a final row for the total EPC cost
    total_row = pd.DataFrame([["-", epc_cost]], columns=["Percentage (%)", "Cost (USD)"], index=["Total EPC Cost"])
    df_breakdown = pd.concat([df_breakdown, total_row], ignore_index=False)

    return epc_cost, df_breakdown

def calculate_total_installed_cost(epc_cost, client_indirects, contingency_percent):
    """
    Calculate the Total Installed Cost (TIC) by adding client indirect costs and contingency to the EPC cost.

    Args:
        epc_cost (float): The total EPC cost (sum of direct and contractor indirect costs).
        client_indirects (dict): A dictionary of percentages for client indirect costs.
        contingency_percent (float): The percentage for contingency to apply on the base cost.

    Returns:
        float: The total installed cost.
        pd.DataFrame: A DataFrame containing the breakdown of client indirects and contingency costs.
    """
    # Extract the relevant percentages for client indirects
    prefeed_feed_percent = client_indirects["prefeed_feed_percent"]
    pmc_pmt_percent = client_indirects["pmc_pmt_percent"]
    insurance_percent = client_indirects["insurance_percent"]

    # Calculate the client indirect costs
    prefeed_feed_cost = epc_cost * prefeed_feed_percent / 100
    pmc_pmt_cost = epc_cost * pmc_pmt_percent / 100
    insurance_cost = epc_cost * insurance_percent / 100

    # Sum up all client indirect costs
    client_indirect_cost = prefeed_feed_cost + pmc_pmt_cost + insurance_cost

    # Contingency cost
    contingency_cost = (epc_cost + client_indirect_cost) * contingency_percent / 100

    # Total Installed Cost (TIC) is the sum of EPC cost, client indirects, and contingency
    total_installed_cost = epc_cost + client_indirect_cost + contingency_cost

    # Create a DataFrame with the breakdown of client indirect costs and contingency
    cost_breakdown = {
        "Category": ["EPC Cost", "PreFEED/FEED", "PMC/PMT", "Insurance", "Contingency"],
        "Percentage (%)": ["-", prefeed_feed_percent, pmc_pmt_percent, insurance_percent, contingency_percent],
        "Cost (USD)": [epc_cost, prefeed_feed_cost, pmc_pmt_cost, insurance_cost, contingency_cost]
    }

    df_breakdown = pd.DataFrame(cost_breakdown)
    df_breakdown.set_index("Category", inplace=True)

    # Add a final row for the total installed cost
    total_row = pd.DataFrame([["-", total_installed_cost]], columns=["Percentage (%)", "Cost (USD)"], index=["Total Installed Cost"])
    df_breakdown = pd.concat([df_breakdown, total_row], ignore_index=False)

    return total_installed_cost, df_breakdown



# Load JSON data from a file
with open('settings.json', 'r') as file:
    settings_dict = json.load(file)

# Initialize console for output
console = Console()

# Create a table object
table = Table(title="Cost Percentages")

# Add columns to the table with fixed widths
table.add_column("Category", justify="left", style="cyan", width=20)
table.add_column("Key", justify="left", style="magenta", width=30)
table.add_column("Value", justify="right", style="green", width=10)

# Iterate through the JSON and handle both dictionaries and integers
for category, values in settings_dict["percentages"].items():
    if isinstance(values, dict):  # If the value is a dictionary
        for key, value in values.items():
            table.add_row(category, key, str(value))
    else:  # If the value is not a dictionary (like an integer or float)
        table.add_row(category, category, str(values))

# Print the table
console.print(table)



# Get material cost input using InquirerPy
material_cost = float(inquirer.text(message="Enter the material cost (USD):").execute())

# Example percentages (taken from settings_dict)
direct_percentages = settings_dict["percentages"]["direct"]  # Example percentages from the JSON file

# Call the function to calculate the direct cost and get the DataFrame
direct_cost, df_direct_cost = calculate_direct_cost(material_cost, direct_percentages)
print(df_direct_cost)


contractor_indirects_percentages = settings_dict["percentages"]["contractor_indirects"]  # Example percentages from the JSON file

# Call the function to calculate the EPC cost and get the breakdown
epc_cost, df_epc_cost = calculate_epc_cost(direct_cost, contractor_indirects_percentages)

# Display the total EPC cost and the breakdown
print(df_epc_cost)

client_indirects_percentages = settings_dict["percentages"]["client_indirects"]  # Example percentages from the JSON file
contingency_percent = settings_dict["percentages"]["contingency_percent"]  # Example percentage from the JSON file

# Call the function to calculate the total installed cost and get the breakdown
total_installed_cost, df_total_installed_cost = calculate_total_installed_cost(epc_cost, client_indirects_percentages, contingency_percent)

# Display the total installed cost and the breakdown
print(df_total_installed_cost)
