import os
import time
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure Gemini
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    # Fallback for demo purposes if env not set, though user should set it
    print("WARNING: GOOGLE_API_KEY not found in .env file.")
    api_key = input("Please enter your Google API Key: ")

genai.configure(api_key=api_key)

class Agent:
    """
    A simple Agent class that holds a persona and history.
    """
    def __init__(self, name: str, role: str, instructions: str):
        self.name = name
        self.role = role
        self.instructions = instructions
        # Updated to use the model available to the user's key
        self.model = genai.GenerativeModel('gemini-2.5-flash')
        self.chat = self.model.start_chat()
        
        # Prime the agent with its system instructions
        self._send_system_prompt()
        
    def _send_system_prompt(self):
        """
        Sets the behavior of the agent using a system prompt.
        """
        system_prompt = (
            f"You are {self.name}, a {self.role}.\n"
            f"Your instructions are: {self.instructions}\n"
            "Keep your responses professional but conversational. "
            "Do not break character."
        )
        try:
            self.chat.send_message(system_prompt)
            print(f"[{self.name}] initialized as {self.role}.")
        except Exception as e:
            print(f"Init failed for {self.name}, retrying in 20s...")
            time.sleep(20)
            try:
                self.chat.send_message(system_prompt)
                print(f"[{self.name}] initialized as {self.role}.")
            except Exception as final_e:
                print(f"Failed to initialize {self.name}: {final_e}")

    def message(self, content: str, sender_name: str) -> str:
        """
        Receive a message and generate a response.
        """
        print(f"\n--- {sender_name} -> {self.name} ---")
        print(f"Failed to load message content? No: {content[:60]}...")
        
        prompt = f"Message from {sender_name}: {content}"
        response = self.chat.send_message(prompt)
        
        print(f"\n[{self.name}]: {response.text}\n")
        return response.text

class Orchestrator:
    """
    Manages the workflow between agents.
    """
    def __init__(self):
        self.agents = {}

    def add_agent(self, agent: Agent):
        self.agents[agent.name] = agent

    def run_blog_post_workflow(self, topic: str):
        print(f"\n=== Starting Blog Post Workflow for topic: '{topic}' ===\n")

        # 1. Editor (Manager) creates the outline
        editor = self.agents["Editor"]
        writer = self.agents["Writer"]
        reviewer = self.agents["Reviewer"]

        print(">>> 1. Editor creates outline...")
        outline_request = f"We need a blog post about '{topic}'. Create a detailed outline for the writer."
        outline = editor.message(outline_request, "Boss")
        
        print("...waiting 15s for rate limit...")
        time.sleep(15)

        # 2. Editor assigns Writer
        print(">>> 2. Editor assigns Writer...")
        write_request = f"Here is the outline. Please write the full blog post.\n\nOutline: {outline}"
        draft_post = writer.message(write_request, "Editor")

        print("...waiting 15s for rate limit...")
        time.sleep(15)

        # 3. Reviewer critiques the draft
        print(">>> 3. Reviewer critiques the draft...")
        review_request = f"Please review this draft blog post and provide constructive feedback.\n\nDraft: {draft_post}"
        feedback = reviewer.message(review_request, "Writer")

        print("...waiting 15s for rate limit...")
        time.sleep(15)

        # 4. Writer revises
        print(">>> 4. Writer revises based on feedback...")
        revise_request = f"Here is the feedback from the reviewer. Please revise the post.\n\nFeedback: {feedback}"
        final_post = writer.message(revise_request, "Reviewer")

        print("\n=== Workflow Complete! ===\n")
        print("FINAL RESULT:\n")
        print(final_post)


def main():
    print("Initializing Editor...")
    editor = Agent(
        name="Editor", 
        role="Senior Content Editor", 
        instructions="You are responsible for planning content. You create strong outlines and give clear direction."
    )
    time.sleep(10)
    
    print("Initializing Writer...")
    writer = Agent(
        name="Writer", 
        role="Content Writer", 
        instructions="You write engaging, high-quality blog posts based on outlines. You accept feedback gracefully."
    )
    time.sleep(10)
    
    print("Initializing Reviewer...")
    reviewer = Agent(
        name="Reviewer", 
        role="Fact Checker & Critic", 
        instructions="You are critical. You look for shallow content, logical errors, and boring introductions. Be constructive."
    )
    time.sleep(10)

    # 2. Setup Orchestrator
    orchestrator = Orchestrator()
    orchestrator.add_agent(editor)
    orchestrator.add_agent(writer)
    orchestrator.add_agent(reviewer)

    # 3. Running the Demo
    topic = input("\nEnter a topic for the blog post (e.g., 'The Future of AI Agents'): ")
    if not topic:
        topic = "The Future of AI Agents"
    
    orchestrator.run_blog_post_workflow(topic)

if __name__ == "__main__":
    main()
