import gradio as gr
import requests

API_URL = "http://localhost:8080/study"  # FastAPI backend


# Function to handle study mentor interaction
def get_study_plan(user_id, topic):
    payload = {"user_id": user_id, "topic": topic}
    response = requests.post(API_URL, json=payload)
    return response.json().get("study_plan", "No study plan available.")


# Define Gradio UI
with gr.Blocks() as demo:
    gr.Markdown("# 📚 Personalized Study Mentor")

    user_id = gr.Textbox(label="User ID", value="user123")
    topic = gr.Textbox(label="Enter Topic to Study")

    submit_btn = gr.Button("Get Study Plan")
    study_plan_output = gr.Textbox(label="Study Plan", interactive=False)

    submit_btn.click(fn=get_study_plan, inputs=[user_id, topic], outputs=study_plan_output)

# Run the Gradio app
if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7860)
