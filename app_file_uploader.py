import streamlit as st
from knowledge_base import KnowledgeBaseService
import time

# 标题
st.title("知识库更新服务")

# 上传文件
uploaded_file = st.file_uploader("上传文件", type=["txt"],accept_multiple_files=False)


if'service' not in st.session_state:
    st.session_state['service']=KnowledgeBaseService()



if uploaded_file is not None:
    file_name=uploaded_file.name
    file_type=uploaded_file.type
    file_size=uploaded_file.size/1024

    st.subheader(f'文件名：{file_name}')
    st.write(f'文件类型：{file_type}')
    st.write(f'文件大小：{file_size:.2f}kB')


    # 读取文件内容
    file_content = uploaded_file.getvalue().decode("utf-8")

    with st.spinner("上传中..."):
        time.sleep(1)
        result=st.session_state['service'].upload_by_str(file_content,file_name)    
        st.write(result)

