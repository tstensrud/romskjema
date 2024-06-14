
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