// Infinite Scroll Implementation for AndroidUICollection
(function() {
    'use strict';
    
    var postsContainer = null;
    var posts = [];
    var currentIndex = 0;
    var postsPerLoad = 24; // Same as original pagination
    var isLoading = false;
    var loadMoreButton = null;
    var spinner = null;
    
    function init() {
        postsContainer = document.querySelector('.post-list');
        if (!postsContainer) return;
        
        // Get all posts from the hidden container
        var allPostsContainer = document.getElementById('all-posts');
        if (!allPostsContainer) return;
        
        posts = Array.from(allPostsContainer.querySelectorAll('.post-card-wrap'));
        
        // Remove the hidden container
        allPostsContainer.remove();
        
        // Create load more button and spinner
        createLoadMoreElements();
        
        // Initially load first batch
        loadMorePosts();
        
        // Add scroll event listener for infinite scroll
        window.addEventListener('scroll', handleScroll);
        
        // Add click event listener for load more button
        loadMoreButton.addEventListener('click', function() {
            loadMorePosts();
        });
    }
    
    function createLoadMoreElements() {
        // Create container
        var container = document.createElement('div');
        container.className = 'load-more-container';
        
        // Create load more button
        loadMoreButton = document.createElement('button');
        loadMoreButton.className = 'load-more-button';
        loadMoreButton.textContent = 'Load More';
        
        // Create spinner
        spinner = document.createElement('div');
        spinner.className = 'loading-spinner';
        spinner.innerHTML = '<div></div>';
        
        container.appendChild(loadMoreButton);
        container.appendChild(spinner);
        
        // Insert after posts container
        postsContainer.parentNode.insertBefore(container, postsContainer.nextSibling);
    }
    
    function loadMorePosts() {
        if (isLoading || currentIndex >= posts.length) return;
        
        isLoading = true;
        
        // Show spinner, hide button
        loadMoreButton.style.display = 'none';
        spinner.style.display = 'block';
        
        // Simulate loading delay for better UX
        setTimeout(function() {
            var fragment = document.createDocumentFragment();
            var endIndex = Math.min(currentIndex + postsPerLoad, posts.length);
            
            for (var i = currentIndex; i < endIndex; i++) {
                fragment.appendChild(posts[i].cloneNode(true));
            }
            
            postsContainer.appendChild(fragment);
            currentIndex = endIndex;
            
            // Apply masonry layout if available
            if (window.applyMasonryLayout) {
                setTimeout(window.applyMasonryLayout, 100);
            }
            
            // Hide spinner, show button
            spinner.style.display = 'none';
            
            if (currentIndex < posts.length) {
                loadMoreButton.style.display = 'inline-block';
                loadMoreButton.textContent = 'Load More (' + (posts.length - currentIndex) + ' remaining)';
            } else {
                loadMoreButton.style.display = 'none';
                
                // Show end message
                var endMessage = document.createElement('p');
                endMessage.textContent = 'All posts loaded!';
                loadMoreButton.parentNode.appendChild(endMessage);
            }
            
            isLoading = false;
        }, 500);
    }
    
    function handleScroll() {
        // Auto-load when user is near bottom (within 200px)
        var scrollPosition = window.innerHeight + window.scrollY;
        var threshold = document.body.offsetHeight - 200;
        
        if (scrollPosition >= threshold && !isLoading && currentIndex < posts.length) {
            loadMorePosts();
        }
    }
    
    // Initialize when DOM is ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }
})();