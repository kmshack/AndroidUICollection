# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

AndroidUICollection is a Jekyll-based static website that showcases open-source Android UI libraries and components. The site is hosted at https://kmshack.github.io/AndroidUICollection

## Common Commands

### Development
```bash
# Install dependencies
bundle install

# Run local development server
bundle exec jekyll serve

# Build the site
bundle exec jekyll build
```

### Adding New UI Libraries
To add a new Android UI library to the collection:
1. Create a new markdown file in `_posts/` with format: `YYYY-MM-DD-LibraryName.md`
2. Use the following front matter structure:
```yaml
---
layout: post
title: LibraryName
featured: true
image: '/images/posts/YYYY-MM-DD-LibraryName.gif'
tag: [relevant, tags, here]
link: 'https://github.com/username/repository'
---

{% remote_markdown https://raw.githubusercontent.com/username/repository/master/README.md %}
```
3. Add the demonstration GIF to `images/posts/`

## Architecture

### Key Components

1. **Remote Markdown Plugin** (`_plugins/remote_markdown.rb`): Fetches README files from GitHub repositories dynamically. Note: It removes all exclamation marks from fetched markdown to prevent image loading issues.

2. **Post Structure**: Each post represents one Android UI library with:
   - Metadata in Jekyll front matter
   - Animated GIF demonstration
   - Dynamically fetched README content from the original repository

3. **Site Configuration** (`_config.yml`):
   - Base URL: `/AndroidUICollection`
   - Pagination: Infinite scrolling
   - Plugins: jekyll-paginate, jekyll-tagging

### Directory Structure
- `_posts/`: Individual UI library showcases (2016-2019)
- `_layouts/`: Jekyll templates (default, page, post, tag_page)
- `_includes/`: Reusable components (analytics, pagination, sidebar)
- `images/posts/`: GIF demonstrations of UI libraries
- `_sass/` & `css/`: Styling (SCSS)
- `js/`: JavaScript functionality (jQuery, search)

### Deployment
The site uses GitHub Pages for hosting. Any push to the repository will trigger a rebuild and deployment.


LLM 코딩 시 흔히 발생하는 오류를 줄이기 위한 행동 지침입니다. 필요에 따라 프로젝트별 지침과 병합하세요.

**절충점:** 이 지침은 속도보다는 신중함을 우선시합니다. 사소한 작업의 경우 판단력을 발휘하십시오.

## 1. 코딩하기 전에 생각하세요

**추측하지 마세요. 혼란스러운 점을 숨기지 마세요. 장단점을 명확히 드러내세요.**

실행하기 전에:
- 가정한 내용을 명확하게 밝히세요. 확실하지 않으면 질문하세요.
- 여러 해석이 가능하다면, 모두 제시하십시오. 묵묵히 하나를 선택하지 마십시오.
- 더 간단한 방법이 있다면 언급하십시오. 필요하다면 반박하십시오.
- 만약 이해가 안 되는 부분이 있다면, 멈추세요. 무엇이 헷갈리는지 말하고 질문하세요.

## 2. 단순함이 최우선

**문제를 해결하는 데 필요한 최소한의 코드만 작성하세요. 추측성 코드는 일절 포함하지 마세요.**

- 요청하신 기능 외에는 추가 기능이 없습니다.
- 일회용 코드에는 추상화 계층이 없습니다.
- 요청하지 않은 "유연성"이나 "설정 가능성"은 없습니다.
- 불가능한 시나리오에 대한 오류 처리가 없습니다.
- 200줄을 썼는데 50줄로 줄일 수 있다면 다시 쓰세요.

스스로에게 "선임 엔지니어가 이것이 지나치게 복잡하다고 말할까?"라고 질문해 보세요. 만약 그렇다면, 단순화하세요.

## 3. 수술적 변화

**필요한 것만 만지세요. 자신이 만든 것만 치우세요.**

기존 코드를 편집할 때:
- 인접한 코드, 주석 또는 서식을 "개선"하지 마십시오.
- 멀쩡한 것을 굳이 리팩토링하지 마세요.
- 기존 스타일과 일치시키세요. 비록 당신이 다르게 표현하더라도 말입니다.
- 관련 없는 사용되지 않는 코드를 발견하면 삭제하지 말고 언급해 주세요.

변경 사항으로 인해 고아 파일이 생성되는 경우:
- 사용자가 변경하여 더 이상 사용되지 않게 된 임포트/변수/함수를 제거하세요.
- 요청받지 않는 한 기존의 사용되지 않는 코드를 삭제하지 마십시오.

테스트: 변경된 모든 줄은 사용자의 요청과 직접적으로 연결되어야 합니다.

## 4. 목표 중심 실행

**성공 기준을 정의하고, 검증될 때까지 반복합니다.**

과제를 검증 가능한 목표로 전환하세요:
- "유효성 검사 추가" → "유효하지 않은 입력에 대한 테스트를 작성한 다음, 해당 테스트를 통과하도록 수정"
- "버그 수정" → "버그를 재현하는 테스트를 작성하고, 테스트를 통과시키세요"
- "X 리팩토링" → "리팩토링 전후에 테스트 통과 확인"

여러 단계를 거치는 작업의 경우, 간략한 계획을 제시하십시오.
```
1. [단계] → 확인: [체크]
2. [단계] → 확인: [확인]
3. [단계] → 확인: [체크]
```

명확한 성공 기준은 독립적인 반복 작업을 가능하게 합니다. 반면, 모호한 기준("그냥 작동하게 하라")은 지속적인 명확화를 요구합니다.

