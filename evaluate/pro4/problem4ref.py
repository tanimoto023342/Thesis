import random

def set_janken_hand(player_choice):
    if player_choice == 0:
        player_hand = "グー"
    elif player_choice == 1:
        player_hand = "チョキ"
    else:
        player_hand = "パー"
    return player_hand

# じゃんけんの手を表示
print("じゃんけんゲームを始めます！")
print("じゃんけんの手を入力してください（グー: 0, チョキ: 1, パー: 2）")

# プレイヤーの手を入力
player_choice = int(input("あなたの選択: "))

# コンピュータの手をランダムに決定
computer_choice = random.randint(0, 2)

# じゃんけんの手の名前
player_hand=set_janken_hand(player_choice)

computer_hand=set_janken_hand(computer_choice)

# コンピュータの手を表示
print("コンピューターの手:", computer_hand)

# 勝敗の判定
if player_choice == computer_choice:
    print("引き分けです！")
elif (player_choice == 0 and computer_choice == 1) or \
     (player_choice == 1 and computer_choice == 2) or \
     (player_choice == 2 and computer_choice == 0):
    print("あなたの勝ちです！")
else:
    print("あなたの負けです！")