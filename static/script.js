document.addEventListener("DOMContentLoaded", function () {
  // Graphique des 3 derniers matchs
  const statsThreeMatch = JSON.parse(
    document.getElementById("stats_three_match_data").textContent
  );
  const ctx1 = document
    .getElementById("lastThreeMatchesChart")
    .getContext("2d");
  new Chart(ctx1, {
    type: "bar",
    data: {
      labels: statsThreeMatch.map((match) => match.champion_name),
      datasets: [
        {
          label: "KDA",
          data: statsThreeMatch.map((match) => match.kda),
          backgroundColor: "rgba(75, 192, 192, 0.6)",
          borderColor: "rgba(75, 192, 192, 1)",
          borderWidth: 1,
        },
        {
          label: "Dégâts (K)",
          data: statsThreeMatch.map(
            (match) => match.total_damage_dealt_to_champions
          ),
          backgroundColor: "rgba(255, 99, 132, 0.6)",
          borderColor: "rgba(255, 99, 132, 1)",
          borderWidth: 1,
        },
        {
          label: "Or (K)",
          data: statsThreeMatch.map((match) => match.gold_earned),
          backgroundColor: "rgba(255, 206, 86, 0.6)",
          borderColor: "rgba(255, 206, 86, 1)",
          borderWidth: 1,
        },
      ],
    },
    options: {
      responsive: true,
      scales: {
        y: {
          beginAtZero: true,
        },
      },
    },
  });

  // Graphique victoires/défaites
  const winLossData = JSON.parse(
    document.getElementById("win_loss_data").textContent
  );
  const ctx2 = document.getElementById("winLossChart").getContext("2d");
  new Chart(ctx2, {
    type: "pie",
    data: {
      labels: ["Victoires", "Défaites"],
      datasets: [
        {
          data: [winLossData.wins, winLossData.losses],
          backgroundColor: [
            "rgba(75, 192, 192, 0.6)",
            "rgba(255, 99, 132, 0.6)",
          ],
          borderColor: ["rgba(75, 192, 192, 1)", "rgba(255, 99, 132, 1)"],
          borderWidth: 1,
        },
      ],
    },
    options: {
      responsive: true,
    },
  });

  // Graphique CS/min
  const csPerMinData = JSON.parse(
    document.getElementById("cs_per_min_data").textContent
  );
  const ctx3 = document.getElementById("csPerMinChart").getContext("2d");
  new Chart(ctx3, {
    type: "line",
    data: {
      labels: Array.from(
        { length: csPerMinData.cs_per_min.length },
        (_, i) => i + 1
      ),
      datasets: [
        {
          label: "CS/min",
          data: csPerMinData.cs_per_min,
          borderColor: "rgba(75, 192, 192, 1)",
          borderWidth: 2,
          fill: false,
        },
      ],
    },
    options: {
      responsive: true,
      scales: {
        y: {
          beginAtZero: true,
        },
      },
    },
  });
});
