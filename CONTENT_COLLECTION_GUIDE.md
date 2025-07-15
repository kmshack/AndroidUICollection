# Android UI Collection 컨텐츠 수집 가이드

이 문서는 AndroidUICollection에 새로운 Android UI 라이브러리를 추가하는 방법을 설명합니다.

## 📋 수집 절차

### 1. 라이브러리 찾기

#### 주요 소스
- **Android Weekly RSS**: https://androidweekly.net/rss.xml
- **GitHub Topics**:
  - https://github.com/topics/jetpack-compose
  - https://github.com/topics/jetpack-compose-library
  - https://github.com/topics/android-ui
  - https://github.com/topics/android-library
- **Awesome Lists**:
  - https://github.com/jetpack-compose/jetpack-compose-awesome
  - https://github.com/wasabeef/awesome-android-ui
  - https://github.com/androiddevnotes/awesome-jetpack-compose-android-apps

#### 검색 키워드
- Jetpack Compose UI
- Android animation library
- Android custom view
- Material Design components
- Android UI components

### 2. 포스트 파일 생성

#### 파일명 규칙
```
YYYY-MM-DD-LibraryName.md
```
예: `2024-01-15-LazyTimetable.md`

#### 필수 Front Matter 구조
```markdown
---
layout: post
title: 라이브러리명
featured: true
image: '/images/posts/라이브러리명.gif'
tag: [관련, 태그, 목록]
link: 'https://github.com/username/repository'
---

{% remote_markdown https://raw.githubusercontent.com/username/repository/main/README.md %}
```

#### 태그 가이드
**Compose 라이브러리**:
- compose
- 기능별: animation, calendar, picker, chart, navigation
- UI 유형: button, card, list, dialog, bottomsheet

**기존 View 시스템**:
- view
- 기능별: loading, indicator, menu, drawer
- Material Design: material, material3

### 3. 이미지 수집

#### 이미지 찾기
1. GitHub README에서 데모 GIF/이미지 찾기
2. 일반적인 위치:
   - `/art/`, `/demo/`, `/screenshots/` 디렉토리
   - README.md 내 임베드된 이미지
   - GitHub 이슈/PR의 이미지

#### 이미지 다운로드
```bash
# GIF 다운로드 예시
curl -L -o LibraryName.gif "https://raw.githubusercontent.com/username/repo/main/demo.gif"

# GitHub user-images URL인 경우
curl -L -o LibraryName.gif "https://user-images.githubusercontent.com/..."
```

#### 이미지 저장 위치
- 경로: `/images/posts/`
- 파일명: 라이브러리명과 동일하게 (예: `LazyTimetable.gif`)
- 지원 형식: .gif, .png, .jpg, .webp

### 4. 대량 수집 자동화

#### Compose 라이브러리 일괄 추가 예시
```javascript
// 라이브러리 목록
const libraries = [
  {
    name: "LazyTimetable",
    github: "MoyuruAizawa/LazyTimetable",
    tags: ["compose", "timetable", "calendar"],
    image: "sample_01.gif"
  },
  // ... 더 많은 라이브러리
];

// 포스트 생성
libraries.forEach(lib => {
  const date = new Date().toISOString().split('T')[0];
  const content = `---
layout: post
title: ${lib.name}
featured: true
image: '/images/posts/${lib.name}.gif'
tag: [${lib.tags.join(', ')}]
link: 'https://github.com/${lib.github}'
---

{% remote_markdown https://raw.githubusercontent.com/${lib.github}/main/README.md %}`;
  
  // 파일 생성
  fs.writeFileSync(`_posts/${date}-${lib.name}.md`, content);
});
```

### 5. 품질 체크리스트

✅ **추가 전 확인사항**:
- [ ] GitHub 저장소가 활성 상태인가? (최근 업데이트)
- [ ] README에 사용법이 잘 문서화되어 있는가?
- [ ] 데모 이미지/GIF가 있는가?
- [ ] 라이선스가 명시되어 있는가?
- [ ] 스타 수가 적절한가? (최소 50+)

✅ **포스트 생성 시**:
- [ ] 파일명 형식이 올바른가?
- [ ] Front Matter가 완전한가?
- [ ] 이미지 경로가 정확한가?
- [ ] 태그가 적절한가?
- [ ] remote_markdown URL이 올바른가?

### 6. 일반적인 문제 해결

#### README URL 찾기
- 기본: `/master/README.md`
- 대안: `/main/README.md`, `/develop/README.md`
- 대소문자 확인: `readme.md`, `Readme.md`

#### 이미지가 없는 경우
1. 라이브러리 실행해서 직접 스크린샷 생성
2. 플레이스홀더 이미지 사용
3. 텍스트 기반 설명 이미지 생성

#### remote_markdown 오류
- 404 오류: URL 경로 확인 (main vs master)
- 인코딩 오류: 특수문자 처리
- 네트워크 오류: 타임아웃 처리 추가

### 7. 유용한 도구

#### Chrome 확장 프로그램
- **GitHub File Finder**: 저장소 파일 구조 빠르게 탐색
- **Octotree**: GitHub 저장소 트리뷰

#### 커맨드라인 도구
```bash
# 여러 이미지 일괄 다운로드
for url in $(cat image_urls.txt); do
  filename=$(basename "$url")
  curl -L -o "$filename" "$url"
done

# WebP를 GIF로 변환
convert input.webp output.gif
```

### 8. 추천 수집 주기

- **주간**: Android Weekly 체크
- **월간**: GitHub Trending 확인
- **분기별**: Awesome 리스트 업데이트 확인

### 9. 컨텐츠 카테고리

현재 주요 카테고리:
- **Compose UI**: 최신 Compose 라이브러리 우선
- **Animation**: 애니메이션, 트랜지션 효과
- **Navigation**: 드로어, 바텀시트, 탭
- **Data Display**: 차트, 캘린더, 리스트
- **Input**: 피커, 슬라이더, 폼
- **Feedback**: 로딩, 프로그레스, 다이얼로그

### 10. 향후 개선 사항

- [ ] GitHub Actions로 자동 수집
- [ ] 인기도 기반 자동 정렬
- [ ] 카테고리별 필터링
- [ ] 검색 기능 강화
- [ ] 라이브러리 업데이트 추적

---

## 📝 참고사항

- 이미지는 가능한 GIF 애니메이션 선호
- 한국어 설명 추가 고려
- 중복 라이브러리 확인 필수
- 업데이트가 중단된 라이브러리는 제외

마지막 업데이트: 2024-01-15