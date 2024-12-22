def validatePassword(password: str) -> bool:
   # バリデーション結果を格納する変数
   isValid = True
   
   # 長さチェック（8-16文字）
   if len(password) < 8 or len(password) > 16:
       print("パスワードは8文字以上16文字以下である必要があります")
       return False  # 長さが無効な場合は即座にFalseを返す
   
   # 半角英数字チェック
   if not password.isalnum():
       print("半角英数字以外の文字が含まれています")
       isValid = False
   
   # 大文字チェック
   hasUpper = any(c.isupper() for c in password)
   if not hasUpper:
       print("大文字アルファベットが含まれていません")
       isValid = False
   
   # 小文字チェック
   hasLower = any(c.islower() for c in password)
   if not hasLower:
       print("小文字アルファベットが含まれていません")
       isValid = False
   
   # 数字チェック
   hasDigit = any(c.isdigit() for c in password)
   if not hasDigit:
       print("数字が含まれていません")
       isValid = False
   
   return isValid
def main():
   while True:
       # パスワード入力
       print("パスワードを入力してください：", end="")
       password = input()
       
       # バリデーション実行
       if validatePassword(password):
           print("Valid Password")
       else:
           print("Invalid Password")
       
       # 継続確認
       print("\n続けて確認しますか？(y/n): ", end="")
       if input().lower() != 'y':
           break
if __name__ == "__main__":
   main()