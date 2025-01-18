    document.querySelector('.saveAll').addEventListener('click', function () {
        const nieuweData = [];
        const tableRows = document.querySelectorAll('tbody tr');

        // Loop door alle rijen en verzamel de nieuwe rijen
        tableRows.forEach(row => {
            const cells = row.querySelectorAll('td');
            if (cells.length > 0) {
                const id = cells[0].innerText;
                const product = cells[1].innerText;
                const leverancier = cells[2].innerText;
                const prijs = cells[3].innerText;
                const datum = cells[4].innerText;

                // Voeg alleen rijen toe die daadwerkelijk gegevens hebben
                if (id && product && prijs && datum) {
                    nieuweData.push({
                        id,
                        product,
                        leverancier,
                        prijs,
                        datum,
                    });
                }
            }
        });

        // Log de verzamelde gegevens of stuur ze naar de server
        console.log('Opgeslagen data:', nieuweData);

        // Als je een backend hebt, kun je een POST-verzoek sturen
        // fetch('/api/savePrices', {
        //     method: 'POST',
        //     headers: {
        //         'Content-Type': 'application/json'
        //     },
        //     body: JSON.stringify(nieuweData)
        // }).then(response => {
        //     if (response.ok) {
        //         alert('Gegevens opgeslagen!');
        //     } else {
        //         alert('Fout bij opslaan.');
        //     }
        // }).catch(error => {
        //     console.error('Error:', error);
        // });

        // Voor nu: melding in de console
        alert('Nieuwe prijzen zijn opgeslagen! Bekijk de console voor details.');
    });
