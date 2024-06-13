

function deleteRoom(event) {
  if (confirm("Vil du slette rom? All data assosisert med rommet blir slettet")) {
    event.preventDefault();
    const button = event.target;
    const row = button.closest("tr")
    const roomIdCell = row.getElementsByTagName("td")[0]
    const roomId = roomIdCell.querySelector(".hidden-text").textContent;
    
    fetch('/rooms/delete_room', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        room_id: roomId,
      })
    })
    .then(response => {
      console.log('Fetch response:', response);
  
      if (!response.ok) {
        throw new Error('Network response was not ok ' + response.statusText);
      }
      return response.json();
    })
    .then(data => {
      console.log('Response data:', data);
  
      if (data.success) {
        window.location.href = data.redirect;
      } else {
        console.error("Update failed:", data);
      }
    })
    .catch(error => {
      console.error("Error:", error);
    });
  }
}

/* Edit table in room list */
document.addEventListener("DOMContentLoaded", function() {
  const table = document.getElementById("roomsTable");
  const cells = table.getElementsByTagName("td");
  const lockedCells = [0,1,2,4,9]

  for (let cell of cells) {
    cell.addEventListener("click", function() {
      if (lockedCells.includes(this.cellIndex)) return;
      if (this.querySelector("input")) return;

      const originalText = this.innerText;
      const input = document.createElement("input");
      input.type = "text";
      input.value = originalText;
      input.classList.add("table-input");
      this.innerHTML = "";
      this.appendChild(input);
      input.focus();

      const saveData = () => {
        const newValue = input.value || originalText;
        if (newValue === originalText) {
          this.textContent = originalText;
          return;
        } 

        this.innerText = newValue;

        const row = this.parentElement;
        const rowData = {};
        const cells = row.getElementsByTagName("td");

        for (let cell of cells) {
          const columnName = cell.getAttribute("data-column");
          const hiddenColumnName = cell.getAttribute("hidden-data-column")
          
          if (columnName) {
            rowData[columnName] = cell.innerText;
          }

          if (hiddenColumnName) {
            rowData[hiddenColumnName] = cell.querySelector(".hidden-text").textContent;
          }
        }

        fetch('/rooms/update_room', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify(rowData)
        })
        .then(response => response.json())
        .then(data => {
          if (data.success) {
            window.location.href = data.redirect;
          } else {
            console.error("Update failed");
          }
        })
        .catch(error => {
          console.error("Error:", error);
        });
      };

      input.addEventListener("blur", saveData);
      input.addEventListener("keypress", function(event) {
        if (event.key === "Enter") {
          saveData();
          input.blur();
        }
      });
    });
  }
});

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