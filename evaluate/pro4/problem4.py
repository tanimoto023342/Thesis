import random

# じゃんけんの手を表示
print("じゃんけんゲームを始めます！")
print("じゃんけんの手を入力してください（グー: 0, チョキ: 1, パー: 2）")

# プレイヤーの手を入力
player_choice = int(input("あなたの選択: "))

# コンピュータの手をランダムに決定
computer_choice = random.randint(0, 2)

# じゃんけんの手の名前
if player_choice == 0:
    player_hand = "グー"
elif player_choice == 1:
    player_hand = "チョキ"
else:
    player_hand = "パー"

if computer_choice == 0:
    computer_hand = "グー"
elif computer_choice == 1:
    computer_hand = "チョキ"
else:
    computer_hand = "パー"

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