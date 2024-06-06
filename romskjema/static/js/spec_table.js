document.addEventListener('DOMContentLoaded', function () {
    const hoverElements = document.querySelectorAll('.hover-popup');
    const minLength = 25;
    const maxLength = 100;

    hoverElements.forEach(element => {
        element.addEventListener('mouseover', function () {
            const popupText = element.getAttribute('data-popup').replace(/\\n/g, '<br>');
            if (popupText.length > minLength) {
                const popup = document.createElement('div');
                popup.className = 'popup';
                popup.innerHTML = popupText;
                document.body.appendChild(popup);

                const rect = element.getBoundingClientRect();
                popup.style.top = `${rect.bottom + window.scrollY}px`;
                if (popupText.length > maxLength) {
                    popup.style.left = `${rect.left + window.scrollX - 500}px`;
                }
                else {
                    popup.style.left = `${rect.left + window.scrollX - 200}px`;
                }
            }
        });

        element.addEventListener('mouseout', function () {
            const popup = document.querySelector('.popup');
            if (popup) {
                document.body.removeChild(popup);
            }
        });
    });
});