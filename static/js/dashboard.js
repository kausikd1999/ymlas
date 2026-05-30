const cpuElement = document.getElementById("cpu");
const memoryElement = document.getElementById("memory");
const diskElement = document.getElementById("disk");

function setMetricColor(element, value) {

    if (value >= 80) {
        element.style.color = "#ef4444"; // Red
    }
    else if (value >= 60) {
        element.style.color = "#f59e0b"; // Orange
    }
    else {
        element.style.color = "#22c55e"; // Green
    }

}

const ctx = document.getElementById("cpuChart");

const cpuChart = new Chart(ctx, {

    type: "line",

    data: {

        labels: [],

        datasets: [

            {
                label: "CPU Usage %",
                data: [],
                borderColor: "#38bdf8",
                backgroundColor: "rgba(56, 189, 248, 0.15)",
                fill: true,
                tension: 0.4,
                borderWidth: 3,
                pointRadius: 4
            }

        ]

    },

    options: {

        responsive: true,

        plugins: {

            legend: {
                labels: {
                    color: "#ffffff"
                }
            }

        },

        scales: {

            x: {

                ticks: {
                    color: "#94a3b8"
                },

                grid: {
                    color: "rgba(255,255,255,0.05)"
                }

            },

            y: {

                min: 0,
                max: 100,

                ticks: {
                    color: "#94a3b8"
                },

                grid: {
                    color: "rgba(255,255,255,0.05)"
                }

            }

        }

    }

});

async function loadMetrics() {

    try {

        const response = await fetch("/api/system");

        const data = await response.json();

        cpuElement.innerText =
            data.cpu.toFixed(1) + "%";

        memoryElement.innerText =
            data.memory.toFixed(1) + "%";

        diskElement.innerText =
            data.disk.toFixed(1) + "%";

        setMetricColor(cpuElement, data.cpu);
        setMetricColor(memoryElement, data.memory);
        setMetricColor(diskElement, data.disk);

        const currentTime =
            new Date().toLocaleTimeString();

        cpuChart.data.labels.push(currentTime);

        cpuChart.data.datasets[0].data.push(data.cpu);

        if (cpuChart.data.labels.length > 20) {

            cpuChart.data.labels.shift();

            cpuChart.data.datasets[0].data.shift();

        }

        cpuChart.update();

    }

    catch (error) {

        console.error(
            "Failed to fetch metrics:",
            error
        );

    }

}

loadMetrics();

setInterval(loadMetrics, 2000);