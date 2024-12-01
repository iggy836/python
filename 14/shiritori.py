def check_shiritori(N, words):
    # 各単語を順番にチェック
    for i in range(N-1):
        current_word = words[i]
        next_word = words[i+1]
        
        # 現在の単語の末尾と次の単語の先頭を比較
        if current_word[-1] != next_word[0]:
            # しりとりが成立しない場合、問題のある文字を返す
            return f"{current_word[-1]} {next_word[0]}"
    
    # すべての単語でしりとりが成立した場合
    return "Yes"

# 入力を受け取る
N = int(input())
words = [input() for _ in range(N)]

# 結果を出力
print(check_shiritori(N, words))