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

