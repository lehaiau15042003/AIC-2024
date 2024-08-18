document.getElementById('search-box').addEventListener('submit', function(event) {
    event.preventDefault();

    const searchText = document.getElementById('search-text').value;
    if (searchText.trim() !== '') {
        console.log('Searching for: ', searchText);
    }
});