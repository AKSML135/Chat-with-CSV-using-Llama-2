import streamlit as st
from langchain.document_loaders import CSVLoader
from langchain.chains import ConversationalRetrievalChain
from store_index import *
from llm_loader import load_llm
import tempfile
from streamlit_chat import message

llm = load_llm()

st.title('Chat with CSV using Llama-2🦙🦜')
st.markdown("<h3 style='text-align: center; color: white;'>Built by <a href='https://github.com/AKSML135'>AMAN ❤️ </a></h3>", unsafe_allow_html=True)

#uploading file from UI
uploaded_file = st.sidebar.file_uploader(label='Upload your file here',type='csv')

#need to create tempfile path as CSV loader accept only path
if uploaded_file:
    with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
        tmp_file.write(uploaded_file.getvalue())
        tmp_file_path = tmp_file.name

    #using CSV loader to load the csv file , providing encoding and delimeter info
    load_csv = CSVLoader(file_path=tmp_file_path, encoding= 'UTF-8', csv_args={'delimiter':','})
    data = load_csv.load()

    #calling storeindex to create index on FAISS CPU
    db = store_index(data=data)

    #calling retrieval chain
    chain = ConversationalRetrievalChain.from_llm(llm=llm, retriever=db.as_retriever())

    def conversational_chat(query):
        result = chain({"question": query, "chat_history": st.session_state['history']})
        st.session_state['history'].append((query, result["answer"]))
        return result["answer"]
    
    if 'history' not in st.session_state:
        st.session_state['history'] = []

    if 'generated' not in st.session_state:
        st.session_state['generated'] = ["Hello ! Ask me anything about " + uploaded_file.name + " 🤗"]

    if 'past' not in st.session_state:
        st.session_state['past'] = ["Hey ! 👋"]

    #container for the chat history
    response_container = st.container()
    #container for the user's text input
    container = st.container()

    with container:
        with st.form(key='my_form', clear_on_submit=True):
            
            user_input = st.text_input("Query:", placeholder="Talk to your csv data here (:", key='input')
            submit_button = st.form_submit_button(label='Send')
            
        if submit_button and user_input:
            output = conversational_chat(user_input)
            
            st.session_state['past'].append(user_input)
            st.session_state['generated'].append(output)

    if st.session_state['generated']:
        with response_container:
            for i in range(len(st.session_state['generated'])):
                message(st.session_state["past"][i], is_user=True, key=str(i) + '_user', avatar_style="big-smile")
                message(st.session_state["generated"][i], key=str(i), avatar_style="thumbs")


