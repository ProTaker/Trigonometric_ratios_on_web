import streamlit as st
import random
import math
import pandas as pd

# タイトル
st.title("三角比クイズアプリ")

# クイズの設定
angles = [0, 30, 45, 60, 90, 120, 135, 150, 180, 210, 225, 240, 270, 300, 315, 330, 360]
ratios = ["sin", "cos", "tan"]

# 状態の初期化
if "question" not in st.session_state:
    st.session_state.question = None
if "answer" not in st.session_state:
    st.session_state.answer = None
if "show_answer" not in st.session_state:
    st.session_state.show_answer = False
if "history" not in st.session_state:
    st.session_state.history = []
if "count" not in st.session_state:
    st.session_state.count = 0

# 新しい問題を作る関数
def new_question():
    angle = random.choice(angles)
    ratio = random.choice(ratios)
    st.session_state.question = f"{ratio}({angle}°)"
    
    if ratio == "sin":
        st.session_state.answer = round(math.sin(math.radians(angle)), 3)
    elif ratio == "cos":
        st.session_state.answer = round(math.cos(math.radians(angle)), 3)
    else:
        try:
            st.session_state.answer = round(math.tan(math.radians(angle)), 3)
        except:
            st.session_state.answer = "定義されない"
    
    st.session_state.show_answer = False

# 初回表示時
if st.session_state.question is None:
    new_question()

# 問題表示
st.header(f"第 {st.session_state.count + 1} 問")
st.subheader(st.session_state.question)

# 回答入力
user_input = st.text_input("あなたの答えを入力（例：0.866 または '定義されない'）")

# ボタン
col1, col2 = st.columns(2)
with col1:
    if st.button("答えを表示"):
        st.session_state.show_answer = True

with col2:
    if st.button("次の問題"):
        # 採点して履歴に追加
        correct = str(st.session_state.answer)
        user_ans = user_input.strip()
        result = "正解" if user_ans == correct else "不正解"
        
        st.session_state.count += 1
        st.session_state.history.append({
            "問題番号": st.session_state.count,
            "問題": st.session_state.question,
            "あなたの解答": user_ans,
            "正解": correct,
            "正誤": result
        })

        new_question()
        st.rerun()

# 答え表示
if st.session_state.show_answer:
    st.write(f"正解： **{st.session_state.answer}**")

# 履歴表示
if len(st.session_state.history) > 0:
    st.subheader("これまでの結果")
    df = pd.DataFrame(st.session_state.history)
    st.dataframe(df, use_container_width=True)
