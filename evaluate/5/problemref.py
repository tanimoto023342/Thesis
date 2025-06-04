import random

# 掛け金を入力する関数
def get_bet(money):
    while True:
        try:
            bet = int(input("いくらかけますか？ ⇒ "))
            if bet > 0 and bet <= money:
                return bet
            else:
                print("無効な入力です！所持金以内の正しい金額を入力してください。")
        except ValueError:
            print("無効な入力です！数字を入力してください。")

# 丁か半かを選択する関数
def get_choice():
    while True:
        try:
            choice = int(input("丁か半か？（丁：0，半：1） ⇒ "))
            if choice == 0 or choice == 1:
                return choice
            else:
                print("無効な入力です！0か1を入力してください。")
        except ValueError:
            print("無効な入力です！数字を入力してください。")

# サイコロを振る関数（リストも使わない）
def roll_dice():
    return random.randint(1,6)

# 続けるかどうかを確認する関数
def ask_continue():
    while True:
        try:
            continue_game = int(input("続けますか？（はい：0，いいえ：1） ⇒ "))
            if continue_game == 0 or continue_game == 1:
                return continue_game
            else:
                print("無効な入力です！0か1を入力してください。")
        except ValueError:
            print("無効な入力です！数字を入力してください。")

# メインのゲーム関数
def cho_han_game():
    print("丁半賭博ゲームを始めます！")
    
    money = 1000  # プレイヤーの初期所持金
    
    while money > 0:
        print(f"プレイヤーの所持金: {money}円")
        
        # 掛け金を取得
        bet = get_bet(money)
        
        # 丁か半かの選択
        choice = get_choice()
        
        # サイコロを振る
        dice1 = roll_dice()
        dice2 = roll_dice()
        dice_sum = dice1 + dice2
        print(f"サイコロの目: {dice1}, {dice2} ⇒ {'丁' if dice_sum % 2 == 0 else '半'}")
        
        # 勝敗判定
        if (dice_sum % 2 == 0 and choice == 0) or (dice_sum % 2 != 0 and choice == 1):
            print(f"あなたの勝ち！賞金は{bet}円")
            money += bet
        else:
            print(f"あなたの負け！{bet}円没収！")
            money -= bet
        
        # 続けるかどうかを確認
        if money > 0:
            if ask_continue() == 1:
                print(f"最終所持金は{money}円でした。")
                break
        else:
            print("所持金がなくなりました。ゲームを終了します。")
            break

    print(f"最終所持金は{money}円でした。丁半賭博ゲームを終わります。")

# ゲームを実行
cho_han_game()