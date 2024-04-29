// Select all elements with the class '.new-fileBtn'
var newFileBtns = document.querySelectorAll('.new-fileBtn');

// Loop through each element and attach mouseover and mouseout event listeners
newFileBtns.forEach(newFileBtn => {
    newFileBtn.addEventListener('mouseover', () => {
        // Select the corresponding tooltip element
        var tooltip = newFileBtn.nextElementSibling;

        // Add the class 'hovered' to the tooltip element
        tooltip.classList.add('hovered');
    });

    newFileBtn.addEventListener('mouseout', () => {
        // Select the corresponding tooltip element
        var tooltip = newFileBtn.nextElementSibling;

        // Remove the class 'hovered' from the tooltip element
        tooltip.classList.remove('hovered');
    });
});


