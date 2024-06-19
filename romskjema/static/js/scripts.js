
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
