from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Risk assessment categories and corresponding questions
questions = {
    "privacy": {
        "genetic": [
            "Do you use at-home DNA testing services like 23andMe or AncestryDNA?",
            "Did you read the terms before submitting your DNA sample?",
            "Are you aware of whether your DNA data can be sold or shared?",
            "Do you know if law enforcement can access your DNA data without consent?",
            "Have you donated blood, sperm, bone marrow or any other biological samples?",
            "Have you enabled privacy settings to restrict third-party access to your genetic data?"
        ],
        "ehr": [
            "Do you use patient portals to access your medical records?",
            "Are you aware of who can access your electronic health records (EHR)?",
            "Have you reviewed the privacy policies of your healthcare provider?",
            "Do you use public Wi-Fi or unsecured networks to access your medical records?",
            "Are you aware of exceptions to doctor patient confidentiality?",
            "Have you ever checked if your medical data has been involved in a data breach?"
        ]
    },
    "safety": {
        "insurance": [
            "Have you ever been denied health insurance due to a pre-existing condition?",
            "Do you believe insurance companies should have access to your genetic testing results?",
            "Have you disclosed past medical conditions on an insurance application without knowing how it will be used?",
            "Are you aware of the Genetic Information Nondiscrimination Act (GINA) and its protections?",
            "Do you know if your insurance provider shares your health data with other companies?",
            "Have you experienced changes in insurance premiums due to health data?",
            "Do you think your insurance company might use health data to deny coverage?",
            "Do you think your employer might use health data to influence employment decisions?"
        ],
        "legal": [
            "Are you aware that some healthcare data can be accessed by law enforcement without a warrant?",
            "Have you reviewed your state's laws on medical data privacy?",
            "Do you know if your health apps (e.g., period trackers, fitness apps) share data with third parties?",
            "Do you use two-factor authentication (2FA) for apps that store your medical data?",
            "Are you aware that doctors may have to share your legal status with authorities?",
            "Have you ever had your medical records accessed without your knowledge?"
        ],
        "gender_lgbtq": [
            "Have you ever been denied medical care based on gender identity or sexual orientation?",
            "Are you aware of your legal rights regarding healthcare discrimination?",
            "Have you faced challenges getting gender-affirming care due to medical policies?",
            "Have you ever been misgendered or had your identity dismissed by a medical provider?",
            "Have you checked for recent abortion laws and how they might affect your healthcare?",
            "Do you know if your doctors provide gender affirming care without alerting authorities?",
            "Do you know if your insurance covers LGBTQ-specific healthcare needs?"
        ]
    }
}

@app.route('/')
def index():
    return render_template('index.html', questions=questions)
@app.route('/questions', methods=['GET'])
def get_questions():
    return jsonify(questions)

@app.route('/calculate_risk', methods=['POST'])
def calculate_risk():
    data = request.json
    total_questions = len(data["responses"])
    yes_count = sum(1 for answer in data["responses"] if answer == "yes")

    risk_percentage = (yes_count / total_questions) * 100

    # Risk Level Interpretation
    if risk_percentage <= 20:
        risk_level = "Low Risk"
        advice = "You're relatively safe, but stay informed!"
    elif risk_percentage <= 50:
        risk_level = "Moderate Risk"
        advice = "Some risks exist. Consider improving privacy/safety habits."
    elif risk_percentage <= 80:
        risk_level = "High Risk"
        advice = "Significant risks detected! Take action to protect yourself."
    else:
        risk_level = "Critical Risk"
        advice = "Your data and safety are at high risk. Urgent action needed!"

    return jsonify({"risk_percentage": risk_percentage, "risk_level": risk_level, "advice": advice})

@app.route('/submit_quiz', methods=['POST'])
def submit_quiz():
    data = request.json
    responses = sum(data.values(), [])  # Flatten all answers into a single list
    total_questions = len(responses)
    yes_count = responses.count("yes")

    risk_percentage = (yes_count / total_questions) * 100

    # Determine risk level
    if risk_percentage <= 20:
        risk_level = "Low Risk"
        recommendation = "You're relatively safe, but stay informed!"
    elif risk_percentage <= 50:
        risk_level = "Moderate Risk"
        recommendation = "Some risks exist. Consider improving privacy/safety habits."
    elif risk_percentage <= 80:
        risk_level = "High Risk"
        recommendation = "Significant risks detected! Take action to protect yourself."
    else:
        risk_level = "Critical Risk"
        recommendation = "Your data and safety are at high risk. Urgent action needed!"

    return jsonify({"risk_level": risk_level, "recommendation": recommendation})

if __name__ == '__main__':
    app.run(debug=True)
