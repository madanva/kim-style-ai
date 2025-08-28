
import os
import torch
import PIL.Image as Image
import numpy as np
import open_clip

MODEL_NAME = os.getenv("CLIP_MODEL", "ViT-L-14")
PRETRAINED = os.getenv("CLIP_PRETRAIN", "openai")

_device = "cuda" if torch.cuda.is_available() else "cpu"
_model, _, _preprocess = open_clip.create_model_and_transforms(MODEL_NAME, pretrained=PRETRAINED, device=_device)
_tokenizer = open_clip.get_tokenizer(MODEL_NAME)

def embed_image(img_path: str) -> list[float]:
    img = Image.open(img_path).convert("RGB")
    with torch.no_grad():
        image = _preprocess(img).unsqueeze(0).to(_device)
        feats = _model.encode_image(image)
        feats = feats / feats.norm(dim=-1, keepdim=True)
        return feats.squeeze(0).cpu().tolist()
