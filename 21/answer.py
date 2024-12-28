"""
ターン制RPG戦闘システム

このプログラムは、プレイヤーとスライムが交互に行動するターン制バトルを実装します。
プレイヤーは3つの行動から1つを選択でき、スライムは状態に応じて攻撃パターンが変化します。
"""

def show_status(player_hp, player_mp, slime_hp, rage_gauge, turn):
    """
    現在のステータスを表示する関数
    
    Args:
        player_hp (int): プレイヤーの現在HP
        player_mp (int): プレイヤーの現在MP
        slime_hp (int): スライムの現在HP
        rage_gauge (int): スライムの怒りゲージ
        turn (int): 現在のターン数
    """
    print(f"\n===== ターン {turn} =====")
    print("===== ステータス =====")
    print("プレイヤー")
    print(f"HP: {player_hp}/100")
    print(f"MP: {player_mp}/50")
    print("-------------------")
    print("スライム")
    print(f"HP: {slime_hp}/50")
    print(f"怒りゲージ: {rage_gauge}/100")
    print("====================")

def show_actions():
    """行動選択肢を表示す���関数"""
    print("\nどのような行動を取りますか？")
    print("1: 剣で攻撃する（スライムに10ダメージ）")
    print("2: 回復魔法を使う（MP-20, HP+30）")
    print("3: 火炎魔法を使う（MP-30, スライムに20ダメージ）")

def player_turn(player_hp, player_mp, slime_hp, rage_gauge):
    """
    プレイヤーのターン処理を行う関数
    
    Returns:
        tuple: 更新後の(player_hp, player_mp, slime_hp, rage_gauge)
    """
    show_actions()
    
    try:
        action = int(input("行動を選択してください（1/2/3）: "))
        
        if action == 1:  # 剣での攻撃
            print("\n剣でスライムを攻撃した！")
            print("スライムに10ダメージ！")
            slime_hp -= 10
            
        elif action == 2:  # 回復魔法
            if player_mp >= 20:
                player_mp -= 20
                recovered = min(30, 100 - player_hp)  # 最大値を超えない回復量
                player_hp += recovered
                print("\n回復魔法を唱えた！")
                print(f"HPが{recovered}回復した！")
                rage_gauge = min(100, rage_gauge + 40)  # 怒りゲージ上昇
            else:
                print("\nMP不足！魔法が暴発した！")
                print(f"現在のMP: {player_mp}/20 必要")
                player_hp -= 15
                player_mp = max(0, player_mp)  # MPが0未満にならないように
                
        elif action == 3:  # 火炎魔法
            if player_mp >= 30:
                player_mp -= 30
                print("\n強大な火炎魔法を放った！")
                print("スライムに20ダメージ！")
                slime_hp -= 20
            else:
                print("\nMP不足！魔法が暴発した！")
                print(f"現在のMP: {player_mp}/30 必要")
                player_hp -= 15
                player_mp = max(0, player_mp)  # MPが0未満にならないように
                
        else:
            print("\n不正な入力です！隙を突かれた！")
            player_hp -= 20
            
    except ValueError:
        print("\n不正な入力です！隙を突かれた！")
        player_hp -= 20
        
    return player_hp, player_mp, slime_hp, rage_gauge

def slime_turn(player_hp, slime_hp, rage_gauge):
    """
    スライムのターン処理を行う関数
    
    Returns:
        tuple: 更新後の(player_hp, rage_gauge)
    """
    print("\nスライムのターン")
    
    if rage_gauge >= 100:  # 必殺技
        print("スライムの必殺技！")
        print("プレイヤーに30ダメージ！")
        player_hp -= 30
        rage_gauge = 0
    elif slime_hp <= 25:  # HP50%以下で強攻撃
        print("スライムの強攻撃！")
        print("プレイヤーに15ダメージ！")
        player_hp -= 15
    else:  # 通常攻撃
        print("スライムの通常攻撃！")
        print("プレイヤーに10ダメージ！")
        player_hp -= 10
        
    # ターン終了時に怒りゲージ上昇
    rage_gauge_before = rage_gauge  # 上昇前の怒りゲージを保存
    rage_gauge = min(100, rage_gauge + 20)
    actual_increase = rage_gauge - rage_gauge_before  # 実際の上昇量を計算
    print(f"\nスライムの怒りゲージが{rage_gauge}%になった！")
    
    return player_hp, rage_gauge

def main():
    # 初期ステータス
    player_hp = 100
    player_mp = 50
    slime_hp = 50
    rage_gauge = 0
    turn = 1
    
    print("暗い森の中、あなたは強大なスライムと対峙しています！")
    
    while True:
        # ステータス表示
        show_status(player_hp, player_mp, slime_hp, rage_gauge, turn)
        
        # プレイヤーのターン
        print("\nプレイヤーのターン")
        player_hp, player_mp, slime_hp, rage_gauge = player_turn(
            player_hp, player_mp, slime_hp, rage_gauge)
            
        # 勝利判定
        if slime_hp <= 0:
            print("\nスライムを倒した！")
            print("勝利！")
            return True
            
        # 敗北判定
        if player_hp <= 0:
            print("\nプレイヤーは倒れた...")
            print("ゲームオーバー")
            return False
            
        # スライムのターン
        player_hp, rage_gauge = slime_turn(player_hp, slime_hp, rage_gauge)
        
        # 敗北判定
        if player_hp <= 0:
            print("\nプレイヤーは倒れた...")
            print("ゲームオーバー")
            return False
            
        turn += 1

if __name__ == "__main__":
    main() 