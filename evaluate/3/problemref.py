import random

def generate_random_number(start, end):
    """ランダムな数字を生成する関数"""
    return random.randint(start, end)

def get_player_guess():
    """プレイヤーからの入力を取得する関数"""
    try:
        return int(input("あなたの予測: "))
    except ValueError:
        print("無効な入力です。数字を入力してください。")

def provide_feedback(guess, correct_number):
    """予測が正解かどうかを判定し、フィードバックを返す関数"""
    if guess < correct_number:
        print("もっと大きい数字です。")
    elif guess > correct_number:
        print("もっと小さい数字です。")

def main():
    """ゲームのメイン関数"""
    correct_number = generate_random_number(1, 100)
    max_attempts = 10
    attempts = 0

    print("1から100までの数字を当ててください！")
    print(f"あなたには {max_attempts} 回のチャンスがあります。")

    while attempts < max_attempts:
        guess = get_player_guess()
        
        attempts += 1
        
        if guess == correct_number:
            print(f"おめでとうございます！正解です！{attempts} 回目で当てました。")
            break
        else:
            provide_feedback(guess, correct_number)
            remaining_attempts = max_attempts - attempts
            print(f"残りのチャンスは {remaining_attempts} 回です。")

    if attempts == max_attempts:
        print(f"残念！正解は {correct_number} でした。次回はもっと頑張りましょう！")

if __name__ == "__main__":
    main()