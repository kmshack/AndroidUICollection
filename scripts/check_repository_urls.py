#!/usr/bin/env python3
"""
Script to check GitHub repository URLs and find the correct branch and README location.
"""

import requests
import json
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

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

def check_url(url, timeout=5):
    """Check if a URL is accessible."""
    try:
        response = requests.head(url, timeout=timeout, allow_redirects=True)
        return response.status_code == 200
    except:
        return False

def get_repo_info(repo_path):
    """Get repository information using GitHub API."""
    try:
        # First check if repo exists using API
        api_url = f"https://api.github.com/repos/{repo_path}"
        response = requests.get(api_url, timeout=5)
        
        if response.status_code == 404:
            return {"exists": False, "error": "Repository not found"}
        elif response.status_code != 200:
            return {"exists": False, "error": f"API error: {response.status_code}"}
            
        repo_data = response.json()
        default_branch = repo_data.get('default_branch', 'main')
        
        return {
            "exists": True,
            "default_branch": default_branch,
            "full_name": repo_data.get('full_name', repo_path),
            "archived": repo_data.get('archived', False),
            "private": repo_data.get('private', False)
        }
    except Exception as e:
        return {"exists": False, "error": str(e)}

def check_readme_variations(repo_path, branch):
    """Check different README URL variations."""
    base_url = f"https://raw.githubusercontent.com/{repo_path}"
    variations = [
        f"{base_url}/{branch}/README.md",
        f"{base_url}/{branch}/readme.md",
        f"{base_url}/{branch}/README.MD",
        f"{base_url}/{branch}/Readme.md",
        f"{base_url}/{branch}/README",
        f"{base_url}/{branch}/readme",
        f"{base_url}/{branch}/README.markdown",
        f"{base_url}/{branch}/readme.markdown",
        f"{base_url}/{branch}/README.rst",
        f"{base_url}/{branch}/readme.rst",
        f"{base_url}/{branch}/README.txt",
        f"{base_url}/{branch}/readme.txt"
    ]
    
    for url in variations:
        if check_url(url):
            return url
    return None

def process_repository(repo_path):
    """Process a single repository to find its correct URL."""
    print(f"\nChecking: {repo_path}")
    result = {
        "repository": repo_path,
        "status": "unknown",
        "details": {}
    }
    
    # Get repository info
    repo_info = get_repo_info(repo_path)
    
    if not repo_info["exists"]:
        result["status"] = "not_found"
        result["details"] = repo_info
        print(f"  ❌ Repository not found or inaccessible")
        return result
    
    if repo_info["private"]:
        result["status"] = "private"
        result["details"] = repo_info
        print(f"  🔒 Repository is private")
        return result
        
    if repo_info["archived"]:
        print(f"  ⚠️  Repository is archived")
    
    # Check for README in default branch
    default_branch = repo_info["default_branch"]
    print(f"  Default branch: {default_branch}")
    
    readme_url = check_readme_variations(repo_path, default_branch)
    
    if readme_url:
        result["status"] = "found"
        result["details"] = {
            **repo_info,
            "readme_url": readme_url,
            "suggested_url": readme_url
        }
        print(f"  ✅ Found README at: {readme_url}")
    else:
        # Try other common branches
        other_branches = ['main', 'master', 'develop', 'dev']
        other_branches = [b for b in other_branches if b != default_branch]
        
        for branch in other_branches:
            readme_url = check_readme_variations(repo_path, branch)
            if readme_url:
                result["status"] = "found"
                result["details"] = {
                    **repo_info,
                    "readme_url": readme_url,
                    "suggested_url": readme_url,
                    "note": f"Found in '{branch}' branch (not default)"
                }
                print(f"  ✅ Found README in '{branch}' branch: {readme_url}")
                break
        
        if result["status"] != "found":
            result["status"] = "no_readme"
            result["details"] = repo_info
            print(f"  ❌ No README found in any common location")
    
    time.sleep(0.1)  # Be nice to GitHub
    return result

def main():
    print("GitHub Repository URL Checker")
    print("=" * 50)
    print(f"Checking {len(REPOSITORIES)} repositories...")
    
    results = []
    
    # Process repositories with thread pool for faster execution
    with ThreadPoolExecutor(max_workers=5) as executor:
        future_to_repo = {executor.submit(process_repository, repo): repo 
                         for repo in REPOSITORIES}
        
        for future in as_completed(future_to_repo):
            try:
                result = future.result()
                results.append(result)
            except Exception as e:
                repo = future_to_repo[future]
                print(f"\n❌ Error processing {repo}: {str(e)}")
                results.append({
                    "repository": repo,
                    "status": "error",
                    "details": {"error": str(e)}
                })
    
    # Sort results by repository name
    results.sort(key=lambda x: x["repository"])
    
    # Save results to JSON file
    output_file = "repository_check_results.json"
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\n\nResults saved to: {output_file}")
    
    # Print summary
    print("\n" + "=" * 50)
    print("SUMMARY")
    print("=" * 50)
    
    status_counts = {}
    for result in results:
        status = result["status"]
        status_counts[status] = status_counts.get(status, 0) + 1
    
    for status, count in sorted(status_counts.items()):
        print(f"{status}: {count}")
    
    # Print suggested fixes
    print("\n" + "=" * 50)
    print("SUGGESTED FIXES FOR _posts FILES")
    print("=" * 50)
    
    for result in results:
        if result["status"] == "found":
            repo = result["repository"]
            suggested_url = result["details"]["suggested_url"]
            print(f"\n{repo}:")
            print(f"  {{% remote_markdown {suggested_url} %}}")
        elif result["status"] == "not_found":
            print(f"\n{result['repository']}:")
            print(f"  ❌ Repository not found - consider removing or finding alternative")
        elif result["status"] == "no_readme":
            print(f"\n{result['repository']}:")
            print(f"  ❌ No README found - check repository manually")

if __name__ == "__main__":
    main()