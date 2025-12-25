from pathlib import Path
import json
import requests
from typing import Dict, Any

def save_data_to_json(data, output_filename: str):
    """Save data to a JSON file.
    
    Args:
        data: The data structure to serialize to JSON.
        output_filename (str): The filename to save to (without path).
                             File will be saved to D:\SourceCode\python\logs\
    """
    output_file_path = f"D:\SourceCode\python\logs\{output_filename}"

    try:
        with open(output_file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        print(f"Dữ liệu đã được lưu thành công vào file: {output_file_path}")
    except Exception as e:
        print(f"Đã xảy ra lỗi khi ghi file JSON: {e}")

def save_to_txt(content, filename):
    """Save text content to a file.
    
    Args:
        content (str): The text content to save.
        filename (str): The output filename (with path).
    """
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Đã lưu file '{filename}' thành công!")
    except Exception as e:
        print(f"Có lỗi xảy ra: {e}")

def send_notification(
    code: str,
    name: str,
    type_: str,
    description: str,
    base_url: str = "http://api.com:1111",
    timeout: int = 10,
) -> Dict[str, Any]:
    """
    Gửi notification tới API.

    Trả về:
        response.json() nếu server trả JSON
        raise Exception nếu lỗi HTTP hoặc parse
    """

    url = f"{base_url}/notification/"

    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
    }

    payload = {
        "code": code,
        "name": name,
        "type": type_,
        "description": description,
    }

    response = requests.post(
        url,
        json=payload,
        headers=headers,
        timeout=timeout,
    )

    # Bắt lỗi HTTP (4xx, 5xx)
    response.raise_for_status()

    # Trả JSON (nếu server không trả JSON sẽ throw)
    return response.json()


