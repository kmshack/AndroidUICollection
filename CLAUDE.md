# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

AndroidUICollection is a Jekyll-based static website that showcases open-source Android UI libraries and components. The site is hosted at https://kmshack.github.io/AndroidUICollection

## Common Commands

### Development
```bash
# Install dependencies
bundle install

# Run local development server
bundle exec jekyll serve

# Build the site
bundle exec jekyll build
```

### Adding New UI Libraries
To add a new Android UI library to the collection:
1. Create a new markdown file in `_posts/` with format: `YYYY-MM-DD-LibraryName.md`
2. Use the following front matter structure:
```yaml
---
layout: post
title: LibraryName
featured: true
image: '/images/posts/YYYY-MM-DD-LibraryName.gif'
tag: [relevant, tags, here]
link: 'https://github.com/username/repository'
---

{% remote_markdown https://raw.githubusercontent.com/username/repository/master/README.md %}
```
3. Add the demonstration GIF to `images/posts/`

## Architecture

### Key Components

1. **Remote Markdown Plugin** (`_plugins/remote_markdown.rb`): Fetches README files from GitHub repositories dynamically. Note: It removes all exclamation marks from fetched markdown to prevent image loading issues.

2. **Post Structure**: Each post represents one Android UI library with:
   - Metadata in Jekyll front matter
   - Animated GIF demonstration
   - Dynamically fetched README content from the original repository

3. **Site Configuration** (`_config.yml`):
   - Base URL: `/AndroidUICollection`
   - Pagination: Infinite scrolling
   - Plugins: jekyll-paginate, jekyll-tagging

### Directory Structure
- `_posts/`: Individual UI library showcases (2016-2019)
- `_layouts/`: Jekyll templates (default, page, post, tag_page)
- `_includes/`: Reusable components (analytics, pagination, sidebar)
- `images/posts/`: GIF demonstrations of UI libraries
- `_sass/` & `css/`: Styling (SCSS)
- `js/`: JavaScript functionality (jQuery, search)

### Deployment
The site uses GitHub Pages for hosting. Any push to the repository will trigger a rebuild and deployment.
