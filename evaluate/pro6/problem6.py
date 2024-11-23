# 石取りゲームの開始
def take_turn(player, stones):
    # 各プレイヤーのターンを処理する関数
    print(f"\n{player}の番です。残りの石は {stones} 個です。")
    
    move = int(input(f"{player}, 何個の石を取りますか？（1~3個まで選べます）："))
    
    # プレイヤーが有効な数を選択するまで繰り返し
    while not (1 <= move <= 3 and move <= stones):
        print("無効な選択です。もう一度選んでください。")
        move = int(input(f"{player}, 何個の石を取りますか？（1~3個まで選べます）："))
    
    # 石を減らす
    stones -= move
    return stones

def play_game():
    # 石取りゲームのメイン関数
    print("石取りゲームへようこそ！")
    stones = 15  # ゲーム開始時の石の数
    turn = 1  # 1ならプレイヤー1、2ならプレイヤー2
    
    # 石が残っている限りゲームを続ける
    while stones > 0:
        # プレイヤーの切り替え
        if turn == 1:
            current_player = "プレイヤー1"
        else:
            current_player = "プレイヤー2"
        
        # 現在のプレイヤーのターンを実行
        stones = take_turn(current_player, stones)
        
        # 石が0になったらゲーム終了
        if stones == 0:
            print(f"\n{current_player}が最後の石を取りました。{current_player}の負けです！")
            break
        
        # ターンを交代
        if turn == 1:
            turn = 2
        else:
            turn = 1

# ゲームの実行
if __name__ == "__main__":
    play_game()