import os
import requests

from config import HUGGINGFACE_API_TOKEN


API_URL = "https://router.huggingface.co/hf-inference/models/stabilityai/stable-diffusion-xl-base-1.0"


async def generate_image_huggingface(file_path: str, prompt: str) -> str:
    headers = {
        "Authorization": f"Bearer {HUGGINGFACE_API_TOKEN}",
        "Content-Type": "application/json",
    }

    payload = {
        "inputs": prompt
    }

    response = requests.post(
        API_URL,
        headers=headers,
        json=payload,
        timeout=120
    )

    if response.status_code != 200:
        raise Exception(
            f"Hugging Face error: {response.status_code} {response.text}"
        )

    os.makedirs("results", exist_ok=True)

    result_path = "results/generated_result.png"

    with open(result_path, "wb") as file:
        file.write(response.content)

    return result_path