// Select elements
const overlays = document.getElementById("student_details_overlay");
const closeOverlayBtn = document.getElementById("close-overlay-btn");

// Hide overlay on close button click
closeOverlayBtn.addEventListener("click", () => {
  overlays.style.display = "none";
});

const ctx = document.getElementById("attendanceChart").getContext("2d");

const data = {
  labels: [
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
  ],
  datasets: [
    {
      label: "Attendance (%)",
      data: [85, 90, 88, 92, 87, 91, 95, 93, 89, 94, 96, 92],
      fill: false,
      borderColor: "#4caf50",
      tension: 0.4,
      pointBackgroundColor: "#4caf50",
      pointBorderColor: "#4caf50",
      pointRadius: 5,
      pointHoverRadius: 7,
    },
  ],
};

const options = {
  responsive: true,
  plugins: {
    legend: {
      display: true,
      labels: {
        color: "#fff", // White legend text
      },
    },
    tooltip: {
      callbacks: {
        label: function (tooltipItem) {
          return tooltipItem.raw + "%";
        },
      },
    },
  },
  scales: {
    x: {
      ticks: {
        color: "#fff", // White X-axis tick labels
      },
      grid: {
        color: "#fff", // White gridlines for X-axis
      },
      title: {
        display: true,
        text: "Month",
        color: "#fff", // White X-axis title
        font: {
          size: 14,
        },
      },
    },
    y: {
      ticks: {
        color: "#fff", // White Y-axis tick labels
        stepSize: 5, // Gap between Y-axis data points
        callback: function (value) {
          return value + "%";
        },
      },
      grid: {
        color: "#fff", // White gridlines for Y-axis
      },
      title: {
        display: true,
        text: "Attendance (%)",
        color: "#fff", // White Y-axis title
        font: {
          size: 14,
        },
      },
      min: 60,
      max: 100,
    },
  },
};

const attendanceChart = new Chart(ctx, {
  type: "line",
  data: data,
  options: options,
});

document.addEventListener("DOMContentLoaded", () => {
  const viewDetailsBtn = document.getElementById("view-details-btn");
  const overlay = document.getElementById("student_view_details_overlay");
  const closeViewDetailsButton = document.getElementById(
    "close-view-details-button"
  );

  // Show overlay
  viewDetailsBtn.addEventListener("click", () => {
    overlay.style.display = "flex";
  });

  // Close overlay
  closeViewDetailsButton.addEventListener("click", () => {
    overlay.style.display = "none";
  });
});

var chartOptions = {
  chart: {
    height: 400,
    type: "line",
    fontFamily: "Helvetica, Arial, sans-serif",
    foreColor: "#fff",
    toolbar: {
      show: false,
    },
  },
  stroke: {
    curve: "smooth",
    width: 2,
  },
  series: [
    {
      name: "Attendence",
      data: [80, 85, 90, 92, 88, 94], // Sample attendance over weeks/months
    },
    {
      name: "Task",
      data: [60, 75, 80, 72, 88, 74],
    },
    {
      name: "Challenge",
      data: [70, 65, 70, 82, 68, 54],
    },
  ],
  title: {
    text: "Student Performance",
    align: "left",
    offsetY: 25,
    offsetX: 5,
    style: {
      fontSize: "14px",
      fontWeight: "bold",
      color: "#fff",
    },
  },
  markers: {
    size: 6,
    strokeWidth: 0,
    hover: {
      size: 9,
    },
  },
  grid: {
    show: true,
    padding: {
      bottom: 0,
    },
  },
  labels: ["week 1", "week 2", "week 3", "week 4", "week 5", "week 6"],
  xaxis: {
    tooltip: {
      enabled: false,
    },
  },
  legend: {
    position: "top",
    horizontalAlign: "right",
    offsetY: -10,
    labels: {
      colors: "#fff",
    },
  },
  grid: {
    borderColor: "#D9DBF3",
    xaxis: {
      lines: {
        show: true,
      },
    },
  },
  tooltip: {
    theme: "dark", // Set the tooltip background to black
    style: {
      fontSize: "12px",
    },
  },
};

var lineChart = new ApexCharts(
  document.querySelector("#line-chart"),
  chartOptions
);
lineChart.render();

var pieChartOptions = {
  chart: {
    type: "pie",
    height: 400,
    fontFamily: "Helvetica, Arial, sans-serif",
  },
  series: [60, 40], // Replace with actual values for boys and girls
  labels: ["Boys", "Girls"], // Labels for the pie slices
  colors: ["#007bff", "#ff66b3"], // Colors for boys and girls
  legend: {
    position: "bottom",
    labels: {
      colors: "#fff", // Text color for legend
    },
  },
  title: {
    text: "Gender Distribution",
    align: "center",
    style: {
      fontSize: "16px",
      fontWeight: "bold",
      color: "#fff",
    },
  },
  tooltip: {
    theme: "dark", // Dark background for tooltip
    y: {
      formatter: function (val) {
        return val + "%"; // Display percentage
      },
    },
  },
};

var genderPieChart = new ApexCharts(
  document.querySelector("#gender-pie-chart"),
  pieChartOptions
);
genderPieChart.render();

document.getElementById('discover-more-btn').addEventListener('click', function (event) {
    event.preventDefault(); // Prevent default link behavior
    document.getElementById('discover-more-container').classList.add('active');
});

document.getElementById('close-btn').addEventListener('click', function () {
    document.getElementById('discover-more-container').classList.remove('active');
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
        document.getElementById("notification-container").style.display = "none";
    });

document
    .getElementById("close-form-btn")
    .addEventListener("click", function () {
        document.getElementById("idea-form-container").style.display = "none";
    });