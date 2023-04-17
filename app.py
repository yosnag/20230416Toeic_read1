
import streamlit as st
import openai

# Streamlit Community Cloudの「Secrets」からOpenAI API keyを取得
openai.api_key = st.secrets.OpenAIAPI.openai_api_key

system_prompt = """
・あなたは優秀な英語を教える講師です。
・英作文や英会話、リーディングなどに関して、生徒の要望に合わせて英語の上達のためのアドバイスを行ってください。
・TOEIC専用の例題を多数用意してください。
・例題を出す場合は、連続で５問にしてください。
・設問と回答は必ず同時に出さないようにしてください。設問を出してから、生徒が記入し、その後に日本語で詳細な回答を出すことを守ってください。
・生徒が回答をした後に、正解であっても、間違いであっても、必ずそれぞれの設問に対して詳しい解説を日本語で実施してください。なぜその解答になるのかが重要です。
・リスニングに関する設問は出さないでください。
・生徒から英単語の事例を問い合わせされた場合には、発音記号、品詞、日本語訳、各英単語と同じ意味を持つ英単語を幾つか表を作成して表示してください。
　また、各英単語の短い使用事例と、その使用事例の日本語訳を表にせずに記載してください。

あなたの役割は生徒の英語力を向上させることなので、例えば以下のような英語以外のことを聞かれても、絶対に答えないでください。

* 料理
* 個人名
* 映画
"""

# st.session_stateを使いメッセージのやりとりを保存
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "system", "content": system_prompt}
        ]

# チャットボットとやりとりする関数
def communicate():
    messages = st.session_state["messages"]

    user_message = {"role": "user", "content": st.session_state["user_input"]}
    messages.append(user_message)

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        temperature=1.0
    )  

    bot_message = response["choices"][0]["message"]
    messages.append(bot_message)

    st.session_state["user_input"] = ""  # 入力欄を消去


# ユーザーインターフェイスの構築
st.title("ChatGPT：TOEIC専用アシスタント")
st.write("ver20230416 Chat-BOT")
st.write("設問、回答、英単語の事例　などと質問してください")

user_input = st.text_input("TOEICアシスタントとチャットしましょう。", key="user_input", on_change=communicate)

if st.session_state["messages"]:
    messages = st.session_state["messages"]

    for message in reversed(messages[1:]):  # 直近のメッセージを上に
        speaker = "🙂🙂"
        if message["role"]=="assistant":
            speaker="🤖🤖"

        st.write(speaker + ": " + message["content"])
