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


    //Hamburgermenu
    document.addEventListener('DOMContentLoaded', function () {
        const toggleMenuButton = document.getElementById('toggle-menu');
        const menuItems = document.getElementById('menu-items');
    
        // Functie om menu te toggelen
        function toggleMenu() {
          if (menuItems.style.display === 'none' || menuItems.style.display === '') {
            menuItems.style.display = 'block'; // Toon menu
            toggleMenuButton.innerHTML = '<i class="fas fa-times"></i>'; // Toon kruisje
          } else {
            menuItems.style.display = 'none'; // Verberg menu
            toggleMenuButton.innerHTML = '<i class="fas fa-bars"></i>'; // Toon hamburger
          }
        }
    
        // Event listener voor klikken
        toggleMenuButton.addEventListener('click', function () {
          if (window.innerWidth <= 1820) {
            toggleMenu();
          }
        });
    
        // Bij vensterresizing verberg menu standaard (alleen voor kleine schermen)
        window.addEventListener('resize', function () {
          if (window.innerWidth <= 1820) {
            menuItems.style.display = 'none';
            toggleMenuButton.innerHTML = '<i class="fas fa-bars"></i>'; // Reset naar hamburger
          } else {
            menuItems.style.display = 'block'; // Toon menu standaard
            toggleMenuButton.innerHTML = ''; // Verberg toggle-knop
          }
        });
    
        // Controleer standaard bij laden
        if (window.innerWidth > 1820) {
          menuItems.style.display = 'block'; // Toon menu standaard
          toggleMenuButton.innerHTML = ''; // Verberg toggle-knop
        }
      });

      