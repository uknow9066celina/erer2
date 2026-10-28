# 5·25 호우 보도자료 대조실 — 배포·사용 안내

## 폴더 구성
| 파일 | 용도 |
|---|---|
| `index.html` | 정적 웹 페이지 (부처 카드 · 키워드 검색 · 정합성 매트릭스 · 외부 리소스) |
| `보도자료데이터.json` | 페이지와 solution.py가 함께 읽는 데이터 (index.html과 같은 폴더) |
| `solution.py` | 키워드 → CSV 추출 도구 |
| `정합성_매트릭스.csv` | Google Sheets로 가져올 매트릭스 원본 |

## 1. Google Sheets 임베드 (선택이지만 권장)
1. Google Sheets 새 시트 → **파일 → 가져오기 → 업로드** → `정합성_매트릭스.csv`
2. **파일 → 공유 → 웹에 게시** → **삽입** 탭 → [게시]
3. 나온 `<iframe src="...">` 의 **src 주소만** 복사
4. `index.html` 아래쪽 `<script>` 맨 위 `const SHEET_EMBED_URL = "";` 따옴표 안에 붙여넣기

(선택) YouTube 영상도 넣으려면 `const YOUTUBE_ID = "";` 에 영상 ID(watch?v= 뒤 11자리)를 넣습니다.
외부 이미지(Wikimedia Commons 사진)는 설정 없이 바로 표시됩니다.

## 2. 무료 호스팅 배포 — GitHub Pages
1. github.com 로그인 → **New repository** (예: `rain-0525`, Public)
2. **Add file → Upload files** → `index.html`, `보도자료데이터.json` 업로드 → Commit
3. **Settings → Pages → Branch: main / (root) → Save**
4. 1~2분 뒤 `https://<아이디>.github.io/rain-0525/` 접속

대안: **Netlify Drop**(app.netlify.com/drop)에 이 폴더를 끌어다 놓기,
또는 **Cloudflare Pages** → Upload assets.

> 로컬에서 index.html을 더블클릭해 열면 브라우저가 JSON 읽기를 막아 내장 사본으로 표시됩니다.
> 배포 후에는 `보도자료데이터.json`을 실제로 읽습니다.

## 3. Python 도구
```
$ python solution.py "1,820"
[OK] 2건 저장 → 결과_1,820.csv
```
- 표준 라이브러리(csv·json·sys·pathlib)만 사용
- CSV는 UTF-8(BOM 포함, 엑셀 한글 깨짐 방지), 헤더 `번호,부처,제목,본문`
- 파일명에 쓸 수 없는 문자(`/ : * ? " < > | \`)는 `_`로 바꿈 (예: `16:30` → `결과_16_30.csv`)
- 인자 없이 실행하면 키워드를 직접 입력받음
