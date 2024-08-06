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

document.getElementById('upload-form').addEventListener('submit', function(event) {
    event.preventDefault();
    const fileInput = document.getElementById('file-input');
    const file = fileInput.files[0];

    if (file) {
        const reader = new FileReader();
        reader.onloadend = function() {
            const base64String = reader.result.split(',')[1];

            const jsonData = JSON.stringify({
                fileName: file.name,
                fileType: file.type,
                fileContent: base64String
            });

            fetch('/upload', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: jsonData
            })
            .then(response => {
                if (response.redirected) {
                    window.location.href = response.url;
                } else {
                    return response.json().then(data => {
                        if (data.message === 'File uploaded successfully') {
                            window.location.href = 'upload/result?file_url=${encodeURIComponent(data.file_url)}';
                        } else {
                            alert("Upload Failed: " + data.error);
                        }
                    })
                }
            })
            
            .catch(error => {
                console.error('Error:', error);
                alert('Upload Failed: ' + error.message);
            });
        };
        reader.readAsDataURL(file);
    } else {
        alert('Please select a file to upload.');
    }
});