#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
기존 View 라이브러리 전수 조사 및 업데이트 스크립트
"""

import os
import re
import time
import urllib.request
import urllib.error
import json
from datetime import datetime

def extract_github_repo(file_path):
    """포스트 파일에서 GitHub 저장소 정보 추출"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
        
    # link 추출
    link_match = re.search(r"link:\s*'([^']+)'", content)
    if link_match:
        link = link_match.group(1)
        # GitHub URL에서 owner/repo 추출
        repo_match = re.search(r'github\.com/([^/]+/[^/]+)', link)
        if repo_match:
            return repo_match.group(1).rstrip('/')
    
    # remote_markdown URL에서도 시도
    remote_match = re.search(r'github\.com/([^/]+/[^/]+)/', content)
    if remote_match:
        return remote_match.group(1)
    
    return None

def check_github_status(repo):
    """GitHub 저장소 상태 확인"""
    api_url = f"https://api.github.com/repos/{repo}"
    
    try:
        req = urllib.request.Request(api_url, headers={
            'Accept': 'application/vnd.github.v3+json',
            'User-Agent': 'AndroidUICollection/1.0'
        })
        
        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read().decode('utf-8'))
            return {
                'exists': True,
                'stars': data.get('stargazers_count', 0),
                'last_update': data.get('updated_at', ''),
                'archived': data.get('archived', False),
                'description': data.get('description', ''),
                'language': data.get('language', ''),
                'topics': data.get('topics', [])
            }
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return {'exists': False}
        print(f"HTTP Error {e.code} checking {repo}")
    except Exception as e:
        print(f"Error checking {repo}: {e}")
    
    return {'exists': 'unknown'}

def find_images_in_readme(repo):
    """README에서 이미지 찾기"""
    readme_urls = [
        f"https://raw.githubusercontent.com/{repo}/master/README.md",
        f"https://raw.githubusercontent.com/{repo}/main/README.md",
        f"https://raw.githubusercontent.com/{repo}/develop/README.md"
    ]
    
    for url in readme_urls:
        try:
            req = urllib.request.Request(url, headers={
                'User-Agent': 'AndroidUICollection/1.0'
            })
            with urllib.request.urlopen(req, timeout=10) as response:
                content = response.read().decode('utf-8')
                
                # 이미지 URL 패턴 찾기
                images = []
                
                # GIF 우선
                gif_pattern = r'https?://[^\s\)]+\.gif'
                gifs = re.findall(gif_pattern, content)
                images.extend([(url, 'gif') for url in gifs])
                
                # PNG/JPG
                img_pattern = r'https?://[^\s\)]+\.(png|jpg|jpeg)'
                imgs = re.findall(img_pattern, content)
                images.extend([(url, url.split('.')[-1]) for url in imgs])
                
                # 상대 경로 이미지
                relative_pattern = r'!\[.*?\]\(([^\)]+\.(gif|png|jpg|jpeg))\)'
                relatives = re.findall(relative_pattern, content)
                for rel_path, ext in relatives:
                    if not rel_path.startswith('http'):
                        base_url = f"https://raw.githubusercontent.com/{repo}/master/"
                        images.append((base_url + rel_path, ext))
                
                return images[:5]  # 최대 5개
                
        except Exception:
            continue
    
    return []

def suggest_tags(library_info, title):
    """라이브러리 정보를 기반으로 태그 제안"""
    tags = set()
    
    # 기본 태그
    tags.add('view')
    
    # GitHub topics 활용
    if 'topics' in library_info:
        for topic in library_info['topics']:
            if 'android' not in topic.lower() and len(topic) > 2:
                tags.add(topic.lower().replace('-', ''))
    
    # 제목 기반 태그
    title_lower = title.lower()
    
    # UI 컴포넌트 타입
    ui_types = {
        'loading': ['loading', 'loader', 'progress'],
        'indicator': ['indicator', 'page'],
        'calendar': ['calendar', 'date', 'time'],
        'animation': ['animation', 'animated', 'animate'],
        'menu': ['menu', 'drawer', 'navigation'],
        'button': ['button', 'btn', 'fab'],
        'dialog': ['dialog', 'alert', 'popup'],
        'picker': ['picker', 'select', 'choose'],
        'chart': ['chart', 'graph'],
        'list': ['list', 'recycler', 'table'],
        'card': ['card'],
        'material': ['material'],
        'fab': ['fab', 'floating'],
        'progressbar': ['progress', 'loading'],
        'switch': ['switch', 'toggle'],
        'tab': ['tab'],
        'swipe': ['swipe', 'slide'],
        'effect': ['effect', 'blur', 'shadow'],
        'image': ['image', 'photo', 'picture'],
        'text': ['text', 'textview', 'label']
    }
    
    for tag, keywords in ui_types.items():
        if any(keyword in title_lower for keyword in keywords):
            tags.add(tag)
    
    # 설명 기반 태그
    if 'description' in library_info and library_info['description']:
        desc_lower = library_info['description'].lower()
        for tag, keywords in ui_types.items():
            if any(keyword in desc_lower for keyword in keywords):
                tags.add(tag)
    
    return sorted(list(tags))

