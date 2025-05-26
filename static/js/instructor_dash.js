let enrollmentsChart;
let completionChart;

function renderCharts() {
  const textColor = getComputedStyle(document.documentElement).getPropertyValue("--text");

  // Destroy existing charts if they exist
  if (enrollmentsChart) enrollmentsChart.destroy();
  if (completionChart) completionChart.destroy();

  // Enrollments Chart
  enrollmentsChart = new Chart(document.getElementById("enrollmentsChart").getContext("2d"), {
    type: "line",
    data: {
      labels: ["Jan", "Feb", "Mar", "Apr", "May", "Jun"],
      datasets: [{
        label: "Enrollments",
        data: [45, 78, 88, 120, 140, 160],
        borderColor: "#3b82f6",
        backgroundColor: "rgba(59, 130, 246, 0.1)",
        tension: 0.4,
        fill: true,
        pointRadius: 5,
        pointBackgroundColor: "#3b82f6"
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          display: true,
          labels: {
            color: textColor
          }
        }
      },
      scales: {
        x: {
          ticks: { color: textColor },
          grid: { color: "transparent" }
        },
        y: {
          ticks: { color: textColor },
          grid: { color: "rgba(203, 213, 225, 0.1)" }
        }
      }
    }
  });

  // Completion Rate Chart
  completionChart = new Chart(document.getElementById("completionChart").getContext("2d"), {
    type: "bar",
    data: {
      labels: ["Course 1", "Course 2", "Course 3", "Course 4"],
      datasets: [{
        label: "Completion Rate",
        data: [85, 72, 90, 68],
        backgroundColor: ["#3b82f6", "#2563eb", "#1d4ed8", "#1e40af"],
        borderRadius: 6
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          display: false
        }
      },
      scales: {
        x: {
          ticks: { color: textColor },
          grid: { color: "transparent" }
        },
        y: {
          ticks: { color: textColor },
          grid: { color: "rgba(203, 213, 225, 0.1)" }
        }
      }
    }
  });
}

// Run charts on page load
window.addEventListener("DOMContentLoaded", renderCharts);

// Optional: expose renderCharts() globally if needed from theme toggle
window.renderCharts = renderCharts;
