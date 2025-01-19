function voegRijToe(button) {
    // Vraag om prijs en datum
    const nieuwePrijs = prompt("Voer de nieuwe prijs in:");
    const nieuweDatum = prompt("Voer de nieuwe datum in (dd-mm-jjjj):");

    // Controleer of beide velden zijn ingevuld
    if (nieuwePrijs && nieuweDatum) {
        // Haal de huidige rij op
        const huidigeRij = button.closest('tr');

        // Maak een nieuwe rij
        const nieuweRij = document.createElement('tr');

        // Voeg cellen toe aan de nieuwe rij
        nieuweRij.innerHTML = `
            <td></td>
            <td></td>
            <td></td>
            <td>€${nieuwePrijs}</td>
            <td>${nieuweDatum}</td>
            <td></td>
        `;

        // Voeg de nieuwe rij toe direct onder de huidige rij
        huidigeRij.parentNode.insertBefore(nieuweRij, huidigeRij.nextSibling);
    } else {
        alert("Vul zowel de prijs als de datum in!");
    }
}