import streamlit as st
import pandas as pd
import plotly.express as px
import time
import csv
import os


from datetime import datetime

def generate_participant_id():

    if os.path.exists("results.csv"):

        df = pd.read_csv("results.csv")

        next_id = len(df) + 1

    else:

        next_id = 1

    return f"P{next_id:05d}"

def save_result():

    file_exists = os.path.isfile("results.csv")

    with open(
        "results.csv",
        "a",
        newline="",
        encoding="utf-8-sig"
    ) as f:

        writer = csv.writer(f)

        if not file_exists:

            header = [
                "Participant_ID",
                "DateTime",
                "BRS_Pre",
                "BRS_Post",
                "BRS_Delta",
                "Stability",
                "Normal_Risk",
                "Stress_Risk",
                "Delta_Risk",
                "Normal_RT",
                "Stress_RT",
                "NoAnswer_Count",
                "Type"
            ]

            for answer in st.session_state.normal_answers:
                header.append(
                    f"Normal_{answer['question_id']}"
                )

            for answer in st.session_state.stress_answers:
                header.append(
                    f"Stress_{answer['question_id']}"
                )

            writer.writerow(header)

        normal_choices = {
            a["question_id"]: a["choice"]
            for a in st.session_state.normal_answers
        }

        stress_choices = {
            a["question_id"]: a["choice"]
            for a in st.session_state.stress_answers
        }

        row = [
            st.session_state.participant_id,
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            st.session_state.brs_score,
            st.session_state.post_brs_score,
            round(
                st.session_state.post_brs_score
                - st.session_state.brs_score,
                2
            ),
            stability,
            normal_risk,
            stress_risk,
            delta_risk,
            normal_rt,
            stress_rt,
            noanswer_count,
            result_type
        ]

        for answer in st.session_state.normal_answers:
            row.append(answer["choice"])

        for answer in st.session_state.stress_answers:
            row.append(answer["choice"])

        writer.writerow(row)

from streamlit_autorefresh import st_autorefresh

if "page" not in st.session_state:
    st.session_state.page = "start"

if "brs_score" not in st.session_state:
    st.session_state.brs_score = None

if "post_brs_score" not in st.session_state:
    st.session_state.post_brs_score = None

if (
    "participant_id" not in st.session_state
    or st.session_state.participant_id is None
):

    st.session_state.participant_id = (
        generate_participant_id()
    )

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

    st.write(
        "ストレス環境による意思決定特性の変化を分析します。"
    )

    if st.button("開始"):

        if (
            "participant_id" not in st.session_state
            or st.session_state.participant_id is None
        ):

            st.session_state.participant_id = (
                generate_participant_id()
            )

        st.session_state.page = "brs"

        st.rerun()
