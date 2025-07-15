#!/bin/bash

# Android UI Collection - 라이브러리 추가 스크립트
# 사용법: ./add_library.sh "LibraryName" "username/repository" "tag1,tag2,tag3"

LIBRARY_NAME=$1
GITHUB_REPO=$2
TAGS=$3
DATE=$(date +%Y-%m-%d)

if [ -z "$LIBRARY_NAME" ] || [ -z "$GITHUB_REPO" ] || [ -z "$TAGS" ]; then
    echo "사용법: ./add_library.sh \"LibraryName\" \"username/repository\" \"tag1,tag2,tag3\""
    echo "예시: ./add_library.sh \"LazyTimetable\" \"MoyuruAizawa/LazyTimetable\" \"compose,timetable,calendar\""
    exit 1
fi

# 태그 배열로 변환
IFS=',' read -ra TAG_ARRAY <<< "$TAGS"
TAG_LIST=""
for tag in "${TAG_ARRAY[@]}"; do
    TAG_LIST="$TAG_LIST$tag, "
done
TAG_LIST=${TAG_LIST%, }  # 마지막 쉼표 제거

# 포스트 파일 생성
POST_FILE="_posts/${DATE}-${LIBRARY_NAME}.md"

cat > "$POST_FILE" << EOF
---
layout: post
title: $LIBRARY_NAME
featured: true
image: '/images/posts/${LIBRARY_NAME}.gif'
tag: [$TAG_LIST]
link: 'https://github.com/$GITHUB_REPO'
---

{% remote_markdown https://raw.githubusercontent.com/$GITHUB_REPO/main/README.md %}
EOF

echo "✅ 포스트 파일 생성: $POST_FILE"

# README에서 이미지 URL 찾기
echo "🔍 이미지 검색 중..."
README_URL="https://raw.githubusercontent.com/$GITHUB_REPO/main/README.md"
README_CONTENT=$(curl -s "$README_URL")

if [ -z "$README_CONTENT" ]; then
    README_URL="https://raw.githubusercontent.com/$GITHUB_REPO/master/README.md"
    README_CONTENT=$(curl -s "$README_URL")
fi

# GIF 이미지 URL 추출 (간단한 정규식)
IMAGE_URLS=$(echo "$README_CONTENT" | grep -oE 'https?://[^"]+\.(gif|png|jpg|webp)' | head -5)

if [ ! -z "$IMAGE_URLS" ]; then
    echo "📷 발견된 이미지:"
    echo "$IMAGE_URLS"
    echo ""
    echo "첫 번째 이미지를 다운로드하시겠습니까? (y/n)"
    read -r response
    
    if [ "$response" = "y" ]; then
        FIRST_IMAGE=$(echo "$IMAGE_URLS" | head -1)
        EXTENSION="${FIRST_IMAGE##*.}"
        curl -L -o "images/posts/${LIBRARY_NAME}.${EXTENSION}" "$FIRST_IMAGE"
        echo "✅ 이미지 다운로드 완료: images/posts/${LIBRARY_NAME}.${EXTENSION}"
        
        # 포스트 파일의 이미지 확장자 업데이트
        if [ "$EXTENSION" != "gif" ]; then
            sed -i '' "s/${LIBRARY_NAME}.gif/${LIBRARY_NAME}.${EXTENSION}/g" "$POST_FILE"
            echo "✅ 포스트 파일 이미지 확장자 업데이트"
        fi
    fi
else
    echo "⚠️  이미지를 찾을 수 없습니다. 수동으로 추가해주세요."
fi

echo ""
echo "📋 다음 단계:"
echo "1. 이미지가 없다면 /images/posts/${LIBRARY_NAME}.gif 추가"
echo "2. 필요시 포스트 파일 수정: $POST_FILE"
echo "3. Jekyll 빌드: bundle exec jekyll build"