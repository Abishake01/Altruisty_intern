function clearInput(button) {
    // Find the input-wrapper of the clicked X button
    const inputWrapper = button.parentElement; // Get the input-wrapper

    // Remove only the input field (not affecting the + button)
    inputWrapper.remove(); // This will remove only the input field and X button
}
let s = [];
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

   
    // Create the X button for deleting the input
    const clearIcon = document.createElement('span');
    clearIcon.classList.add('clear-icon');
    clearIcon.innerHTML = '&#10006;';
    clearIcon.setAttribute('onclick', 'clearInput(this)');

    // Append the input and clearIcon to the new wrapper
    newInputWrapper.appendChild(newInput);
    newInputWrapper.appendChild(clearIcon);

    // Append the new input-wrapper above the + button wrapper
    container.insertBefore(newInputWrapper, container.querySelector('.add-point-wrapper'));
}
async function goToPointsPage() {
    let object1 = `strength--${s}`
    window.location.href = `http://127.0.0.1:8000/points/${object1}`;