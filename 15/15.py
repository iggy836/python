# 必要なモジュールをインポート
import os                   # フォルダの作成や操作を行うためのモジュール
from datetime import datetime   # 日付を扱うためのモジュール

# 現在の日付を取得
today = datetime.now()      # 現在の日時を取得してtodayに保存

# 日付を「YYYY-MM-DD」形式の文字列に変換
# strftimeで日付のフォーマットを指定（%Y=年4桁, %m=月2桁, %d=日2桁）
folder_name = today.strftime("%Y%m%d")

# フォルダが既に存在するかチェック
if not os.path.exists(folder_name):    # フォルダが存在しない場合
    os.makedirs(folder_name)           # 新しいフォルダを作成
    print(f"フォルダ '{folder_name}' を作成しました")  # 作成完了メッセージを表示
else:
    print(f"フォルダ '{folder_name}' は既に存在します")  # フォルダが既に存在する場合のメッセージ