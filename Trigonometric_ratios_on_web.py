import streamlit as st
import random
import time
from decimal import Decimal, ROUND_HALF_UP
import pandas as pd 

st.title("三角比クイズ（sin・cos・tan 有名角編）")

# -----------------------------
# CSS（ボタンサイズ調整と列幅固定、中央揃えの再適用）
# -----------------------------
st.markdown("""
<style>
/* 選択肢ボタンのサイズとフォントを統一 */
div.stButton > button {
    width: 160px !important;
    height: 70px !important;
    font-size: 22px;
}
/* st.table/st.dataframe のセル内の数式表示を調整 */
.stTable, .stDataFrame {
    font-size: 18px; /* 全体フォントサイズ調整 */
}

/* ⭐︎ テーブル全体の配置を中央に (再適用) ⭐︎ */
.stTable {
    width: fit-content; 
    margin-left: auto;  
    margin-right: auto; 
}

/* ⭐︎ すべてのセルを中央揃えにする (再適用) ⭐︎ */
.stTable table th, .stTable table td {
    white-space: nowrap; /* セル内の折り返しを禁止 */
    /* !important を付けて強制的に中央揃えを適用 */
    text-align: center !important; 
    vertical-align: middle !important; /* 縦方向も中央に */
}

/* ⭐︎ 列幅固定の維持 (再適用) ⭐︎ */
/* 1列目 (番号/インデックス) */
.stTable table th:nth-child(1), .stTable table td:nth-child(1) {
    width: 60px; 
}
/* 2列目 (問題) - 広い幅を確保 */
.stTable table th:nth-child(2), .stTable table td:nth-child(2) {
    min-width: 220px; 
}
/* 3列目 (あなたの解答) */
.stTable table th:nth-child(3), .stTable table td:nth-child(3) {
    min-width: 150px; 
}
/* 4列目 (正解) */
.stTable table th:nth-child(4), .stTable table td:nth-child(4) {
    min-width: 150px; 
}
/* 5列目 (正誤) - 狭い幅を固定 */
.stTable table th:nth-child(5), .stTable table td:nth-child(5) {
    width: 60px; 
}
</style>
""", unsafe_allow_html=True)

# -----------------------------
# 角度範囲の定義
# -----------------------------
ANGLE_RANGES = {
    "0~90": [0, 30, 45, 60, 90],
    "0~180": [0, 30, 45, 60, 90, 120, 135, 150, 180],
    "ALL": [-360, -330, -315, -300, -270, -240, -225, -210, -180, -150, -135, -120, -90, -60, -45, -30,
            0, 30, 45, 60, 90, 120, 135, 150, 180, 210, 225, 240, 270, 300, 315, 330, 360, 390, 405, 420, 450]
}
functions = ["sin", "cos", "tan"]

# 選択肢、正解の定義 (変更なし、中略)
# ...
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
    "なし": r"$\text{なし}$"
}

sin_cos_options = [
    "1/2", "√2/2", "√3/2", "1",
    "-1/2", "-√2/2", "-√3/2", "-1", "0",
]
tan_options = [
    "0", "1/√3", "1", "√3",
    "なし", "-1/√3", "-1", "-√3"
    
]

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
        -360: "0", -330: "1/√3", -315: "1", -300: "√3", -270: "なし",
        -240: "√3", -225: "1", -210: "1/√3", -180: "0", -150: "-1/√3",
        -135: "-1", -120: "-√3", -90: "なし", -60: "-√3", -45: "-1",
        -30: "-1/√3", 0: "0", 30: "1/√3", 45: "1", 60: "√3", 90: "なし",
        120: "-√3", 135: "-1", 150: "-1/√3", 180: "0", 210: "1/√3",
        225: "1", 240: "√3", 270: "なし", 300: "-√3", 315: "-1",
        330: "-1/√3", 360: "0", 390: "1/√3", 405: "1", 420: "√3", 450: "なし"
    }
}
MAX_QUESTIONS = 10 

# 関数定義
def new_question():
    st.session_state.func = random.choice(functions)
    st.session_state.angle = random.choice(ANGLE_RANGES[st.session_state.angle_range])
    st.session_state.selected = None
    st.session_state.result = ""
    st.session_state.show_result = False

