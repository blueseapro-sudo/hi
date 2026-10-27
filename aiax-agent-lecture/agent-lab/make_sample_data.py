# 실습용 가짜 데이터 생성기 (실제 개인정보·내부 자료 아님)
# 실행: python make_sample_data.py   (필요: pip install openpyxl)
from openpyxl import Workbook

def save(path, header, rows):
    wb = Workbook(); ws = wb.active; ws.title = "Sheet1"
    ws.append(header)
    for r in rows: ws.append(r)
    wb.save(path)

# 1) 주간 출동 실적 (6강 데모용) - 마지막 열 '합계'에 일부러 틀린 값 1개
rows = [
    ["가센터", 3, 5, 21, 29],
    ["나센터", 2, 4, 18, 24],
    ["다센터", 1, 7, 25, 33],
    ["라센터", 4, 3, 15, 22],   # 정답 22
    ["마센터", 2, 6, 19, 30],   # 오류: 정답은 27
]
save("data/weekly_stats.xlsx", ["센터", "화재", "구조", "구급", "합계"], rows)

# 2) 예산 집행 현황 (4강 지시 비교용)
budget = [
    ["소방장비 유지관리", 50000, 32000],
    ["청사 시설관리", 80000, 61000],
    ["안전교육 운영", 12000, 9000],
    ["의용소방대 지원", 30000, 15000],
    ["119생활안전", 20000, 17500],
]
save("data/budget.xlsx", ["세부사업", "예산액(천원)", "집행액(천원)"], budget)
print("data/weekly_stats.xlsx, data/budget.xlsx 생성 완료")
