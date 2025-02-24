document.addEventListener("DOMContentLoaded", function () {
  // ================== View Details Overlay ================== //
  const studentOverlay = document.getElementById("student_view_details_overlay");
  const closeOverlayBtn = document.getElementById("close-view-details-button");

  // Get the elements inside the overlay that will be updated
  const studentIdSpan = document.getElementById("student-id"); 
  const studentNameSpan = document.getElementById("student-name");
  const studentProfileImg = document.getElementById("student-profile");

  // Select all "View Details" buttons
  document.querySelectorAll(".view-details-btn").forEach((btn) => {
    btn.addEventListener("click", (event) => {
      event.preventDefault();

      // Get student data from button attributes
      const userId = btn.getAttribute("data-user-id");
      const studentName = btn.getAttribute("data-student-name");
      const profileImage = btn.getAttribute("data-profile");

      // Insert student data into the overlay
      studentIdSpan.textContent = userId;
      studentNameSpan.textContent = studentName;
      studentProfileImg.src = profileImage; 

      // Show the overlay
      studentOverlay.style.display = "flex";
    });
  });

  // Close overlay on button click
  closeOverlayBtn.addEventListener("click", () => {
    studentOverlay.style.display = "none";
  });

  // Close overlay when clicking outside the inner container
  studentOverlay.addEventListener("click", (event) => {
    if (event.target === studentOverlay) {
      studentOverlay.style.display = "none";
    }
  });

  // ================== Attendance Chart (Chart.js) ================== //
  if (document.getElementById("attendanceChart")) {
    const ctx = document.getElementById("attendanceChart").getContext("2d");

    const data = {
      labels: ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
      datasets: [
        {
          label: "Attendance (%)",
          data: [85, 90, 88, 92, 87, 91, 95, 93, 89, 94, 96, 92],
          borderColor: "#4caf50",
          backgroundColor: "rgba(76, 175, 80, 0.2)",
          tension: 0.4,
          pointBackgroundColor: "#4caf50",
          pointRadius: 5,
        },
      ],
    };

    new Chart(ctx, {
      type: "line",
      data: data,
      options: {
        responsive: true,
        plugins: {
          legend: {
            labels: { color: "#fff" },
          },
          tooltip: {
            callbacks: {
              label: (tooltipItem) => `${tooltipItem.raw}%`,
            },
          },
        },
        scales: {
          x: {
            ticks: { color: "#fff" },
            grid: { color: "#fff" },
            title: { display: true, text: "Month", color: "#fff", font: { size: 14 } },
          },
          y: {
            ticks: { color: "#fff", stepSize: 5, callback: (value) => `${value}%` },
            grid: { color: "#fff" },
            title: { display: true, text: "Attendance (%)", color: "#fff", font: { size: 14 } },
            min: 60,
            max: 100,
          },
        },
      },
    });
  }

  // ================== Student Performance Chart (ApexCharts) ================== //
  if (document.querySelector("#line-chart")) {
    var studentChart = new ApexCharts(
      document.querySelector("#line-chart"),
      {
        chart: { height: 400, type: "line", fontFamily: "Arial, sans-serif", foreColor: "#fff" },
        stroke: { curve: "smooth", width: 2 },
        series: [
          { name: "Attendance", data: [80, 85, 90, 92, 88, 94] },
          { name: "Task", data: [60, 75, 80, 72, 88, 74] },
          { name: "Challenge", data: [70, 65, 70, 82, 68, 54] },
        ],
        labels: ["Week 1", "Week 2", "Week 3", "Week 4", "Week 5", "Week 6"],
        title: { text: "Student Performance", align: "left", style: { fontSize: "14px", color: "#fff" } },
        markers: { size: 6, hover: { size: 9 } },
        legend: { position: "top", horizontalAlign: "right", labels: { colors: "#fff" } },
        tooltip: { theme: "dark" },
      }
    );
    studentChart.render();
  }

  // ================== Gender Distribution Pie Chart (ApexCharts) ================== //
  if (document.querySelector("#gender-pie-chart")) {
    var genderPieChart = new ApexCharts(
      document.querySelector("#gender-pie-chart"),
      {
        chart: { type: "pie", height: 400, fontFamily: "Arial, sans-serif" },
        series: [60, 40], // Boys: 60%, Girls: 40%
        labels: ["Boys", "Girls"],
        colors: ["#007bff", "#ff66b3"],
        legend: { position: "bottom", labels: { colors: "#fff" } },
        title: { text: "Gender Distribution", align: "center", style: { fontSize: "16px", color: "#fff" } },
        tooltip: { theme: "dark", y: { formatter: (val) => `${val}%` } },
      }
    );
    genderPieChart.render();
  }

  // ================== Discover More Section ================== //
  const discoverMoreBtn = document.getElementById("discover-more-btn");
  const discoverMoreContainer = document.getElementById("discover-more-container");
  const closeBtn = document.getElementById("close-btns");  // ✅ Corrected ID

  if (discoverMoreBtn && discoverMoreContainer && closeBtn) {
      discoverMoreBtn.addEventListener("click", function (event) {
          event.preventDefault();
          discoverMoreContainer.classList.add("active");
      });

      closeBtn.addEventListener("click", function () {
          discoverMoreContainer.classList.remove("active");
      });
  }

  // ================== Notification Toggle ================== //
  const notificationContainer = document.getElementById("notification-container");
  const closeNotificationBtn = document.getElementById("close-btn-notification");

  if (notificationContainer && closeNotificationBtn) {
    document.getElementById("toggle-notification-btn").addEventListener("click", function () {
      notificationContainer.classList.toggle("visible");
    });

    closeNotificationBtn.addEventListener("click", function () {
      notificationContainer.style.display = "none";
    });
  }

  // ================== Close Idea Form ================== //
  const ideaFormContainer = document.getElementById("idea-form-container");
  const closeFormBtn = document.getElementById("close-form-btn");

  if (ideaFormContainer && closeFormBtn) {
    closeFormBtn.addEventListener("click", function () {
      ideaFormContainer.style.display = "none";
    });
  }
});
