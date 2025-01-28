import os
from dotenv import load_dotenv
load_dotenv()

import streamlit as st
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

from src.tools import get_member_info, get_member_icp
from src.prompt import SYSTEM_PROMPT


# Page config
st.set_page_config(page_title="ICP Plan Chatbot", page_icon="🤖")

# Initialize session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

def initialize_agent():
    model = ChatOpenAI(model="gpt-4o-mini")

    prompt = ChatPromptTemplate.from_messages([
        ("system", SYSTEM_PROMPT),
        ("human", "{input}"),
        ("placeholder", "{agent_scratchpad}"),
    ])

    tools = [get_member_info, get_member_icp]
    agent = create_tool_calling_agent(model, tools, prompt)
    return AgentExecutor(agent=agent, tools=tools)


# Main UI elements
st.title("ICP Plan Assistant 🤖")
st.write("Ask me about ICP plans and member information!")


# Initialize the agent
@st.cache_resource
def get_agent():
    return initialize_agent()


agent_executor = get_agent()

# Chat input
if prompt := st.chat_input("What would you like to know about ICP plans?"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.write(prompt)

    # Show thinking message while processing
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        message_placeholder.text("🤔 Thinking...")

        try:
            # Get response from agent
            response = agent_executor.invoke({"input": prompt})
            response_content = response["output"]

            # Update thinking message with actual response
            message_placeholder.text(response_content)

            # Add assistant message to chat history
            st.session_state.messages.append({"role": "assistant", "content": response_content})

        except Exception as e:
            message_placeholder.text(f"Sorry, I encountered an error: {str(e)}")
            st.error(f"Error: {str(e)}")

# Display chat history
for message in st.session_state.messages[:-2]:  # Don't show the last 2 messages since they're already displayed
    with st.chat_message(message["role"]):
        st.write(message["content"])

# Add some helpful information in the sidebar
with st.sidebar:
    st.title("About")
    st.write("""
    This chatbot can help you:
    - Search for ICP plans
    - Get member information
    - Find suitable plans based on age and conditions
    """)

    # Add example queries
    st.subheader("Example Queries")
    example_queries = [
        "What ICP plans are available for seniors aged 80-90?",
        "Tell me about ICP plans for heart disease patients",
        "Can you find plans for elderly with chronic conditions?"
    ]

    for query in example_queries:
        if st.button(query):
            # Set the query in the chat input
            st.chat_input(query)