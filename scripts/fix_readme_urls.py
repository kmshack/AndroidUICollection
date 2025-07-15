#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
README URL 수정 스크립트
"""

import os
import re
import urllib.request
import urllib.error

def check_readme_url(url):
    """URL이 유효한지 확인"""
    try:
        req = urllib.request.Request(url, headers={
            'User-Agent': 'AndroidUICollection/1.0'
        })
        with urllib.request.urlopen(req, timeout=5) as response:
            return response.getcode() == 200
    except:
        return False

def find_correct_readme_url(repo):
    """올바른 README URL 찾기"""
    branches = ['master', 'main', 'develop']
    filenames = ['README.md', 'readme.md', 'Readme.md']
    
    for branch in branches:
        for filename in filenames:
            url = f"https://raw.githubusercontent.com/{repo}/{branch}/{filename}"
            if check_readme_url(url):
                return url
    return None

def fix_post_readme_url(file_path, new_url):
    """포스트 파일의 README URL 수정"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # remote_markdown URL 수정
    content = re.sub(
        r'{% remote_markdown https://raw\.githubusercontent\.com/[^}]+\.md %}',
        f'{{% remote_markdown {new_url} %}}',
        content
    )
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

def main():
    """404 오류가 나는 라이브러리들 수정"""
    
    # 문제가 있는 라이브러리들
    problematic_libs = [
        ('2016-09-27-SpringIndicator.md', 'chenupt/SpringIndicator'),
        ('2024-01-15-ComposePreference.md', 'zhanghai/ComposePreference'),
        ('2024-01-15-ExplodingComposable.md', 'omkar-tenkale/ExplodingComposable'),
        ('2024-01-15-FloatingBubbleView.md', 'dofire/Floating-Bubble-View'),
        ('2024-01-15-WheelPickerCompose.md', 'commandiron/WheelPickerCompose')
    ]
    
    print("🔧 README URL 수정 시작...\n")
    
    for post_file, repo in problematic_libs:
        file_path = os.path.join('_posts', post_file)
        if not os.path.exists(file_path):
            print(f"❌ {post_file} - 파일이 존재하지 않음")
            continue
        
        print(f"📍 {post_file} ({repo})")
        
        # 올바른 URL 찾기
        correct_url = find_correct_readme_url(repo)
        
        if correct_url:
            print(f"  ✅ 올바른 URL 발견: {correct_url}")
            fix_post_readme_url(file_path, correct_url)
            print(f"  ✅ 수정 완료")
        else:
            print(f"  ❌ README를 찾을 수 없음")
            # 저장소 자체 확인
            api_url = f"https://api.github.com/repos/{repo}"
            try:
                req = urllib.request.Request(api_url, headers={
                    'User-Agent': 'AndroidUICollection/1.0'
                })
                with urllib.request.urlopen(req, timeout=5) as response:
                    print(f"  ℹ️  저장소는 존재하지만 README가 없음")
            except urllib.error.HTTPError as e:
                if e.code == 404:
                    print(f"  ⚠️  저장소가 삭제됨")
                else:
                    print(f"  ⚠️  오류: {e.code}")

if __name__ == "__main__":
    main()