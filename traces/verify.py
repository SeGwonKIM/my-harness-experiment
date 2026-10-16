"""discount.py 의 여러 상태를 같은 기준으로 다시 재는 스크립트.

기준(정답): 원 단위 정수 계산 price * (100 - percent) // 100
범위: 가격 100원~100,000원(100원 단위 1,000종) x 할인율 0~100% (101종) = 101,000건

실행: python traces/verify.py   (저장소 맨 위에서)
"""
import importlib.util, pathlib, sys

sys.stdout.reconfigure(encoding="utf-8")
HERE = pathlib.Path(__file__).parent / "states"
STATES = [
    ("fixture (원본 버그)", "discount_fixture.py"),
    ("test 폴더 (출처 미확인 수정)", "discount_test-folder.py"),
    ("search·replace 제안 문장 그대로", "discount_search-replace-proposal.py"),
    ("run-B 수정 후 (search·replace 조건)", "discount_run-B-after.py"),
    ("test2 수정 후 (자유 텍스트 조건)", "discount_test2-after.py"),
]


def load(path):
    spec = importlib.util.spec_from_file_location(path.stem, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.apply_discount


cases = [(p, c) for p in range(100, 100_001, 100) for c in range(0, 101)]
print(f"{'상태':<34}{'기존 테스트':<12}{'값 틀림':>10}{'정수 아님':>10}")
for label, name in STATES:
    f = load(HERE / name)
    base = "통과" if f(20000, 10) == 18000 else "실패"
    wrong = sum(f(p, c) != p * (100 - c) // 100 for p, c in cases)
    not_int = sum(not isinstance(f(p, c), int) for p, c in cases)
    print(f"{label:<34}{base:<12}{wrong:>10,}{not_int:>10,}")
print(f"(전체 {len(cases):,}건 중)")
