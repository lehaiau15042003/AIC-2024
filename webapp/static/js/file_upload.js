document.getElementById('upload-link').addEventListener('click', function(event) {
    event.preventDefault();
    document.getElementById('file-input').click();
});

document.getElementById('file-input').addEventListener('change', function(event) {
    const file = event.target.files[0];
    if (file) {
        console.log('File selected: ', file.name);
        const reader = new FileReader();
        
        const videoPreview = document.getElementById('video-preview');
        videoPreview.style.display = 'none';
        
        if (file.type.startsWith('video/')) {
            reader.onload = function(e) {
                videoPreview.src = e.target.result;
                videoPreview.style.display = 'block';
            };
            reader.readAsDataURL(file);
            
            uploadFile(file).then(result => {
                document.getElementById('prediction-info').textContent = JSON.stringify(result);
            }).catch(error => {
                console.error('Error uploading file:', error);
            });
        } else {
            alert('Please upload a valid video file.');
        }
    }
});

async function uploadFile(file) {
    const formData = new FormData();
    formData.append('file', file);
    try {
        const response = await fetch('http://localhost:8000/upload', {
            method: 'POST',
            body: formData
        });
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        const result = await response.json();
        return result.predictions;
    } catch (error) {
        console.error('Error uploading file:', error);
        throw error;
    }
}
