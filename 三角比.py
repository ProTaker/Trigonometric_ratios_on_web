from math import radians, degrees, sin, cos, tan, isclose, pi
import random

def main():
    print("三角比テストプログラム")
    print("最初に計算モードを選択してください：")
    print("1. 度数法 (Degrees)")
    print("2. 弧度法 (Radians)")
    
    while True:
        mode = input("\nモードを選択してください (1 または 2): ")
        if mode == "1":
            mode = "degrees"
            break
        elif mode == "2":
            mode = "radians"
            break
        else:
            print("無効な選択です。もう一度試してください。")
    
    print(f"\nモード: {'度数法' if mode == 'degrees' else '弧度法'}")
    
    while True:
        print("\n1. 三角比を確認する")
        print("2. 三角比のクイズに挑戦する")
        print("0. 終了する")
        
        choice = input("\n選択してください (0, 1, 2): ")
        if choice == "1":
            calculate_trig_with_root_and_approximation(mode)
        elif choice == "2":
            trig_quiz_with_choices(mode)
        elif choice == "0":
            print("プログラムを終了します。")
            break
        else:
            print("無効な選択です。もう一度試してください。")

# 特定の角度に対する三角比の値を定義
def trig_values():
    """ 度数法での特定の角度に対する三角比の値 """
    degree_values = {
        -360: {"sin": "0", "cos": "1", "tan": "0"},
        -330: {"sin": "-1/2", "cos": "√3/2", "tan": "-1/√3"},
        -315: {"sin": "-√2/2", "cos": "√2/2", "tan": "-1"},
        -300: {"sin": "-√3/2", "cos": "1/2", "tan": "-√3"},
        -270: {"sin": "-1", "cos": "0", "tan": "定義なし"},
        -240: {"sin": "-√3/2", "cos": "-1/2", "tan": "√3"},
        -225: {"sin": "-√2/2", "cos": "-√2/2", "tan": "1"},
        -210: {"sin": "-1/2", "cos": "-√3/2", "tan": "1/√3"},
        -180: {"sin": "0", "cos": "-1", "tan": "0"},
        -150: {"sin": "1/2", "cos": "-√3/2", "tan": "-1/√3"},
        -135: {"sin": "√2/2", "cos": "-√2/2", "tan": "-1"},
        -120: {"sin": "√3/2", "cos": "-1/2", "tan": "-√3"},
        -90: {"sin": "1", "cos": "0", "tan": "定義なし"},
        -60: {"sin": "√3/2", "cos": "1/2", "tan": "√3"},
        -45: {"sin": "√2/2", "cos": "√2/2", "tan": "1"},
        -30: {"sin": "1/2", "cos": "√3/2", "tan": "1/√3"},
        0: {"sin": "0", "cos": "1", "tan": "0"},
        30: {"sin": "1/2", "cos": "√3/2", "tan": "1/√3"},
        45: {"sin": "√2/2", "cos": "√2/2", "tan": "1"},
        60: {"sin": "√3/2", "cos": "1/2", "tan": "√3"},
        90: {"sin": "1", "cos": "0", "tan": "定義なし"},
        120: {"sin": "√3/2", "cos": "-1/2", "tan": "-√3"},
        135: {"sin": "√2/2", "cos": "-√2/2", "tan": "-1"},
        150: {"sin": "1/2", "cos": "-√3/2", "tan": "-1/√3"},
        180: {"sin": "0", "cos": "-1", "tan": "0"},
        210: {"sin": "-1/2", "cos": "-√3/2", "tan": "1/√3"},
        225: {"sin": "-√2/2", "cos": "-√2/2", "tan": "1"},
        240: {"sin": "-√3/2", "cos": "-1/2", "tan": "√3"},
        270: {"sin": "-1", "cos": "0", "tan": "定義なし"},
        300: {"sin": "-√3/2", "cos": "1/2", "tan": "-√3"},
        315: {"sin": "-√2/2", "cos": "√2/2", "tan": "-1"},
        330: {"sin": "-1/2", "cos": "√3/2", "tan": "-1/√3"},
        360: {"sin": "0", "cos": "1", "tan": "0"},
        390: {"sin": "1/2", "cos": "√3/2", "tan": "1/√3"},
        405: {"sin": "√2/2", "cos": "√2/2", "tan": "1"},
        420: {"sin": "√3/2", "cos": "1/2", "tan": "√3"},
        450: {"sin": "1", "cos": "0", "tan": "定義なし"},
    }
    return degree_values

def calculate_trig_with_root_and_approximation(mode):
    try:
        angle = float(input("角度を入力してください（有名角のみ対応）: "))
        values = trig_values()

        n_angle = normalize_angle(angle, mode)
        if mode == "degrees" and n_angle in values:
            print(f"\n角度: {n_angle} 度")
            print(f"sin({n_angle}) = {values[n_angle]['sin']}")
            print(f"cos({n_angle}) = {values[n_angle]['cos']}")
            print(f"tan({n_angle}) = {values[n_angle]['tan']}")
        else:
            print("この角度はサポートされていません。")
    except Exception as e:
        print(f"エラーが発生しました: {e}")

def trig_quiz_with_choices(mode):
    values = trig_values()
    special_angles = list(values.keys())  # 有名角をリストにする
    random_angle = random.choice(special_angles)

    if mode == "radians":
        n_angle = radians(random_angle)  # 弧度法の場合は変換
        angle_display = f"{n_angle:.2f} ラジアン"
    else:
        n_angle = random_angle
        angle_display = f"{n_angle} 度"

    correct_answers = values[random_angle]

    print(f"\nクイズ: 次の角度 {n_angle} についての三角比を答えてください。")

    # sinの選択肢
    sin_choices = generate_choices(correct_answers["sin"])
    print(f"\nsin({angle_display}) の選択肢:")
    for i, choice in enumerate(sin_choices):
        print(f"{i + 1}. {choice}")
    sin_answer = int(input("正しい選択肢の番号を入力してください: "))
    check_answer("sin", sin_choices[sin_answer - 1], correct_answers["sin"])

    # cosの選択肢
    cos_choices = generate_choices(correct_answers["cos"])
    print("\ncos の選択肢:")
    for i, choice in enumerate(cos_choices):
        print(f"{i + 1}. {choice}")
    cos_answer = int(input("正しい選択肢の番号を入力してください: "))
    check_answer("cos", cos_choices[cos_answer - 1], correct_answers["cos"])

    # tanの選択肢
    tan_choices = generate_choices(correct_answers["tan"])
    print("\ntan の選択肢:")
    for i, choice in enumerate(tan_choices):
        print(f"{i + 1}. {choice}")
    tan_answer = int(input("正しい選択肢の番号を入力してください: "))
    check_answer("tan", tan_choices[tan_answer - 1], correct_answers["tan"])

def normalize_angle(angle, mode):
    """ 角度を正規化して、範囲内に収める """
    if mode == "degrees":
        return angle % 360
    elif mode == "radians":
        return angle % (2 * pi)

def generate_choices(correct_value):
    """ 正しい値を含む選択肢を生成 """
    incorrect_choices = {"1/2", "√3/2", "√2/2", "0", "1", "-1", "定義なし"} - {correct_value}
    return random.sample(list(incorrect_choices), 3) + [correct_value]

def check_answer(name, user_choice, correct_value):
    """ 回答をチェックして結果を表示 """
    if user_choice == correct_value:
        print(f"{name}: 正解です！")
    else:
        print(f"{name}: 不正解です。正解は {correct_value} です。")

if __name__ == "__main__":
    main()
