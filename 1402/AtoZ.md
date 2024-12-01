問題
アルファベットの大文字を A から Z まで順番に出力するプログラムを作成してください。
出力例：
ABCDEFGHIJKLMNOPQRSTUVWXYZ
ヒント
Pythonでは以下の方法でアルファベットを扱うことができます：
chr() 関数：数値（ASCII コード）から文字に変換
ord() 関数：文字から数値（ASCII コード）に変換
'A' の ASCII コードは 65
'Z' の ASCII コードは 90
以下のいずれかの方法で解くことができます：
for ループと range() を使用する
リスト内包表記を使用する
string モジュールの ascii_uppercase を使用する
出力時に改行を入れたくない場合は、print() 関数の end パラメータを使用します：
   print(文字, end='')