// Save this file as /static/script.js
function pasteLink() {
    navigator.clipboard.readText().then(function(text) {
        document.getElementById('video-url').value = text;
    }).catch(function(err) {
        console.error('Failed to read clipboard: ', err);
    });
}

function clearInput() {
    document.getElementById('video-url').value = ''; // Clear the input field
}
