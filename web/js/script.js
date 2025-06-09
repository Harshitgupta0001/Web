// Add interactive functionality to the web interface
document.addEventListener('DOMContentLoaded', function() {
    // Add loading state when selecting channel
    const channelSelect = document.querySelector('select[name="channel"]');
    if (channelSelect) {
        channelSelect.addEventListener('change', function() {
            // Show loading indicator
            const loader = document.createElement('div');
            loader.className = 'loading';
            loader.innerHTML = 'Loading files...';
            document.querySelector('.file-grid').prepend(loader);
        });
    }

    // Add search functionality
    const searchInput = document.createElement('input');
    searchInput.type = 'text';
    searchInput.placeholder = 'Search files...';
    searchInput.style.padding = '8px';
    searchInput.style.marginLeft = '10px';
    searchInput.style.borderRadius = '4px';
    searchInput.style.border = '1px solid #ddd';

    searchInput.addEventListener('input', function(e) {
        const searchTerm = e.target.value.toLowerCase();
        const fileCards = document.querySelectorAll('.file-card');
        
        fileCards.forEach(card => {
            const fileName = card.querySelector('.file-name').textContent.toLowerCase();
            if (fileName.includes(searchTerm)) {
                card.style.display = 'block';
            } else {
                card.style.display = 'none';
            }
        });
    });

    // Add search box to the header
    const header = document.querySelector('.header');
    if (header) {
        header.appendChild(searchInput);
    }
});
