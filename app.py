import streamlit as st
import time

if "page" not in st.session_state:
    st.session_state.page = "start"

if "brs_score" not in st.session_state:
    st.session_state.brs_score = None

if "normal_index" not in st.session_state:
    st.session_state.normal_index = 0

if "normal_answers" not in st.session_state:
    st.session_state.normal_answers = []

if "stress_index" not in st.session_state:
    st.session_state.stress_index = 0

if "stress_answers" not in st.session_state:
    st.session_state.stress_answers = []

if "start_time" not in st.session_state:
    st.session_state.start_time = None

# ----------------------
# 初期化
# ----------------------
if "page" not in st.session_state:
    st.session_state.page = "start"
if "brs_score" not in st.session_state:
    st.session_state.brs_score = None

# ----------------------
# Start画面
# ----------------------
if st.session_state.page == "start":

    st.title("意思決定分析システム")

    st.write("ストレス環境による意思決定特性の変化を分析します。")

    if st.button("開始"):
        st.session_state.page = "brs"
        st.rerun()

# ----------------------
# BRS画面
# ----------------------
elif st.session_state.page == "brs":

    st.title("レジリエンス測定（BRS）")

    st.write("以下の質問について最も当てはまるものを選択してください。")

    questions = [
        "私は困難な出来事からすぐに立ち直る。",
        "私はストレスの多い出来事から立ち直るのが難しい。",
        "私は病気や困難を経験してもすぐ回復する。",
        "私は挫折から立ち直るのに時間がかかる。",
        "私は困難な状況を乗り越えるのが得意である。",
        "私は失敗を経験すると立ち直るのが難しい。"
    ]

    options = [1, 2, 3, 4, 5]

    answers = []

    for i, q in enumerate(questions):

        answer = st.radio(
            q,
            options,
            index=None,
            key=f"brs_{i}"
        )

        answers.append(answer)

    if st.button("次へ"):

        if None in answers:
            st.error("すべての質問に回答してください。")

        else:

            scored = answers.copy()

            scored[1] = 6 - scored[1]
            scored[3] = 6 - scored[3]
            scored[5] = 6 - scored[5]

            brs_score = round(sum(scored) / 6, 2)

            st.session_state.brs_score = brs_score

            st.session_state.page = "normal"
            st.rerun()
# ----------------------
# 通常条件
# ----------------------
elif st.session_state.page == "normal":

    questions = [
        {"id":"G1","text":"A：50%で1200円獲得、50%で0円\n\nB：確実に600円獲得"},
        {"id":"G2","text":"A：80%で1000円獲得、20%で0円\n\nB：確実に800円獲得"},
        {"id":"G3","text":"A：40%で2000円獲得、60%で0円\n\nB：確実に700円獲得"},
        {"id":"G4","text":"A：30%で2500円獲得、70%で0円\n\nB：確実に600円獲得"},
        {"id":"G5","text":"A：20%で3000円獲得、80%で0円\n\nB：確実に500円獲得"},
        {"id":"G6","text":"A：10%で7000円獲得、90%で0円\n\nB：確実に400円獲得"},

        {"id":"L1","text":"A：50%で1200円損失、50%で0円\n\nB：確実に600円損失"},
        {"id":"L2","text":"A：80%で1000円損失、20%で0円\n\nB：確実に800円損失"},
        {"id":"L3","text":"A：40%で2000円損失、60%で0円\n\nB：確実に700円損失"},
        {"id":"L4","text":"A：30%で2500円損失、70%で0円\n\nB：確実に600円損失"},
        {"id":"L5","text":"A：20%で3000円損失、80%で0円\n\nB：確実に500円損失"},
        {"id":"L6","text":"A：10%で7000円損失、90%で0円\n\nB：確実に400円損失"},

        {"id":"C1","text":"A：90%で900円獲得、10%で0円\n\nB：確実に800円獲得"},
        {"id":"C2","text":"A：95%で800円獲得、5%で0円\n\nB：確実に700円獲得"},
        {"id":"C3","text":"A：90%で900円損失、10%で0円\n\nB：確実に800円損失"},
        {"id":"C4","text":"A：95%で800円損失、5%で0円\n\nB：確実に700円損失"},
    ]

    idx = st.session_state.normal_index

    if st.session_state.start_time is None:
        st.session_state.start_time = time.time()

    if idx < len(questions):

        q = questions[idx]

        st.title("通常条件")

        st.write(f"問題 {idx+1}/{len(questions)}")

        st.write(q["text"])

        choice = st.radio(
            "選択してください",
            ["A", "B"],
            index=None,
            key=f"normal_{idx}"
        )

        if st.button("次へ", key=f"normal_next_{idx}"):

            if choice is None:

                st.error("選択してください")

            else:

                reaction_time = round(
                    time.time() - st.session_state.start_time,
                    2
                )

                st.session_state.normal_answers.append(
                    {
                        "question_id": q["id"],
                        "choice": choice,
                        "reaction_time": reaction_time
                    }
                )

                st.session_state.start_time = None

                st.session_state.normal_index += 1

                st.rerun()

    else:

        st.success("通常条件終了")

        if st.button("バッファへ"):

            st.session_state.page = "buffer"

            st.rerun()
