

function deleteRoom(event) {
  if (confirm("Vil du slette rom? All data assosisert med rommet blir slettet")) {
    event.preventDefault();
    const button = event.target;
    const row = button.closest("tr")
    const roomIdCell = row.getElementsByTagName("td")[0]
    const roomId = roomIdCell.querySelector(".hidden-text").textContent;
    const projectId = document.getElementById("project_id").value;
    
    fetch(`/${projectId}/rooms/delete_room`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        room_id: roomId,
        project_id: projectId
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
  const lockedCells = [0, 1, 2, 4, 9];
  const projectId = document.getElementById("project_id").value;

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

          const saveData = async () => {
              const newValue = input.value;
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
                  const hiddenColumnName = cell.getAttribute("hidden-data-column");

                  if (columnName) {
                      rowData[columnName] = cell.innerText;
                  }

                  if (hiddenColumnName) {
                      rowData[hiddenColumnName] = cell.querySelector(".hidden-text").textContent;
                  }
                  rowData["project_id"] = projectId;
              }

              try {
                  const response = await fetch(`/${projectId}/rooms/update_room`, {
                      method: 'POST',
                      headers: {
                          'Content-Type': 'application/json'
                      },
                      body: JSON.stringify(rowData)
                  });
                  const data = await response.json();
                  if (data.success) {
                      window.location.href = data.redirect;
                  } else {
                      console.error("Update failed");
                  }
              } catch (error) {
                  console.error("Error:", error);
              }
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
  var form = document.getElementById('new_room');
  var inputFieldArea = document.getElementById('room_area');
  var inputFieldPeople = document.getElementById('room_people');

  form.addEventListener('submit', function(event) {
      var inputValueArea = inputFieldArea.value;
      var inputValuePeople = inputFieldPeople.value;

      if (isNaN(inputValueArea) || !Number.isInteger(parseFloat(inputValueArea))) {
          alert('Areal kan kun inneholde tall');
          event.preventDefault();
      }

      if (isNaN(inputValueArea) || !Number.isInteger(parseInt(inputValuePeople))) {
          alert('Personer kan kun inneholde tall');
          event.preventDefault(); 
      }
  });
});