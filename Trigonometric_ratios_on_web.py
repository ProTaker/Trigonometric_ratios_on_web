import streamlit as st
import random

st.title("三角比クイズ（sin・cos・tan 有名角編）")

# 有名角（度数法）
famous_angles = [-360, -330, -315, -300, -270, -240, -225, -210, -180, -150, -135, -120, -90, -60, -45, -30,
                 0, 30, 45, 60, 90, 120, 135, 150, 180, 210, 225, 240, 270, 300, 315, 330, 360, 390, 405, 420, 450]

# 出題対象の三角関数
functions = ["sin", "cos", "tan"]

# ✅ 選択肢（LaTeX表記できれいに）
latex_options = {
    "0": r"$\displaystyle 0$",
    "1/2": r"$\displaystyle \frac{1}{2}$",
    "√2/2": r"$\displaystyle \frac{\sqrt{2}}{2}$",
    "√3/2": r"$\displaystyle \frac{\sqrt{3}}{2}$",
    "1": r"$\displaystyle 1$",
    "-1/2": r"$\displaystyle -\frac{1}{2}$",
    "-√2/2": r"$\displaystyle -\frac{\sqrt{2}}{2}$",
    "-√3/2": r"$\displaystyle -\frac{\sqrt{3}}{2}$",
    "-1": r"$\displaystyle -1$",
    "√3": r"$\displaystyle \sqrt{3}$",
    "-√3": r"$\displaystyle -\sqrt{3}$",
    "1/√3": r"$\displaystyle \frac{1}{\sqrt{3}}$",
    "-1/√3": r"$\displaystyle -\frac{1}{\sqrt{3}}$",
    "定義なし": r"$\text{定義なし}$"
}

# -----------------------------------------------
# 選択肢の分類（sin/cos 用と tan 用）
# -----------------------------------------------
sin_cos_options = [
    "0", "1/2", "√2/2", "√3/2", "1",
    "-1/2", "-√2/2", "-√3/2", "-1"
]
tan_options = [
    "0", "1", "√3", "1/√3",
    "-1", "-√3", "-1/√3",
    "定義なし"
]

# 有名角に対する正解辞書
answers = {
    "sin": {
        -360: "0", -330: "1/2", -315: "√2/2", -300: "√3/2", -270: "1",
        -240: "√3/2", -225: "√2/2", -210: "1/2", -180: "0", -150: "-1/2",
        -135: "-√2/2", -120: "-√3/2", -90: "-1", -60: "-√3/2", -45: "-√2/2",
        -30: "-1/2", 0: "0", 30: "1/2", 45: "√2/2", 60: "√3/2", 90: "1",
        120: "√3/2", 135: "√2/2", 150: "1/2", 180: "0", 210: "-1/2",
        225: "-√2/2", 240: "-√3/2", 270: "-1", 300: "-√3/2", 315: "-√2/2",
        330: "-1/2", 360: "0", 390: "1/2", 405: "√2/2", 420: "√3/2", 450: "1"
    },
    "cos": {
        -360: "1", -330: "√3/2", -315: "√2/2", -300: "1/2", -270: "0",
        -240: "-1/2", -225: "-√2/2", -210: "-√3/2", -180: "-1", -150: "-√3/2",
        -135: "-√2/2", -120: "-1/2", -90: "0", -60: "1/2", -45: "√2/2",
        -30: "√3/2", 0: "1", 30: "√3/2", 45: "√2/2", 60: "1/2", 90: "0",
        120: "-1/2", 135: "-√2/2", 150: "-√3/2", 180: "-1", 210: "-√3/2",
        225: "-√2/2", 240: "-1/2", 270: "0", 300: "1/2", 315: "√2/2",
        330: "√3/2", 360: "1", 390: "√3/2", 405: "√2/2", 420: "1/2", 450: "0"
    },
    "tan": {
        -360: "0", -330: "1/√3", -315: "1", -300: "√3", -270: "定義なし",
        -240: "√3", -225: "1", -210: "1/√3", -180: "0", -150: "-1/√3",
        -135: "-1", -120: "-√3", -90: "定義なし", -60: "-√3", -45: "-1",
        -30: "-1/√3", 0: "0", 30: "1/√3", 45: "1", 60: "√3", 90: "定義なし",
        120: "-√3", 135: "-1", 150: "-1/√3", 180: "0", 210: "1/√3",
        225: "1", 240: "√3", 270: "定義なし", 300: "-√3", 315: "-1",
        330: "-1/√3", 360: "0", 390: "1/√3", 405: "1", 420: "√3", 450: "定義なし"
    }
}

