import random
import time
import pandas as pd
from decimal import Decimal, ROUND_HALF_UP

# 簡単化ルール辞書
def simplify(func, base_angle):
    rules = {
        "sin": {
            0: "sinθ",
            90: "cosθ",
            180: "-sinθ",
            270: "-cosθ",
            360: "sinθ",
            -90: "-cosθ",
            -180: "-sinθ",
            -270: "cosθ"
        },
        "cos": {
            0: "cosθ",
            90: "-sinθ",
            180: "-cosθ",
            270: "sinθ",
            360: "cosθ",
            -90: "sinθ",
            -180: "-cosθ",
            -270: "-sinθ"
        },
        "tan": {
            0: "tanθ",
            90: "1/tanθ",
            180: "tanθ",
            270: "-1/tanθ",
            360: "tanθ",
            -90: "-1/tanθ",
            -180: "tanθ",
            -270: "1/tanθ"
        }
    }
    return rules[func][base_angle]

# 選択肢は固定
OPTIONS = ["sinθ", "-sinθ", "cosθ", "-cosθ", "tanθ", "-tanθ", "1/tanθ", "-1/tanθ"]

def generate_question():
    funcs = ["sin", "cos", "tan"]
    base_angles = [0, 90, 180, 270, 360, -90, -180, -270]

    func = random.choice(funcs)
    angle = random.choice(base_angles)

    # 角度が0なら括弧なし
    if angle == 0:
        problem = f"{func}θ"
    else:
        sign = "+" if angle > 0 else ""
        problem = f"{func}({angle}°{sign}θ)"

    correct = simplify(func, angle)

    return problem, correct

def main():
    results = []

    while True:
        score = 0
        start_time = time.time()
        feedback = []

        for q in range(1, 11):  # 10問
            problem, correct = generate_question()

            print(f"\n問題{q}: {problem} を簡単にせよ")
            for i, opt in enumerate(OPTIONS, 1):
                print(f"   {i}: {opt}")

            while True:
                try:
                    ans = int(input("答えを選んでください（1-8）: "))
                    if ans in range(1, 9):
                        break
                except ValueError:
                    pass

            if OPTIONS[ans-1] == correct:
                score += 1
                feedback.append(f"問題{q}: 正解！")
            else:
                feedback.append(f"問題{q}: × 正解は {correct}")

        end_time = time.time()
        elapsed = Decimal(str(end_time - start_time)).quantize(Decimal('0.01'), ROUND_HALF_UP)
        total = score * 10  # 10問×10点で100点満点

        print("\n=== 結果 ===")
        for f in feedback:
            print(f)
        print(f"\n得点: {total}/100 点")
        print(f"経過時間: {elapsed} 秒")

        results.append((total, elapsed))
        df = pd.DataFrame(results, columns=["得点", "時間"])
        print("\n試験結果の履歴:")
        print(df)

        retry = int(input("\nもう一度やりますか？（1: はい, 2: いいえ）: "))
        if retry == 2:
            break

if __name__ == "__main__":
    main()
