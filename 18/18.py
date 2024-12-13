def is_alphanumeric(text):
    # ASCII文字のみを判定
    return all(ord(char) < 128 and char.isalnum() for char in text)

# 入力を受け取る
input_text = input("文字列を入力してください:")

# 判定結果を出力
result = is_alphanumeric(input_text)
print(result)
