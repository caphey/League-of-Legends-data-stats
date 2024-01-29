function setStatusMessage(message, isError) {
  // fonction pour changer le message de statut et la classe de l'élément statusMessage
  var statusMessage = document.getElementById("statusMessage"); // récupère l'élément avec l'id statusMessage
  // change le texte et la classe de l'élément
  statusMessage.textContent = message;
  // si isError est true, la classe sera "status-message error", sinon "status-message success"
  statusMessage.className = "status-message " + (isError ? "error" : "success");
}

function checkSummonerStatus() {
  var summonerName = document.getElementById("summonerName").value.trim(); // trim() enlever les espaces avant et après le nom
  if (!summonerName) {
    // vérifie si le nom est vide
    setStatusMessage("Please enter a summoner name.", true);
    return;
  }

  setStatusMessage("Checking status...", false); // affiche le message de chargement en attendant la réponse de l'API

  // fetch() est une fonction qui permet de faire des requêtes HTTP (GET, POST, PUT, DELETE, etc.) en JavaScript (équivalent de cURL en PHP)
  // la fonction retourne une promesse (promise) qui sera résolue (then) ou rejetée (catch) en fonction de la réponse du serveur
  fetch(
    "http://localhost:5000/summoner/status/" + encodeURIComponent(summonerName) // encodeURIComponent() encode les caractères spéciaux pour les URL (ex: espace -> %20)
  )
    .then(function (response) {
      // fonction qui sera exécutée si la promesse est résolue (status code 200) et qui retourne la réponse en JSON
      return response.json();
    })
    .then(function (data) {
      // affiche le message de statut en fonction du status code de la réponse
      if (data.status_code === 200) {
        setStatusMessage(
          "Summoner found with status code: " + data.status_code,
          false // false pour success car le status code est 200 (OK) donc le summoner existe bien dans la base de données de Riot Games
        );
      } else {
        // si le status code est différent de 200, le summoner n'existe pas dans la base de données de Riot Games (ou l'API est indisponible)
        setStatusMessage(
          "Summoner not found with status code: " + data.status_code,
          true
        );
      }
    })
    .catch(function (error) { // fonction qui sera exécutée si la promesse est rejetée (status code 404, 500, etc.) et qui retourne l'erreur
      setStatusMessage("An error occurred: " + error, true);
    });
}
