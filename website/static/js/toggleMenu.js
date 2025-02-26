document.addEventListener("DOMContentLoaded", () => {
    const menuToggle = document.getElementById("menu-toggle");
    const sidebar = document.querySelector(".bg-dark");
    const hamburgerContainer = document.querySelector(".hamburgerPosition");

    // Check schermgrootte bij laden en bij resize
    function checkScreenSize() {
        if (window.innerWidth < 1245) {
            sidebar.style.transform = "translateX(-100%)"; // Verberg sidebar
            menuToggle.checked = false;
        } else {
            sidebar.style.transform = "translateX(0)"; // Toon sidebar
            menuToggle.checked = true;
        }
    }

    checkScreenSize();
    window.addEventListener("resize", checkScreenSize);

    // Toggle menu bij klikken op het hele hamburgerPosition gebied
    hamburgerContainer.addEventListener("click", () => {
        menuToggle.checked = !menuToggle.checked;
        sidebar.style.transform = menuToggle.checked ? "translateX(0)" : "translateX(-100%)";
    });
});