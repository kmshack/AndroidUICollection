#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
누락된 이미지 확인 및 다운로드
"""

import os
import re
import urllib.request
import urllib.error

def check_missing_images():
    """누락된 이미지 확인"""
    posts_dir = "_posts"
    images_dir = "images/posts"
    
    missing = []
    existing = []
    
    # 모든 포스트 확인
    posts = [f for f in os.listdir(posts_dir) if f.endswith('.md')]
    posts.sort()
    
    for post_file in posts:
        file_path = os.path.join(posts_dir, post_file)
        
        # 이미지 경로 추출
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        image_match = re.search(r"image:\s*'([^']+)'", content)
        if image_match:
            image_path = image_match.group(1)
            # 상대 경로로 변환
            if image_path.startswith('/images/posts/'):
                image_name = image_path.replace('/images/posts/', '')
                full_path = os.path.join(images_dir, image_name)
                
                if os.path.exists(full_path):
                    existing.append((post_file, image_name))
                else:
                    missing.append((post_file, image_name))
    
    print(f"📊 이미지 현황")
    print(f"  ✅ 존재: {len(existing)}개")
    print(f"  ❌ 누락: {len(missing)}개")
    
    if missing:
        print(f"\n📋 누락된 이미지 목록:")
        for post, image in missing[:20]:  # 처음 20개만 표시
            print(f"  - {post}: {image}")
        
        if len(missing) > 20:
            print(f"  ... 외 {len(missing) - 20}개")
    
    return missing

def find_image_url(post_file):
    """포스트에서 GitHub 저장소 찾고 이미지 URL 검색"""
    file_path = os.path.join("_posts", post_file)
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # GitHub 저장소 추출
    link_match = re.search(r"link:\s*'([^']+)'", content)
    if not link_match:
        return None
    
    link = link_match.group(1)
    repo_match = re.search(r'github\.com/([^/]+/[^/]+)', link)
    if not repo_match:
        return None
    
    repo = repo_match.group(1).rstrip('/')
    
    # README 확인
    readme_urls = [
        f"https://raw.githubusercontent.com/{repo}/master/README.md",
        f"https://raw.githubusercontent.com/{repo}/main/README.md"
    ]
    
    for url in readme_urls:
        try:
            req = urllib.request.Request(url, headers={
                'User-Agent': 'AndroidUICollection/1.0'
            })
            with urllib.request.urlopen(req, timeout=10) as response:
                readme_content = response.read().decode('utf-8')
                
                # 이미지 찾기 (GIF 우선)
                gif_pattern = r'https?://[^\s\)]+\.gif'
                gifs = re.findall(gif_pattern, readme_content)
                if gifs:
                    return gifs[0]
                
                # PNG/JPG
                img_pattern = r'https?://[^\s\)]+\.(png|jpg|jpeg)'
                imgs = re.findall(img_pattern, readme_content)
                if imgs:
                    return imgs[0]
                
        except Exception:
            continue
    
    return None

def download_image(url, save_path):
    """이미지 다운로드"""
    try:
        req = urllib.request.Request(url, headers={
            'User-Agent': 'AndroidUICollection/1.0'
        })
        with urllib.request.urlopen(req, timeout=30) as response:
            with open(save_path, 'wb') as f:
                f.write(response.read())
        return True
    except Exception as e:
        print(f"    다운로드 실패: {e}")
        return False

def main():
    """메인 실행"""
    missing = check_missing_images()
    
    if not missing:
        print("\n✨ 모든 이미지가 존재합니다!")
        return
    
    print(f"\n🔄 누락된 이미지 다운로드 시작...")
    
    success_count = 0
    for i, (post_file, image_name) in enumerate(missing[:10], 1):  # 처음 10개만
        print(f"\n[{i}/10] {post_file}")
        
        # 이미지 URL 찾기
        image_url = find_image_url(post_file)
        if image_url:
            print(f"  📷 발견: {image_url}")
            
            # 확장자 확인
            ext = image_url.split('.')[-1].lower()
            if ext in ['gif', 'png', 'jpg', 'jpeg', 'webp']:
                # 기존 이미지명의 확장자 변경 필요 여부 확인
                current_ext = image_name.split('.')[-1].lower()
                if current_ext != ext:
                    new_image_name = image_name.replace(f'.{current_ext}', f'.{ext}')
                    print(f"  📝 이미지명 변경: {image_name} → {new_image_name}")
                else:
                    new_image_name = image_name
                
                # 다운로드
                save_path = os.path.join("images/posts", new_image_name)
                if download_image(image_url, save_path):
                    print(f"  ✅ 다운로드 완료: {new_image_name}")
                    success_count += 1
                    
                    # 포스트 파일 업데이트 필요시
                    if current_ext != ext:
                        update_post_image_ext(post_file, current_ext, ext)
        else:
            print(f"  ❌ 이미지를 찾을 수 없음")
    
    print(f"\n✅ 완료! 성공: {success_count}/10")

def update_post_image_ext(post_file, old_ext, new_ext):
    """포스트 파일의 이미지 확장자 업데이트"""
    file_path = os.path.join("_posts", post_file)
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    content = content.replace(f'.{old_ext}', f'.{new_ext}')
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"  ✏️  포스트 파일 업데이트 완료")

if __name__ == "__main__":
    main()