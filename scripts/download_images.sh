#!/bin/bash

# Create images directory if it doesn't exist
mkdir -p images/posts

echo "Downloading sample images for new UI libraries..."
echo "Note: These are placeholder images. You should replace them with actual screenshots/GIFs from each library."

# Download some placeholder images from the existing libraries as examples
# You can replace these with actual screenshots later

# List of new libraries that need images
libraries=(
    "peekaboo"
    "material3-windowsizeclass-multiplatform"
    "compose-destinations"
    "compose-animated-navigationbar"
    "compose-recyclerview"
    "rich-editor-compose"
    "gemini-android"
    "PrevGen"
    "squiggly-slider"
    "Minesweeper"
    "PhotoView"
    "Vico"
    "ComposeOClock"
    "ComposeInvestigator"
    "composable-sheep-lib"
    "compose-report-to-html"
    "pokedex-compose"
    "compose-menu"
    "ComposeGuard"
    "soil"
    "Jetmagic"
    "LuckyWheelView"
    "Dropdown"
    "landscapist"
    "material-you-grid"
    "RelayMe"
    "vec2compose"
    "cloudy"
    "reveal"
    "Ksoup"
    "shimmer-compose-multiplatform"
    "sandwich"
    "Valkyrie"
    "ComposableScreens"
    "CinematicEffect"
    "FancyGrid"
    "HackerNewsMultiplatform"
    "kmpnotifier"
    "Scratchify"
    "ElegantOTP"
    "compose-multiplatform-mesh-gradient"
    "AudioWaveformView"
    "jnovel"
    "ClickClickUp"
    "ComposeKit"
    "ComposeHabitToolkit"
    "ComposeDesktop2040"
    "FigmaToCompose"
    "KmpAuth"
    "compose-tooltip"
    "paging-multiplatform"
    "ComposeScrollbars"
    "ComposeNestedScroll"
    "lazybones"
)

# For now, copy an existing image as placeholder
# You should replace these with actual screenshots/GIFs from each library
for lib in "${libraries[@]}"; do
    if [ ! -f "images/posts/${lib}.gif" ] && [ ! -f "images/posts/${lib}.png" ]; then
        echo "Creating placeholder for ${lib}"
        # Copy an existing image as placeholder
        cp images/posts/ComposeCalendar.jpg "images/posts/${lib}.gif" 2>/dev/null || echo "  - Skipped (no source image found)"
    else
        echo "Image already exists for ${lib}"
    fi
done

echo ""
echo "Done! Placeholder images created."
echo ""
echo "IMPORTANT: You need to:"
echo "1. Visit each GitHub repository"
echo "2. Take screenshots or find GIFs demonstrating the UI"
echo "3. Replace the placeholder images in images/posts/"
echo ""
echo "Some suggested sources for images:"
echo "- README files in the repositories"
echo "- 'art' or 'screenshots' directories in the repos"
echo "- Demo apps or example projects"