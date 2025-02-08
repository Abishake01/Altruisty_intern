document.addEventListener("DOMContentLoaded", function () {
    // Typing effect for the heading
    const heading = document.querySelector('.overview-heading');
    const headingText = heading.textContent;
    heading.textContent = '';
    
    let i = 0;
    const typingInterval = setInterval(() => {
        if (i < headingText.length) {
            heading.textContent += headingText[i];
            i++;
        } else {
            clearInterval(typingInterval);
            // Show the cards after the heading is typed
            showCards();
        }
    }, 50); // Typing speed in milliseconds

    function showCards() {
        const leftCard = document.getElementById('left-card');
        const rightCard = document.getElementById('right-card');

        // Add a timeout to stagger the card animations
        setTimeout(() => {
            leftCard.classList.add('visible');
        }, 300); // Delay for left card

        setTimeout(() => {
            rightCard.classList.add('visible');
        }, 600); // Delay for right card
    }

    // Button click event
    // document.getElementById('start-now').addEventListener('click', function () {
    //     // Navigate to the SWOT page (replace 'swot.html' with your actual page)
    //     window.location.href = '/list/'; // Example URL for the SWOT page
    // });

    
});