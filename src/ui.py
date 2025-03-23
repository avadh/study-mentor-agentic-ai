import gradio as gr
from agent import invoke_crew

def study_mentor_interface(user_id, topic):
    result = invoke_crew(user_id, topic)
    return result

# Define Gradio UI
with gr.Blocks() as demo:
    gr.Markdown("# 📚 Personalized Study Mentor")

    user_id = gr.Textbox(label="User ID", value="user123")
    topic = gr.Textbox(label="Enter Topic to Study")

    submit_btn = gr.Button("Get Study Plan")
    study_plan_output = gr.Textbox(label="Study Plan", interactive=False)

    submit_btn.click(fn=study_mentor_interface, inputs=[user_id, topic], outputs=study_plan_output)

# Run the Gradio app
if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7860)