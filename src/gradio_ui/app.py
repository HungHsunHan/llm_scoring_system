import gradio as gr

from src.gradio_ui.tabs import batch_processing_tab, single_file_tab


def create_demo():
    with gr.Blocks(
        css="""
    .gr-button {
        background-color: #4CAF50;
        color: white;
        font-weight: bold;
    }
    .gr-textbox textarea {
        font-family: monospace;
        font-size: 14px;
    }
    """
    ) as demo:
        gr.Markdown(
            "# Scoring System\nWelcome! Upload your files and get detailed LLM-based evaluations. Use the tabs below to select single or batch processing."
        )
        with gr.Tab("Single File Scoring"):
            single_file_tab.create_single_file_tab()
        with gr.Tab("Batch Processing"):
            batch_processing_tab.create_batch_processing_tab()
    return demo


if __name__ == "__main__":
    demo = create_demo()
    demo.launch()
