/* DARK/LIGHT mode */
document.addEventListener('DOMContentLoaded', function () {
  const modeSwitch = document.querySelector('.mode-switch');

  function applyTheme(theme) {
      if (theme === 'light') {
          document.documentElement.classList.add('light');
          modeSwitch.classList.add('active');
      } else {
          document.documentElement.classList.remove('light');
          modeSwitch.classList.remove('active');
      }
  }

  const savedTheme = localStorage.getItem('theme');
  if (savedTheme) {
      applyTheme(savedTheme);
  } else {
      applyTheme('dark');
  }

  modeSwitch.addEventListener('click', function () {
      document.documentElement.classList.toggle('light');
      modeSwitch.classList.toggle('active');
      let currentTheme = document.documentElement.classList.contains('light') ? 'light' : 'dark';
      localStorage.setItem('theme', currentTheme);
  });
});

/* New specification room */
function submitNewRoom() {
  const data = {};
  const specification = document.getElementById("spec").value;
  data["spec"] = document.getElementById("spec").value;
  data["spec_id"] = document.getElementById("spec_id").value;
  data["room_type"] = document.getElementById("room_type").value;
  data["air_p_p"] = document.getElementById("air_per_person").value;
  data["air_emission"] = document.getElementById("air_emission").value;
  data["air_process"] = document.getElementById("air_process").value;
  data["air_minimum"] = document.getElementById("air_minimum").value;
  data["vent_princ"] = document.getElementById("ventilation_principle").value;
  data["heat_ex"] = document.getElementById("heat_ex").value;
  data["db_t"] = document.getElementById("db_technical").value;
  data["db_n"] = document.getElementById("db_neighbour").value;
  data["db_c"] = document.getElementById("db_corridor").value;
  
  let vavcav;
  const vavcav_radio = document.getElementsByName("vav")
  for (const choice of vavcav_radio) {
    if(choice.checked) {
        vavcav = choice.value;
        break;
    }
  }

  data["control_vav"] = vavcav;
  data["control_temp"] = document.getElementById("temp").checked;
  data["control_co2"] = document.getElementById("co2").checked;
  data["control_movement"] = document.getElementById("movement").checked;
  data["control_moisture"] = document.getElementById("moisture").checked;
  data["control_time"] = document.getElementById("time").checked;
  data["notes"] = document.getElementById("notes").value;

  const jsonData = JSON.stringify(data);

  fetch(`/specifications/${specification}/new_room`, {
      method: 'POST',
      headers: {
          'Content-Type': 'application/json'
      },
      body: jsonData,
  })
  .then(response => response.json())
  .then(data => {
      if (data.success) {
        console.log("Update success:", data.message);
      } else {
          console.error("Update failed:", data.message || 'Unknown error');
      }
      window.location.href = data.redirect;
  })
  .catch(error => {
      console.error("Error:", error);
  });
}


/* Todo-list-popup script*/
document.getElementById('todo-openPopup').addEventListener('click', function(event) {
    event.preventDefault();
    document.getElementById('todo-popup').style.display = 'flex';
});

document.querySelector('.todo-close-btn').addEventListener('click', function() {
    document.getElementById('todo-popup').style.display = 'none';
});

document.getElementById("submitTodoButton").addEventListener("click", function(event) {
    event.preventDefault();
    newTodoItem();
});

/* New todo-item */
async function newTodoItem() {
    const data = {};
    const projectId = document.getElementById("project_id").value;
    data["user_id"] = document.getElementById("user_id").value;
    data["todo_content"] = document.getElementById("todo_content").value;
    const jsonData = JSON.stringify(data);
    console.log("Sending data:", jsonData);

    try {
        await new Promise(resolve => setTimeout(resolve, 500));
        const response = await fetch(`/${projectId}/project/new_todo_item`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: jsonData,
        });

        console.log("Received response:", response);

        if (!response.ok) {
            throw new Error('Network response was not ok ' + response.statusText);
        }

        const responseData = await response.json();
        console.log("Response data:", responseData);

        if (responseData.success) {
            console.log("Update success:", responseData.message);
            window.location.href = responseData.redirect;
        } else {
            console.error("Update failed:", responseData.message || 'Unknown error');
        }
    } catch (error) {
        if (error.name === 'AbortError') {
            console.error("Fetch aborted:", error);
        } else {
            console.error("Error:", error);
        }
    }
}

/* Mark Todo-item as completed */
document.addEventListener('DOMContentLoaded', function() {
    const data = {}
    var showListButton = document.getElementById('todo-openPopup');
    var todoListContainer = document.getElementById('todo-popup-item-container');
    const projectId = document.getElementById("project_id").value;
    const userId = document.getElementById("user_id").value;
    data["user_id"] = userId;

    showListButton.addEventListener('click', function() {
        var buttons = todoListContainer.querySelectorAll('.todo-list-button');
        buttons.forEach(function(button) {
            button.addEventListener('click', function() {
                var parentDiv = button.closest('.todo-popup-listitem');
                var inputField = parentDiv.querySelector('.item-id');
                var itemId = inputField.value;
                data["item_id"] = itemId

                console.log('Item ID:', itemId);

                fetch(`/${projectId}/project/todo_item_complete`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(data)
                })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        parentDiv.classList.add('todo-completed');
                        console.log("Completed")
                    } else {
                        console.error("Failed to complete task")
                    }
                })
                .catch(error => console.error('Error:', error));
            });
        });
    });
});