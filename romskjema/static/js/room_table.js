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

function removeRow(button) {
    const row = button.parentNode.parentNode;
    row.parentNode.removeChild(row);
}

document.addEventListener("DOMContentLoaded", function() {
    const activeElement = document.getElementById("alwaysActive");

    function setFocus() {
        activeElement.focus();
    }

    // Initially set the focus
    setFocus();

    // Set focus on the element whenever the window or form loses focus
    document.getElementById("myForm").addEventListener("focusout", setFocus);
    window.addEventListener("focus", setFocus);
});

/*

      document.addEventListener("DOMContentLoaded", function() {
        const table = document.getElementById("editable-table");
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