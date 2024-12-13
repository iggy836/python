# 1から10までの連番のテキストファイルを作成
for i in range(1, 11):
    # ゼロ埋めした2桁のファイル名を作成（例：01.txt, 02.txt）
    filename = f"{i:02d}.txt"
    
    # ファイルを作成して書き込み
    with open(filename, 'w') as f:
        f.write(f"これは{filename}のコンテンツです。")

print("全てのファイルが作成されました。") 