
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