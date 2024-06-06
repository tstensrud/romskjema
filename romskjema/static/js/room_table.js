

function deleteRoom(event) {
  if (confirm("Vil du slette rom? All data assosisert med rommet blir slettet")) {
    event.preventDefault();
    const button = event.target;
    const row = button.closest("tr")
    const buildingCell = row.getElementsByTagName("td")[0]
    const floorCell = row.getElementsByTagName("td")[1]
    const roomNumberCell = row.getElementsByTagName("td")[2]
    const buildingCellText = buildingCell.innerText;
    const floorCellText = floorCell.innerText;
    const roomNumberCellText = roomNumberCell.innerText;
    
    fetch('/update_room', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        building: buildingCellText,
        floor: floorCellText,
        room_number: roomNumberCellText,
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

    for (let cell of cells) {
        cell.addEventListener("click", function() {
          const lockedCells = [0,1,7,8]  
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

            input.addEventListener("blur", function() {
                cell.innerText = this.value || originalText;
            });

            input.addEventListener("keypress", function(event) {
                if (event.key === "Enter") {
                    this.blur();
                }
            });
        });
    }
});



/*

      document.addEventListener("DOMContentLoaded", function() {
        const table = document.getElementById("roomsTable");
        const cells = table.getElementsByTagName("td");

        for (let cell of cells) {
          cell.addEventListener("click", function() {
            if (this.querySelector("input")) return;

            const originalText = this.innerText;
            const input = document.createElement("input");
            input.type = "text";
            input.value = originalText;
            input.classList.add("form-control");
            this.innerHTML = "";
            this.appendChild(input);
            input.focus();

            const saveData = () => {
              const newValue = input.value || originalText;
              this.innerText = newValue;

              const roomId = this.parentElement.getAttribute("data-room-id");
              const columnName = this.getAttribute("data-column");

              // Send AJAX request to update the database
              fetch('/update_room', {
                method: 'POST',
                headers: {
                  'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                  room_id: roomId,
                  column_name: columnName,
                  new_value: newValue
                })
              })
              .then(response => response.json())
              .then(data => {
                if (data.success) {
                  console.log("Update successful");
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

*/