# ----------------------
# バッファ画面
# ----------------------
elif st.session_state.page == "buffer":

    st.title("条件切替")

    st.write("次は時間制限付き意思決定タスクです。")

    st.warning("各問題は短時間で回答していただきます。")

    if st.button("開始"):

        st.session_state.page = "stress"

        st.rerun()

# ----------------------
# ストレス条件
# ----------------------
elif st.session_state.page == "stress":

    questions = [

        # g（利得）
        {
            "id":"g1",
            "text":"A：50%で1200円獲得、50%で0円\n\nB：確実に600円獲得"
        },
        {
            "id":"g2",
            "text":"A：80%で1000円獲得、20%で0円\n\nB：確実に800円獲得"
        },
        {
            "id":"g3",
            "text":"A：40%で2000円獲得、60%で0円\n\nB：確実に700円獲得"
        },
        {
            "id":"g4",
            "text":"A：30%で2500円獲得、70%で0円\n\nB：確実に600円獲得"
        },
        {
            "id":"g5",
            "text":"A：20%で3000円獲得、80%で0円\n\nB：確実に500円獲得"
        },
        {
            "id":"g6",
            "text":"A：10%で7000円獲得、90%で0円\n\nB：確実に400円獲得"
        },

        # l（損失）
        {
            "id":"l1",
            "text":"A：50%で1200円損失、50%で0円\n\nB：確実に600円損失"
        },
        {
            "id":"l2",
            "text":"A：80%で1000円損失、20%で0円\n\nB：確実に800円損失"
        },
        {
            "id":"l3",
            "text":"A：40%で2000円損失、60%で0円\n\nB：確実に700円損失"
        },
        {
            "id":"l4",
            "text":"A：30%で2500円損失、70%で0円\n\nB：確実に600円損失"
        },
        {
            "id":"l5",
            "text":"A：20%で3000円損失、80%で0円\n\nB：確実に500円損失"
        },
        {
            "id":"l6",
            "text":"A：10%で7000円損失、90%で0円\n\nB：確実に400円損失"
        },

        # c（確実性）
        {
            "id":"c1",
            "text":"A：90%で900円獲得、10%で0円\n\nB：確実に800円獲得"
        },
        {
            "id":"c2",
            "text":"A：95%で800円獲得、5%で0円\n\nB：確実に700円獲得"
        },
        {
            "id":"c3",
            "text":"A：90%で900円損失、10%で0円\n\nB：確実に800円損失"
        },
        {
            "id":"c4",
            "text":"A：95%で800円損失、5%で0円\n\nB：確実に700円損失"
        }

    ]

    idx = st.session_state.stress_index

    if st.session_state.start_time is None:
        st.session_state.start_time = time.time()

    if idx < len(questions):

        q = questions[idx]

        st.title("ストレス条件")

        st.write(f"問題 {idx+1}/{len(questions)}")

        st.write(q["text"])

        choice = st.radio(
            "選択してください",
            ["A", "B"],
            index=None,
            key=f"stress_{idx}"
        )

        if st.button("次へ", key=f"stress_next_{idx}"):

            if choice is None:

                st.error("選択してください")

            else:

                reaction_time = round(
                    time.time() - st.session_state.start_time,
                    2
                )

                st.session_state.stress_answers.append(
                    {
                        "question_id": q["id"],
                        "choice": choice,
                        "reaction_time": reaction_time
                    }
                )

                st.session_state.start_time = None

                st.session_state.stress_index += 1

                st.rerun()

    else:

        st.success("ストレス条件終了")

        if st.button("結果を見る"):

            st.session_state.page = "result"

            st.rerun()
