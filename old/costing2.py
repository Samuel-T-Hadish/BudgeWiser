from InquirerPy import inquirer

# Radio button prompt
answer = inquirer.select(
    message="Choose your option:",
    choices=["Option 1", "Option 2", "Option 3"],
).execute()

print(f"You selected: {answer}")

# Checkbox prompt
answers = inquirer.checkbox(
    message="Select multiple options:",
    choices=["Option A", "Option B", "Option C", "Option D"],
).execute()

print(f"You selected: {answers}")

# Dropdown-like prompt (select)
choice = inquirer.select(
    message="Select from dropdown:",
    choices=["Dropdown 1", "Dropdown 2", "Dropdown 3"],
).execute()

print(f"Dropdown selected: {choice}")
