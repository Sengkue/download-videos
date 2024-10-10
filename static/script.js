// Save this file as /static/script.js
function pasteLink() {
    navigator.clipboard.readText().then(function(text) {
        document.getElementById('video-url').value = text;
        toggleClearIcon(); // Show clear icon after pasting
    }).catch(function(err) {
        console.error('Failed to read clipboard: ', err);
    });
}

function clearInput() {
    document.getElementById('video-url').value = ''; // Clear the input field
    toggleClearIcon(); // Hide clear icon after clearing
}

function toggleClearIcon() {
    const inputField = document.getElementById('video-url');
    const clearIcon = document.querySelector('.clear-icon');

    // Show clear icon if the input field has value
    if (inputField.value) {
        clearIcon.style.display = 'block';
    } else {
        clearIcon.style.display = 'none';
    }
}
