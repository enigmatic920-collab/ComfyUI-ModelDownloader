import os
import urllib.request
from pathlib import Path

import folder_paths


ALLOWED_EXTENSIONS = (
    ".safetensors",
    ".ckpt",
    ".pt",
    ".pth",
    ".bin",
    ".gguf",
)


class DownloadModelByURL:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "url": ("STRING", {"default": "https://"}),
                "model_type": ([
                    "checkpoints",
                    "loras",
                    "vae",
                    "clip",
                    "clip_vision",
                    "controlnet",
                    "upscale_models",
                    "diffusion_models",
                    "text_encoders",
                ],),
                "filename": ("STRING", {"default": "model.safetensors"}),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("status",)
    FUNCTION = "download"
    CATEGORY = "utils/model_downloader"

    def download(self, url, model_type, filename):
        if not url.startswith("https://"):
            return ("Ошибка: разрешены только https-ссылки",)

        safe_name = os.path.basename(filename.strip())

        if not safe_name:
            return ("Ошибка: неверное имя файла",)

        if ".." in filename or "/" in filename or "\\" in filename:
            return ("Ошибка: имя файла не должно содержать путь",)

        if not safe_name.lower().endswith(ALLOWED_EXTENSIONS):
            return ("Ошибка: разрешены только модели .safetensors, .ckpt, .pt, .pth, .bin, .gguf",)

        base_models_dir = Path(folder_paths.models_dir)
        target_dir = base_models_dir / model_type
        target_dir.mkdir(parents=True, exist_ok=True)

        target_path = target_dir / safe_name

        if target_path.exists():
            return (f"Файл уже существует: {target_path}",)

        try:
            urllib.request.urlretrieve(url, target_path)
            return (f"Готово. Модель загружена: {target_path}",)
        except Exception as e:
            return (f"Ошибка загрузки: {str(e)}",)


NODE_CLASS_MAPPINGS = {
    "DownloadModelByURL": DownloadModelByURL,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "DownloadModelByURL": "Download Model by URL",
}
