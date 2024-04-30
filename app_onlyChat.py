import streamlit as st
from openai import OpenAI
import os
from datas import dataset


def main():
    st.title("ChatGPT Basic")
    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"], base_url=None)
    # st.write(client.models.list())

    if "openai_model" not in st.session_state:
        st.session_state["openai_model"] = "gpt-3.5-turbo"
    
    if "messages" not in st.session_state:
        st.session_state.messages = []
        st.write("1", st.session_state.messages)
    
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            st.write("2", st.session_state.messages)
    
    

    # Handling user input through Streamlit's chat input box
    if prompt := st.chat_input("What is up?"):
        # system role
        if st.session_state.messages["role"] != "system":
            st.session_state.messages.append({"role": "system", "content": """I want you to act as a support agent. Your name is "My Super Assistant". You will provide me with answers from the given info. If the answer is not included, say exactly "Ooops! I don't know that." and stop after that. Refuse to answer any question not about the info. Never break character."""})
            st.write("3", st.session_state.messages)
    
        # st.session_state.messages.append({"role": "user", "content": dataset})
        # Appending the user's message to the session state
        st.session_state.messages.append({"role": "user", "content": prompt})

        # Displaying the user's message in the chat interface
        with st.chat_message("user"):
            st.markdown(prompt)
        
        
        # Preparing to display the assistant's response
        with st.chat_message("assistant"):
            message_placeholder = st.empty()  # Placeholder for assistant's response
            full_response = ""  # Initializing a variable to store the full response

            responses = client.chat.completions.create(
                model=st.session_state["openai_model"],
                messages=[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages],  # Passing the conversation history
                temperature=0,
                max_tokens=200,
                stream=True,  # Enabling real-time streaming of the response
                )
            for response in responses:
                full_response += (response.choices[0].delta.content or "")
                message_placeholder.markdown(full_response + " ▌")  # Displaying the response as it's being 'typed'
                # st.write(response.choices[0].delta.content)
            # Updating the placeholder with the final response once fully received
            message_placeholder.markdown(full_response)

        # Appending the assistant's response to the session's message list
        st.session_state.messages.append({"role": "assistant", "content": full_response})

        st.subheader("Session State")
        st.write(st.session_state.messages)
        # st.subheader("Dataset")
        # st.write(dataset)


if __name__ == '__main__':
    main()
    