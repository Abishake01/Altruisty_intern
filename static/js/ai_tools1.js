
    function showMoreProjects() {
        // Select all hidden project items and make them visible
        document
            .querySelectorAll(".hidden-project")
            .forEach(function (item) {
                item.style.display = "block";
            });
    // Hide the "See All" link after expanding
    document.querySelector(".see_more").style.display = "none";
                }


    function showMoreProjects() {
        // Select all hidden project items and make them visible
        document
            .querySelectorAll(".hidden-project")
            .forEach(function (item) {
                item.style.display = "block";
            });
    // Hide the "See All" link after expanding
    document.querySelector(".see_more").style.display = "none";
    }

    function openModal() {
        document.getElementById("createProjectModal").style.display = "flex";
    }

    function closeModal() {
        document.getElementById("createProjectModal").style.display = "none";
    }

    // Attach to your button
    document.querySelector(".create-project-btn").onclick = openModal;

    let scrollPosition = 0;
    const scrollAmount = 200; // Amount to scroll each time

    function scrollRight() {
        const container = document.getElementById("scrollableContainer");
    const maxScroll = container.scrollWidth - container.clientWidth;

    if (scrollPosition < maxScroll) {
        scrollPosition += scrollAmount;
            if (scrollPosition > maxScroll) scrollPosition = maxScroll; // Prevent over-scrolling
    container.style.transform = `translateX(-${scrollPosition}px)`;
        }

        // Show/hide arrows based on position
        document.getElementById("leftArrow").style.display = scrollPosition > 0 ? "block" : "none";
    document.getElementById("rightArrow").style.display = scrollPosition < maxScroll ? "block" : "none";
    }

    function scrollLeftTools() {
        const container = document.getElementById("scrollableContainer");

        if (scrollPosition > 0) {
        scrollPosition -= scrollAmount;
    console.log("scrollLeft");
    if (scrollPosition < 0) scrollPosition = 0; // Prevent negative scrolling
    container.style.transform = `translateX(-${scrollPosition}px)`;
        }

        // Show/hide arrows based on position
        document.getElementById("leftArrow").style.display = scrollPosition > 0 ? "block" : "none";
    document.getElementById("rightArrow").style.display = scrollPosition < container.scrollWidth - container.clientWidth ? "block" : "none";
    }

    // Initialize arrow visibility on page load
    document.addEventListener("DOMContentLoaded", function () {
        document.getElementById("leftArrow").style.display = "none"; // Hide left arrow initially
    });

    //recent

    let recentScrollPosition = 0;
    const recentScrollAmount = 200; // Adjust this value as needed

    function scrollRightRecent() {
        const container = document.getElementById("recentScrollableContainer");
    const maxScroll = container.scrollWidth - container.clientWidth;

    if (recentScrollPosition < maxScroll) {
        recentScrollPosition += recentScrollAmount;
            if (recentScrollPosition > maxScroll) recentScrollPosition = maxScroll; // Prevent over-scrolling
    container.style.transform = `translateX(-${recentScrollPosition}px)`;
        }

        // Show/hide arrows based on position
        document.getElementById("recentLeftArrow").style.display = recentScrollPosition > 0 ? "block" : "none";
    document.getElementById("recentRightArrow").style.display = recentScrollPosition < maxScroll ? "block" : "none";
    }

    function scrollLeftRecent() {
        const container = document.getElementById("recentScrollableContainer");

        if (recentScrollPosition > 0) {
        recentScrollPosition -= recentScrollAmount;
    if (recentScrollPosition < 0) recentScrollPosition = 0; // Prevent negative scrolling
    container.style.transform = `translateX(-${recentScrollPosition}px)`;
        }

        // Show/hide arrows based on position
        document.getElementById("recentLeftArrow").style.display = recentScrollPosition > 0 ? "block" : "none";
    document.getElementById("recentRightArrow").style.display = recentScrollPosition < container.scrollWidth - container.clientWidth ? "block" : "none";
    }


    // Function to open the modal
    function openCreateProjectModal() {
        document.getElementById("createProjectModal").style.display = "flex";
    }

    // Function to close the modal
    function closeModal() {
        document.getElementById("createProjectModal").style.display = "none";
    }

