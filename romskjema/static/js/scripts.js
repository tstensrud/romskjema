
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
    const form = document.getElementById('new_room');
    const specification = document.getElementById("spec").value;
    console.log(specification)

    const formData = new FormData(form);
    const data = {};

    formData.forEach((value, key) => {
        data[key] = value;
    });

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
          window.location.href = data.redirect;
        } else {
          console.error("Update failed");
        }
      })
      .catch(error => {
        console.error("Error:", error);
      });
}
