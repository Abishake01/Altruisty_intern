document
  .getElementById("joinClassButton")
  .addEventListener("click", function (event) {
    event.preventDefault(); // Prevent default link behavior
    document.getElementById("overlay").style.display = "block";
    document.getElementById("classDetails").style.display = "block";
  });

document
  .getElementById("closeDivButton")
  .addEventListener("click", function () {
    document.getElementById("overlay").style.display = "none";
    document.getElementById("classDetails").style.display = "none";
  });

document
  .getElementById("closeDivButton")
  .addEventListener("click", function () {
    document.getElementById("overlay").style.display = "none";
    document.getElementById("classDetails").style.display = "none";
  });

document.getElementById("overlay").addEventListener("click", function () {
  document.getElementById("overlay").style.display = "none";
  document.getElementById("classDetails").style.display = "none";
});

document
  .getElementById("submit-idea-btn")
  .addEventListener("click", function (e) {
    e.preventDefault(); // Prevent default anchor behavior

    // Show the new container and background overlay
    document.getElementById("new-container").style.display = "block";
    document.getElementById("overlay").style.display = "block";

    // Optional: Add a smooth transition for the new container
    document.getElementById("new-container").style.transition =
      "opacity 0.3s ease-in-out";
    document.getElementById("new-container").style.opacity = 1;

    // Optional: Hide the original content (or fade it out)
    document.querySelector(".tf-section.action").style.display = "none";
  });

function toggleNotification() {
  const notificationContainer = document.getElementById(
    "notification-container"
  );
  notificationContainer.classList.toggle("visible");
}

document
  .getElementById("close-btn-notification")
  .addEventListener("click", function () {
    document.getElementById("notification-container").console.log();
  });

document
  .getElementById("submit-idea-btn")
  .addEventListener("click", function (e) {
    e.preventDefault();
    document.getElementById("idea-form-container").style.display = "flex";
  });

document
  .getElementById("close-form-btn")
  .addEventListener("click", function () {
    document.getElementById("idea-form-container").style.display = "none";
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
    dropdown.querySelector(".dropdown-menu").style.display = "none";
  }
});

document
  .getElementById("discover-more-btn")
  .addEventListener("click", function (event) {
    event.preventDefault(); // Prevent default link behavior
    document.getElementById("discover-more-container").classList.add("active");
  });

document.getElementById("close-btn").addEventListener("click", function () {
  document.getElementById("discover-more-container").classList.remove("active");
});

const container = document.getElementById("realtimeContainer");
const modal = document.getElementById("customModal");
const overlay = document.getElementById("modalOverlay");
const closeModal = document.getElementById("closeModal");

container.addEventListener("click", async () => {
    url = `http://127.0.0.1:8000/applyrtime/{{id}}`
    try {
        response = await fetch(url, {
            method: "GET"
        })
        if (response.ok) {
            alert('your apllication is submitted')
        }
        else {
            alert('error in application submission')
        }
    }
    catch (err) {
        alert('Internal error')
    }

});

document
    .getElementById("submit-idea-btn")
    .addEventListener("click", function (e) {
        e.preventDefault();
        document.getElementById("idea-form-container").style.display =
            "flex";
    });

document
    .getElementById("close-form-btn")
    .addEventListener("click", function () {
        document.getElementById("idea-form-container").style.display =
            "none";
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

sessionStorage.setItem('user_id', document.getElementById('user_id').value)
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
    url = `http://127.0.0.1:8000/appintern/${id}/${domain}`
    try {
        response = await fetch(url, {
            method: "GET"
        })
        if (response.ok) {
            alert('successfully registered')
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
    window.location.href = 'http://127.0.0.1:8000/idea-submission'
}

      // JavaScript to handle modal opening and closing
    const viewCertificateBtn = document.getElementById("viewCertificateBtn");
    const viewCertificateContainer = document.getElementById(
    "viewCertificateContainer"
    );
    const certificateOverlay = document.getElementById("certificateOverlay");
    const closeCertificateBtn = document.getElementById(
    "viewCertificateclsbtn"
    );

      // Show modal
      viewCertificateBtn.addEventListener("click", (e) => {
        e.preventDefault(); // Prevent default link behavior
    viewCertificateContainer.style.display = "block";
    certificateOverlay.style.display = "block";
      });

      // Close modal
      const closeModal = () => {
        viewCertificateContainer.style.display = "none";
    certificateOverlay.style.display = "none";
      };

    closeCertificateBtn.addEventListener("click", closeModal);
    certificateOverlay.addEventListener("click", closeModal);

    function deleteTask(button) {
        const todoItem = button.parentElement;
    todoItem.remove();
      }

    function addTask() {
        const todoList = document.querySelector(".todo-list");

    // Create a new todo item
    const newTask = document.createElement("div");
    newTask.classList.add("todo-item");
    newTask.innerHTML = `
    <input type="checkbox" />
    <label>New Task</label>
    <button class="delete-btn-todo" onclick="deleteTask(this)">
        <i class="fas fa-trash-alt"></i>
    </button>
          `;

        // Append the new task to the list
        todoList.appendChild(newTask);
      }
   

