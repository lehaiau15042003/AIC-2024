document.getElementById('upload-link').addEventListener('click', function(event) {
    event.preventDefault();
    document.getElementById('file-input').click();
});

document.getElementById('file-input').addEventListener('change', function(event){
    const file = event.target.files[0];
    if (file) {
        console.log('File selected: ', file.name);
        const reader = new FileReader();
        reader.onload = function(e) {
            const imagePreview = document.getElementById('image-preview');
            const videoPreview = document.getElementById('video-preview');
            if (file.type.startsWith('image/')){
                imagePreview.src = e.target.result;
                imagePreview.style.display = "block";
                videoPreview.style.display = 'none';
            } else if (file.type.startsWith('video/')) {
                videoPreview.src = e.target.result;
                videoPreview.style.display = 'block';
                imagePreview.style.display = 'none';
            }
            
        }

        reader.readAsDataURL(file);
    }
});

async function uploadImage(file) {
    const formData = new FormData();
    formData.append('file', file);

    const response = await fetch('http://localhost:8000/predict', {
        method: 'POST',
        body: formData
    });

    const result = await response.json();
    return result;
}

async function UploadVideo(file){
    const formData = new FormData();
    formData.append('file', file);

    const response = await fetch('http://localhost:8000/predict', {
        method: 'POST',
        body: formData
    });

    const result = await response.json();
    return result;
}
