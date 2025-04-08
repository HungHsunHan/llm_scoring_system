import asyncio

import gradio as gr

from config.config import DEFAULT_PROMPT, LLM_MODELS, TOP_N_FREE_MODELS
from src.llm.llm_handler import get_top_n_free_models
from src.processing.file_handler import process_file, save_results_to_csv


# 創建單一文件處理的Gradio UI介面
def create_single_file_tab():
    top_n_models = get_top_n_free_models()
    default_model = (
        top_n_models[0] if top_n_models else LLM_MODELS[0]["name"] if LLM_MODELS else ""
    )

    with gr.Column():
        file_input = gr.File(label="Upload File")
        prompt_input = gr.Textbox(
            label="Evaluation Criteria Prompt", value=DEFAULT_PROMPT
        )
        model_dropdown = gr.Dropdown(
            [model["name"] for model in LLM_MODELS],
            label="Select LLM Model",
            value=default_model,
        )
        score_output = gr.Textbox(label="Score")
        criteria_str = gr.Textbox(label="Criteria")
        download_output = gr.File(label="Download CSV")
        process_button = gr.Button("Process File")

        process_button.click(
            process_single_file,
            inputs=[file_input, prompt_input, model_dropdown],
            outputs=[score_output, criteria_str, download_output],
        )


# 處理單個文件並返回評分結果和標準
async def process_single_file(file_obj, prompt, model):
    import datetime
    import json
    import os

    if file_obj is None:
        return None, "Error: No file uploaded.", None

    file_path = file_obj.name
    file_path, score, criteria, error = await process_file(file_path, prompt)

    # Convert criteria list to pretty JSON string
    try:
        criteria_str = json.dumps(criteria, indent=2, ensure_ascii=False)
    except Exception:
        criteria_str = str(criteria)

    results = [(file_path, score, criteria, error)]

    # Generate timestamped filename
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M")
    csv_filename = f"results_{timestamp}.csv"
    csv_path = os.path.join("data", csv_filename)

    # Ensure data directory exists
    os.makedirs("data", exist_ok=True)

    # Save CSV
    save_results_to_csv(results, csv_path)

    return score, criteria_str, csv_path
