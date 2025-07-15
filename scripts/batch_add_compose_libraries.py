#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Android UI Collection - Compose 라이브러리 일괄 추가 스크립트
사용법: python3 batch_add_compose_libraries.py
"""

import os
import json
import requests
from datetime import datetime
import time

# 추가할 라이브러리 목록
LIBRARIES = [
    {
        "name": "Landscapist",
        "repo": "skydoves/Landscapist",
        "tags": ["compose", "image", "loading", "coil", "glide"],
        "description": "Jetpack Compose image loading library"
    },
    {
        "name": "Accompanist",
        "repo": "google/accompanist",
        "tags": ["compose", "google", "utilities", "permissions"],
        "description": "A collection of extension libraries for Jetpack Compose"
    },
    {
        "name": "Compose-Multiplatform-iOS-Android-Template",
        "repo": "JetBrains/compose-multiplatform-ios-android-template",
        "tags": ["compose", "multiplatform", "kotlin", "template"],
        "description": "Compose Multiplatform iOS+Android Application project template"
    },
    # 더 많은 라이브러리 추가...
]

def create_post_file(library, date):
    """포스트 파일 생성"""
    tags = ", ".join(library["tags"])
    content = f"""---
layout: post
title: {library["name"]}
featured: true
image: '/images/posts/{library["name"]}.gif'
tag: [{tags}]
link: 'https://github.com/{library["repo"]}'
---

{{% remote_markdown https://raw.githubusercontent.com/{library["repo"]}/main/README.md %}}"""
    
    filename = f"_posts/{date}-{library['name']}.md"
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)
    
    return filename

def find_image_in_readme(repo):
    """README에서 이미지 URL 찾기"""
    # main 브랜치 시도
    readme_urls = [
        f"https://raw.githubusercontent.com/{repo}/main/README.md",
        f"https://raw.githubusercontent.com/{repo}/master/README.md"
    ]
    
    for url in readme_urls:
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                content = response.text
                
                # 이미지 URL 패턴 찾기
                import re
                # GIF 우선
                gif_pattern = r'https?://[^\s\)]+\.gif'
                gifs = re.findall(gif_pattern, content)
                if gifs:
                    return gifs[0], 'gif'
                
                # PNG/JPG
                img_pattern = r'https?://[^\s\)]+\.(png|jpg|jpeg)'
                imgs = re.findall(img_pattern, content)
                if imgs:
                    return imgs[0][0], imgs[0][1]
                
                # 상대 경로 이미지
                relative_pattern = r'!\[.*?\]\(([^\)]+\.(gif|png|jpg|jpeg))\)'
                relatives = re.findall(relative_pattern, content)
                if relatives:
                    relative_path = relatives[0][0]
                    ext = relatives[0][1]
                    # 상대 경로를 절대 경로로 변환
                    base_url = f"https://raw.githubusercontent.com/{repo}/main/"
                    return base_url + relative_path, ext
                    
        except Exception as e:
            print(f"  ⚠️  README 접근 실패: {e}")
            continue
    
    return None, None

def download_image(url, filename):
    """이미지 다운로드"""
    try:
        response = requests.get(url, timeout=30)
        if response.status_code == 200:
            with open(filename, 'wb') as f:
                f.write(response.content)
            return True
    except Exception as e:
        print(f"  ❌ 다운로드 실패: {e}")
    return False

def main():
    """메인 실행 함수"""
    date = datetime.now().strftime("%Y-%m-%d")
    
    print("🚀 Android UI Collection - Compose 라이브러리 일괄 추가")
    print(f"📅 날짜: {date}")
    print(f"📚 추가할 라이브러리: {len(LIBRARIES)}개\n")
    
    success_count = 0
    
    for i, library in enumerate(LIBRARIES, 1):
        print(f"\n[{i}/{len(LIBRARIES)}] {library['name']}")
        print(f"  📍 저장소: {library['repo']}")
        
        # 포스트 파일 생성
        try:
            post_file = create_post_file(library, date)
            print(f"  ✅ 포스트 생성: {post_file}")
        except Exception as e:
            print(f"  ❌ 포스트 생성 실패: {e}")
            continue
        
        # 이미지 찾기 및 다운로드
        print("  🔍 이미지 검색 중...")
        image_url, ext = find_image_in_readme(library['repo'])
        
        if image_url:
            print(f"  📷 이미지 발견: {image_url}")
            image_filename = f"images/posts/{library['name']}.{ext}"
            
            if download_image(image_url, image_filename):
                print(f"  ✅ 이미지 저장: {image_filename}")
                
                # 확장자가 gif가 아닌 경우 포스트 파일 업데이트
                if ext != 'gif':
                    with open(post_file, 'r', encoding='utf-8') as f:
                        content = f.read()
                    content = content.replace(f"{library['name']}.gif", f"{library['name']}.{ext}")
                    with open(post_file, 'w', encoding='utf-8') as f:
                        f.write(content)
                    print(f"  ✅ 포스트 파일 이미지 확장자 업데이트")
                
                success_count += 1
            else:
                print(f"  ⚠️  이미지 다운로드 실패")
        else:
            print(f"  ⚠️  이미지를 찾을 수 없음")
        
        # API 제한 방지를 위한 지연
        time.sleep(1)
    
    print(f"\n✨ 완료! 성공: {success_count}/{len(LIBRARIES)}")
    print("\n📋 다음 단계:")
    print("1. 이미지가 없는 라이브러리는 수동으로 추가")
    print("2. bundle exec jekyll build 실행")
    print("3. 사이트 확인")

if __name__ == "__main__":
    main()