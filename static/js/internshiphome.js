document.addEventListener('DOMContentLoaded', function () {
    user_id = document.getElementById('user_id').innerHTML
    sessionStorage.setItem('user_id',user_id);
    console.log(sessionStorage.getItem('user_id'))
   
});
document.addEventListener("DOMContentLoaded", () => {
    // Get references to the elements
    const closeDivButton = document.getElementById("closeDivButton");
    const ideaFormContainer = document.getElementById("idea-form-container");

    // Add click event listener to the close button
    if (closeDivButton && ideaFormContainer) {
        closeDivButton.addEventListener("click", () => {
            // Hide the container on click
            ideaFormContainer.style.display = "none";
        });
    } else {
        console.error("Close button or idea form container not found.");
    }
});

const container = document.getElementById("realtimeContainer");

// Create the floating card dynamically
const floatingCard = document.createElement("div");
floatingCard.id = "floatingCard";
floatingCard.style.position = "fixed";
floatingCard.style.top = "50%";
floatingCard.style.left = "50%";
floatingCard.style.transform = "translate(-50%, -50%) scale(0.8)";
floatingCard.style.width = "400px";
floatingCard.style.height = "200px";
floatingCard.style.padding = "20px";
floatingCard.style.backgroundColor = "#333";
floatingCard.style.color = "#fff";
floatingCard.style.boxShadow = "0 8px 16px rgba(0, 0, 0, 0.2)";
floatingCard.style.borderRadius = "12px";
floatingCard.style.textAlign = "center";
floatingCard.style.display = "none"; // Initially hidden
floatingCard.style.opacity = "0"; // Start transparent
floatingCard.style.transition = "opacity 0.3s ease, transform 0.3s ease"; // Smooth transition
floatingCard.style.zIndex = "1000";

// Add close button to the card
const closeCardButton = document.createElement("button");
closeCardButton.textContent = "Close";
closeCardButton.style.marginTop = "20px";
closeCardButton.style.padding = "10px 20px";
closeCardButton.style.backgroundColor = "#ddf247";
closeCardButton.style.color = '#000';
closeCardButton.style.border = "none";
closeCardButton.style.borderRadius = "8px";
closeCardButton.style.cursor = "pointer";
closeCardButton.style.fontSize = "16px";

// Add text to the card
const cardText = document.createElement("p");
cardText.textContent = "Your application has been submitted successfully!";
cardText.style.fontSize = "18px";
cardText.style.margin = "0";
cardText.style.padding = "0";

// Append text and button to the card
floatingCard.appendChild(cardText);
floatingCard.appendChild(closeCardButton);

// Append the card to the body
document.body.appendChild(floatingCard);

// Add event listener for close button
closeCardButton.addEventListener("click", () => {
    floatingCard.style.opacity = "0"; // Fade out
    floatingCard.style.transform = "translate(-50%, -50%) scale(0.8)"; // Scale down
    setTimeout(() => {
        floatingCard.style.display = "none"; // Hide after transition
    }, 300);
});

// Event listener for the container click
container.addEventListener("click", async () => {
    const url = `http://127.0.0.1:8000/applyrtime/`;
    try {
        const response = await fetch(url, {
            method: "GET"
        });
        if (response.ok) {
            rstatus = await response.json()
            if (rstatus.status == 'success') {
                floatingCard.style.display = "block";
                setTimeout(() => {
                    floatingCard.style.opacity = "1"; // Fade in
                    floatingCard.style.transform = "translate(-50%, -50%) scale(1)"; // Scale up
                }, 0);
            } else if (rstatus.status == 'already_applied') {
                alert('Already a request is in process')
            }
            
        } else {
            alert('Error in application submission');
        }
    } catch (err) {
        alert('Internal error');
    }
});

submitideabtn = document
    .getElementById("submit-idea-btn")
    submitideabtn.addEventListener("click", function (e) {
        e.preventDefault();
    document.getElementById("idea-form-container").style.display =
    "flex";
    });


    // JavaScript function to update the dropdown text when an item is selected
    function selectCategory(category) {
                        // Get the dropdown button and the text element
                        const dropdownButton = document.querySelector(
    ".dropdown-toggle .dropdown-text"
    );

    // Update the button text to the selected category
    dropdownButton.textContent = category;

    // Close the dropdown after selection (optional)
    document.querySelector(".dropdown-menu").style.display = "none";
                    }

    // Optional: Close the dropdown if you click outside
    document.addEventListener("click", function (event) {
                        const dropdown = document.querySelector(".dropdown-category");
    if (!dropdown.contains(event.target)) {
        dropdown.querySelector(".dropdown-menu").style.display =
        "none";
                        }
                    });



    const badgeContainer = document.getElementById("badgeContainer");
    const badgeModal = document.getElementById("badgeModal");
    const badgeModalOverlay = document.getElementById("badgeModalOverlay");
    const closeBadgeButton = document.getElementById("closeBadgeButton");

    // Function to display the badge modal with dynamic content
    function showBadgeModal(title, content) {
        document.getElementById("badgeModalTitle").textContent = title;
    document.getElementById("badgeModalContent").textContent = content;
    badgeModal.style.display = "block";
    badgeModalOverlay.style.display = "block";
}

badgeContainer.addEventListener("click", () => {
        showBadgeModal("Congratulations!", "You have earned 200 points.");
});

closeBadgeButton.addEventListener("click", () => {
        badgeModal.style.display = "none";
    badgeModalOverlay.style.display = "none";
});

badgeModalOverlay.addEventListener("click", () => {
        badgeModal.style.display = "none";
    badgeModalOverlay.style.display = "none";
});

          
    console.log(sessionStorage.getItem('user_id'))
    document.getElementById('discover-more-btn').addEventListener('click', function (event) {
        event.preventDefault(); // Prevent default link behavior
    document.getElementById('discover-more-container').classList.add('active');
});

    document.getElementById('close-btn').addEventListener('click', function () {
        document.getElementById('discover-more-container').classList.remove('active');
    
});
    async function appintern(domain) {
        id = sessionStorage.getItem('user_id')
            url = `http://127.0.0.1:8000/appintern/${domain}`
    try {
        response = await fetch(url, {
            method: "GET"
        })
        if (response.ok) {
            rstatus = await response.json()
            if (rstatus.status == 'success') {
                alert('successfully registered')
            }
            else if (rstatus.status == 'already_applied') {
                alert('Already a request is in process')
            }
    }
    else {
        alert('error')
    }
            }
    catch (err) {
        alert('error,try again')
    }
        }

    function navigate(stid) {
        sessionStorage.setItem('statement_id', stid)
        window.location.href='http://127.0.0.1:8000/idea-submission'
    }

