#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
View 라이브러리 태그 일괄 업데이트
"""

import os
import re
import time
import urllib.request
import urllib.error
import json

def extract_github_repo(file_path):
    """포스트 파일에서 GitHub 저장소 정보 추출"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
        
    link_match = re.search(r"link:\s*'([^']+)'", content)
    if link_match:
        link = link_match.group(1)
        repo_match = re.search(r'github\.com/([^/]+/[^/]+)', link)
        if repo_match:
            return repo_match.group(1).rstrip('/')
    
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
                'archived': data.get('archived', False),
                'description': data.get('description', ''),
                'topics': data.get('topics', [])
            }
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return {'exists': False}
    except Exception:
        pass
    
    return {'exists': 'unknown'}

def get_current_tags(file_path):
    """현재 태그 가져오기"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    tag_match = re.search(r'tag:\s*\[([^\]]+)\]', content)
    if tag_match:
        tags = [tag.strip() for tag in tag_match.group(1).split(',')]
        return tags
    return []

def suggest_tags(library_info, title, current_tags=[]):
    """라이브러리 정보를 기반으로 태그 제안"""
    tags = set()
    
    # 기본 태그
    tags.add('view')
    
    # 현재 태그 중 의미있는 것 유지
    preserve_tags = {'material', 'material3', 'compose'}
    for tag in current_tags:
        if tag in preserve_tags:
            tags.add(tag)
    
    # GitHub topics 활용
    if 'topics' in library_info:
        for topic in library_info['topics']:
            clean_topic = topic.lower().replace('-', '').replace('_', '')
            if 'android' not in clean_topic and len(clean_topic) > 2:
                tags.add(clean_topic)
    
    # 제목과 설명 기반 태그
    title_lower = title.lower()
    desc = library_info.get('description', '')
    desc_lower = desc.lower() if desc else ''
    
    # UI 컴포넌트 매핑
    tag_mappings = {
        # Loading & Progress
        ('loading', 'progress', 'loader'): 'loading',
        ('indicator',): 'indicator',
        ('progressbar', 'progress bar'): 'progress',
        ('shimmer',): 'shimmer',
        
        # Navigation
        ('navigation', 'navbar', 'nav'): 'navigation',
        ('menu', 'drawer', 'reside'): 'menu',
        ('tab', 'tablayout'): 'tab',
        ('bottomsheet', 'bottom sheet'): 'bottomsheet',
        
        # Animation & Effects
        ('animation', 'animated', 'animate', 'anim'): 'animation',
        ('transition',): 'transition',
        ('blur', 'blurview'): 'blur',
        ('shadow',): 'shadow',
        ('wave',): 'wave',
        ('explod', 'explosion'): 'explosion',
        
        # Input & Selection
        ('calendar', 'date', 'datepicker'): 'calendar',
        ('picker', 'select', 'choose'): 'picker',
        ('switch', 'toggle'): 'switch',
        ('slider', 'seekbar', 'seek'): 'slider',
        ('rating', 'ratingbar'): 'rating',
        
        # Display
        ('card', 'cardview'): 'card',
        ('list', 'listview', 'recycler'): 'list',
        ('chart', 'graph'): 'chart',
        ('image', 'photo', 'gallery'): 'image',
        ('text', 'textview', 'label'): 'text',
        ('table',): 'table',
        
        # Interaction
        ('swipe', 'slide', 'sliding', 'slidr'): 'swipe',
        ('drag', 'draggable'): 'drag',
        ('pull', 'refresh', 'ptr'): 'refresh',
        ('scroll',): 'scroll',
        ('expand', 'collapse', 'fold'): 'expand',
        
        # Dialogs & Overlays
        ('dialog', 'alert', 'popup'): 'dialog',
        ('toast', 'snackbar'): 'toast',
        ('floating', 'fab'): 'floating',
        ('bubble',): 'bubble',
        
        # Others
        ('material',): 'material',
        ('button', 'btn'): 'button',
        ('badge',): 'badge',
        ('chip',): 'chip',
        ('stepper',): 'stepper',
        ('intro', 'onboarding', 'showcase'): 'intro',
        ('permission',): 'permission',
        ('camera', 'video'): 'media',
        ('music', 'audio', 'player'): 'audio',
        ('qr', 'barcode'): 'scanner',
        ('ribbon',): 'ribbon',
        ('ticket',): 'ticket',
        ('compass',): 'compass',
        ('tree',): 'tree',
        ('snowfall', 'snow'): 'effect',
        ('konfetti', 'confetti'): 'effect',
        ('cropper', 'crop'): 'crop',
        ('webview', 'web'): 'webview'
    }
    
    combined_text = f"{title_lower} {desc_lower}"
    
    for keywords, tag in tag_mappings.items():
        if any(keyword in combined_text for keyword in keywords):
            tags.add(tag)
    
    # 최대 6개 태그로 제한
    tags_list = sorted(list(tags))
    if len(tags_list) > 6:
        # view는 항상 포함, 나머지는 중요도 순
        priority_tags = ['view', 'material', 'animation', 'loading', 'navigation', 'picker']
        final_tags = ['view']
        for tag in priority_tags[1:]:
            if tag in tags_list and len(final_tags) < 6:
                final_tags.append(tag)
        for tag in tags_list:
            if tag not in final_tags and len(final_tags) < 6:
                final_tags.append(tag)
        return final_tags
    
    return tags_list

def update_post_tags(file_path, new_tags):
    """포스트 파일의 태그 업데이트"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    new_tags_str = ", ".join(new_tags)
    content = re.sub(r'tag:\s*\[[^\]]*\]', f'tag: [{new_tags_str}]', content)
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