MAX_QUESTIONS = 10 # 制限問題数

# 新しい問題を作る関数
def new_question():
    st.session_state.func = random.choice(functions)
    st.session_state.angle = random.choice(famous_angles)
    st.session_state.selected = None
    st.session_state.result = ""
    st.session_state.show_result = False # 結果表示フラグをリセット

# セッションステートの初期化とリセット
def initialize_session_state():
    if 'func' not in st.session_state:
        st.session_state.score = 0
        st.session_state.question_count = 0
        st.session_state.history = []
        st.session_state.show_result = False # 結果表示フラグ
        new_question()

def check_answer_and_advance():
    if st.session_state.selected is None:
        st.session_state.result = "選択肢を選んでください。"
        return

    current_func = st.session_state.func
    current_angle = st.session_state.angle
    correct = answers[current_func][current_angle]
    
    is_correct = (st.session_state.selected == correct)
    
    # 履歴に保存
    st.session_state.history.append({
        "func": current_func,
        "angle": current_angle,
        "user_answer": st.session_state.selected,
        "correct_answer": correct,
        "is_correct": is_correct
    })

    if is_correct:
        st.session_state.score += 1

    st.session_state.question_count += 1
    
    # 問題数制限に達したら結果表示フラグを立てる
    if st.session_state.question_count >= MAX_QUESTIONS:
        st.session_state.show_result = True
    else:
        new_question()
    
    st.rerun() # 画面を更新

# 初期化実行
initialize_session_state()

# -----------------------------------------------
# アプリの描画
# -----------------------------------------------

# 問題数が MAX_QUESTIONS に達しているかチェック
if st.session_state.show_result:
    st.header("✨ クイズ終了！ 結果発表 ✨")
    st.markdown(f"**あなたのスコア: {st.session_state.score} / {MAX_QUESTIONS} 問正解**")
    st.divider()
    
    st.subheader("全解答の確認")
    for i, item in enumerate(st.session_state.history):
        question_text = f"Q{i+1}: ${item['func']}({item['angle']}^\\circ)$"
        user_latex = latex_options.get(item['user_answer'], item['user_answer'])
        correct_latex = latex_options.get(item['correct_answer'], item['correct_answer'])
        
        result_icon = "✅" if item['is_correct'] else "❌"
        
        st.markdown(f"**{result_icon}** {question_text}")
        st.markdown(f"**あなたの答え:** {user_latex}")
        st.markdown(f"**正解:** {correct_latex}")
        st.markdown("---")
        
    if st.button("もう一度挑戦する"):
        st.session_state.clear()
        initialize_session_state()
        st.rerun()
    
else:
    # 問題の表示
    st.subheader(f"第 {st.session_state.question_count + 1} 問 / {MAX_QUESTIONS}")
    
    current_func = st.session_state.func
    st.subheader(f"${current_func}({st.session_state.angle}^\\circ)$ の値は？")

    # 選択肢の決定
    if current_func in ["sin", "cos"]:
        display_options = sin_cos_options
    else:
        display_options = tan_options

    # 選択肢ボタンの表示と処理
    cols = st.columns(4) 
    for i, key in enumerate(display_options):
        with cols[i % 4]:
            # ボタンのキーを問題ごとにユニークにする
            button_key = f"option_{st.session_state.question_count}_{key}"
            if st.button(latex_options[key], use_container_width=True, key=button_key):
                st.session_state.selected = key
                st.session_state.result = f"選択中: {latex_options[key]}"

    # 結果表示（選択中の答えを示すために利用）
    st.markdown(st.session_state.result)
    
    # 「解答を確認」ボタンは非表示（ご要望により10問終わるまでスキップ）
    # 代わりに「次の問題へ」ボタンで回答をチェックし、進める

    # 次の問題ボタン（回答確定と次の問題への遷移を兼ねる）
    if st.button("解答を確定し、次の問題へ"):
        check_answer_and_advance()

    # st.markdown(st.session_state.result) # ここは選択中の答え表示に使うため、結果表示は最後に集約