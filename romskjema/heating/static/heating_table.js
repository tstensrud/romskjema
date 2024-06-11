/* Edit table in room list - ventilation */
document.addEventListener("DOMContentLoaded", function() {
    const table = document.getElementById("heatingTable");
    const cells = table.getElementsByTagName("td");
    const lockedCells = [0,1,2,3,4,5,6,7,8,9,10,11,14,15]
  
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
            rowData["system_update"] = false
          }
  
          // Send AJAX request to update the database
          fetch('/ventilation/update_ventilation', {
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

  /* Updating the ventilation system */

  document.addEventListener('DOMContentLoaded', (event) => {
    let currentSystemId = 0;
    document.querySelectorAll('select').forEach((selectElement) => {
      selectElement.addEventListener('click', () => {
        currentSystemId = selectElement.value;
        console.log(currentSystemId);
      });
  
      selectElement.addEventListener('change', async () => {
        await autoSubmitSystemForm(selectElement, currentSystemId);
      });
    });
  });
  
  async function autoSubmitSystemForm(selectElement, currentSystemId) {
    const row = selectElement.closest('tr');
    const row_id = row.cells[0].innerText;
    const system_id = selectElement.value;
  
    if (system_id != "none") {
      try {
        const response = await fetch('/heating/update_heating', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            system_update: true,
            old_system_id: currentSystemId,
            row_id: row_id,
            system_id: system_id
          })
        });
  
        if (!response.ok) {
          const errorDetail = await response.text(); // Get detailed error message from response
          console.error(`Network response was not ok: ${response.status} ${response.statusText}. Details: ${errorDetail}`);
          throw new Error('Network response was not ok');
        }
  
        const result = await response.json();
        console.log('Success:', result);
        window.location.reload();
      } catch (error) {
        console.error('Error:', error.message);
        window.location.reload();
      }
    }
  }

  /* Auto submit on the building selector */
  function showBuildings() {
    document.getElementById("project_building").submit();
}