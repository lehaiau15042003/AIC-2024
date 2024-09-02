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

            if (data.videos.length === 0) {
                videoGallery.innerHTML = '<p>No videos found</p>';
                return;
            }

            data.videos.forEach(video => {
                const videoItem = document.createElement('div');
                videoItem.className = 'video-item';

                const thumbnail = document.createElement('img');
                thumbnail.src = video.thumbnail_url;
                thumbnail.alt = video.title;
                thumbnail.className = 'video-thumbnail';

                const descriptionElement = document.createElement('div');
                descriptionElement.className = 'video-description';
                descriptionElement.innerText = video.title;

                videoItem.appendChild(thumbnail);
                videoItem.appendChild(descriptionElement);

                videoItem.addEventListener('click', () => {
                    document.getElementById('video-player').src = video.watch_url;
                    document.getElementById('frame-image').src = video.thumbnail_url;
                    document.getElementById('description').innerText = video.description;
                    highlightVideo(videoItem);
                });

                videoGallery.appendChild(videoItem);
            });
        } catch (error) {
            console.error('Error fetching search results:', error);
            alert('Error fetching search results. Please try again later.');
        }
    }

    async function loadVideos() {
        try {
            const response = await fetch('/videos');
            if (!response.ok) throw new Error('Network response was not ok');
            const data = await response.json();

            const videoGallery = document.getElementById('video-gallery');
            videoGallery.innerHTML = '';

            if (data.videos.length === 0) {
                videoGallery.innerHTML = '<p>No videos available</p>';
                return;
            }

            data.videos.forEach(video => {
                const videoItem = document.createElement('div');
                videoItem.className = 'video-item';

                const thumbnail = document.createElement('img');
                thumbnail.src = video.thumbnail_url;
                thumbnail.alt = video.title;
                thumbnail.className = 'video-thumbnail';

                const descriptionElement = document.createElement('div');
                descriptionElement.className = 'video-description';
                descriptionElement.innerText = video.title;

                videoItem.appendChild(thumbnail);
                videoItem.appendChild(descriptionElement);

                videoItem.addEventListener('click', () => {
                    document.getElementById('video-player').src = video.watch_url;
                    document.getElementById('frame-image').src = video.thumbnail_url;
                    document.getElementById('description').innerText = video.description;
                    highlightVideo(videoItem);
                });

                videoGallery.appendChild(videoItem);
            });
        } catch (error) {
            console.error('Error loading videos:', error);
            alert('Error loading videos. Please try again later.');
        }
    }

    function highlightVideo(videoItem) {
        const videoItems = document.querySelectorAll('.video-item');
        videoItems.forEach(item => item.classList.remove('highlight'));

        videoItem.classList.add('highlight');
    }

    loadVideos();
});
