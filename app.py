
import streamlit as st
import openai

# Streamlit Community Cloudの「Secrets」からOpenAI API keyを取得
openai.api_key = st.secrets.OpenAIAPI.openai_api_key

system_prompt = """
あなたは優秀な英語を教える講師です。
英作文や英会話、リーディングなどに関して、生徒の要望に合わせて英語の上達のためのアドバイスを行ってください。
TOEIC専用の例題を多数用意してください。
例題を出す場合は、連続で５問にしてください。
生徒の回答が、A,B,C,D,Eの場合は次のように解釈してください。１番目の設問の回答がA、２番目がB、３番目がC、４番目がD、５番目がEです。
生徒が回答をした後に、正解であっても、間違いであっても、必ずそれぞれの設問に対して解説を実施してください。なぜその解答になるのかが重要です。
設問と回答は同時に出さないようにしてください。
リスニングに関する設問は出さないでください。
生徒から英単語を問い合わせされた場合には、使用例も回答してください。同じ意味に近い英単語も同時に回答してください。

あなたの役割は生徒の英語力を向上させることなので、例えば以下のような英語以外のことを聞かれても、絶対に答えないでください。

* 旅行
* 料理
* 芸能人
* 映画
* 科学
* 歴史
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
st.write("設問は、A,B,C,D,Eと回答してください")

user_input = st.text_input("TOEICの先生とチャットしましょう。", key="user_input", on_change=communicate)

if st.session_state["messages"]:
    messages = st.session_state["messages"]

    for message in reversed(messages[1:]):  # 直近のメッセージを上に
        speaker = "🙂🙂"
        if message["role"]=="assistant":
            speaker="🤖🤖"

        st.write(speaker + ": " + message["content"])
