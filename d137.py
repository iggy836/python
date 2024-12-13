# 7日分の気温データを入力として受け取る
temperatures = []
for i in range(7):
    temp = int(input())
    temperatures.append(temp)

# 最高気温を求める
max_temp = max(temperatures)

# 結果を出力
print(f"最高気温は {max_temp} 度です。")