$(document).ready(function() {

  'use strict';

  // =================
  // Responsive videos
  // =================

  $('.post-content').fitVids();

  // ===============
  // Off Canvas menu
  // ===============

  $('.off-canvas-toggle').click(function(e) {
    e.preventDefault();
    $('.off-canvas-container').toggleClass('is-active');
  });

  // ======
  // Search
  // ======

  var search_field = $('.search-form__field'),
      search_results = $('.search-results'),
      toggle_search = $('.toggle-search-button'),
      close_search = $('.close-search-button'),
      search_result_template = "\
        <div class='search-results__item'>\
          <a class='search-results__item__title' href='{{link}}'>{{title}}</a>\
          <span class='post__date'>{{pubDate}}</span>\
        </div>";

  toggle_search.click(function(e) {
    e.preventDefault();
    $('.search-form-container').addClass('is-active');

    // If off-canvas is active, just disable it
    $('.off-canvas-container').removeClass('is-active');

    setTimeout(function() {
      search_field.focus();
    }, 500);
  });

  $('.search-form-container, .close-search-button').on('click keyup', function(event) {
    if (event.target == this || event.target.className == 'close-search-button' || event.keyCode == 27) {
      $('.search-form-container').removeClass('is-active');
    }
  });

  search_field.ghostHunter({
    results: search_results,
    onKeyUp         : true,
    rss             : base_url + '/feed.xml',
    zeroResultsInfo : false,
    info_template   : "<h4 class='heading'>Number of posts found: {{amount}}</h4>",
    result_template : search_result_template,
    before: function() {
      search_results.fadeIn();
    }
  });

});