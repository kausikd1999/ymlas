let allLogs = [];


/*
===========================
Render Logs Table
===========================
*/

function renderLogs(logs) {

    const tableBody =
        document.getElementById("logsTableBody");

    tableBody.innerHTML = "";

    logs.forEach(log => {

        let badgeClass = "bg-success";

        if (log.level === "WARNING") {
            badgeClass = "bg-warning text-dark";
        }

        if (log.level === "ERROR") {
            badgeClass = "bg-danger";
        }

        const row = `

            <tr>

                <td>${log.timestamp}</td>

                <td>
                    <span class="badge ${badgeClass}">
                        ${log.level}
                    </span>
                </td>

                <td>${log.service}</td>

                <td>${log.message}</td>

            </tr>

        `;

        tableBody.innerHTML += row;

    });

}


/*
===========================
Load Logs From API
===========================
*/

async function loadLogs() {

    try {

        const response =
            await fetch("/api/logs");

        allLogs =
            await response.json();

        applyFilters();

    }

    catch (error) {

        console.error(
            "Failed to load logs",
            error
        );

    }

}


/*
===========================
Search + Filter Logic
===========================
*/

function applyFilters() {

    const searchInput =
        document
        .getElementById("searchInput")
        .value
        .toLowerCase();

    const levelFilter =
        document
        .getElementById("levelFilter")
        .value;

    const filteredLogs =
        allLogs.filter(log => {

            const matchesSearch =

                log.message
                .toLowerCase()
                .includes(searchInput)

                ||

                log.service
                .toLowerCase()
                .includes(searchInput)

                ||

                log.level
                .toLowerCase()
                .includes(searchInput);

            const matchesLevel =

                levelFilter === "ALL"

                ||

                log.level === levelFilter;

            return matchesSearch &&
                   matchesLevel;

        });

    renderLogs(filteredLogs);

}


/*
===========================
Event Listeners
===========================
*/

document
.getElementById("searchInput")
.addEventListener("keyup", applyFilters);


document
.getElementById("levelFilter")
.addEventListener("change", applyFilters);


document
.getElementById("refreshButton")
.addEventListener("click", loadLogs);


/*
===========================
Initial Load
===========================
*/

loadLogs();
setInterval(loadLogs, 5000);