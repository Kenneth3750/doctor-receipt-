

function processImage(event) {
    var imageFile = event.target.files[0];

    var formData = new FormData();
    formData.append('file', imageFile);

    fetch('/process_image', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        console.log(data);
        // Aquí puedes manejar la respuesta del servidor.
    });
}