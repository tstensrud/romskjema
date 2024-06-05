document.addEventListener('DOMContentLoaded', function() {
    // Get the form and input elements
    var form = document.getElementById('new_room');
    var inputFieldArea = document.getElementById('room_area');
    var inputFieldPeople = document.getElementById('room_people');

    // Add submit event listener to the form
    form.addEventListener('submit', function(event) {
        // Get the value of the input field
        var inputValueArea = inputFieldArea.value;
        var inputValuePeople = inputFieldPeople.value;

        // Check if the input value is an integer
        if (isNaN(inputValueArea) || !Number.isInteger(parseFloat(inputValueArea))) {
            // If it is an integer, show an alert and prevent form submission
            alert('Areal kan kun inneholde tall');
            event.preventDefault(); // Prevent form submission
        }

        if (isNaN(inputValueArea) || !Number.isInteger(parseInt(inputValuePeople))) {
            // If it is an integer, show an alert and prevent form submission
            alert('Personer kan kun inneholde tall');
            event.preventDefault(); // Prevent form submission
        }
    });
});