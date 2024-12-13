import tkinter as tk
import threading
import time
import math
import random

# ウィンドウやルーレットの設定値を定数として定義
# これらの値を変更することで、ルーレットの見た目や動作を簡単に調整できます
WINDOW_SIZE = 500          # アプリケーションウィンドウの縦横サイズ（ピクセル）
CANVAS_SIZE = 300         # ルーレットを描画する領域のサイズ（ピクセル）
ROULETTE_RADIUS = 120     # ルーレットの大きさ（中心から外周までの距離）
POINTER_SIZE = 20         # 上部の矢印（指針）の大きさ
ROTATION_SPEED = 0.1      # ルーレットが1回転するのにかかる時間（秒）
ANGLE_STEP = 5           # 1フレームあたりの回転角度（大きいほど速く回転）

# ルーレットで使用する色の定義
# 各色に日本語名とHTML/CSSで使用する色コードを設定
COLORS = [
    {"name": "赤", "code": "red"},    # name: 結果表示用の日本語名
    {"name": "青", "code": "blue"},   # code: 実際の描画に使用する色指定
    {"name": "緑", "code": "green"},
    {"name": "黄", "code": "yellow"},
    {"name": "紫", "code": "purple"},
    {"name": "オレンジ", "code": "orange"}
]

class RouletteApp:
    def __init__(self):
        """
        アプリケーションの初期化を行うメソッド
        ウィンドウの作成や初期設定を行います
        """
        # メインウィンドウの作成と設定
        self.window = tk.Tk()
        self.window.title("ルーレット")
        self.window.geometry(f"{WINDOW_SIZE}x{WINDOW_SIZE}")
        
        # 各種変数の初期化
        self.is_spinning = False
        self.angle = 0
        self.spin_thread = None
        
        # 初期状態（0度）での配置を定義
        # 12時の位置（三角形の位置）から時計回りに配置
        self.initial_colors = [
            {"name": "赤", "code": "red"},        # 0度（12時）
            {"name": "青", "code": "blue"},       # 60度
            {"name": "緑", "code": "green"},      # 120度
            {"name": "黄", "code": "yellow"},     # 180度
            {"name": "紫", "code": "purple"},     # 240度
            {"name": "オレンジ", "code": "orange"} # 300度
        ]
        
        # UIコンポーネントの作成
        self.create_widgets()
        self.create_roulette()
        self.create_pointer()
        
        # メインループの開始
        self.window.mainloop()

    def create_widgets(self):
        """
        画面上の各要素（ウィジェット）を作成・配置するメソッド
        - キャンバス：ルーレットを描画する領域
        - ボタン：スタート・ストップの制御用
        - ラベル：結果表示用
        """
        # キャンバスの作成
        self.canvas = tk.Canvas(self.window, width=CANVAS_SIZE, height=CANVAS_SIZE, bg='white')
        self.canvas.pack(pady=20)
        
        # ボタンフレームの作成
        button_frame = tk.Frame(self.window)
        button_frame.pack(pady=10)
        
        # スタートボタン
        self.start_button = tk.Button(button_frame, text="スタート", command=self.start_spin)
        self.start_button.pack(side=tk.LEFT, padx=10)
        
        # ストップボタン
        self.stop_button = tk.Button(button_frame, text="ストップ", command=self.stop_spin)
        self.stop_button.pack(side=tk.LEFT, padx=10)
        
        # 結果表示用のフレーム
        result_frame = tk.Frame(self.window)
        result_frame.pack(pady=10)
        
        # 結果表示ラベル（大きなフォントで表示）
        self.result_label = tk.Label(result_frame, text="結果: ", font=("Arial", 20))
        self.result_label.pack()

    def create_roulette(self):
        """
        ルーレットを描画するメソッド
        - 6色の扇形を描画して円形のルーレットを作成
        - 各扇形は60度（360度÷6）の角度を持つ
        - self.angleの値に応じて回転状態が変化
        """
        # キャンバスの中心座標を計算
        center_x = CANVAS_SIZE // 2
        center_y = CANVAS_SIZE // 2
        
        # 6色の扇形を順番に描画
        for i, color in enumerate(self.initial_colors):
            # 各扇形の開始角度を計算
            # i * 60: 各色の基準位置（0度, 60度, 120度...）
            # self.angle: 現在の回転角度
            start_angle = i * 60 + self.angle

            # create_arcで扇形を描画
            # 引数の説明：
            # 1-4: 扇形が内接する四角形の座標（左上x, 左上y, 右下x, 右下y）
            # start: 扇形の開始角度（90度から開始して時計回りに描画）
            # extent: 扇形の角度（60度）
            # fill: 扇形の塗りつぶし色
            self.canvas.create_arc(
                center_x - ROULETTE_RADIUS,  # 左上のX座標
                center_y - ROULETTE_RADIUS,  # 左上のY座標
                center_x + ROULETTE_RADIUS,  # 右下のX座標
                center_y + ROULETTE_RADIUS,  # 右下のY座標
                start=90-start_angle,  # 90度から開始（12時の位置を基準）
                extent=60,  # 扇形の角度（360度÷6色）
                fill=color["code"]  # 色の指定（例：'red', 'blue'など）
            )

    def create_pointer(self):
        """
        ルーレットの上部に表示される矢印（指針）を描画するメソッド
        
        三角形の形状で描画され、常に下向きで固定されています。
        キャンバスの上部中央に配置されます。
        """
        # キャンバスの水平方向の中心を計算
        center_x = CANVAS_SIZE // 2
        # 三角形の頂点のY座標（上からの距離）
        top_y = 30
        
        # 三角形の3つの頂点の座標を定義
        points = [
            center_x, top_y,  # 頂点の座標（中心, 上部）
            # 左下の頂点（中心からPOINTER_SIZEの半分だけ左に移動）
            center_x - POINTER_SIZE//2, top_y + POINTER_SIZE,
            # 右下の頂点（中心からPOINTER_SIZEの半分だけ右に移動）
            center_x + POINTER_SIZE//2, top_y + POINTER_SIZE
        ]
        
        # create_polygonメソッドを使用して三角形を描画
        # points: 三角形の頂点座標のリスト
        # fill: 三角形の塗りつぶし色（黒）
        self.pointer = self.canvas.create_polygon(points, fill="black")

    def start_spin(self):
        """
        ルーレットの回転を開始するメソッド
        スタートボタンが押された時に呼び出されます
        """
        # ルーレットが既に回転していない場合のみ実行
        if not self.is_spinning:
            # 回転中フラグをTrueに設定
            self.is_spinning = True
            # スタートボタンを無効化（連打防止）
            self.start_button.config(state=tk.DISABLED)
            # 別スレッドでルーレットの回転処理を開始
            # メインのGUI処理をブロックしないようにするため
            self.spin_thread = threading.Thread(target=self.spin)
            self.spin_thread.start()

    def stop_spin(self):
        """
        ルーレットの回転を停止するメソッド
        ストップボタンが押された時に呼び出されます
        """
        # ルーレットが回転中の場合のみ実行
        if self.is_spinning:
            # 回転中フラグをFalseに設定して回転を停止
            self.is_spinning = False
            # スタートボタンを再度有効化
            self.start_button.config(state=tk.NORMAL)
            # 停止時の結果を判定して表示
            self.determine_result()

    def spin(self):
        """
        ルーレットを回転させる処理を行うメソッド
        別スレッドで実行され、以下の処理を繰り返します：
        1. 角度を更新（self.angle）
        2. 古い描画を消去
        3. 新しい角度でルーレットを再描画
        4. 指定時間待機
        """
        while self.is_spinning:
            self.angle = (self.angle + ANGLE_STEP) % 360  # 現在の角度を更新（360度で一周）
            self.canvas.delete("all")  # 古い描画を全て消去
            self.create_roulette()    # 新しい角度でルーレットを描画
            self.create_pointer()     # 指針（矢印）を再描画
            time.sleep(ROTATION_SPEED)  # 次の描画までの待機時間

    def determine_result(self):
        """
        ルーレットが停止した時の結果を判定するメソッド
        
        処理の流れ：
        1. 現在の回転角度を計算
        2. 各色の現在の角度を計算
        3. 12時の位置（0-60度の範囲）にある色を特定
        4. 結果をGUI上に表示し、ログにも出力
        """
        # 現在の回転角度を360度以内に正規化
        current_angle = self.angle % 360
        
        print("\n=== ルーレットの状態 ===")
        print(f"開始時の12時の位置: {self.initial_colors[0]['name']}")
        print(f"回転角度: {current_angle}度")
        
        # 各色の現在の角度を計算し、リストに保存
        colors_at_angles = []
        for i, color in enumerate(self.initial_colors):
            # 各色の現在の角度を計算
            # i * 60: 初期位置での角度（0度, 60度, 120度...）
            # current_angle: ルーレットの現在の回転角度
            # % 360: 角度を0-359度の範囲に収める
            color_angle = (i * 60 + current_angle) % 360
            colors_at_angles.append({
                "color": color,  # 色の情報（名前とコード）
                "angle": color_angle  # 計算された現在の角度
            })
            # デバッグ用：各色の現在の角度を表示
            print(f"{color['name']}: {color_angle}度")
        
        # 結果となる色（12時の位置にある色）を特定
        result_color = None
        for color_info in colors_at_angles:
            angle = color_info["angle"]
            # 12時の位置は0-60度の範囲
            if 0 <= angle < 60:
                result_color = color_info["color"]
                break  # 該当する色が見つかったらループを抜ける
        
        # 結果をGUI上に表示
        self.result_label.configure(
            text=f"当選色：{result_color['name']}",  # 結果のテキスト
            fg=result_color['code'],  # テキストの色を当選色に設定
            font=("Arial", 20, "bold")  # フォントスタイルを設定
        )
        
        print(f"\n最終結果: {result_color['name']} (0-60度の位置)")

if __name__ == "__main__":
    RouletteApp()
