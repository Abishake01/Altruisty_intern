// Questions array
const questions = [
    "Did you usually submit your projects before the deadline in college?",
    "Do you regularly keep up with new trends and innovations in your field?",
    "Do you often find it difficult to focus on one task for long periods?",
    "Have you ever missed important deadlines for assignments or projects?",
    "Do you often procrastinate when starting new tasks?",
    "Do you feel confident about pitching your ideas to others?",
    "Do you have experience managing your personal finances or budgets?",
    "Do you often feel anxious about taking risks?",
    "Have you ever struggled to complete a project due to lack of motivation?",
    "Do you have access to resources like workshops or startup programs to help you?",
    "Do you see any technological advancements that could benefit your business?",
    "Are there gaps in the market that your product or service can fill?",
    "Is your business idea aligned with current customer trends or preferences?",
    "Do you have access to potential mentors or advisors who can help you develop your business?"
];
// Initialize the question index and circle number
let currentQuestionIndex = 0;
let currentCircleNumber = 1;
let object = { "strength": s, "weakness": w, "opportunities": o, "threat": t }
let s=[];
let w=[];
let o=[];
let t=[];

// Function to handle answering the questions
function answerQuestion(answer) {
    if (currentQuestionIndex == 0) {
        if (answer == "Yes") {
            s.push('Time management and Discipline')
        }
        else {
            w.push('Struggle with deadlines')
        }
    }
    else if (currentQuestionIndex == 1) {
        if (answer == "Yes") {
            s.push('Adaptable and keen on continous learning ')
        }
        else {
            w.push('gap in staying updated with industry changes')
        }
    }
    else if (currentQuestionIndex == 2) {
        if (answer == "Yes") {
            w.push('Issues with focus and concentration')
        }
        else {
            s.push('focused and concentrated')
        }
    }
    else if (currentQuestionIndex == 3) {
        if (answer == "Yes") {
            w.push('Struggle with deadlines ')
        }
        else {
            s.push('Time management and Discipline')
        }
    }
    else if (currentQuestionIndex == 4) {
        if (answer == "Yes") {
            w.push('Struggle with Procastination ')
        }
        else {
            s.push('Productivity')
        }
    }
    else if (currentQuestionIndex == 5) {
        if (answer == "Yes") {
            s.push('Strong communication skills ')
        }
        else {
            w.push('lack of communication skills')
        }
    }
    else if (currentQuestionIndex == 6) {
        if (answer == "Yes") {
            s.push('Financial Management')
        }
        else {
            w.push('Financial Management')
        }
    }
    else if (currentQuestionIndex == 7) {
        if (answer == "Yes") {
            w.push('hesitation to take risk ')
        }
        else {
            s.push('ready to take risk')
        }
    }
    else if (currentQuestionIndex == 8) {
        if (answer == "Yes") {
            w.push('Low motivation ')
        }
        else {
            s.push('Highly motivated')
        }
    }
    else if (currentQuestionIndex == 9) {
        if (answer == "Yes") {
            o.push('Access to startup resource')
        }
        else {
            t.push('Lack of resource')
        }
    }
    else if (currentQuestionIndex == 10) {
        if (answer == "Yes") {
            o.push('Utilize new technology')
        }
        else {
            t.push('Missing out on tech innovation')
        }
    }
    else if (currentQuestionIndex == 11) {
        if (answer == "Yes") {
            o.push('Gap in market that will be filled with your services')
        }
        else {
            t.push('heavy competition may exist')
        }
    }
    else if (currentQuestionIndex == 12) {
        if (answer == "Yes") {
            o.push('Aligned with trend')
        }
        else {
            t.push('Out of sync with trend')
        }
    }
    else if (currentQuestionIndex == 13) {
        if (answer == "Yes") {
            o.push('Access to mentorship')
        }
        else {
            t.push('Lack of mentorship')
        }
    }
    console.log("You answered: " + answer);
  

    // Move to the next question
    currentQuestionIndex++;

    // Increment the circle number
    currentCircleNumber++;

    // Check if there are more questions
    if (currentQuestionIndex < questions.length) {
        // Update the question text with typing effect
        typeQuestion(questions[currentQuestionIndex]);

        // Update the number in the circle
        document.getElementById("circle-number").textContent = currentCircleNumber;

        // Add the transition effect for the number coming from below
        document.getElementById("circle-number").classList.add('animate-from-bottom');
        setTimeout(() => {
            document.getElementById("circle-number").classList.remove('animate-from-bottom');
        }, 1000);

    } else {
        // End of questions
        document.getElementById("question-text").textContent = "Thank you for completing the questions!";

        
        // Show the "Add Points" button
        document.getElementById("add-points-button").style.display = 'block';
    }
}

// Function to create typing effect for the question
function typeQuestion(question) {
    let i = 0;
    const questionElement = document.getElementById("question-text");
    questionElement.textContent = ''; // Clear previous question

    const typingInterval = setInterval(() => {
        if (i < question.length) {
            questionElement.textContent += question[i];
            i++;
        } else {
            clearInterval(typingInterval); // Clear interval when the question is done typing
        }
    }, 10); // Speed of typing (50ms per character)
}

// Function to navigate to the points page when "Add Points" button is clicked
function goToPointsPage() {
    window.location.href = 'points/';
; // Assuming the points page is located at /points
}

// Event listeners for the yes and no buttons
document.getElementById("yes-button").addEventListener("click", () => answerQuestion('Yes'));
document.getElementById("no-button").addEventListener("click", () => answerQuestion('No'));

// Ensure typing effect starts after the page loads
window.onload = function() {
    typeQuestion(questions[currentQuestionIndex]); // Start with the first question
    document.getElementById("circle-number").textContent = currentCircleNumber;
};