import gradio as gr

from src.gradio_ui.tabs import batch_processing_tab, single_file_tab


def create_demo():
    with gr.Blocks() as demo:
        gr.Markdown("# Scoring System")
        with gr.Tab("Single File Scoring"):
            single_file_tab.create_single_file_tab()
        with gr.Tab("Batch Processing"):
            batch_processing_tab.create_batch_processing_tab()
    return demo


if __name__ == "__main__":
    demo = create_demo()
    demo.launch()
