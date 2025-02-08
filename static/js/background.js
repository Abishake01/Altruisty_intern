document.addEventListener("DOMContentLoaded", () => {
    const items = document.querySelectorAll(".bg-item");
    const container = document.querySelector(".icon-wrapper");

    items.forEach((item) => {
        // Generate random positions
        const x = Math.random() * container.offsetWidth; // Random x-axis
        const y = Math.random() * container.offsetHeight; // Random y-axis

        // Apply positions
        item.style.left = `${x}px`;
        item.style.top = `${y}px`;

        // Add random rotation
        const rotation = Math.random() * 360;
        item.style.transform = `rotate(${rotation}deg)`;
    });
});
