function voegRijToe(button) {
    // Vraag om prijs en datum
    const nieuwePrijs = prompt("Voer de nieuwe prijs in:");
    const nieuweDatum = prompt("Voer de nieuwe datum in (dd-mm-jjjj):");

    // Controleer of beide velden zijn ingevuld
    if (nieuwePrijs && nieuweDatum) {
        // Haal de huidige rij op
        const huidigeRij = button.parentElement.parentElement;

        // Maak een nieuwe rij
        const nieuweRij = document.createElement('tr');

        // Voeg cellen toe met bestaande data
        nieuweRij.innerHTML = `
            <td></td>
            <td></td>
            <td></td>
            <td>€${nieuwePrijs}</td>
            <td>${nieuweDatum}</td>
            <td><button class="nieuwePrijs button" onclick="voegRijToe(this)">Nieuwe Prijs toevoegen</button></td>
        `;

        // Voeg de nieuwe rij toe onder de huidige
        huidigeRij.parentNode.insertBefore(nieuweRij, huidigeRij.nextSibling);
    } else {
        alert("Vul zowel de prijs als de datum in!");
    }
}