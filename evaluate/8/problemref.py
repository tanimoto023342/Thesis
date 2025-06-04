import random

def display_tiles(title, tiles):
    print(f"{title}⇒【", end="")
    print(" ,".join([str(tile) if tile != -1 else "-" for tile in tiles]), end="")
    print("】")

def display_scores(player_score, computer_score):
    print(f"プレイヤーの得点　： {player_score}点")
    print(f"コンピュータの得点： {computer_score}点")

def get_player_choice(tiles):
    while True:
        try:
            choice = int(input("持ち牌の中から出す牌を選択してください > "))
            if choice in tiles:
                return choice
            else:
                print("無効な選択です。再度選択してください。")
        except ValueError:
            print("数字を入力してください。")

def get_computer_choice(tiles):
    return random.choice(tiles)

def judge_win_or_lose(player_score,computer_score):
    if player_score > computer_score:
        print("プレイヤーの勝利です！")
    elif player_score < computer_score:
        print("コンピュータの勝利です！")
    else:
        print("引き分けです！")

def show_result(player_score,computer_score):
    display_scores(player_score, computer_score)

    judge_win_or_lose(player_score,computer_score)

def main():
    # プレイヤーとコンピュータの持ち牌（1〜9）
    player_tiles = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    computer_tiles = [1, 2, 3, 4, 5, 6, 7, 8, 9]

    # プレイヤーとコンピュータの得点
    player_score = 0
    computer_score = 0

    print("ナインゲームを開始します！")

    for round_num in range(1, 10):
        # 現在の回戦を表示
        print(f"\n【第{round_num}回戦】")

        # 現在の得点を表示
        display_scores(player_score, computer_score)

        # 現在の持ち牌を表示
        display_tiles("☆プレイヤーの持ち牌", player_tiles)
        display_tiles("コンピュータの持ち牌", computer_tiles)

        # プレイヤーが牌を選択
        player_choice = get_player_choice([tile for tile in player_tiles if tile != -1])

        # コンピュータが牌を選択
        computer_choice = get_computer_choice([tile for tile in computer_tiles if tile != -1])

        # 両者の牌を比較し、結果を表示
        print(f"プレイヤーの打牌：{player_choice}", end="")
        if player_choice > computer_choice:
            print(f"　＞　{computer_choice}：コンピュータの打牌")
            player_score += player_choice
            print(f"プレイヤーは{player_choice}点獲得")
        elif player_choice < computer_choice:
            print(f"　＜　{computer_choice}：コンピュータの打牌")
            computer_score += computer_choice
            print(f"コンピュータは{computer_choice}点獲得")
        else:
            print(f"　＝　{computer_choice}：コンピュータの打牌")
            print("引き分けです。得点はなし")

        # 使用した牌を無効にする
        player_tiles[player_tiles.index(player_choice)] = -1
        computer_tiles[computer_tiles.index(computer_choice)] = -1

    # 最終結果を表示
    print("\nゲーム終了！")
    show_result(player_score, computer_score)

if __name__ == "__main__":
    main()