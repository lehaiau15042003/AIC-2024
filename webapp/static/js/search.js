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
                const videoItem = document.createElement('li');
                videoItem.className = 'video-item';

                const thumbnailContainer = document.createElement('div');
                thumbnailContainer.className = 'video-thumbnail-container';

                const thumbnail = document.createElement('img');
                thumbnail.src = video.thumbnail_url;
                thumbnail.alt = video.title;
                thumbnail.dataset.url = video.watch_url.replace('watch?v=', 'embed/');

                thumbnailContainer.appendChild(thumbnail);
                videoItem.appendChild(thumbnailContainer);

                const titleElement = document.createElement('h3');
                titleElement.innerText = video.title;
                videoItem.appendChild(titleElement);

                videoGallery.appendChild(videoItem);
            });
        } catch (error) {
            console.error('Error fetching search results:', error);
            alert('Error fetching search results. Please try again later.');
        }
    }

    document.getElementById('video-gallery').addEventListener('click', (event) => {
        const thumbnail = event.target.closest('img[data-url]');
        if (thumbnail) {
            const url = thumbnail.getAttribute('data-url');
            console.log('Video URL:', url);
            const iframe = document.getElementById('video-player');
            iframe.src = url;
            iframe.style.display = 'block';
            document.getElementById('video-player-container').style.display = 'block';
        }
    });
    const iframe = document.getElementById('video-player');
    iframe.style.display = 'none';
});
