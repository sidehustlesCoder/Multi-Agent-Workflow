import streamlit as st
import time
import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load Env
load_dotenv()

st.set_page_config(page_title="Multi-Agent Blog Factory", layout="wide")

st.title("🤖 Multi-Agent Blog Post Factory !")
st.markdown("Watch three AI agents collaborate to write a blog post for you.")

# Sidebar for Config
with st.sidebar:
    st.header("Configuration")
    api_key_input = st.text_input("Google API Key", value=os.getenv("GOOGLE_API_KEY", ""), type="password")
    topic = st.text_input("Blog Topic", "The Future of AI Agents")
    start_btn = st.button("Start Workflow")

# Agent Class (Adapted for Streamlit to stream output)
class Agent:
    def __init__(self, name, role, instructions, api_key, avatar):
        self.name = name
        self.role = role
        self.instructions = instructions
        self.avatar = avatar
        
        # Configure GenAI
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-2.5-flash')
        
    def init_chat(self):
        try:
            self.chat = self.model.start_chat()
            system_prompt = (
                f"You are {self.name}, a {self.role}.\n"
                f"Your instructions are: {self.instructions}\n"
                "Keep your responses professional but conversational."
            )
            self.chat.send_message(system_prompt)
            return True
        except Exception as e:
            st.error(f"Failed to initialize {self.name}: {e}")
            return False

    def message(self, content, sender_name):
        with st.chat_message(self.name, avatar=self.avatar):
            st.write(f"**{self.name} ({self.role})**")
            st.write(f"*Receiving message from {sender_name}...*")
            
            try:
                prompt = f"Message from {sender_name}: {content}"
                response = self.chat.send_message(prompt)
                st.markdown(response.text)
                return response.text
            except Exception as e:
                st.error(f"Error: {e}")
                return "Error generating response."

# Main Workflow
if start_btn:
    if not api_key_input:
        st.error("Please provide a Google API Key.")
    else:
        st.divider()
        
        # Initialize Agents
        with st.status("Initializing Agents...", expanded=True) as status:
            st.write(" waking up Editor...")
            editor = Agent("Editor", "Senior Editor", "Plan content and outlines.", api_key_input, "👨‍💼")
            if editor.init_chat():
                st.write("✅ Editor Ready")
            
            st.write("Waiting 5s for rate limits...")
            time.sleep(5)
            
            st.write(" waking up Writer...")
            writer = Agent("Writer", "Content Writer", "Write engaging posts.", api_key_input, "👩‍💻")
            if writer.init_chat():
                 st.write("✅ Writer Ready")
            
            st.write("Waiting 5s for rate limits...")
            time.sleep(5)

            st.write(" waking up Reviewer...")
            reviewer = Agent("Reviewer", "Critic", "Critique and improve content.", api_key_input, "🧐")
            if reviewer.init_chat():
                st.write("✅ Reviewer Ready")
                
            status.update(label="Agents Initialized!", state="complete", expanded=False)

        # 1. Editor -> Outline
        st.subheader("Step 1: Planning")
        outline = editor.message(f"Create an outline for: '{topic}'", "User")
        
        with st.spinner("Cooling down (10s)..."):
            time.sleep(10)

        # 2. Editor -> Writer
        st.subheader("Step 2: Drafting")
        st.caption("Editor is assigning the task to Writer...")
        draft = writer.message(f"Write the post based on this outline:\n{outline}", "Editor")

        with st.spinner("Cooling down (10s)..."):
            time.sleep(10)

        # 3. Reviewer -> Feedback
        st.subheader("Step 3: Review")
        feedback = reviewer.message(f"Review this draft:\n{draft}", "Writer")
        
        with st.spinner("Cooling down (10s)..."):
            time.sleep(10)

        # 4. Writer -> Final
        st.subheader("Step 4: Final Polish")
        final_post = writer.message(f"Fix the post based on this feedback:\n{feedback}", "Reviewer")
        
        st.success("Workflow Complete!")
