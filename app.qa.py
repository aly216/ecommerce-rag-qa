import streamlit as st
from rag import RAGService
import config_data as config


st.title("问答服务")
st.divider()   # 分隔线



if'messages' not in st.session_state:
    st.session_state['messages']=[{'role':'user','content':'你好,我是问答服务'}]

if 'rag' not in st.session_state:
    st.session_state['rag']=RAGService()

for message in st.session_state['messages']:
    st.chat_message(message['role']).write(message['content'])


prompt=st.chat_input()


if prompt:
    st.chat_message('user').write(prompt)
    st.session_state['messages'].append({'role':'user','content':prompt})

    cache_list=[]
    with st.spinner():
        res=st.session_state['rag'].chain.stream({'input':prompt},config.session_config)

        def capture(generator,cache_list):
            for chunk in generator:
                cache_list.append(chunk)
                yield chunk


        st.chat_message('assistant').write_stream(capture(res,cache_list))
        st.session_state['messages'].append({'role':'assistant','content':''.join(cache_list)})     
