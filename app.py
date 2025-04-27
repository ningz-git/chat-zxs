import streamlit as st
import os
import sys
from openai import OpenAI


def main():
    # 设置页面标题
    st.title("chat assistant")
    client = OpenAI(
        base_url='https://api-inference.modelscope.cn/v1/',
        api_key='fcae64d1-40d5-4f83-bb02-b628befc7ebf', # ModelScope Token
    )

    def generate_response(prompt):
        # 创建流式完成
        stream = client.chat.completions.create(
            model="Qwen/Qwen2.5-VL-72B-Instruct",
            messages=[
                {"role": "user", "content": prompt}
            ],
            stream=True,
        )
        
        # 使用 Streamlit 的流式输出功能
        response_container = st.empty()
        full_response = ""
        
        # 迭代流式响应
        for chunk in stream:
            if chunk.choices and len(chunk.choices) > 0:
                content = chunk.choices[0].delta.content
                if content is not None:
                    full_response += content
                    response_container.markdown(full_response)
        
        return full_response

    if "messages" not in st.session_state:
        st.session_state.messages = []
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    prompt = st.chat_input("请输入您的问题")
    if prompt:
        with st.chat_message("user"):
            st.markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        with st.chat_message("assistant"):
            response = generate_response(prompt)
        st.session_state.messages.append({"role": "assistant", "content": response})

if __name__ == "__main__":
    main()