def main():
    """메인 실행 함수"""
    posts_dir = "_posts"
    
    # Compose 포스트 제외
    posts = [f for f in os.listdir(posts_dir) if f.endswith('.md') and not f.startswith('2024-01')]
    posts.sort()
    
    print(f"🏷️  View 라이브러리 태그 일괄 업데이트")
    print(f"📚 총 {len(posts)}개 라이브러리\n")
    
    stats = {
        'total': 0,
        'updated': 0,
        'failed': 0,
        'not_found': 0
    }
    
    for i, post_file in enumerate(posts, 1):
        file_path = os.path.join(posts_dir, post_file)
        title = post_file.replace('.md', '').split('-', 3)[-1]
        
        print(f"\r[{i}/{len(posts)}] {title:<40}", end='', flush=True)
        stats['total'] += 1
        
        # GitHub 저장소 추출
        repo = extract_github_repo(file_path)
        if not repo:
            stats['failed'] += 1
            continue
        
        # 현재 태그
        current_tags = get_current_tags(file_path)
        
        # GitHub 상태 확인
        status = check_github_status(repo)
        
        if status['exists'] == False:
            stats['not_found'] += 1
            continue
        elif status['exists'] == 'unknown':
            stats['failed'] += 1
            continue
        
        # 태그 제안
        suggested_tags = suggest_tags(status, title, current_tags)
        
        # 태그가 변경된 경우만 업데이트
        if set(current_tags) != set(suggested_tags):
            try:
                update_post_tags(file_path, suggested_tags)
                stats['updated'] += 1
            except Exception:
                stats['failed'] += 1
        
        # API 제한 방지
        if i % 10 == 0:
            time.sleep(1)
    
    # 결과 출력
    print(f"\n\n✅ 태그 업데이트 완료!")
    print(f"  📊 총 {stats['total']}개 라이브러리")
    print(f"  ✏️  업데이트: {stats['updated']}개")
    print(f"  ❌ 삭제된 저장소: {stats['not_found']}개")
    print(f"  ⚠️  실패: {stats['failed']}개")

if __name__ == "__main__":
    main()