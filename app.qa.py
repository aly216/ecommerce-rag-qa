import streamlit as st
from rag import RAGService
import config_data as config

# 浏览器标签页配置
st.set_page_config(
    page_title="服饰电商智能客服",
    layout="wide",
)

# 标题区
st.title("服饰电商智能客服")
st.caption("基于 RAG 的商品知识库问答，覆盖 **尺码推荐 / 洗涤养护 / 颜色搭配** 三类高频咨询")

st.divider()

# 会话状态初始化
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {
            "role": "assistant",
            "content": (
                "你好，我是**服饰电商智能客服** \n\n"
                "可以帮你解决：\n"
                "-  尺码推荐（按身高体重选码）\n"
                "-  洗涤养护（洗护技巧）\n"
                "-  颜色搭配（肤色 / 场合选色）"
            ),
        }
    ]

if "rag" not in st.session_state:
    st.session_state["rag"] = RAGService()

# 渲染历史消息
for message in st.session_state["messages"]:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# 输入
prompt = st.chat_input("输入你的尺码 / 洗护 / 颜色问题…")

if prompt:
    st.chat_message("user").write(prompt)
    st.session_state["messages"].append({"role": "user", "content": prompt})

    cache_list = []
    with st.spinner("正在检索知识库…"):
        res = st.session_state["rag"].chain.stream({"input": prompt}, config.session_config)

        def capture(generator, cache_list):
            for chunk in generator:
                cache_list.append(chunk)
                yield chunk

        with st.chat_message("assistant"):
            st.write_stream(capture(res, cache_list))

    st.session_state["messages"].append({"role": "assistant", "content": "".join(cache_list)})
