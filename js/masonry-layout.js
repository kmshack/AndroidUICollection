// Masonry Layout Implementation for AndroidUICollection
(function() {
    'use strict';
    
    var masonryContainer = null;
    var resizeTimer = null;
    var columnGap = 20;
    var columns = 4; // Default columns
    
    function init() {
        masonryContainer = document.querySelector('.post-list');
        if (!masonryContainer) return;
        
        // Apply masonry styles to container
        masonryContainer.style.position = 'relative';
        
        // Initial layout
        applyMasonryLayout();
        
        // Re-layout on window resize
        window.addEventListener('resize', function() {
            clearTimeout(resizeTimer);
            resizeTimer = setTimeout(applyMasonryLayout, 250);
        });
        
        // Re-layout when images load
        var images = masonryContainer.querySelectorAll('img, .CoverImage');
        images.forEach(function(img) {
            if (img.complete) return;
            img.addEventListener('load', applyMasonryLayout);
        });
        
        // Observer for dynamically added content
        var observer = new MutationObserver(function(mutations) {
            mutations.forEach(function(mutation) {
                if (mutation.addedNodes.length > 0) {
                    setTimeout(applyMasonryLayout, 100);
                }
            });
        });
        
        observer.observe(masonryContainer, {
            childList: true,
            subtree: true
        });
    }
    
    function getColumns() {
        var width = window.innerWidth;
        if (width >= 1200) return 4;
        if (width >= 900) return 3;
        if (width >= 600) return 2;
        return 1;
    }
    
    function applyMasonryLayout() {
        if (!masonryContainer) return;
        
        var items = Array.from(masonryContainer.querySelectorAll('.post-card-wrap'));
        if (items.length === 0) return;
        
        columns = getColumns();
        var containerWidth = masonryContainer.offsetWidth;
        var columnWidth = (containerWidth - (columnGap * (columns - 1))) / columns;
        
        // Initialize column heights
        var columnHeights = new Array(columns).fill(0);
        
        items.forEach(function(item, index) {
            // Remove any existing column classes
            item.className = item.className.replace(/\s*column\s+medium-\d+\s+large-\d+/g, '');
            
            // Apply absolute positioning
            item.style.position = 'absolute';
            item.style.width = columnWidth + 'px';
            
            // Find shortest column
            var shortestColumn = 0;
            var minHeight = columnHeights[0];
            
            for (var i = 1; i < columns; i++) {
                if (columnHeights[i] < minHeight) {
                    minHeight = columnHeights[i];
                    shortestColumn = i;
                }
            }
            
            // Position item
            var x = shortestColumn * (columnWidth + columnGap);
            var y = columnHeights[shortestColumn];
            
            item.style.left = x + 'px';
            item.style.top = y + 'px';
            
            // Update column height
            columnHeights[shortestColumn] += item.offsetHeight + columnGap;
        });
        
        // Set container height
        var maxHeight = Math.max.apply(null, columnHeights);
        masonryContainer.style.height = maxHeight + 'px';
    }
    
    // Initialize when DOM is ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }
    
    // Export for external use
    window.applyMasonryLayout = applyMasonryLayout;
})();