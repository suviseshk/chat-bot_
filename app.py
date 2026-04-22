import streamlit as st
import os
import bs4
from langchain_community.document_loaders import WebBaseLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_community.vectorstores import FAISS
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate

# --- CONFIGURATION ---
# Replace with your actual Gemini API Key
os.environ["GOOGLE_API_KEY"] = "AIzaSyDdmr68gi0zywrlryBLgXQQRsSiwC0JXb0"

st.set_page_config(page_title="JACSICE Assistant", page_icon="🎓")
st.title("🎓 Jayaraj Annapackiam CSI College Bot")

# --- LIST THE COLLEGE PAGES TO SCRAPE ---
URLS_TO_SCRAPE = [
    "https://www.jacsicoe.in/",
    # Add other specific pages below, for example:
    # "https://www.jacsicoe.in/about-us",
    # "https://www.jacsicoe.in/cse-department",
    # "https://www.jacsicoe.in/admissions"
]

@st.cache_resource
def initialize_web_rag_pipeline():
    try:
        # 1. Scrape the websites directly
        st.info("Fetching latest data from the college website...")
        loader = WebBaseLoader(web_paths=URLS_TO_SCRAPE)
        docs = loader.load()

        # 2. Split the scraped website text into manageable chunks
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        chunks = text_splitter.split_documents(docs)

        # 3. Create Embeddings and Vector Store
        embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
        vector_store = FAISS.from_documents(chunks, embeddings)
        retriever = vector_store.as_retriever()

        # 4. Setup the Gemini LLM
        llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0.3)

        # 5. Create the Prompt Template
        system_prompt = (
            "You are a helpful and friendly assistant for Jayaraj Annapackiam CSI College of Engineering (JACSICE) in Nazareth. "
            "Use the following pieces of retrieved website context to answer the user's question. "
            "If you do not know the answer based on the context, politely say 'I don't have that information on the college website.'\n\n"
            "{context}"
        )
        prompt = ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            ("human", "{input}"),
        ])

        # 6. Build the chain
        question_answer_chain = create_stuff_documents_chain(llm, prompt)
        rag_chain = create_retrieval_chain(retriever, question_answer_chain)
        
        return rag_chain
    except Exception as e:
        st.error(f"Error scraping website: {e}")
        return None

# Initialize the backend
rag_chain = initialize_web_rag_pipeline()

# --- STREAMLIT CHAT UI ---
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Welcome to JACSICE! Ask me anything about our campus, courses, or admissions."}]

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

user_input = st.chat_input("E.g., 'What courses do you offer?'")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        if rag_chain is None:
             st.error("Website data not loaded.")
        else:
            with st.spinner("Searching the college website..."):
                response = rag_chain.invoke({"input": user_input})
                answer = response["answer"]
                
                st.markdown(answer)
                st.session_state.messages.append({"role": "assistant", "content": answer})