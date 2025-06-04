#cite from https://programming-mondai.com/top/python_top/
import random

def main():
    # 挨拶を表示
    name = input("あなたの名前を教えてください: ")
    print(f"こんにちは、{name}さん！")

    # ユーザーに2つの数値を入力してもらう
    print("簡単な計算をしましょう！")
    num1 = int(input("最初の数を入力してください: "))
    num2 = int(input("次の数を入力してください: "))

    # 足し算と掛け算を行う
    addition = num1 + num2
    multiplication = num1 * num2

    # 結果を表示する
    print(f"{num1} と {num2} を足すと {addition} になります。")
    print(f"{num1} と {num2} を掛けると {multiplication} になります。")

    # 今日のラッキーナンバーを決める
    random_number = random.randint(1, 10)
    print(f"今日のあなたのラッキーナンバーは {random_number} です！")

    # 終了メッセージ
    print("これでレッスン１の総復習は終わりです。お疲れさまでした！")

main()