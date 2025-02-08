let questions = [];
let currentQuestion = 0;
let correctAnswers = 0;
let selectedAnswer = null;


fetch('/api/questions/')
    .then(response => response.json())
    .then(data => {
        questions = data.questions;
        updateQuestion();
    })
    .catch(error => console.error('Error fetching questions:', error));

function updateQuestion() {
    if (questions.length === 0) return;

    const question = questions[currentQuestion];
    document.getElementById('questionNumber').textContent = `Question ${currentQuestion + 1}/${questions.length}`;
    document.getElementById('progressFill').style.width = `${((currentQuestion + 1) / questions.length) * 100}%`;
    document.getElementById('question').textContent = question.question;

    const options = document.querySelectorAll('.option');
    options.forEach((option, index) => {
        option.querySelector('.option-text').textContent = question.options[index].text;
        option.className = 'option';
        option.disabled = false;
        option.querySelector('.percentage-bar').style.display = 'none';

        const existingDescription = option.querySelector('.option-description');
        if (existingDescription) {
            existingDescription.remove();
        }
    });

    document.getElementById('nextButton').style.display = 'none';
}

async function showResults() {
    
    document.querySelector('.quiz-card').style.display = 'none';
    document.getElementById('results').style.display = 'block';

    // Debug: Check if correctAnswers and questions are defined
    console.log('Correct Answers:', correctAnswers);
    console.log('Questions:', questions);

    const efficiencyScore = (correctAnswers / questions.length) * 100;
    console.log('Efficiency Score:', efficiencyScore); // Debugging the calculated score
    document.getElementById('score').textContent = `Your Efficiency: ${efficiencyScore.toFixed(2)}%`;
    const category = sessionStorage.getItem("costcuttingcategory");
    console.log('Category:', category); // Debugging category value

    // Check if category is set properly
    if (!category) {
        console.error("Category is not set in sessionStorage!");
    }

    const data = new FormData();
    data.append('score', efficiencyScore);
    data.append('category', category);
    data.append('game', 'cost_cutting');
    const url = `http://127.0.0.1:8000/api/updatescorecost/`
    try {
        // Debug: Check if FormData contains the correct values
        console.log('FormData:', data.get('score'), data.get('category'), data.get('game'));

        response = await fetch(url, {
            method: 'POST',
            body: data
        });

        // Check if the response is successful
        if (response.ok) {
            console.log('Success:', await response.json());
        } else {
            console.error('Manual error:', await response.text());
        }
    } catch (error) {
        console.error('Technical error:', error); // Log the actual error to understand the issue
    }

}


function selectAnswer(index) {
    if (selectedAnswer !== null) return;

    selectedAnswer = index;
    const question = questions[currentQuestion];
    const options = document.querySelectorAll('.option');

    options.forEach((option, i) => {
        option.disabled = true;
        option.classList.add('disabled');

        const percentageBar = option.querySelector('.percentage-bar');
        const percentageFill = percentageBar.querySelector('.percentage-fill');
        const percentageText = percentageBar.querySelector('.percentage-text');

        percentageBar.style.display = 'block';
        percentageFill.style.width = `${question.options[i].percentage}%`;
        percentageText.textContent = `${question.options[i].percentage}%`;

        if (question.correct_answer === question.options[i].text) {
            option.classList.add('correct');
        }
        if (i === index && question.correct_answer !== question.options[i].text) {
            option.classList.add('wrong');
        }

        const descriptionText = question.options[i].description || 'No description available.';
        const descriptionDiv = document.createElement('div');
        descriptionDiv.classList.add('option-description');
        descriptionDiv.textContent = `Justification:--> ${descriptionText}`;

        option.appendChild(descriptionDiv);
    });

    if (question.correct_answer === question.options[index].text) {
        correctAnswers++;
    }

    document.getElementById('nextButton').style.display = 'flex';
}

function nextQuestion() {
    selectedAnswer = null;
    currentQuestion++;

    if (currentQuestion >= questions.length) {
        showResults();
    } else {
        updateQuestion();
    }
}

function restartQuiz() {
    currentQuestion = 0;
    correctAnswers = 0;
    selectedAnswer = null;
    document.querySelector('.quiz-card').style.display = 'block';
    document.getElementById('results').style.display = 'none';
    updateQuestion();
}

document.querySelectorAll('.option').forEach((option, index) => {
    option.addEventListener('click', () => selectAnswer(index));
});

document.getElementById('nextButton').addEventListener('click', nextQuestion);
document.getElementById('restartButton').addEventListener('click', restartQuiz);
