/* Edit heating table */

document.addEventListener("DOMContentLoaded", function() {
  const table = document.getElementById("coolingTable");
  const cells = table.getElementsByTagName("td");
  const lockedCells = [0,1,2,3,13,14,15];
  const buildingId = document.getElementById('building_select').value;
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
                  const hiddenColumnName = cell.getAttribute("hidden-data-column");
                  rowData["building_id"] = buildingId;
                  rowData["project_id"] = projectId;
                  if (columnName) {
                      rowData[columnName] = cell.innerText;
                  }

                  if (hiddenColumnName) {
                      rowData[hiddenColumnName] = cell.querySelector(".hidden-text").textContent;
                  }
              }

              try {
                  const response = await fetch(`/${projectId}/cooling/update_cooling_table`, {
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

  /* Auto submit on the building selector */
  function showBuildings() {
    document.getElementById("project_building").submit();
}

/* Update building heating settings */

document.getElementById('building_cooling_settings').addEventListener('submit', function(event) {
  event.preventDefault();
  const buildingId = document.getElementById('building_select').value;
  const form = event.target;
  const projectId = document.getElementById("project_id").value;

  if (!form) {
    console.error('Form not found!');
    return;
  }

  const formData = {};

  Array.from(form.elements).forEach(element => {
    if (element.name) {
      formData[element.name] = element.value;
    }
  });
  formData["building_id"] = buildingId;
  formData["projet_id"] = projectId;


  const url = `/${projectId}/cooling/building_cooling_settings`;
  //console.log('Form Data:', formData);
  //console.log('Fetch URL:', url);

  fetch(url, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(formData)
  })
  .then(response => {
    //console.log('Fetch response:', response);

    if (!response.ok) {
      throw new Error('Network response was not ok: ' + response.statusText);
    }

    return response.json();
  })
  .then(data => {
    console.log('Response data:', data);

    if (data.success) {
      window.location.href = data.redirect;
    } else {
      console.error('Update failed:', data);
    }
  })
  .catch(error => {
    console.error('Fetch error:', error);
  });
});