# ----------------------
# BRS画面
# ----------------------
elif st.session_state.page == "brs":

    st.title("レジリエンス測定（BRS）")

    st.write("以下の質問について最も当てはまるものを選択してください。")
    
    st.info(
    """
        1：まったく当てはまらない

        2：あまり当てはまらない

        3：どちらともいえない

        4：やや当てはまる

        5：とても当てはまる
        """
    )

    questions = [
        "私はつらい時があった後でも、素早く立ち直れる。",
        "私はストレスの多い出来事を乗り越えるのに苦労する。",
        "ストレスが多い出来事から立ち直るのに長くはかからない。",
        "なにかしら不遇な出来事が起きた時に立ち直るのは難しい。",
        "ささいな問題があっても、たいていやり過ごせる。",
        "人生における遅れを取り戻すのに時間がかかる。"
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

        total_questions = len(questions) * 2

        progress = (
            idx + 1
        ) / total_questions

        st.write(
            f"全体進捗：{int(progress * 100)}%"
        )

        st.progress(progress)

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
        st.session_state.stress_index = 0

        st.session_state.start_time = None
       
        st.session_state.page = "stress"

        st.rerun()

# ----------------------
# ストレス条件
# ----------------------
elif st.session_state.page == "stress":

    st_autorefresh(interval=200, key="stress_refresh")

    TIME_LIMIT = 5

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

    TIME_LIMIT = 5

    if st.session_state.start_time is None:
        st.session_state.start_time = time.time()

    elapsed = time.time() - st.session_state.start_time

    remain = max(
        0,
        round(TIME_LIMIT - elapsed, 1)
    )

    if idx < len(questions):

        q = questions[idx]

        st.title("ストレス条件")

        st.write(f"問題 {idx+1}/{len(questions)}")

        total_questions = len(questions) * 2

        progress = (
            len(questions) + idx + 1
        ) / total_questions

        st.write(
            f"全体進捗：{int(progress * 100)}%"
        )

        st.progress(progress)

        if remain > 3:
            st.success(f"残り時間：{remain:.1f}秒")

        elif remain > 1:
            st.warning(f"残り時間：{remain:.1f}秒")

        else:
            st.error(f"残り時間：{remain:.1f}秒")

        st.write(q["text"])

        choice = st.radio(
            "選択してください",
            ["A", "B"],
            index=None,
            key=f"stress_{idx}"
        )
        
        # ----------------------
        # タイムオーバー
        # ----------------------

        if remain <= 0:

            st.session_state.stress_answers.append(
                {
                    "question_id": q["id"],
                    "choice": "NoAnswer",
                    "reaction_time": TIME_LIMIT
                }
            )

            st.session_state.start_time = None
            st.session_state.stress_index += 1

            st.rerun()

        # ----------------------
        # 回答処理
        # ----------------------

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

        if st.button("事後レジリエンス測定へ"):

            st.session_state.page = "post_brs"

            st.rerun()
# ----------------------
# 事後BRS
# ----------------------
elif st.session_state.page == "post_brs":

    st.title("レジリエンス測定（事後）")

    st.write("タスク終了後の状態について回答してください。")
    
    st.info(
    """
        1：まったく当てはまらない

        2：あまり当てはまらない

        3：どちらともいえない

        4：やや当てはまる

        5：とても当てはまる
        """
    )

    questions = [
        "私はつらい時があった後でも、素早く立ち直れる。",
        "私はストレスの多い出来事を乗り越えるのに苦労する。",
        "ストレスが多い出来事から立ち直るのに長くはかからない。",
        "なにかしら不遇な出来事が起きた時に立ち直るのは難しい。",
        "ささいな問題があっても、たいていやり過ごせる。",
        "人生における遅れを取り戻すのに時間がかかる。"
    ]

    options = [1, 2, 3, 4, 5]

    answers = []

    for i, q in enumerate(questions):

        answer = st.radio(
            q,
            options,
            index=None,
            key=f"post_brs_{i}"
        )

        answers.append(answer)

    if st.button("結果を見る"):

        if None in answers:

            st.error("すべての質問に回答してください。")

        else:

            scored = answers.copy()

            scored[1] = 6 - scored[1]
            scored[3] = 6 - scored[3]
            scored[5] = 6 - scored[5]

            post_brs_score = round(
                sum(scored) / 6,
                2
            )

            st.session_state.post_brs_score = post_brs_score

            st.session_state.page = "result"

            st.rerun()
# ----------------------
# 結果画面
# ----------------------
elif st.session_state.page == "result":

    st.title("意思決定分析結果")

    st.info(
        f"参加者ID：{st.session_state.participant_id}"
    )

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
    brs_delta = round(
    st.session_state.post_brs_score
    - st.session_state.brs_score,
    2
    )

    if st.session_state.post_brs_score < 3.0:

        brs_comment = (
            "少しお疲れ気味です。休息や気分転換を意識してみましょう。"
        )

    elif st.session_state.post_brs_score < 4.3:

        brs_comment = (
            "平均的な回復力を持っています。"
        )

    else:

        brs_comment = (
            "非常に高いレジリエンスを持っています。"
        )

    type_description = {

    "慎重安定型":
    "ストレス環境でも判断基準が安定しており、慎重な選択を維持する傾向があります。リスクを避けながらも一貫した意思決定ができるタイプです。",

    "中立安定型":
    "ストレス環境でも判断基準がほとんど変化しない安定したタイプです。状況に左右されにくく、バランスの取れた意思決定を行う傾向があります。",

    "挑戦安定型":
    "ストレス環境でも積極的な意思決定を維持するタイプです。プレッシャー下でも挑戦的な選択を継続しやすい傾向があります。",

    "慎重適応型":
    "状況の変化に応じて判断を調整しながらも、全体としては慎重な選択を行う傾向があります。柔軟性と安全志向を併せ持つタイプです。",

    "標準型":
    "判断の安定性とリスク傾向のバランスが取れた平均的なタイプです。ストレス環境でも大きく偏ることなく意思決定を行う傾向があります。",

    "挑戦適応型":
    "状況に応じて柔軟に判断しながら、必要に応じてリスクを取る方向へ適応する傾向があります。変化への対応力を持つタイプです。",

    "慎重変動型":
    "ストレス環境によって判断が変化しやすく、回避的な選択が増える傾向があります。プレッシャー下では安全性を重視しやすいタイプです。",

    "中立変動型":
    "ストレス環境によって判断基準が変化しやすいタイプです。状況による影響を受けやすく、選択傾向が一定しない場合があります。",

    "挑戦変動型":
    "ストレス環境でリスク選択が大きく増加するタイプです。プレッシャー下で積極性が高まりやすく、挑戦的な意思決定を行う傾向があります。"
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
    
    noanswer_count = sum(
        1
        for a in st.session_state.stress_answers
        if a["choice"] == "NoAnswer"
    )

    # ----------------------
    # 結果表示
    # ----------------------
    if "saved" not in st.session_state:

        save_result()

        st.session_state.saved = True

    st.subheader(f"あなたのタイプ：{result_type}")

    st.write(type_description[result_type])

    st.caption(
        f"判定根拠：判断安定性「{stability_level}」 × リスク傾向「{risk_type}」"
    )

    st.success(
        f"あなたはストレス環境で『{risk_type}』傾向を示し、"
        f"判断安定性は『{stability_level}』と判定されました。"
    )

    st.info(
        "ストレス環境での意思決定特性は状況によって変化するため、"
        "今回の結果は現在の傾向を示す参考情報としてご利用ください。"
    )

    st.info(
        "タイプ判定は、判断安定性とリスク傾向の組み合わせによって算出されています。"
    )

    st.divider()

    st.write(f"判断安定性：{stability}%")
    if stability >= 80:

        st.success(
            "ストレス環境でも判断基準が安定している傾向があります。"
        )

    elif stability >= 50:

        st.info(
            "ストレス環境によって一部の判断が変化した可能性があります。"
        )

    else:

        st.warning(
            "ストレス環境による判断変化が比較的大きくみられました。"
        )
    st.caption(
        "80%以上：高　/　50〜79%：中　/　50%未満：低"
    )
    st.write(f"通常条件リスク率：{normal_risk}%")
    st.write(f"ストレス条件リスク率：{stress_risk}%")
    st.write(f"ΔRisk：{delta_risk}%")
    if delta_risk <= -20:

        st.warning(
            "ストレス環境でリスク回避的な判断が増加しました。"
        )

    elif delta_risk >= 20:

        st.success(
            "ストレス環境で挑戦的な判断が増加しました。"
        )

    else:

        st.info(
            "ストレス環境によるリスク傾向の大きな変化はみられませんでした。"
        )

    st.caption(
        "-20%以下：回避化　/　-20%〜20%：中立　/　20%以上：挑戦化"
    )

    st.write(
    f"事前BRS：{st.session_state.brs_score}"
    )
    
    st.write(
    f"レジリエンス評価：{brs_comment}"
    )
     
    st.write(
        f"事後BRS：{st.session_state.post_brs_score}"
    )

    if st.session_state.post_brs_score < 3.0:

        st.warning(
            "少しお疲れ気味です。ストレスへの回復に時間がかかる傾向がみられます。"
        )

    elif st.session_state.post_brs_score < 4.3:

        st.info(
            "平均的な回復力を持っています。一般的なレベルのレジリエンスがあると考えられます。"
        )

    else:

        st.success(
            "非常に高いレジリエンスを持っています。ストレスからの回復力が高い傾向にあります。"
        )

    st.caption(
        "BRS-Jでは合計点÷6で平均スコアを算出します。"
    )

    st.caption(
        "3.0未満：低め　/　3.0〜4.3：平均的　/　4.3以上：高め"
    )

    st.write(
        f"ΔBRS：{brs_delta}"
    )

    if brs_delta > 0.3:

        st.success(
            "利用後にレジリエンス認識が向上しました。"
        )

    elif brs_delta < -0.3:

        st.warning(
            "利用後にレジリエンス認識が低下しました。"
        )

    else:

        st.info(
            "利用前後で大きな変化はみられませんでした。"
        )

    st.write(f"通常条件平均反応時間：{normal_rt}秒")
    st.write(f"ストレス条件平均反応時間：{stress_rt}秒")

    st.subheader("リスク選択率比較")

    risk_df = pd.DataFrame(
        {
            "条件": [
                "通常条件",
                "ストレス条件"
            ],
            "リスク率": [
                normal_risk,
                stress_risk
            ]
        }
    )

    fig = px.bar(
        risk_df,
        x="条件",
        y="リスク率",
        text="リスク率",
        category_orders={
            "条件": [
                "通常条件",
                "ストレス条件"
            ]
        },
        title="通常条件とストレス条件のリスク選択率比較"
    )

    fig.update_traces(
        texttemplate="%{text:.0f}%",
        textposition="outside"
    )

    fig.update_layout(
        yaxis_title="リスク選択率（%）",
        xaxis_title="",
        showlegend=False
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

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

    st.divider()

    st.subheader("アンケートのお願い")

    st.info(
        f"""
    参加者ID：{st.session_state.participant_id}

    アンケート回答時にこの参加者IDを入力してください。
    """
    )

    st.write(
        "本システム改善のため、1～2分程度のアンケートへのご協力をお願いいたします。"
    )

    st.link_button(
        "アンケートを開く",
        "https://docs.google.com/forms/d/e/1FAIpQLScfm696xD7aC6sulynGL89QjnaxyHZ9EqthhA4HV0UqMqGV5Q/viewform?usp=publish-editor"
    )

    st.divider()

    if st.button("最初に戻る"):
        if "saved" in st.session_state:
            del st.session_state["saved"]

        st.session_state.page = "start"

        st.session_state.normal_index = 0
        st.session_state.stress_index = 0

        st.session_state.normal_answers = []
        st.session_state.stress_answers = []

        st.session_state.start_time = None

         # 新しい参加者IDを発行
        st.session_state.participant_id = (
            generate_participant_id()
        )


        st.rerun()
