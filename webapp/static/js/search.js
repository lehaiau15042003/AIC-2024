document.addEventListener('DOMContentLoaded', () => {
    const videoGallery = document.getElementById('video-gallery');
    const videoPlayerContainer = document.getElementById('video-player-container');
    const videoPlayer = document.getElementById('video-player');
    const closeVideoBtn = document.getElementById('close-btn');

    document.getElementById('search-box').addEventListener('submit', function(event) {
        event.preventDefault();
        const searchText = document.getElementById('search-text').value;
        if (searchText.trim() !== '') {
            search(searchText);
        }
    });

    async function search(searchText) {
        try {
            videoGallery.innerHTML = '<p>Loading...</p>';

            const embeddingResponse = await fetch(`/get_embedding?query=${encodeURIComponent(searchText)}`);
            if (!embeddingResponse.ok) throw new Error('Failed to fetch embedding');
                    
            const embedding = await embeddingResponse.json();
            if (!Array.isArray(embedding) || embedding.length === 0) {
                throw new Error('Invalid embedding received');
            }

            const response = await fetch('/search_by_embedding', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ 
                    query_embedding: embedding,
                    threshold: 0.3,
                    limit: 50
                })
            });

            if (!response.ok) throw new Error('Network response was not ok');

            const data = await response.json(); 
            if (!data || !Array.isArray(data.videos)) {
                throw new Error('Invalid response structure');
            }

            videoGallery.innerHTML = '';
            if (data.videos.length === 0) {
                videoGallery.innerHTML = '<p>No videos found</p>';
                return;
            }

            const videoItems = data.videos.map(video => {
                const videoItem = document.createElement('li');
                videoItem.className = 'video-item';

                const thumbnailContainer = document.createElement('div');
                thumbnailContainer.className = 'video-thumbnail-container';

                const thumbnail = document.createElement('img');
                thumbnail.src = video.thumbnail_url;
                thumbnail.alt = video.title;
                thumbnail.dataset.url = video.watch_url.replace('watch?v=', 'embed/');
                thumbnail.loading = 'lazy';

                thumbnailContainer.appendChild(thumbnail);
                videoItem.appendChild(thumbnailContainer);

                const titleElement = document.createElement('h3');
                titleElement.innerText = video.title;
                videoItem.appendChild(titleElement);

                return videoItem;
            });

            videoItems.forEach(item => videoGallery.appendChild(item));
            console.log('Response data:', data);

        } catch (error) {
            console.error('Error fetching search results:', error);
            alert(`Error fetching search results. Please try again later. Error: ${error.message}`);
            videoGallery.innerHTML = '<p>Error fetching results. Please try again.</p>';
        }
    }

    videoGallery.addEventListener('click', (event) => {
        const thumbnail = event.target.closest('img[data-url]');
        if (thumbnail) {
            const url = thumbnail.getAttribute('data-url');
            videoPlayer.src = url;
            videoPlayer.style.display = 'block';
            videoPlayerContainer.style.display = 'flex';
        }
    });

    videoPlayerContainer.addEventListener('click', function(event) {
        if (!videoPlayer.contains(event.target)) {
            this.style.display = 'none';
            videoPlayer.src = ''; 
        }
    });

    closeVideoBtn.addEventListener('click', () => {
        videoPlayerContainer.style.display = 'none';
        videoPlayer.src = '';
    });

    document.getElementById('search-btn').addEventListener('click', () => {
        const searchText = document.getElementById('search-text').value;
        if (searchText.trim() !== '') {
            search(searchText);
        }
    });

    document.getElementById('search-text').addEventListener('keydown', function(event) {
        if (event.key === 'Enter') {
            const searchText = this.value;
            if (searchText.trim() !== '') {
                search(searchText);
            }
        }
    });
});
