function addNewCard() {
  console.log("addNewCard functie is aangeroepen");

  // Vraag de gebruiker om een titel voor de nieuwe kaart
  const userTitle = prompt("Voer een titel in voor de nieuwe kaart:");
  if (!userTitle) {
    alert("Er is geen titel ingevoerd!");
    return; // Stop als er geen titel is ingevoerd
  }
  console.log(`Titel ingevoerd: ${userTitle}`);

  // Selecteer de container waar de kaarten worden geplaatst
  const mainContent = document.querySelector(".row.g-4");
  if (!mainContent) {
    console.error("De .row.g-4 container is niet gevonden!");
    return;
  }
  console.log(".row.g-4 container gevonden");

  // Maak een nieuwe kolom (Bootstrap layout)
  const newCol = document.createElement("div");
  newCol.className = "col-md-6 col-lg-4";

  // Maak de kaart met Bootstrap-stijlen
  const newCard = `
    <div class="card shadow">
      <div class="card-body text-center">
        <h5 class="card-title">${userTitle}</h5>
        <p class="card-text">Dit is een dynamisch toegevoegde kaart.</p>
        <button class="btn btn-danger w-100 mt-2" onclick="removeCard(this)">Verwijderen</button>
      </div>
    </div>
  `;
  newCol.innerHTML = newCard;
  console.log("Nieuwe kaart gemaakt");

  // Voeg de nieuwe kaart toe vóór de "plus"-knop
  const addCardButton = document.querySelector(".add-card").parentElement;
  if (!addCardButton) {
    console.error("De .add-card knop is niet gevonden!");
    return;
  }
  console.log(".add-card knop gevonden");

  mainContent.insertBefore(newCol, addCardButton);
  console.log("Nieuwe kaart toegevoegd aan de container");
}

function removeCard(button) {
  console.log("removeCard functie is aangeroepen");

  // Verwijder de kaart die bij de verwijderknop hoort
  const card = button.closest(".col-md-6.col-lg-4");
  if (card) {
    card.remove();
    console.log("Kaart is verwijderd");
  } else {
    console.error("De bovenliggende kaart is niet gevonden!");
  }
}


// Validate Bootstrap
// Voeg dit script toe om validatie te activeren
    (function () {
        'use strict'

        // Fetch all the forms we want to apply custom Bootstrap validation styles to
        var forms = document.querySelectorAll('.needs-validation')

        // Loop over them and prevent submission
        Array.prototype.slice.call(forms)
            .forEach(function (form) {
                form.addEventListener('submit', function (event) {
                    if (!form.checkValidity()) {
                        event.preventDefault()
                        event.stopPropagation()
                    }
                    form.classList.add('was-validated')
                }, false)
            })
    })()