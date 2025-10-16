# trig_quiz_app_on_web.py
import streamlit as st
from pathlib import Path

# --- 設定：既存ファイル名（必要ならここを編集） ---
DEGREE_FILE = "trig_quiz_choice_app_on_web.py"
RADIAN_FILE = "trig_quiz_choice_rad_app_on_web.py"

# セッション状態の初期化
if "page" not in st.session_state:
    st.session_state.page = "home"

def go_home():
    st.session_state.page = "home"
    # 明示的に再実行（必要なら）
    st.experimental_rerun()

def run_external_script(path: str):
    """
    与えられたファイルの Python ソースを読み込んで、そのまま exec して実行します。
    実行時には streamlit (st) を使えるように globals に渡します。
    """
    p = Path(path)
    if not p.exists():
        st.error(f"ファイルが見つかりません: {path}")
        return

    src = p.read_text(encoding="utf-8")

    # 外部スクリプト実行用のグローバル名前空間を用意。
    # st を渡すことで、外部ファイル内の st.xxx 呼び出しが動作します。
    exec_globals = {
        "__name__": "__main__",  # スクリプト実行時と同じ振る舞いに
        "st": st,
    }

    # 実行。外部ファイル内のトップレベルの Streamlit UI がここで描画される。
    try:
        exec(compile(src, path, "exec"), exec_globals)
    except Exception as e:
        st.exception(e)

# --- UI: ホーム画面 ---
st.title("🎯 三角関数クイズ（統合版）")

if st.session_state.page == "home":
    st.write("モードを選んでください。")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("度数法（°）"):
            st.session_state.page = "degree"
            st.experimental_rerun()
    with col2:
        if st.button("弧度法（ラジアン）"):
            st.session_state.page = "radian"
            st.experimental_rerun()

# --- 度数法ページ ---
elif st.session_state.page == "degree":
    st.markdown("## 📏 度数法モード")
    st.write("以下は既存の度数法版スクリプトをそのまま実行します。")
    run_external_script(DEGREE_FILE)
    st.divider()
    if st.button("ホームに戻る"):
        go_home()

# --- 弧度法ページ ---
elif st.session_state.page == "radian":
    st.markdown("## 📐 弧度法モード")
    st.write("以下は既存の弧度法版スクリプトをそのまま実行します。")
    run_external_script(RADIAN_FILE)
    st.divider()
    if st.button("ホームに戻る"):
        go_home()
