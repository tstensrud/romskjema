document.addEventListener('DOMContentLoaded', function () {
    const hoverElements = document.querySelectorAll('.notes-popup');
    const minLength = 25;
    const maxLength = 100;

    hoverElements.forEach(element => {
        element.addEventListener('mouseover', function () {
            const popupText = element.getAttribute('data-popup').replace(/\\n/g, '<br>');
            if (popupText.length > minLength) {
                const popup = document.createElement('div');
                popup.className = 'popup';
                popup.innerHTML = popupText;
                document.body.appendChild(popup);
                const rect = element.getBoundingClientRect();
                popup.style.top = `${rect.bottom + window.scrollY}px`;
                if (popupText.length > maxLength) {
                    popup.style.left = `${rect.left + window.scrollX - 500}px`;
                }
                else {
                    popup.style.left = `${rect.left + window.scrollX - 200}px`;
                }
            }
        });
        element.addEventListener('mouseout', function () {
            const popup = document.querySelector('.popup');
            if (popup) {
                document.body.removeChild(popup);
            }
        });
    });
});

document.addEventListener('DOMContentLoaded', function () {
    const hoverElements = document.querySelectorAll('.hover-popup');
    const minLength = 25;

    hoverElements.forEach(element => {
        element.addEventListener('mouseover', function () {
            const popupText = element.getAttribute('data-popup').replace(/\\n/g, '<br>');
            if (popupText.length > minLength) {
                const popup = document.createElement('div');
                popup.className = 'popup';
                popup.innerHTML = popupText;
                document.body.appendChild(popup);
                const rect = element.getBoundingClientRect();
                popup.style.top = `${rect.bottom + window.scrollY}px`;
                popup.style.left = `${rect.left + window.scrollX}px`;
            }
        });
        element.addEventListener('mouseout', function () {
            const popup = document.querySelector('.popup');
            if (popup) {
                document.body.removeChild(popup);
            }
        });
    });
});


// Check on inputfields that they only contain numbers
document.addEventListener('DOMContentLoaded', function() {
    var form = document.getElementById('new_room');
    var inputFieldAirPp = document.getElementById('air_per_person');
    var inputFieldAirE = document.getElementById('air_emission');
    var inputFieldAIrPro = document.getElementById('air_process')
    var inputFieldAirMin = document.getElementById('air_minimum')

    form.addEventListener('submit', function(event) {
        
        var inputValueAirPp = inputFieldAirPp.value;
        var inputValueAirE = inputFieldAirE.value;
        var inputValueAirPro = inputFieldAIrPro.value;
        var inputValueAirMin = inputFieldAirMin.value;

        if (isNaN(inputValueAirPp) || !Number.isInteger(parseFloat(inputValueAirPp))) {
            alert('Luft per person kan kun inneholde tall. Eks: 7,2');
            event.preventDefault();
        }

        if (isNaN(inputValueAirE) || !Number.isInteger(parseFloat(inputFieldAirE))) {
            alert('Emisjonstall kan kun inne holde tall. Eks 3,6')
            event.preventDefault();
        }

        if (isNaN(inputValueAirPro) || !Number.isInteger(parseFloat(inputValueAirPro))) {
            alert('Prosess kan kun inne holde tall. Eks 200')
            event.preventDefault();
        }

        if (isNaN(inputValueAirMin) || !Number.isInteger(parseFloat(inputValueAirMin))) {
            alert('Minimumsverdi kan kun inne holde tall. Eks 3,6')
            event.preventDefault();
        }

    });
});