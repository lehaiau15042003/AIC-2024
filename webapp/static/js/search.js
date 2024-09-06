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


// inform search

document.getElementById('search-btn').addEventListener('click', sendMessage);
document.getElementById('search-text').addEventListener('keydown', function(event) {
    if (event.key === 'Enter') sendMessage();
});

function sendMessage() {
    const input = document.getElementById('search-text');
    const message = input.value.trim();
    
    if (message) {
        addMessage(message, 'user');
        input.value = '';

        // Giả lập phản hồi từ bot sau 1 giây
        setTimeout(() => {
            const botReply = generateBotReply(message);
            addMessage(botReply, 'bot');
        }, 1000);
    }
}

function addMessage(text, sender) {
    const messageContainer = document.getElementById('messages');
    const messageElement = document.createElement('div');
    messageElement.classList.add('message', sender);
    messageElement.textContent = text;
    messageContainer.appendChild(messageElement);
    messageContainer.scrollTop = messageContainer.scrollHeight;  // Tự động cuộn xuống cuối
}

function generateBotReply(userMessage) {
    // Logic trả lời bot cơ bản, có thể thay bằng gọi API GPT-3, GPT-4, v.v.
    return `Bot: Bạn đã nói "${userMessage}"`;
}

// close video
// Function to show the video player with the specified URL
function showVideoPlayer(videoUrl) {
    const videoPlayerContainer = document.getElementById('video-player-container');
    const videoPlayer = document.getElementById('video-player');
    
    videoPlayer.src = videoUrl;
    videoPlayerContainer.style.display = 'flex'; // Show the container
}

// Event listener to close the video player when clicking outside the iframe
document.getElementById('video-player-container').addEventListener('click', function(event) {
    const videoPlayer = document.getElementById('video-player');
    
    // Check if the click was outside the iframe
    if (!videoPlayer.contains(event.target)) {
        this.style.display = 'none'; // Hide the container
        videoPlayer.src = ''; // Stop the video
    }
});

// Example usage: showing the video player when a thumbnail is clicked
document.querySelectorAll('.video-thumbnail-container img').forEach(img => {
    img.addEventListener('click', function() {
        const videoUrl = this.getAttribute('data-url');
        showVideoPlayer(videoUrl);
    });
});
