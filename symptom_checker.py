import json
from fuzzywuzzy import process

# Load the pet symptoms data
def load_data():
    with open('pet_symptoms.json', 'r') as file:
        return json.load(file)

# Get common symptoms for display
def get_common_symptoms(pet_type, data):
    return data.get(pet_type, {}).get("common_symptoms", [])

# Fuzzy matching for symptom input
def suggest_symptom(input_symptom, common_symptoms):
    match, score = process.extractOne(input_symptom, common_symptoms)
    return match if score >= 70 else None  # Suggest if score is above a threshold

# Get possible conditions based on symptoms
def get_possible_conditions(pet_type, symptom, data):
    if pet_type in data:
        if symptom in data[pet_type]:
            conditions_info = data[pet_type][symptom]
            conditions = conditions_info["conditions"]
            severity = conditions_info["severity"]
            action = conditions_info["action"]
            return conditions, severity, action
        else:
            return None, None, f"Sorry, no data available for '{symptom}' in {pet_type}."
    else:
        return None, None, f"Sorry, no data available for '{pet_type}'."

# Main function to run the checker
def symptom_checker():
    data = load_data()
    
    print("Welcome to the Pet Symptom Checker!")
    pet_type = input("Enter your pet type (e.g., dog, cat): ").lower()
    common_symptoms = get_common_symptoms(pet_type, data)
    
    print("Common symptoms for {}: {}".format(pet_type.capitalize(), ", ".join(common_symptoms)))
    
    symptom = input("Enter the main symptom (or type 'help' for suggestions): ").lower()
    
    if symptom == 'help':
        print("Common symptoms you can choose from: {}".format(", ".join(common_symptoms)))
        symptom = input("Enter the main symptom: ").lower()
    
    suggested_symptom = suggest_symptom(symptom, common_symptoms)
    
    if suggested_symptom:
        print(f"Did you mean '{suggested_symptom}'?")
        confirm = input("Type 'yes' to confirm or 'no' to re-enter: ").lower()
        if confirm == 'yes':
            symptom = suggested_symptom
    
    conditions, severity, action = get_possible_conditions(pet_type, symptom, data)
    
    if conditions:
        print(f"Possible conditions for {pet_type} with symptom '{symptom}':")
        for condition in conditions:
            print(f"- {condition}")
        print(f"Severity: {severity}")
        print(f"Recommended action: {action}")
    else:
        print(action)

if __name__ == "__main__":
    symptom_checker()
