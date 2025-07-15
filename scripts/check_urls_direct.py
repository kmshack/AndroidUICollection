#!/usr/bin/env python3
"""
Direct URL checker for GitHub repositories without using API.
"""

import requests
import time

# List of repositories to check
REPOSITORIES = [
    "chenupt/SpringIndicator",
    "massoudss/audioWaveformView", 
    "thisismesebin/CinematicEffect",
    "PedroOkawa/click-click-up",
    "composablehorizons/composable-screens",
    "zach-klippenstein/ComposeDesktop2040",
    "skydoves/ComposeHabitToolkit",
    "ra0321/ComposeKit",
    "KevinnZou/compose-multiplatform-mesh-gradient",
    "skydoves/ComposeNestedScroll",
    "skydoves/compose-tooltip",
    "raheemadamboev/elegant-otp",
    "PedroOkawa/fancy-grid",
    "goo-ood/FigmaToCompose",
    "SimonSchubert/HackerNewsMultiplatform",
    "Timurea/jnovel",
    "BuggieSlugger/lazybones",
    "SimplyBuilt/material-you-grid",
    "cashapp/paging-multiplatform"
]

def check_url(url, timeout=10):
    """Check if a URL is accessible."""
    try:
        response = requests.get(url, timeout=timeout)
        return response.status_code == 200
    except:
        return False

def check_repository(repo_path):
    """Check different README URL variations for a repository."""
    print(f"\nChecking: {repo_path}")
    base_url = f"https://raw.githubusercontent.com/{repo_path}"
    
    # Common branch names to try
    branches = ['main', 'master', 'develop']
    
    # README file variations
    readme_files = [
        'README.md', 'readme.md', 'README.MD', 'Readme.md',
        'README', 'readme', 'README.markdown', 'readme.markdown'
    ]
    
    found_urls = []
    
    for branch in branches:
        for readme in readme_files:
            url = f"{base_url}/{branch}/{readme}"
            if check_url(url):
                found_urls.append(url)
                print(f"  ✅ Found: {url}")
                return url  # Return first working URL
            time.sleep(0.1)  # Be nice to GitHub
    
    if not found_urls:
        print(f"  ❌ No README found")
    
    return None

def main():
    print("Direct GitHub Repository URL Checker")
    print("=" * 50)
    print(f"Checking {len(REPOSITORIES)} repositories...")
    
    results = {}
    
    for repo in REPOSITORIES:
        working_url = check_repository(repo)
        results[repo] = working_url
        time.sleep(0.5)  # Additional delay between repositories
    
    # Print summary
    print("\n" + "=" * 50)
    print("WORKING URLs FOR _posts FILES")
    print("=" * 50)
    
    for repo, url in sorted(results.items()):
        if url:
            print(f"\n{repo}:")
            print(f"  {{% remote_markdown {url} %}}")
        else:
            print(f"\n{repo}:")
            print(f"  ❌ No working URL found")
    
    # Count statistics
    working_count = sum(1 for url in results.values() if url)
    print(f"\n\nFound working URLs for {working_count}/{len(REPOSITORIES)} repositories")

if __name__ == "__main__":
    main()