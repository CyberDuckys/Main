      //   Update datum en tijd
function updateTime() {
    let now = new Date();
    
    // Tijd ophalen in HH:MM formaat
    let hours = now.getHours().toString().padStart(2, '0');
    let minutes = now.getMinutes().toString().padStart(2, '0');
    document.getElementById("clock").innerText = `${hours}:${minutes}`;
    
    // Datum ophalen in DD-MM-YYYY formaat
    let day = now.toLocaleDateString('nl-NL', { weekday: 'long' });
    let date = now.toLocaleDateString('nl-NL');
    document.getElementById("date").innerHTML = `${day}<br/>${date}`;
}

// Update de tijd en datum elke seconde
setInterval(updateTime, 1000);

// Voer de functie direct uit bij het laden van de pagina
updateTime();