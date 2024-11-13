

# funcdef文 - 関数を定義
def process_numbers(numbers):
    total = 0            # 代入文 - 初期化
    for num in numbers:   # for文とelse文
        # 累算代入文 - 合計に加算
        total += num

        # if文とelif, else文
        if num < 0:
            print("Negative number found, stopping process.")
            break        # break文
        elif num == 0:
            print("Zero found, continuing to next number.")
            continue     # continue文
        else:
            print(f"Processing number: {num}")

    else:
        # for文に伴うelse文 - breakが発生しない場合に実行
        print("All numbers processed successfully.")

    return total

# メインの処理
numbers = [1, 2, 3, -1, 5]   # リストの定義
result = process_numbers(numbers)   # 式文 - 関数呼び出しを文として使用
print("Total:", result)

# while文とelse文
count = 0
while count < 3:
    print(f"Count is {count}")
    count += 1    # 累算代入文 - インクリメント
else:
    print("Reached the end of the while loop.")

# pass文
for _ in range(5):
    pass    # pass文 - 何も行わないプレースホルダー
