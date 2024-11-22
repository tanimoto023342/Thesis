import random

def high_and_row_game():
    # ハイアンドローゲーム開始メッセージ
    print("=== ハイアンドローゲームへようこそ！ ===")

    # プレイヤーとコンピュータにランダムなカード（1〜13の数字）を配る
    player_card = random.randint(1, 13)
    computer_card = random.randint(1, 13)

    # プレイヤーに配られたカードを表示し、コンピュータのカードはまだ表示しない
    print(f"【プレイヤー】{player_card} VS ??【コンピュータ】")

    # プレイヤーにコンピュータのカードが大きいか小さいかを予想させる
    print("あなたのカードはコンピュータのカードより大きい？小さい？")
    print("1: 大きい、2: 小さい")
    choice = int(input("⇒ "))

    # コンピュータのカードを表示
    print(f"【プレイヤー】{player_card} VS {computer_card}【コンピュータ】")

    # 勝負の結果を判定
    if player_card == computer_card:
        print("引き分け！")
    elif (player_card < computer_card and choice == 1) or (player_card > computer_card and choice == 2):
        print("正解！あなたの勝ち！")
    else:
        print("残念！あなたの負け！")

high_and_row_game()