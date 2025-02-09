document.addEventListener("DOMContentLoaded", () => {
    const menuToggle = document.getElementById("menu-toggle");
    const sidebar = document.querySelector(".bg-dark");
    const toggleMenuLabel = document.getElementById("toggle-menu");

    // Zorg ervoor dat de sidebar standaard gesloten is bij kleinere schermen
    function checkScreenSize() {
        if (window.innerWidth < 1245) {
            sidebar.style.transform = "translateX(-100%)"; // Verberg sidebar
            menuToggle.checked = false; // Zorg ervoor dat de checkbox uit staat
        } else {
            sidebar.style.transform = "translateX(0)"; // Toon sidebar bij grotere schermen
            menuToggle.checked = true;
        }
    }

    // Roep de functie aan bij paginalading en wanneer het venster wordt aangepast
    checkScreenSize();
    window.addEventListener("resize", checkScreenSize);

    // Toggle menu met klik
    toggleMenuLabel.addEventListener("click", () => {
        if (menuToggle.checked) {
            sidebar.style.transform = "translateX(-100%)"; // Sluiten
            menuToggle.checked = false;
        } else {
            sidebar.style.transform = "translateX(0)"; // Openen
            menuToggle.checked = true;
        }
    });
});

  document.addEventListener("DOMContentLoaded", () => {
    // Get elements
    const menuToggle = document.getElementById("menu-toggle");
    const toggleMenuLabel = document.getElementById("toggle-menu");

    // Event listener for toggle
    toggleMenuLabel.addEventListener("click", () => {
      // Toggle the checked state of the checkbox
      menuToggle.checked = !menuToggle.checked;
    });
  });