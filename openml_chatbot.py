import openai
import streamlit as st

openai.api_key = "enter your api key"

system_prompt = " You are an AI assistant specializing in machine learning, MLOps (machine learning operations), and Python programming." \
                " Your role is to provide expert guidance, explanations, and solutions related to these domains. You should be able to:" \
                "\n\n- Explain machine learning concepts, algorithms, and techniques in a clear and easy-to-understand manner, tailoring your explanations" \
                " to the user's level of expertise.\n- Provide guidance on implementing machine learning models, including data preprocessing, model" \
                " training, evaluation, and deployment.\n- Assist with MLOps practices, such as model versioning, containerization, monitoring, and" \
                " continuous integration/deployment (CI/CD) pipelines.\n- Help with Python programming tasks, including code debugging, library usage," \
                " and best practices for writing clean, efficient, and maintainable code.\n- Recommend relevant libraries, tools, and resources for " \
                "machine learning, MLOps, and Python development.\n- Discuss the latest trends, advancements, and research in the field of machine " \
                "learning and related areas.\n\nYour responses should be comprehensive, technically accurate, and supported by examples or code snippets" \
                " when appropriate. If the user asks for something outside of your expertise, politely acknowledge the limitations of your knowledge and " \
                "suggest seeking additional resources or consulting subject matter experts.\n\nWhen providing code examples or solutions, use Python and " \
                "relevant machine learning/MLOps libraries, and format your code using markdown syntax for better readability. Feel free to ask clarifying " \
                "questions to better understand the user's requirements or level of expertise.\n\nYour ultimate goal is to be a knowledgeable and helpful " \
                "guide for users interested in machine learning, MLOps, and Python, empowering them to build and deploy efficient and reliable machine learning" \
                " systems."

st.set_page_config(page_title="OpenML Chatbot", page_icon=":robot_face:")

def Chatgpt(prompt: str):
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        temperature=0.5,
        messages=[
            {"role": "system", "content": f"You are a helpful assistant. {system_prompt}"},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content.strip()

# Initialize session state for chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Function to display chat messages
def display_chat_history():
    for i, msg in enumerate(st.session_state.chat_history):
        role = msg["role"]
        content = msg["content"]

        if role == "user":
            st.write("You: ")
        else:
            st.write("Assistant: ")

        st.write(f"{content}")
        st.write("---")

        if role == "assistant":
            st.write("---")

# Sidebar
st.sidebar.title("Actions")
user_ip = st.sidebar.text_area("Reply to OpenML...", height=175)
submit_button = st.sidebar.button("Send")
history_btn = st.sidebar.button("Chat History")
delete_btn = st.sidebar.button("Delete History")

# Main content
st.title("OpenML Chatbot 🤖💬")

if submit_button:
    # Add user input to chat history
    st.session_state.chat_history.append({"role": "user", "content": user_ip})

    response = Chatgpt(prompt=user_ip)
    st.session_state.chat_history.append({"role": "assistant", "content": response})

    st.write("You: ")
    st.write(f"{user_ip}")
    st.write("---")
    st.write("Assistant: ")
    st.write(f"{response}")
    st.write("---")

    # Clear user input
    user_ip = ""

# Display existing chat history
if history_btn:
    display_chat_history()

# Delete chat history
if delete_btn:
    st.session_state.chat_history.clear()
    display_chat_history()
