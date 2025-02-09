document.addEventListener("DOMContentLoaded", function () {
    function updateCO2Data() {
        fetch("/api/co2-data")
            .then(response => {
                if (!response.ok) {
                    throw new Error(`HTTP error! Status: ${response.status}`);
                }
                return response.json();
            })
            .then(data => {
                document.getElementById("total-km").textContent = `${data.totaal_km} Km`;
                document.getElementById("total-co2").textContent = `${data.totaal_co2} Ton CO₂`;
                document.getElementById("urgent-km").textContent = `${data.urgent_km} Km`;
                document.getElementById("urgent-co2").textContent = `${data.urgent_co2} Ton CO₂`;
            })
            .catch(error => {
                console.error("Fout bij ophalen CO₂-data:", error);
                document.getElementById("total-km").textContent = "Niet beschikbaar";
                document.getElementById("total-co2").textContent = "Niet beschikbaar";
                document.getElementById("urgent-km").textContent = "Niet beschikbaar";
                document.getElementById("urgent-co2").textContent = "Niet beschikbaar";
            });
    }

    updateCO2Data();
    setInterval(updateCO2Data, 60000); // Elke 60 sec updaten
});