# ----------------------
# 結果画面
# ----------------------
elif st.session_state.page == "result":

    st.title("意思決定分析結果")

    # ----------------------
    # 判断安定性
    # ----------------------

    match_count = 0

    for n, s in zip(
        st.session_state.normal_answers,
        st.session_state.stress_answers
    ):

        if n["choice"] == s["choice"]:
            match_count += 1

    stability = round(
        match_count / len(st.session_state.normal_answers) * 100,
        1
    )

    # ----------------------
    # リスク選択率
    # ----------------------

    normal_risk = round(
        sum(
            1
            for x in st.session_state.normal_answers
            if x["choice"] == "A"
        )
        / len(st.session_state.normal_answers)
        * 100,
        1
    )

    stress_risk = round(
        sum(
            1
            for x in st.session_state.stress_answers
            if x["choice"] == "A"
        )
        / len(st.session_state.stress_answers)
        * 100,
        1
    )

    delta_risk = round(
        stress_risk - normal_risk,
        1
    )

    # ----------------------
    # 安定性分類
    # ----------------------

    if stability >= 80:
        stability_level = "高"

    elif stability >= 50:
        stability_level = "中"

    else:
        stability_level = "低"

    # ----------------------
    # リスク変化分類
    # ----------------------

    if delta_risk <= -20:
        risk_type = "回避化"

    elif delta_risk >= 20:
        risk_type = "挑戦化"

    else:
        risk_type = "中立"

    # ----------------------
    # 9分類
    # ----------------------

    type_table = {

        ("高","回避化"): "慎重安定型",
        ("高","中立"): "中立安定型",
        ("高","挑戦化"): "挑戦安定型",

        ("中","回避化"): "慎重適応型",
        ("中","中立"): "標準型",
        ("中","挑戦化"): "挑戦適応型",

        ("低","回避化"): "慎重変動型",
        ("低","中立"): "中立変動型",
        ("低","挑戦化"): "挑戦変動型"
    }

    result_type = type_table[
        (stability_level, risk_type)
    ]
    type_description = {

    "慎重安定型":
    "ストレス下でも判断が安定しており、リスクを避ける傾向がみられます。",

    "中立安定型":
    "ストレス下でも判断基準がほとんど変化しない安定したタイプです。",

    "挑戦安定型":
    "ストレス下でも積極的な意思決定を維持するタイプです。",

    "慎重適応型":
    "状況に応じて柔軟に判断を変えつつ、やや慎重な傾向があります。",

    "標準型":
    "判断の安定性とリスク傾向のバランスが取れた平均的なタイプです。",

    "挑戦適応型":
    "状況に応じてリスクを取る方向へ適応する傾向があります。",

    "慎重変動型":
    "ストレスによって判断が変化しやすく、回避的な選択が増えるタイプです。",

    "中立変動型":
    "ストレスによって判断基準が変化しやすいタイプです。",

    "挑戦変動型":
    "ストレス環境でリスク選択が大きく増加するタイプです。"
}

    # ----------------------
    # 平均反応時間
    # ----------------------

    normal_rt = round(
        sum(
            x["reaction_time"]
            for x in st.session_state.normal_answers
        )
        / len(st.session_state.normal_answers),
        2
    )

    stress_rt = round(
        sum(
            x["reaction_time"]
            for x in st.session_state.stress_answers
        )
        / len(st.session_state.stress_answers),
        2
    )

    # ----------------------
    # 結果表示
    # ----------------------
    st.subheader(f"あなたのタイプ：{result_type}")

    st.write(type_description[result_type])

    st.divider()

    st.write(f"判断安定性：{stability}%")
    st.write(f"通常条件リスク率：{normal_risk}%")
    st.write(f"ストレス条件リスク率：{stress_risk}%")
    st.write(f"ΔRisk：{delta_risk}%")

    st.write(f"BRSスコア：{st.session_state.brs_score}")

    st.write(f"通常条件平均反応時間：{normal_rt}秒")
    st.write(f"ストレス条件平均反応時間：{stress_rt}秒")

    st.divider()

    st.subheader("3×3分類マトリクス")

    matrix = f"""
| 安定性 \\ リスク | 回避化 | 中立 | 挑戦化 |
|------|------|------|------|
| 高 | {"■" if (stability_level=="高" and risk_type=="回避化") else "□"} | {"■" if (stability_level=="高" and risk_type=="中立") else "□"} | {"■" if (stability_level=="高" and risk_type=="挑戦化") else "□"} |
| 中 | {"■" if (stability_level=="中" and risk_type=="回避化") else "□"} | {"■" if (stability_level=="中" and risk_type=="中立") else "□"} | {"■" if (stability_level=="中" and risk_type=="挑戦化") else "□"} |
| 低 | {"■" if (stability_level=="低" and risk_type=="回避化") else "□"} | {"■" if (stability_level=="低" and risk_type=="中立") else "□"} | {"■" if (stability_level=="低" and risk_type=="挑戦化") else "□"} |
"""

    st.markdown(matrix)
    
    st.info(
        "本分析は正誤を評価するものではなく、"
        "ストレス環境による意思決定特性の変化を可視化することを目的としています。"
    )

    if st.button("最初に戻る"):

        st.session_state.page = "start"

        st.session_state.normal_index = 0
        st.session_state.stress_index = 0

        st.session_state.normal_answers = []
        st.session_state.stress_answers = []

        st.session_state.start_time = None

        st.rerun()