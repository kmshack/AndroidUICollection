#!/usr/bin/env python3
import os
import requests
import re
from urllib.parse import urlparse

# List of libraries with their GitHub URLs
libraries = [
    ("peekaboo", "https://github.com/TEAM-PREAT/peekaboo"),
    ("material3-windowsizeclass-multiplatform", "https://github.com/chrisbanes/material3-windowsizeclass-multiplatform"),
    ("compose-destinations", "https://github.com/raamcosta/compose-destinations"),
    ("compose-animated-navigationbar", "https://github.com/canopas/compose-animated-navigationbar"),
    ("compose-recyclerview", "https://github.com/canopas/compose-recyclerview"),
    ("rich-editor-compose", "https://github.com/canopas/rich-editor-compose"),
    ("gemini-android", "https://github.com/skydoves/gemini-android"),
    ("PrevGen", "https://github.com/Vram-Voskanyan/PrevGen"),
    ("squiggly-slider", "https://github.com/saket/squiggly-slider"),
    ("Minesweeper", "https://github.com/arkivanov/Minesweeper"),
    ("PhotoView", "https://github.com/GetStream/photoview-android"),
    ("Vico", "https://github.com/patrykandpatrick/vico"),
    ("ComposeOClock", "https://github.com/Splitties/ComposeOClock"),
    ("ComposeInvestigator", "https://github.com/jisungbin/ComposeInvestigator"),
    ("composable-sheep-lib", "https://github.com/nicole-terc/composable-sheep-lib"),
    ("compose-report-to-html", "https://github.com/PatilShreyas/compose-report-to-html"),
    ("pokedex-compose", "https://github.com/skydoves/pokedex-compose"),
    ("compose-menu", "https://github.com/composablehorizons/compose-menu"),
    ("ComposeGuard", "https://github.com/j-roskopf/ComposeGuard"),
    ("soil", "https://github.com/soil-kt/soil"),
    ("Jetmagic", "https://github.com/JohannRosenberg/Jetmagic"),
    ("LuckyWheelView", "https://github.com/caneryilmaz52/LuckyWheelView"),
    ("Dropdown", "https://github.com/AndroidPoet/Dropdown"),
    ("landscapist", "https://github.com/skydoves/landscapist"),
    ("material-you-grid", "https://github.com/SimplyBuilt/material-you-grid"),
    ("RelayMe", "https://github.com/buggily/RelayMe"),
    ("vec2compose", "https://github.com/LennartEgb/vec2compose"),
    ("cloudy", "https://github.com/skydoves/cloudy"),
    ("reveal", "https://github.com/svenjacobs/reveal"),
    ("Ksoup", "https://github.com/MohamedRejeb/Ksoup"),
    ("shimmer-compose-multiplatform", "https://github.com/TEAM-PREAT/shimmer-compose-multiplatform"),
    ("sandwich", "https://github.com/skydoves/sandwich"),
    ("Valkyrie", "https://github.com/ComposeGears/Valkyrie"),
    ("ComposableScreens", "https://github.com/composablehorizons/composable-screens"),
    ("CinematicEffect", "https://github.com/thisismesebin/CinematicEffect"),
    ("FancyGrid", "https://github.com/PedroOkawa/fancy-grid"),
    ("HackerNewsMultiplatform", "https://github.com/SimonSchubert/HackerNewsMultiplatform"),
    ("kmpnotifier", "https://github.com/mirzemehdi/kmpnotifier"),
    ("Scratchify", "https://github.com/kabirnayeem99/scratchify"),
    ("ElegantOTP", "https://github.com/raheemadamboev/elegant-otp"),
    ("compose-multiplatform-mesh-gradient", "https://github.com/KevinnZou/compose-multiplatform-mesh-gradient"),
    ("AudioWaveformView", "https://github.com/massoudss/audioWaveformView"),
    ("jnovel", "https://github.com/Timurea/jnovel"),
    ("ClickClickUp", "https://github.com/PedroOkawa/click-click-up"),
    ("ComposeKit", "https://github.com/ra0321/ComposeKit"),
    ("ComposeHabitToolkit", "https://github.com/skydoves/ComposeHabitToolkit"),
    ("ComposeDesktop2040", "https://github.com/zach-klippenstein/ComposeDesktop2040"),
    ("FigmaToCompose", "https://github.com/goo-ood/FigmaToCompose"),
    ("KmpAuth", "https://github.com/mirzemehdi/KmpAuth"),
    ("compose-tooltip", "https://github.com/skydoves/compose-tooltip"),
    ("paging-multiplatform", "https://github.com/cashapp/paging-multiplatform"),
    ("ComposeScrollbars", "https://github.com/GIGAMOLE/ComposeScrollbars"),
    ("ComposeNestedScroll", "https://github.com/skydoves/ComposeNestedScroll"),
    ("lazybones", "https://github.com/BuggieSlugger/lazybones")
]