def initialize_session_state():
    if 'range_selected' not in st.session_state:
        st.session_state.range_selected = False
        st.session_state.angle_range = "ALL"
    
    # range_selected が True の場合のみクイズの初期化を行う
    if 'func' not in st.session_state and st.session_state.range_selected:
        st.session_state.score = 0
        st.session_state.question_count = 0
        st.session_state.history = []
        st.session_state.show_result = False
        st.session_state.start_time = time.time()
        new_question()

def check_answer_and_advance():
    if st.session_state.selected is None:
        st.session_state.result = "選択肢を選んでください。"
        return

    current_func = st.session_state.func
    current_angle = st.session_state.angle
    correct = answers[current_func][current_angle]
    
    is_correct = (st.session_state.selected == correct)
    
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
    
    if st.session_state.question_count >= MAX_QUESTIONS:
        st.session_state.show_result = True
    else:
        new_question()
    
    st.rerun()

initialize_session_state()

# -----------------------------------------------
# アプリの描画
# -----------------------------------------------

if not st.session_state.range_selected:
    # 範囲選択画面
    st.header("出題範囲を選択してください")
    
    range_cols = st.columns(3)
    
    if range_cols[0].button(r"$0^\circ \sim 90^\circ$", use_container_width=True):
        st.session_state.angle_range = "0~90"
        st.session_state.range_selected = True
        initialize_session_state()
        st.rerun()
        
    if range_cols[1].button(r"$0^\circ \sim 180^\circ$", use_container_width=True):
        st.session_state.angle_range = "0~180"
        st.session_state.range_selected = True
        initialize_session_state()
        st.rerun()

    if range_cols[2].button(r"$-360^\circ \sim 450^\circ$", use_container_width=True):
        st.session_state.angle_range = "ALL"
        st.session_state.range_selected = True
        initialize_session_state()
        st.rerun()

elif st.session_state.show_result:
    # 結果表示
    end_time = time.time()
    elapsed = Decimal(str(end_time - st.session_state.start_time)).quantize(Decimal('0.01'), ROUND_HALF_UP)
    
    st.header("✨ クイズ終了！ 結果発表 ✨")
    st.markdown(f"**あなたのスコア: {st.session_state.score} / {MAX_QUESTIONS} 問正解**")
    st.write(f"**経過時間: {elapsed} 秒**")
    st.divider()
    
    st.subheader("全解答の確認")
    
    # DataFrame生成
    table_data = []
    for i, item in enumerate(st.session_state.history, 1):
        # 結果表の表示は、\text{} を使って正しく表示
        if item['angle'] < 0:
            func_disp = rf"$\text{{{item['func']}}}\left({item['angle']}^\circ\right)$"
        else:
            func_disp = rf"$\text{{{item['func']}}}  {item['angle']}^\circ$"
            
        user_disp = latex_options.get(item['user_answer'], item['user_answer'])
        correct_disp = latex_options.get(item['correct_answer'], item['correct_answer'])
        mark = "○" if item['is_correct'] else "×"
        
        table_data.append({
            "番号": i,
            "問題": func_disp,
            "あなたの解答": user_disp,
            "正解": correct_disp,
            "正誤": mark
        })

    df = pd.DataFrame(table_data)

    # st.tableで表示（CSSで列幅を固定し、テーブル全体を中央揃え）
    st.table(df.set_index("番号"))
    

    if st.button("もう一度挑戦する"):
        st.session_state.clear()
        initialize_session_state()
        st.rerun()
    
else:
    # クイズ本体
    st.subheader(f"問題 {st.session_state.question_count + 1} / {MAX_QUESTIONS}")
    
    current_func = st.session_state.func
    current_angle = st.session_state.angle
    
    # \sin, \cosなどの標準的な\LaTeXコマンドで表示
    if current_angle < 0:
        question_latex = rf"$$ \{current_func}\left({current_angle}^\circ\right)\ の値は？ $$"
    else:
        question_latex = rf"$$ \{current_func} {current_angle}^\circ\ の値は？ $$"
        
    st.markdown(question_latex)

    if current_func in ["sin", "cos"]:
        display_options = sin_cos_options
    else:
        display_options = tan_options

    cols = st.columns(4) 
    for i, key in enumerate(display_options):
        with cols[i % 4]:
            button_key = f"option_{st.session_state.question_count}_{key}"
            if st.button(latex_options[key], use_container_width=True, key=button_key):
                st.session_state.selected = key
                check_answer_and_advance() 
    
    st.markdown("---")