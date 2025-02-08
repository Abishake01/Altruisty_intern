function clearInput(button) {
    // Find the input-wrapper of the clicked X button
    const inputWrapper = button.parentElement; // Get the input-wrapper

    // Remove only the input field (not affecting the + button)
    inputWrapper.remove(); // This will remove only the input field and X button
}

function addPoint(containerId) {
    // Find the container to add the new input fields
    const container = document.getElementById(containerId);

    // Create a new div for the input and X button
    const newInputWrapper = document.createElement('div');
    newInputWrapper.classList.add('input-wrapper');

    // Create the new input field
    const newInput = document.createElement('input');
    newInput.type = 'text';
    newInput.placeholder = 'Enter Improvement';
    newInput.classList.add('point-input');

    const newInput1 = document.createElement('input');
    newInput1.type = 'text';
    newInput1.placeholder = 'Enter solution';
    newInput1.classList.add('point-input');

   
    // Create the X button for deleting the input
    const clearIcon = document.createElement('span');
    clearIcon.classList.add('clear-icon');
    clearIcon.innerHTML = '&#10006;';
    clearIcon.setAttribute('onclick', 'clearInput(this)');

    // Append the input and clearIcon to the new wrapper
    newInputWrapper.appendChild(newInput);
    newInputWrapper.appendChild(space)
    newInputWrapper.appendChild(newInput1);
    newInputWrapper.appendChild(clearIcon);

    // Append the new input-wrapper above the + button wrapper
    container.insertBefore(newInputWrapper, container.querySelector('.add-point-wrapper'));
}
