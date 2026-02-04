# SyntecxHub Medical Expert System
from flask import Flask, render_template, request

app = Flask(__name__)

#                    KNOWLEDGE BASE 

RULES = [
    {"name": "Common Cold", "symptoms": ["runny_nose", "sneezing", "sore_throat", "cough"]},
    {"name": "Flu (Influenza)", "symptoms": ["fever", "body_aches", "fatigue", "dry_cough", "chills"]},
    {"name": "COVID-19", "symptoms": ["fever", "dry_cough", "loss_of_smell", "shortness_of_breath", "fatigue"]},
    {"name": "Sinus Infection", "symptoms": ["headache", "facial_pain", "runny_nose", "congestion"]},
    {"name": "Asthma", "symptoms": ["shortness_of_breath", "wheezing", "chest_tightness", "cough"]},
    {"name": "Food Poisoning", "symptoms": ["nausea", "vomiting", "diarrhea", "stomach_cramps", "fever"]},
    {"name": "Migraine", "symptoms": ["severe_headache", "nausea", "sensitivity_to_light", "visual_aura"]},
    {"name": "Malaria", "symptoms": ["high_fever", "shaking_chills", "sweating", "headache", "nausea"]},
    {"name": "Nipah Virus", "symptoms": ["fever", "seizures", "difficulty_breathing", "unconsciousness","severe_headache","paralysis","jerky_movements","personality_changes" ]}
]

#                      FACT BASE 

ALL_SYMPTOMS = []

for rule in RULES:
    for symptom in rule["symptoms"]:
        if symptom not in ALL_SYMPTOMS:
            ALL_SYMPTOMS.append(symptom)

ALL_SYMPTOMS.sort()

#                     INFERENCE ENGINE 

def analyze_symptoms(user_symptoms):
    logs = []
    best_match = ""
    best_count = 0
    exact_match_found = False

    # Forward chaining applied here
    for rule in RULES:
        disease = rule["name"]
        rule_symptoms = rule["symptoms"]

        match_count = 0

        # Count matching facts
        for symptom in rule_symptoms:
            if symptom in user_symptoms:
                match_count += 1

        logs.append(
            "Checked " + disease + ": Matched "
            + str(match_count) + "/" + str(len(rule_symptoms))
        )

        # Exact match
        if match_count == len(rule_symptoms):
            best_match = disease
            exact_match_found = True
            break

        # Partial match
        if match_count > best_count and match_count >= 2:
            best_match = disease
            best_count = match_count

    #                      CONCLUSION 
    if exact_match_found:
        diagnosis = best_match
        severity = "high"
    elif best_match != "":
        diagnosis = "Likely " + best_match + " (Partial Match)"
        severity = "medium"
    else:
        diagnosis = "Unknown Condition (Insufficient symptoms)"
        severity = "low"

    return diagnosis, logs, severity

#                     FLASK ROUTES 

@app.route('/', methods=['GET', 'POST'])
def home():
    diagnosis = None
    logs = []
    severity = "low"

    if request.method == 'POST':
        selected_symptoms = request.form.getlist('symptoms')

        if len(selected_symptoms) > 0:
            diagnosis, logs, severity = analyze_symptoms(selected_symptoms)

    return render_template(
        'index.html',
        diagnosis=diagnosis,
        logs=logs,
        severity=severity,
        all_symptoms=ALL_SYMPTOMS
    )

if __name__ == '__main__':
    app.run(debug=True)
