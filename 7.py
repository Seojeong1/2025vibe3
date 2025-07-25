import pandas as pd

# 예시 데이터: 국가별 FTO 유전자 빈도와 비만률
data = {
    "국가": ["한국", "미국", "일본", "독일", "인도"],
    "FTO_빈도": [0.12, 0.45, 0.08, 0.31, 0.05],
    "비만률": [5.3, 36.2, 4.2, 22.1, 3.9]
}

df = pd.DataFrame(data)

# 피어슨 상관계수 계산
r = df["FTO_빈도"].corr(df["비만률"])
print(f"FTO 유전자 빈도와 비만률 간의 상관계수: {r:.2f}")
