def show_pocket(pocket):
    print("\n現在のポケット：")
    for snack, count in pocket.items():
        print(f"- {snack}: {count}個")

def add_snack(pocket, snack_name):
    if snack_name in pocket:
        pocket[snack_name] += 1
        print(f"\nポケットをたたきました！")
        print(f"{snack_name}が1個増えました！")
    else:
        pocket[snack_name] = 1
        print(f"\nポケットをたたきました！")
        print(f"新しいお菓子「{snack_name}」が追加されました！")

def main():
    # 初期のポケットの状態
    pocket = {
        "ポッキー": 2,
        "キットカット": 1,
        "ぷっちょ": 3
    }

    while True:
        show_pocket(pocket)
        print("\n追加したいお菓子を入力してください（終了する場合は'q'）：", end=" ")
        snack_name = input()
        
        if snack_name.lower() == 'q':
            print("\nプログラムを終了します。")
            break
            
        add_snack(pocket, snack_name)

if __name__ == "__main__":
    main() 