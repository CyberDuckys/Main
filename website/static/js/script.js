function addNewCard() {
    // Selecteer de container waar de kaarten worden geplaatst
    const mainContent = document.querySelector('.main-content');

    // Maak een nieuw kaart-element
    const newCard = document.createElement('div');
    newCard.className = 'card'; // Voeg de class 'card' toe

    // Voeg inhoud toe aan de kaart, inclusief de verwijderknop
    newCard.innerHTML = `
        <button class="remove-button" onclick="removeCard(this)">X</button>
        <h2>Nieuwe kaart</h2>
        <p>Dit is een dynamisch toegevoegde kaart.</p>
        <button class="button" onclick="alert('Actie op nieuwe kaart')">Actie</button>
    `;

    // Voeg de nieuwe kaart toe vóór de plus-knop
    const addCardButton = document.querySelector('.add-card');
    mainContent.insertBefore(newCard, addCardButton);
}

function removeCard(button) {
    // Verwijder de kaart die bij de verwijderknop hoort
    const card = button.parentElement; // De kaart is de ouder van de knop
    card.remove();
}