window.addEventListener("load", function () {
    document.querySelector(".preload-container").style.display = "none";
});

function showSection(sectionId) {
    const sections = document.querySelectorAll(".tab-content");
    sections.forEach((section) => {
        section.classList.add("hidden");
        section.classList.remove("active");
    });

    const activeSection = document.getElementById(sectionId);
    activeSection.classList.remove("hidden");
    activeSection.classList.add("active");
}