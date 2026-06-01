const chartColors = [
    "#4c78a8",
    "#f58518",
    "#e45756",
    "#72b7b2",
    "#54a24b",
    "#eeca3b",
];

const data = window.dashboardData || {};

function buildDoughnut(elementId, dataset, label) {
    const ctx = document.getElementById(elementId);
    if (!ctx) {
        return;
    }
    new Chart(ctx, {
        type: "doughnut",
        data: {
            labels: dataset.labels || [],
            datasets: [
                {
                    label,
                    data: dataset.values || [],
                    backgroundColor: chartColors,
                },
            ],
        },
        options: {
            responsive: true,
            plugins: {
                legend: { position: "bottom" },
            },
        },
    });
}

function buildBar(elementId, dataset, label) {
    const ctx = document.getElementById(elementId);
    if (!ctx) {
        return;
    }
    new Chart(ctx, {
        type: "bar",
        data: {
            labels: dataset.labels || [],
            datasets: [
                {
                    label,
                    data: dataset.values || [],
                    backgroundColor: chartColors,
                },
            ],
        },
        options: {
            responsive: true,
            plugins: {
                legend: { display: false },
            },
        },
    });
}

function buildLine(elementId, dataset, label) {
    const ctx = document.getElementById(elementId);
    if (!ctx) {
        return;
    }
    new Chart(ctx, {
        type: "line",
        data: {
            labels: dataset.labels || [],
            datasets: [
                {
                    label,
                    data: dataset.values || [],
                    borderColor: "#4c78a8",
                    backgroundColor: "rgba(76, 120, 168, 0.15)",
                    tension: 0.3,
                    fill: true,
                },
            ],
        },
        options: {
            responsive: true,
            plugins: {
                legend: { display: false },
            },
        },
    });
}

buildDoughnut("chartLeadsOrigem", data.leads_por_origem || {}, "Leads");
buildBar("chartLeadsMes", data.leads_por_mes || {}, "Leads");
buildDoughnut("chartConversoes", data.conversoes_por_canal || {}, "Conversoes");
buildBar("chartScores", data.scores_distribuicao || {}, "Scores");
buildLine("chartEvolucao", data.evolucao_leads || {}, "Evolucao");
