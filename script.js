document.addEventListener("DOMContentLoaded", function () {
    const quizForm = document.getElementById("quiz-form");
    const quizContainer = document.getElementById("quiz-questions");
    const resultContainer = document.getElementById("result");
    const riskLevelText = document.getElementById("risk-level");
    const recommendationText = document.getElementById("recommendation");

    // Fetch quiz questions from backend
    fetch("/questions")
        .then(response => response.json())
        .then(data => {
            let html = "";
            Object.keys(data).forEach(category => {
                html += `<h3>${category.replace('_', ' ').toUpperCase()}</h3>`;
                data[category].forEach((question, index) => {
                    html += `
                        <label>${question.q}</label><br>
                        <input type="radio" name="${category}-${index}" value="yes"> Yes
                        <input type="radio" name="${category}-${index}" value="no"> No
                        <br><br>
                    `;
                });
            });
            quizContainer.innerHTML = html;
        })
        .catch(error => console.error("Error fetching questions:", error));

    // Handle form submission
    quizForm.addEventListener("submit", function (event) {
        event.preventDefault();

        let userAnswers = {};
        let inputs = document.querySelectorAll("input[type=radio]:checked");

        // Group answers by category
        inputs.forEach(input => {
            let [category, index] = input.name.split("-");
            if (!userAnswers[category]) {
                userAnswers[category] = [];
            }
            userAnswers[category].push(input.value);
        });

        // Send data to backend
        fetch("/submit_quiz", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(userAnswers)
        })
        .then(response => response.json())
        .then(data => {
            resultContainer.classList.remove("hidden");
            riskLevelText.innerText = `Risk Level: ${data.risk_level.toUpperCase()}`;
            recommendationText.innerText = `Recommendation: ${data.recommendation}`;
        })
        .catch(error => console.error("Error submitting quiz:", error));
    });
});