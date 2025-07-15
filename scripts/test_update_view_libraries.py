#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
기존 View 라이브러리 전수 조사 테스트 (처음 10개만)
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

def suggest_tags(library_info, title, current_tags=[]):
    """라이브러리 정보를 기반으로 태그 제안"""
    tags = set()
    
    # 기본 태그
    tags.add('view')
    
    # 현재 태그 중 유효한 것 유지
    keep_tags = ['animation', 'material', 'loading', 'indicator', 'menu', 'calendar', 'picker']
    for tag in current_tags:
        if tag in keep_tags:
            tags.add(tag)
    
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
        'menu': ['menu', 'drawer', 'navigation', 'reside'],
        'button': ['button', 'btn', 'fab'],
        'dialog': ['dialog', 'alert', 'popup'],
        'picker': ['picker', 'select', 'choose'],
        'chart': ['chart', 'graph'],
        'list': ['list', 'recycler', 'table'],
        'card': ['card'],
        'material': ['material'],
        'fab': ['fab', 'floating'],
        'progress': ['progress', 'loading'],
        'switch': ['switch', 'toggle'],
        'tab': ['tab'],
        'swipe': ['swipe', 'slide', 'slidr'],
        'effect': ['effect', 'blur', 'shadow'],
        'image': ['image', 'photo', 'picture'],
        'text': ['text', 'textview', 'label'],
        'wave': ['wave'],
        'refresh': ['refresh', 'pull']
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

def get_current_tags(file_path):
    """현재 태그 가져오기"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    tag_match = re.search(r'tag:\s*\[([^\]]+)\]', content)
    if tag_match:
        tags = [tag.strip() for tag in tag_match.group(1).split(',')]
        return tags
    return []

def main():
    """메인 실행 함수"""
    posts_dir = "_posts"
    
    # Compose 포스트 제외
    posts = [f for f in os.listdir(posts_dir) if f.endswith('.md') and not f.startswith('2024-01')]
    posts.sort()
    posts = posts[:10]  # 처음 10개만
    
    print(f"🔍 View 라이브러리 테스트 조사 (처음 10개)")
    print(f"📚 총 {len(posts)}개 라이브러리\n")
    
    for i, post_file in enumerate(posts, 1):
        file_path = os.path.join(posts_dir, post_file)
        title = post_file.replace('.md', '').split('-', 3)[-1]
        
        print(f"\n[{i}/{len(posts)}] {title}")
        
        # GitHub 저장소 추출
        repo = extract_github_repo(file_path)
        if not repo:
            print("  ❌ GitHub 저장소를 찾을 수 없음")
            continue
        
        print(f"  📍 저장소: {repo}")
        
        # 현재 태그
        current_tags = get_current_tags(file_path)
        print(f"  🏷️  현재 태그: {', '.join(current_tags)}")
        
        # GitHub 상태 확인
        status = check_github_status(repo)
        
        if status['exists'] == False:
            print("  ❌ 저장소가 존재하지 않음 (삭제됨)")
            continue
        elif status['exists'] == 'unknown':
            print("  ⚠️  상태 확인 실패")
            continue
        
        # 상태 출력
        print(f"  ⭐ Stars: {status['stars']:,}")
        print(f"  📅 최종 업데이트: {status['last_update'][:10] if status['last_update'] else 'Unknown'}")
        
        if status['archived']:
            print("  🗄️  보관됨 (Archived)")
        
        # 태그 제안
        suggested_tags = suggest_tags(status, title, current_tags)
        print(f"  🏷️  추천 태그: {', '.join(suggested_tags)}")
        
        # API 제한 방지
        time.sleep(2)

if __name__ == "__main__":
    main()