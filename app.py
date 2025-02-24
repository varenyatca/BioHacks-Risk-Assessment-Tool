from flask import Flask, request, jsonify
import json

app = Flask(__name__)

# Risk categories and scoring system
RISK_FACTORS = {
    "genetic_testing": {
        "questions": [
            {"q": "Have you taken a commercial genetic test (e.g., 23andMe, AncestryDNA)?", "low": 0, "high": 2},
            {"q": "Are you aware of who owns your genetic data after testing?", "low": 0, "high": 2},
            {"q": "Do you read privacy policies before submitting DNA for testing?", "low": 0, "high": 2},
        ]
    },
    "ehr_risks": {
        "questions": [
            {"q": "Do you know who has access to your electronic health records?", "low": 0, "high": 2},
            {"q": "Have you checked if your EHR provider shares data with third parties?", "low": 0, "high": 2},
        ]
    },
    "insurance_risks": {
        "questions": [
            {"q": "Do you think health insurers can use your genetic information to deny coverage?", "low": 0, "high": 2},
            {"q": "Have you experienced premium changes due to a medical condition?", "low": 0, "high": 2},
        ]
    },
    "legal_risks": {
        "questions": [
            {"q": "Are you aware that law enforcement can access your medical records under certain conditions?", "low": 0, "high": 2},
            {"q": "Do you know if your health data is shared with third-party research firms?", "low": 0, "high": 2},
        ]
    },
}

# Recommendations based on risk level
RECOMMENDATIONS = {
    "low": "Your privacy risk appears low. Continue practicing good security habits and stay informed.",
    "moderate": "Your privacy risk is moderate. Consider reviewing your privacy settings and limiting data sharing.",
    "high": "Your privacy risk is high. Take immediate steps to protect your health data and consult privacy experts if needed."
}

def calculate_risk(user_answers):
    """Calculate total risk score and return a risk level"""
    total_score = 0
    for category, answers in user_answers.items():
        for i, answer in enumerate(answers):
            question = RISK_FACTORS[category]["questions"][i]
            total_score += question["high"] if answer.lower() == "yes" else question["low"]

    # Define risk level based on score
    if total_score <= 4:
        return "low"
    elif total_score <= 8:
        return "moderate"
    else:
        return "high"

@app.route('/submit_quiz', methods=['POST'])
def submit_quiz():
    """Handles quiz submission and returns risk assessment"""
    try:
        user_answers = request.json  # Expecting a JSON payload
        risk_level = calculate_risk(user_answers)
        response = {
            "risk_level": risk_level,
            "recommendation": RECOMMENDATIONS[risk_level]
        }
        return jsonify(response), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/questions', methods=['GET'])
def get_questions():
    """Returns quiz questions"""
    questions = {category: RISK_FACTORS[category]["questions"] for category in RISK_FACTORS}
    return jsonify(questions), 200

if __name__ == '__main__':
    app.run(debug=True)
