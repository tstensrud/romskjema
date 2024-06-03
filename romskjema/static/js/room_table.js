function addRow() {
    const table = document.getElementById("roomsTable").getElementsByTagName('tbody')[0];
    const newRow = table.insertRow();
    newRow.className = `products-row`;

    for (let i = 0; i < 6; i++) {
        const newCell = newRow.insertCell();
        newCell.contentEditable = "true";
        newCell.innerText = `Row ${table.rows.length} Col ${i + 1}`;
        newCell.className = `product-cell status-cell`;  // Add a class to each cell
    }

    const actionsCell = newRow.insertCell();
    actionsCell.innerHTML = '<button onclick="removeRow(this)" class="table-button">Slett</button>';
    actionsCell.className = 'product-cell status-cell';  // Add a class to the actions cell if needed
}

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