#!/usr/bin/env python3
import os
from datetime import datetime

libraries = [
    ("peekaboo", "https://github.com/TEAM-PREAT/peekaboo", ["compose", "multiplatform", "image-picker"]),
    ("material3-windowsizeclass-multiplatform", "https://github.com/chrisbanes/material3-windowsizeclass-multiplatform", ["compose", "multiplatform", "material3"]),
    ("compose-destinations", "https://github.com/raamcosta/compose-destinations", ["compose", "navigation", "ksp"]),
    ("compose-animated-navigationbar", "https://github.com/canopas/compose-animated-navigationbar", ["compose", "navigation", "animation"]),
    ("compose-recyclerview", "https://github.com/canopas/compose-recyclerview", ["compose", "recyclerview", "interop"]),
    ("rich-editor-compose", "https://github.com/canopas/rich-editor-compose", ["compose", "editor", "wysiwyg"]),
    ("gemini-android", "https://github.com/skydoves/gemini-android", ["compose", "ai", "chat"]),
    ("PrevGen", "https://github.com/Vram-Voskanyan/PrevGen", ["compose", "preview", "generator"]),
    ("squiggly-slider", "https://github.com/saket/squiggly-slider", ["compose", "slider", "animation"]),
    ("Minesweeper", "https://github.com/arkivanov/Minesweeper", ["compose", "multiplatform", "game"]),
    ("PhotoView", "https://github.com/GetStream/photoview-android", ["compose", "image", "zoom"]),
    ("Vico", "https://github.com/patrykandpatrick/vico", ["compose", "chart", "visualization"]),
    ("ComposeOClock", "https://github.com/Splitties/ComposeOClock", ["compose", "wearos", "watchface"]),
    ("ComposeInvestigator", "https://github.com/jisungbin/ComposeInvestigator", ["compose", "debugging", "recomposition"]),
    ("composable-sheep-lib", "https://github.com/nicole-terc/composable-sheep-lib", ["compose", "animation", "fun"]),
    ("compose-report-to-html", "https://github.com/PatilShreyas/compose-report-to-html", ["compose", "gradle", "reporting"]),
    ("pokedex-compose", "https://github.com/skydoves/pokedex-compose", ["compose", "demo", "pokemon"]),
    ("compose-menu", "https://github.com/composablehorizons/compose-menu", ["compose", "multiplatform", "menu"]),
    ("ComposeGuard", "https://github.com/j-roskopf/ComposeGuard", ["compose", "gradle", "regression"]),
    ("soil", "https://github.com/soil-kt/soil", ["compose", "multiplatform", "architecture"]),
    ("Jetmagic", "https://github.com/JohannRosenberg/Jetmagic", ["compose", "responsive", "framework"]),
    ("LuckyWheelView", "https://github.com/caneryilmaz52/LuckyWheelView", ["kotlin", "wheel", "animation"]),
    ("Dropdown", "https://github.com/AndroidPoet/Dropdown", ["compose", "multiplatform", "dropdown"]),
    ("MBCompass", "https://github.com/Kashif-E/MBCompass", ["compose", "compass", "ui"]),
    ("landscapist", "https://github.com/skydoves/landscapist", ["compose", "image", "loading"]),
    ("LazyTimetable", "https://github.com/qamarelsafadi/LazyTimetable", ["compose", "timetable", "calendar"]),
    ("material-you-grid", "https://github.com/SimplyBuilt/material-you-grid", ["compose", "material3", "grid"]),
    ("RelayMe", "https://github.com/buggily/RelayMe", ["compose", "game", "multiplatform"]),
    ("vec2compose", "https://github.com/LennartEgb/vec2compose", ["compose", "svg", "converter"]),
    ("cloudy", "https://github.com/skydoves/cloudy", ["compose", "blur", "effect"]),
    ("reveal", "https://github.com/svenjacobs/reveal", ["compose", "multiplatform", "swipe"]),
    ("Ksoup", "https://github.com/MohamedRejeb/Ksoup", ["multiplatform", "html", "parser"]),
    ("shimmer-compose-multiplatform", "https://github.com/TEAM-PREAT/shimmer-compose-multiplatform", ["compose", "multiplatform", "shimmer"]),
    ("sandwich", "https://github.com/skydoves/sandwich", ["kotlin", "network", "retrofit"]),
    ("Valkyrie", "https://github.com/ComposeGears/Valkyrie", ["compose", "svg", "converter"]),
    ("ComposableScreens", "https://github.com/composablehorizons/composable-screens", ["compose", "ui", "design"]),
    ("CinematicEffect", "https://github.com/thisismesebin/CinematicEffect", ["compose", "filter", "camera"]),
    ("FancyGrid", "https://github.com/PedroOkawa/fancy-grid", ["compose", "grid", "layout"]),
    ("HackerNewsMultiplatform", "https://github.com/SimonSchubert/HackerNewsMultiplatform", ["compose", "multiplatform", "demo"]),
    ("kmpnotifier", "https://github.com/mirzemehdi/kmpnotifier", ["multiplatform", "notification", "push"]),
    ("Scratchify", "https://github.com/kabirnayeem99/scratchify", ["compose", "multiplatform", "scratch-card"]),
    ("ElegantOTP", "https://github.com/raheemadamboev/elegant-otp", ["compose", "otp", "input"]),
    ("compose-multiplatform-mesh-gradient", "https://github.com/KevinnZou/compose-multiplatform-mesh-gradient", ["compose", "multiplatform", "gradient"]),
    ("AudioWaveformView", "https://github.com/massoudss/audioWaveformView", ["android", "audio", "waveform"]),
    ("jnovel", "https://github.com/Timurea/jnovel", ["compose", "multiplatform", "reader"]),
    ("ClickClickUp", "https://github.com/PedroOkawa/click-click-up", ["compose", "game", "clicker"]),
    ("ComposeKit", "https://github.com/ra0321/ComposeKit", ["compose", "multiplatform", "components"]),
    ("ComposeHabitToolkit", "https://github.com/skydoves/ComposeHabitToolkit", ["compose", "demo", "habits"]),
    ("ComposeDesktop2040", "https://github.com/zach-klippenstein/ComposeDesktop2040", ["compose", "desktop", "piano"]),
    ("FigmaToCompose", "https://github.com/goo-ood/FigmaToCompose", ["compose", "figma", "converter"]),
    ("KmpAuth", "https://github.com/mirzemehdi/KmpAuth", ["multiplatform", "authentication", "social"]),
    ("compose-tooltip", "https://github.com/skydoves/compose-tooltip", ["compose", "tooltip", "ui"]),
    ("paging-multiplatform", "https://github.com/cashapp/paging-multiplatform", ["multiplatform", "paging", "compose"]),
    ("ComposeScrollbars", "https://github.com/GIGAMOLE/ComposeScrollbars", ["compose", "scrollbar", "multiplatform"]),
    ("ComposeNestedScroll", "https://github.com/skydoves/ComposeNestedScroll", ["compose", "scroll", "nested"]),
    ("lazybones", "https://github.com/BuggieSlugger/lazybones", ["compose", "forms", "validation"])
]

def create_post_file(name, url, tags):
    # Get repository owner and name from URL
    parts = url.replace("https://github.com/", "").split("/")
    owner = parts[0]
    repo = parts[1] if len(parts) > 1 else name
    
    # Create date
    date = "2024-01-15"
    
    # Generate filename
    filename = f"{date}-{name.replace('-', '').replace('_', '').title()}.md"
    filepath = os.path.join("_posts", filename)
    
    # Skip if file already exists
    if os.path.exists(filepath):
        print(f"Skipping {filename} - already exists")
        return
    
    # Generate post content
    content = f"""---
layout: post
title: {name}
featured: true
image: '/images/posts/{name}.gif'
tag: {tags}
link: '{url}'
---

{{% remote_markdown https://raw.githubusercontent.com/{owner}/{repo}/master/README.md %}}
"""
    
    # Write file
    with open(filepath, 'w') as f:
        f.write(content)
    
    print(f"Created {filename}")

# Create posts directory if it doesn't exist
os.makedirs("_posts", exist_ok=True)

# Process all libraries
for name, url, tags in libraries:
    create_post_file(name, url, tags)

print("\nDone! Created post files for all libraries.")
print("\nNote: You'll need to add demonstration images (GIF/PNG) for each library to the images/posts/ directory.")