def update_post_file(file_path, tags, image_info=None):
    """포스트 파일 업데이트"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 태그 업데이트
    new_tags = ", ".join(tags)
    content = re.sub(r'tag:\s*\[[^\]]*\]', f'tag: [{new_tags}]', content)
    
    # 이미지 업데이트 (필요시)
    if image_info:
        old_image = re.search(r"image:\s*'([^']+)'", content)
        if old_image:
            # 기존 이미지 확장자 확인
            old_ext = old_image.group(1).split('.')[-1]
            new_ext = image_info[1]
            if old_ext != new_ext:
                content = re.sub(
                    r"image:\s*'[^']+'", 
                    f"image: '{old_image.group(1).replace(f'.{old_ext}', f'.{new_ext}')}'", 
                    content
                )
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

def main():
    """메인 실행 함수"""
    posts_dir = "_posts"
    results = {
        'total': 0,
        'active': 0,
        'archived': 0,
        'not_found': 0,
        'updated': 0,
        'needs_image': []
    }
    
    # Compose 포스트 제외
    posts = [f for f in os.listdir(posts_dir) if f.endswith('.md') and not f.startswith('2024-01')]
    posts.sort()
    
    print(f"🔍 기존 View 라이브러리 전수 조사 시작")
    print(f"📚 총 {len(posts)}개 라이브러리\n")
    
    for i, post_file in enumerate(posts, 1):
        file_path = os.path.join(posts_dir, post_file)
        title = post_file.replace('.md', '').split('-', 3)[-1]
        
        print(f"\n[{i}/{len(posts)}] {title}")
        results['total'] += 1
        
        # GitHub 저장소 추출
        repo = extract_github_repo(file_path)
        if not repo:
            print("  ❌ GitHub 저장소를 찾을 수 없음")
            continue
        
        print(f"  📍 저장소: {repo}")
        
        # GitHub 상태 확인
        status = check_github_status(repo)
        
        if status['exists'] == False:
            print("  ❌ 저장소가 존재하지 않음 (삭제됨)")
            results['not_found'] += 1
            continue
        elif status['exists'] == 'unknown':
            print("  ⚠️  상태 확인 실패")
            continue
        
        # 상태 출력
        print(f"  ⭐ Stars: {status['stars']:,}")
        print(f"  📅 최종 업데이트: {status['last_update'][:10]}")
        
        if status['archived']:
            print("  🗄️  보관됨 (Archived)")
            results['archived'] += 1
        else:
            results['active'] += 1
        
        # 태그 제안
        suggested_tags = suggest_tags(status, title)
        print(f"  🏷️  추천 태그: {', '.join(suggested_tags)}")
        
        # 이미지 찾기
        images = find_images_in_readme(repo)
        if images:
            print(f"  📷 발견된 이미지: {len(images)}개")
            # 첫 번째 이미지 정보 저장
            image_url, ext = images[0]
            results['needs_image'].append({
                'post': post_file,
                'title': title,
                'image_url': image_url,
                'ext': ext
            })
        else:
            print("  ⚠️  이미지를 찾을 수 없음")
        
        # 포스트 파일 업데이트
        try:
            update_post_file(file_path, suggested_tags)
            results['updated'] += 1
            print("  ✅ 태그 업데이트 완료")
        except Exception as e:
            print(f"  ❌ 업데이트 실패: {e}")
        
        # API 제한 방지
        time.sleep(1)
    
    # 결과 요약
    print("\n" + "="*50)
    print("📊 전수 조사 결과")
    print(f"  총 라이브러리: {results['total']}")
    print(f"  활성 상태: {results['active']}")
    print(f"  보관됨: {results['archived']}")
    print(f"  삭제됨: {results['not_found']}")
    print(f"  업데이트됨: {results['updated']}")
    print(f"  이미지 필요: {len(results['needs_image'])}")
    
    # 이미지 다운로드 필요 목록 저장
    if results['needs_image']:
        with open('need_images.txt', 'w', encoding='utf-8') as f:
            f.write("# 이미지 다운로드 필요 목록\n\n")
            for item in results['needs_image']:
                f.write(f"{item['title']}\n")
                f.write(f"  파일: {item['post']}\n")
                f.write(f"  URL: {item['image_url']}\n")
                f.write(f"  확장자: {item['ext']}\n\n")
        print(f"\n📝 이미지 다운로드 목록이 need_images.txt에 저장되었습니다.")

if __name__ == "__main__":
    main()