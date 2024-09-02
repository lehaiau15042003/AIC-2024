document.addEventListener('DOMContentLoaded', () => {
    document.getElementById('search-box').addEventListener('submit', function(event) {
        event.preventDefault();
        const searchText = document.getElementById('search-text').value;
        if (searchText.trim() !== '') {
            search(searchText);
        }
    });

    async function search(searchText) {
        try {
            const response = await fetch(`/search?query=${encodeURIComponent(searchText)}`);
            if (!response.ok) throw new Error('Network response was not ok');
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
        } catch (error) {
            console.error('Error fetching search results:', error);
        }
    }

    async function loadVideos() {
        try {
            const response = await fetch('/videos');
            if (!response.ok) throw new Error('Network response was not ok');
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
        } catch (error) {
            console.error('Error loading videos:', error);
        }
    }

    loadVideos();
});
