/* Edit table in room list - ventilation */
document.addEventListener("DOMContentLoaded", function() {
    const table = document.getElementById("roomsTableVentilation");
    const cells = table.getElementsByTagName("td");
    const lockedCells = [0,1,2,3,4,5,6,7,9,12]
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