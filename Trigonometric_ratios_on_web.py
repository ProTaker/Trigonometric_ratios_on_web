if st.session_state.show_result:
    end_time = time.time()
    elapsed = Decimal(str(end_time - st.session_state.start_time)).quantize(Decimal('0.01'), ROUND_HALF_UP)
    
    st.header("✨ クイズ終了！ 結果発表 ✨")
    st.markdown(f"**あなたのスコア: {st.session_state.score} / {MAX_QUESTIONS} 問正解**")
    st.write(f"**経過時間: {elapsed} 秒**")
    st.divider()
    
    st.subheader("全解答の確認")

    # HTMLテーブル生成
    table_html = """
    <style>
        table {
            border-collapse: collapse;
            width: 100%;
            text-align: center;
            font-size: 16px;
        }
        th, td {
            border: 1px solid #999;
            padding: 8px;
        }
        th {
            background-color: #f0f0f0;
        }
        .correct { color: green; font-weight: bold; }
        .wrong { color: red; font-weight: bold; }
    </style>
    <table>
        <tr>
            <th>番号</th>
            <th>問題</th>
            <th>あなたの解答</th>
            <th>正解</th>
            <th>正誤</th>
        </tr>
    """

    for i, item in enumerate(st.session_state.history, 1):
        question_text = f"\\({item['func']}({item['angle']}^\\circ)\\)"
        user_latex = latex_options.get(item['user_answer'], item['user_answer'])
        correct_latex = latex_options.get(item['correct_answer'], item['correct_answer'])
        mark = "○" if item['is_correct'] else "×"
        mark_class = "correct" if item['is_correct'] else "wrong"
        
        row_html = f"""
        <tr>
            <td>{i}</td>
            <td>{question_text}</td>
            <td>\\({user_latex}\\)</td>
            <td>\\({correct_latex}\\)</td>
            <td class="{mark_class}">{mark}</td>
        </tr>
        """
        table_html += row_html

    table_html += "</table>"

    # 表示（LaTeXも有効化）
    st.markdown(table_html, unsafe_allow_html=True)

    if st.button("もう一度挑戦する"):
        st.session_state.clear()
        initialize_session_state()
        st.rerun()
