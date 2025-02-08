
    // Get Elements
    // Get Elements
    const addMemberButton = document.getElementById("addMemberButton");
    const modal = document.getElementById("addMemberModal");
    const closeModalButton = document.getElementById("closeModalButton");

// Show Modal when the addMemberButton is clicked
addMemberButton.addEventListener("click", (e) => {
        e.preventDefault(); // Prevent default link behavior
    modal.style.display = "flex"; // Show the modal
});

// Close Modal when the close button is clicked
closeModalButton.addEventListener("click", () => {
        modal.style.display = "none"; // Hide the modal
});

// Close Modal if clicked outside the modal content
window.addEventListener("click", (e) => {
    if (e.target === modal) {
        modal.style.display = "none"; // Hide the modal
    }
});

document.addEventListener("DOMContentLoaded", function() {
   user_id = document.getElementById('user_id').innerText
   sessionStorage.setItem('user_id',user_id)
});

    document
    .getElementById("badges-container")
    .addEventListener("click", function () {
        // Show the overlay container
        document.getElementById("badges-overlay-container").style.display =
        "block";
          });

    document
    .getElementById("badges-close-button")
    .addEventListener("click", function () {
        // Hide the overlay container
        document.getElementById("badges-overlay-container").style.display =
        "none";
          });
