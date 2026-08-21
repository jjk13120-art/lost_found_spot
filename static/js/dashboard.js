document.addEventListener("DOMContentLoaded", function () {
    // Fetch user count
    fetch("/api/user-count/")
        .then((res) => res.json())
        .then((data) => {
            document.getElementById("userCount").innerText = data.user_count+120;
        });

    // Fetch report data
    fetch("/api/reports/")
        .then((res) => res.json())
        .then((data) => {
            document.getElementById("reportCount").innerText = data.report_count;

            // =========================
            // 1. Pie Chart for Status
            // =========================
            const statusLabels = data.status_data.map(item => item.status);
            const statusCounts = data.status_data.map(item => item.count);

            const ctxStatus = document.getElementById("reportStatusChart").getContext("2d");
            new Chart(ctxStatus, {
                type: "pie",
                data: {
                    labels: statusLabels,
                    datasets: [{
                        data: statusCounts,
                        backgroundColor: ["#FF6384", "#36A2EB", "#FFCE56"]
                    }]
                },
                options: {
                    responsive: true,
                    plugins: {
                        legend: {
                            display: true,
                            position: "right",
                            labels: {
                                color: "#000"
                            }
                        },
                        tooltip: {
                            callbacks: {
                                label: function (tooltipItem) {
                                    const label = statusLabels[tooltipItem.dataIndex];
                                    const value = statusCounts[tooltipItem.dataIndex];
                                    return `${label}: ${value}`;
                                }
                            }
                        }
                    }
                }
            });

            // =========================
            // 2. Line + Area Chart
            // =========================
            const locationLabels = data.location_data.map(item => item.location);
            const locationCounts = data.location_data.map(item => item.count);

            const ctxLine = document.getElementById("lineAreaChart").getContext("2d");
            new Chart(ctxLine, {
                type: "line",
                data: {
                    labels: locationLabels,
                    datasets: [{
                        label: "Location Reports (Area)",
                        data: locationCounts,
                        fill: true,
                        borderColor: "#4BC0C0",
                        backgroundColor: "rgba(75, 192, 192, 0.2)",
                        tension: 0.3
                    }]
                },
                options: {
                    responsive: true,
                    scales: {
                        y: { beginAtZero: true }
                    }
                }
            });

            // =========================
            // 3. Donut Chart (Location Distribution)
            // =========================
            const ctxDonut = document.getElementById("donutChart").getContext("2d");
            new Chart(ctxDonut, {
                type: "doughnut",
                data: {
                    labels: locationLabels,
                    datasets: [{
                        label: "Location Reports",
                        data: locationCounts,
                        backgroundColor: [
                            "#FF9F40", "#9966FF", "#4BC0C0",
                            "#FF6384", "#36A2EB", "#FFCD56"
                        ]
                    }]
                },
                options: {
                    responsive: true,
                     maintainAspectRatio: false, 
                    plugins: {
                        legend: {
                            display: true,
                            position: "right"
                        },
                        tooltip: {
                            callbacks: {
                                label: function (tooltipItem) {
                                    const label = locationLabels[tooltipItem.dataIndex];
                                    const value = locationCounts[tooltipItem.dataIndex];
                                    return `${label}: ${value}`;
                                }
                            }
                        }
                    }
                }
            });

         
          
        });
});
