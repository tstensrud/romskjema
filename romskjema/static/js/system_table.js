function deleteSystem(event) {
  if (confirm("Vil du slette system? All data assosisert med dette systemet blir slettet")) {
    event.preventDefault();
    const projectId = document.getElementById("project_id").value;
    const button = event.target;
    const row = button.closest("tr")
    const roomIdCell = row.getElementsByTagName("td")[0]
    const systemId = roomIdCell.querySelector(".hidden-text").textContent;
    
    fetch(`/${projectId}/ventsystems/delete_system`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        system_id: systemId,
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

/* Update systems table */
document.addEventListener("DOMContentLoaded", function() {
    const table = document.getElementById("systemsTableVentilation");
    const cells = table.getElementsByTagName("td");
    const lockedCells = [0,1,5,6,7,8,9,10]
    const projectId = document.getElementById("project_id").value;
  
    for (let cell of cells) {
      cell.addEventListener("click", function() {
        if (lockedCells.includes(this.cellIndex)) return;
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

            rowData["project_id"] = projectId;
          }
  
          // Send AJAX request to update the database
          fetch(`/${projectId}/ventsystems/update_system`, {
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

  /* Input check on airflow */
  document.addEventListener('DOMContentLoaded', function() {
    var form = document.getElementById('system');
    var inputFieldArea = document.getElementById('airflow');

    form.addEventListener('submit', function(event) {
        var inputValueArea = inputFieldArea.value;

        if (isNaN(inputValueArea) || !Number.isInteger(parseFloat(inputValueArea))) {
            alert('Luftmengde kan kun inneholde tall.');
            event.preventDefault();
        }
    });
});