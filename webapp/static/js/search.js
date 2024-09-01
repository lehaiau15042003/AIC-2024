document.addEventListener('DOMContentLoaded', () => {
    document.getElementById('search-box').addEventListener('submit', function(event) {
        event.preventDefault();
        const searchText = document.getElementById('search-text').value;
        if (searchText.trim() !== '') {
            search(searchText);
        }
    });

    async function search(searchText) {
        const response = await fetch(`/search?query=${encodeURIComponent(searchText)}`);
        const data = await response.json(); 

        const videoGallery = document.getElementById('video-gallery');
        videoGallery.innerHTML = '';

        data.videos.forEach(video => {
            const videoItem = document.createElement('div');
            videoItem.className = 'video-item';

            const thumbnail = document.createElement('img');
            thumbnail.src = video.thumbnail_path;
            thumbnail.alt = video.description;
            thumbnail.className = 'video-thumbnail';

            const descriptionElement = document.createElement('div');
            descriptionElement.className = 'video-description';
            descriptionElement.innerText = video.description;

            videoItem.appendChild(thumbnail);
            videoItem.appendChild(descriptionElement);

            videoItem.addEventListener('click', () => {
                document.getElementById('video-player').src = video.video_path;
                document.getElementById('frame-image').src = video.frame_image;
                document.getElementById('description').innerText = video.description;
            });

            videoGallery.appendChild(videoItem);
        });
    }
    async function loadVideos() {
        const response = await fetch('/videos');
        const data = await response.json();

        const videoGallery = document.getElementById('video-gallery');
        videoGallery.innerHTML = '';

        data.videos.forEach(video => {
            const videoItem = document.createElement('div');
            videoItem.className = 'video-item';

            const thumbnail = document.createElement('img');
            thumbnail.src = video.thumbnail_path;
            thumbnail.alt = video.description;
            thumbnail.className = 'video-thumbnail';

            const descriptionElement = document.createElement('div');
            descriptionElement.className = 'video-description';
            descriptionElement.innerText = video.description;

            videoItem.appendChild(thumbnail);
            videoItem.appendChild(descriptionElement);

            videoItem.addEventListener('click', () => {
                document.getElementById('video-player').src = video.video_path;
                document.getElementById('frame-image').src = video.frame_image;
                document.getElementById('description').innerText = video.description;
            });

            videoGallery.appendChild(videoItem);
        });
    }
    loadVideos();
});
