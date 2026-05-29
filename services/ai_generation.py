import os
import time
import base64
import requests

from config import YANDEX_API_KEY, YANDEX_FOLDER_ID


async def generate_image_huggingface(file_path: str, prompt: str) -> str:
    generate_url = "https://llm.api.cloud.yandex.net/foundationModels/v1/imageGenerationAsync"

    headers = {
        "Authorization": f"Api-Key {YANDEX_API_KEY}",
        "x-folder-id": YANDEX_FOLDER_ID,
        "Content-Type": "application/json",
    }

    payload = {
        "modelUri": f"art://{YANDEX_FOLDER_ID}/yandex-art/latest",
        "generationOptions": {
            "mimeType": "image/jpeg"
        },
        "messages": [
            {
                "text": prompt
            }
        ]
    }

    response = requests.post(generate_url, headers=headers, json=payload, timeout=60)

    if response.status_code != 200:
        raise Exception(f"YandexART error: {response.status_code} {response.text}")

    operation_id = response.json()["id"]
    operation_url = f"https://operation.api.cloud.yandex.net/operations/{operation_id}"

    for _ in range(30):
        result_response = requests.get(
            operation_url,
            headers={"Authorization": f"Api-Key {YANDEX_API_KEY}"},
            timeout=30
        )

        data = result_response.json()

        if data.get("done"):
            image_base64 = data["response"]["image"]
            image_bytes = base64.b64decode(image_base64)

            os.makedirs("results", exist_ok=True)
            result_path = "results/generated_result.jpg"

            with open(result_path, "wb") as file:
                file.write(image_bytes)

            return result_path

        time.sleep(3)

    raise Exception("YandexART generation timeout")