document.addEventListener("DOMContentLoaded", () => {
    // Verkrijg elementen
    const menuToggle = document.getElementById("menu-toggle");
    const sidebar = document.querySelector(".bg-dark");
    const toggleMenuLabel = document.getElementById("toggle-menu");

    // Event listener voor toggle
    toggleMenuLabel.addEventListener("click", () => {
        const isChecked = menuToggle.checked;
        if (isChecked) {
            // Menu is open, dus sluit het
            sidebar.style.transform = "translateX(-100%)";
            menuToggle.checked = false;
        } else {
            // Menu is gesloten, dus open het
            sidebar.style.transform = "translateX(0)";
            menuToggle.checked = true;
        }
    });

    // Herstel het menu wanneer het scherm groter wordt
    window.addEventListener("resize", () => {
        if (window.innerWidth > 768) { // Aanpassen op basis van jouw breakpoint
            sidebar.style.transform = "translateX(0)"; // Zet het menu terug op zichtbaar
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