
            // Fund raised data for each month (in rupees)
    const monthlyFunds = [
    500000, 1000000, 1500000, 1200000, 1800000, 2200000, 2500000,
    3000000, 3500000, 4000000, 4500000, 5000000,
    ]; // Example funds raised per month
    const months = [
    "Jan",
    "Feb",
    "Mar",
    "Apr",
    "May",
    "Jun",
    "Jul",
    "Aug",
    "Sep",
    "Oct",
    "Nov",
    "Dec",
    ]; // Months of the year

    // Create a line chart using Chart.js
    const ctx = document
    .getElementById("fundsRaisedChart")
    .getContext("2d");
    const fundsRaisedChart = new Chart(ctx, {
        type: "line", // Line chart type
    data: {
        labels: months, // X-axis labels (months)
    datasets: [
    {
        label: "Funds Raised (₹)", // Label for the dataset
    data: monthlyFunds, // Data for funds raised each month
    borderColor: "#ddf247", // Line color
    backgroundColor: "#def24767", // Line fill color
    fill: true, // Fill under the line
    tension: 0.4, // Smooth the line
    pointRadius: 5, // Size of the points
    pointBackgroundColor: "#ddf247", // Color of points
                        },
    ],
                },
    options: {
        responsive: true,
    scales: {
        y: {
        beginAtZero: true, // Start Y-axis from zero
    title: {
        display: true,
    text: "Funds Raised (₹)", // Y-axis title (Rupees)
                            },
    ticks: {
        callback: function (value) {
                                    return "₹" + value.toLocaleString(); // Format ticks to show rupees symbol and commas
                                },
                            },
                        },
    x: {
        title: {
        display: true,
    text: "Months", // X-axis title
                            },
                        },
                    },
    plugins: {
        legend: {
        display: false, // Hide the legend if not needed
                        },
                    },
                },
            });

    const number = document.getElementById("number");
    let counter = 0;
    const goal = 65; // Example: 65% goal reached

            setInterval(() => {
                if (counter === goal) {
        clearInterval();
                } else {
        counter += 1;
    number.innerHTML = counter + "%";
                }
            }, 30);


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


    document
    .getElementById("discover-more-btn")
    .addEventListener("click", function (event) {
        event.preventDefault(); // Prevent default link behavior
    document
    .getElementById("discover-more-container")
    .classList.add("active");
        });

    document
    .getElementById("close-btn")
    .addEventListener("click", function () {
        document
            .getElementById("discover-more-container")
            .classList.remove("active");
        });

    const badgeContainer =
    document.getElementById("badgeContainer");
    const badgeModal = document.getElementById("badgeModal");
    const badgeModalOverlay =
    document.getElementById("badgeModalOverlay");
    const closeBadgeButton =
    document.getElementById("closeBadgeButton");

    // Function to display the badge modal with dynamic content
    function showBadgeModal(title, content) {
        document.getElementById("badgeModalTitle").textContent =
        title;
    document.getElementById("badgeModalContent").textContent =
    content;
    badgeModal.style.display = "block";
    badgeModalOverlay.style.display = "block";
    }

    badgeContainer.addEventListener("click", () => {
        showBadgeModal(
            "Congratulations!",
            "You have earned 200 points."
        );
    });

    closeBadgeButton.addEventListener("click", () => {
        badgeModal.style.display = "none";
    badgeModalOverlay.style.display = "none";
    });

    badgeModalOverlay.addEventListener("click", () => {
        badgeModal.style.display = "none";
    badgeModalOverlay.style.display = "none";
    });
