import asyncio
import json
import os
from pathlib import Path

import gradio as gr

from config.config import DEFAULT_PROMPT, LLM_MODELS, TOP_N_FREE_MODELS
from src.llm.llm_handler import get_top_n_free_models
from src.processing.file_handler import process_directory, save_results_to_csv


# 創建批次處理的Gradio UI介面
def create_batch_processing_tab():
    top_n_models = get_top_n_free_models()
    default_model = (
        top_n_models[0] if top_n_models else LLM_MODELS[0]["name"] if LLM_MODELS else ""
    )

    with gr.Column():
        directory_input = gr.Textbox(label="Directory Path")
        prompt_input = gr.Textbox(
            label="Evaluation Criteria Prompt", value=DEFAULT_PROMPT, lines=10, scale=1
        )
        model_dropdown = gr.Dropdown(
            [model["name"] for model in LLM_MODELS],
            label="Select LLM Model",
            value=default_model,
        )
        score_output = gr.Dataframe(headers=["File", "Score", "Comment"])
        process_button = gr.Button("Process Directory")

        process_button.click(
            process_batch,
            inputs=[directory_input, prompt_input, model_dropdown],
            outputs=[score_output],
        )


# 非同步處理目錄中的所有文件並返回評分結果
async def process_batch(directory_path, prompt, model):
    if not os.path.isdir(directory_path):
        return [["", "", "Error: Invalid directory path."]]
    results = await process_directory(directory_path, prompt)
    save_results_to_csv(results)
    return [
        [
            Path(file_path).stem,
            final_score,
            (
                json.dumps(criteria, ensure_ascii=False, indent=2)
                if criteria
                else str(error)
            ),
        ]
        for file_path, final_score, criteria, error in results
    ]
