async def generate_image_mock(file_path: str, prompt: str) -> str:
    print("Фото для генерации:", file_path)
    print("Промт:", prompt)

    return file_path