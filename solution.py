"""3부처 보도자료 키워드 추출 도구.

보도자료데이터.json을 읽어 본문에 키워드가 들어 있는 보도자료만 골라
결과_<키워드>.csv(UTF-8, 헤더: 번호·부처·제목·본문)로 저장한다.

사용법:
    python solution.py "1,820"
    python solution.py            # 인자가 없으면 키워드를 직접 입력받음
"""
import csv
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
DATA = HERE / "보도자료데이터.json"
HEADER = ["번호", "부처", "제목", "본문"]
# Windows·macOS 파일명에 쓸 수 없는 문자
BAD_CHARS = '\\/:*?"<>|'


def get_keyword():
    """명령행 인자 1개를 키워드로 쓰고, 없으면 입력을 받는다."""
    if len(sys.argv) >= 2:
        keyword = " ".join(sys.argv[1:])
    else:
        try:
            keyword = input("검색할 키워드를 입력하세요: ")
        except EOFError:
            keyword = ""
    keyword = keyword.strip()
    if not keyword:
        print('사용법: python solution.py <키워드>   예) python solution.py "1,820"')
        sys.exit(1)
    return keyword


def load_articles(path):
    """JSON 파일을 읽어 보도자료 목록을 돌려준다."""
    if not path.exists():
        print(f"[오류] 데이터 파일이 없습니다: {path.name} (solution.py와 같은 폴더에 두세요)")
        sys.exit(1)
    try:
        articles = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        print(f"[오류] JSON 형식이 올바르지 않습니다: {e}")
        sys.exit(1)
    if not isinstance(articles, list):
        print("[오류] JSON 최상위는 보도자료 배열이어야 합니다.")
        sys.exit(1)
    return articles


def safe_filename(keyword):
    """파일명에 쓸 수 없는 문자를 '_'로 바꾼다. (쉼표 등은 그대로 유지)"""
    return "".join("_" if c in BAD_CHARS else c for c in keyword)


def main():
    keyword = get_keyword()
    articles = load_articles(DATA)

    filtered = [a for a in articles if keyword in str(a.get("본문", ""))]

    out = HERE / f"결과_{safe_filename(keyword)}.csv"
    # utf-8-sig: UTF-8에 BOM을 붙여 엑셀에서 열어도 한글이 깨지지 않음
    with out.open("w", encoding="utf-8-sig", newline="") as f:
        w = csv.writer(f)
        w.writerow(HEADER)
        for a in filtered:
            w.writerow([a.get(col, "") for col in HEADER])

    print(f"[OK] {len(filtered)}건 저장 → {out.name}")


if __name__ == "__main__":
    main()
