import asyncio
import csv
import json
import os
import re

from src.llm.llm_handler import get_llm_response
from src.processing.document_parser import parse_document


# 從LLM回應中提取分數(0-100)，若無效則返回None
def extract_score_from_response(response):
    """
    Extracts an integer score between 0 and 100 from the LLM response text.
    Returns None if no valid score is found.
    """
    if not response:
        return None
    matches = re.findall(r"\b\d{1,3}\b", response)
    for match in matches:
        try:
            score = int(match)
            if 0 <= score <= 100:
                return score
        except ValueError:
            continue
    return None


# 解析LLM的JSON回應，提取最終分數和評分標準
# 返回 (final_score, criteria_list)，若無效則返回 (None, [])
def extract_detailed_scores_from_response(response):
    """
    Parses the LLM response JSON and extracts:
    - final_score: int
    - criteria: list of dicts with 'name', 'score', 'reason'
    Returns (final_score, criteria_list)
    If response is not valid JSON, returns (None, []) to trigger error handling.
    """
    try:
        # Remove Markdown code block markers if present
        response = response.strip()
        response = re.sub(r"^```(?:json)?\s*", "", response)
        response = re.sub(r"\s*```$", "", response)

        data = json.loads(response)
        final_score = data.get("final_score")
        raw_criteria = data.get("criteria", [])
        # Map criteria list to dict for lookup
        crit_map = {c.get("name", ""): c for c in raw_criteria if isinstance(c, dict)}
        # Fixed criteria names
        fixed_names = ["Grammar", "Structure", "Creativity", "Relevance"]
        fixed_criteria = []
        for name in fixed_names:
            c = crit_map.get(name, {})
            fixed_criteria.append(
                {
                    "name": name,
                    "score": c.get("score", ""),
                    "reason": c.get("reason", ""),
                }
            )
        return final_score, fixed_criteria
    except Exception:
        # If not JSON, treat as error
        print(f"Invalid JSON response:\n{response}")
        return None, []


# 處理單個文件：提取文本並從LLM獲取詳細評分
async def process_file(file_path, prompt):
    """
    Processes a single file, extracts text, and gets detailed scores from the LLM.
    """
    try:
        text = parse_document(file_path)
        if not text:
            return file_path, None, [], "Error: Could not extract text from file."
        response = await get_llm_response(prompt, text)
        print(response)
        if response is None:
            return (
                file_path,
                None,
                [],
                "Error: LLM call failed or returned no response.",
            )
        final_score, criteria = extract_detailed_scores_from_response(response)
        if final_score is None:
            return (
                file_path,
                None,
                [],
                f"Error: Could not extract score from LLM response: {response}",
            )
        return file_path, final_score, criteria, None
    except Exception as e:
        return file_path, None, [], f"Exception during processing: {e}"


# 非同步處理目錄中的所有文件
async def process_directory(directory_path, prompt):
    """
    Processes all files in a directory asynchronously.
    """
    results = []
    tasks = []
    for filename in os.listdir(directory_path):
        file_path = os.path.join(directory_path, filename)
        if os.path.isfile(file_path):
            tasks.append(process_file(file_path, prompt))

    for task in asyncio.as_completed(tasks):
        file_path, final_score, criteria, error = await task
        results.append((file_path, final_score, criteria, error))
    return results


# 將評分結果保存為CSV文件（固定欄位格式）
def save_results_to_csv(results, output_path="scoring_results.csv"):
    """
    Saves the scoring results to a CSV file with fixed columns.
    """
    # Fixed criteria names
    criteria_names = ["Grammar", "Structure", "Creativity", "Relevance"]

    # Prepare fixed header
    header = ["name", "final_score", "error"]
    for cname in criteria_names:
        header.append(f"{cname}_score")
        header.append(f"{cname}_reason")

    with open(output_path, "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(header)

        for file_path, final_score, criteria, error in results:
            # Map criteria list to dict for easy lookup
            crit_map = {c.get("name", ""): c for c in criteria}
            row = [file_path, final_score, error]
            for cname in criteria_names:
                c = crit_map.get(cname, {})
                row.append(c.get("score", ""))
                row.append(c.get("reason", ""))
            writer.writerow(row)

    print(f"Scoring results saved to {output_path}")