def get_readme_url(github_url):
    """Convert GitHub URL to raw README URL"""
    parts = github_url.replace("https://github.com/", "").split("/")
    owner = parts[0]
    repo = parts[1] if len(parts) > 1 else ""
    return f"https://raw.githubusercontent.com/{owner}/{repo}/master/README.md"

def find_image_urls(readme_content, github_url):
    """Find all image URLs in README content"""
    # Pattern to find image URLs in markdown
    pattern = r'!\[.*?\]\((.*?)\)'
    urls = re.findall(pattern, readme_content)
    
    # Also find direct image links
    img_pattern = r'(https?://[^\s]+\.(?:gif|png|jpg|jpeg|webp))'
    direct_urls = re.findall(img_pattern, readme_content, re.IGNORECASE)
    
    all_urls = urls + direct_urls
    
    # Convert relative URLs to absolute
    absolute_urls = []
    for url in all_urls:
        if url.startswith('http'):
            absolute_urls.append(url)
        elif url.startswith('/'):
            # Relative to repo root
            parts = github_url.replace("https://github.com/", "").split("/")
            owner = parts[0]
            repo = parts[1] if len(parts) > 1 else ""
            absolute_urls.append(f"https://raw.githubusercontent.com/{owner}/{repo}/master{url}")
        else:
            # Relative to README location
            parts = github_url.replace("https://github.com/", "").split("/")
            owner = parts[0]
            repo = parts[1] if len(parts) > 1 else ""
            absolute_urls.append(f"https://raw.githubusercontent.com/{owner}/{repo}/master/{url}")
    
    return absolute_urls

def download_image(url, filename):
    """Download image from URL"""
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            with open(filename, 'wb') as f:
                f.write(response.content)
            return True
    except Exception as e:
        print(f"Error downloading {url}: {e}")
    return False

# Create images directory if it doesn't exist
os.makedirs("images/posts", exist_ok=True)

print("Searching for and downloading images from GitHub repositories...\n")

for name, github_url in libraries:
    # Check if image already exists
    existing_files = [f for f in os.listdir("images/posts") if f.startswith(name)]
    if existing_files:
        print(f"✓ {name} - image already exists: {existing_files[0]}")
        continue
    
    print(f"Processing {name}...")
    
    # Get README content
    readme_url = get_readme_url(github_url)
    try:
        response = requests.get(readme_url, timeout=10)
        if response.status_code == 200:
            readme_content = response.text
            
            # Find image URLs
            image_urls = find_image_urls(readme_content, github_url)
            
            if image_urls:
                # Try to find the best image (prefer GIFs)
                gif_urls = [url for url in image_urls if '.gif' in url.lower()]
                if gif_urls:
                    selected_url = gif_urls[0]
                    ext = 'gif'
                else:
                    selected_url = image_urls[0]
                    ext = selected_url.split('.')[-1].split('?')[0].lower()
                    if ext not in ['png', 'jpg', 'jpeg', 'webp']:
                        ext = 'png'
                
                # Download the image
                filename = f"images/posts/{name}.{ext}"
                if download_image(selected_url, filename):
                    print(f"✓ Downloaded {filename}")
                else:
                    print(f"✗ Failed to download image for {name}")
            else:
                print(f"✗ No images found in README for {name}")
        else:
            print(f"✗ Could not fetch README for {name}")
    except Exception as e:
        print(f"✗ Error processing {name}: {e}")

print("\nDone! Check the images/posts directory for downloaded images.")
print("Note: Some libraries may not have images in their README. You may need to:")
print("1. Take screenshots manually")
print("2. Look for images in the repository's other directories")
print("3. Use placeholder images")