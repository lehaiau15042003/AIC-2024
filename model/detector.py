import av
import torch
from transformers import LlavaNextVideoProcessor, LlavaNextVideoForConditionalGeneration
import numpy as np
from huggingface_hub import hf_hub_download

model_id = "llava-hf/LLaVA-NeXT-Video-7B-hf-DPO"

model = LlavaNextVideoForConditionalGeneration.from_pretrained(
    model_id,
    torch_dtype=torch.float16,
    low_cpu_mem_usage=True,
).to('cuda')

processor = LlavaNextVideoProcessor.from_pretrained(model_id) 

def read_video(container, indices):
    frames = []
    container.seek(0)
    start_index = indices[0]
    end_index = indices[-1]
    for i, frame in enumerate(container.decode(video=0)):
        if i > end_index:
            break
        if i >= start_index and i in indices:
            frames.append(frame)
    return np.stack([x.to_ndarray(format='rgb24') for x in frames])

conversation = [
    {
        "role": "user",
        "content": [
            {"type": "text", "text": "What is content of this video"},
            {"type": "video"},
        ],
    },
]

prompt = processor.apply_chat_template(conversation, add_generation_prompt=True)
video_path = "../webapp/static/upload/208442_small.mp4"
container = av.open(video_path)

total_frames = container.streams.video[0].frames
indices = np.arange(0, total_frames, total_frames / 8).astype(int)
clip = read_video(container, indices)

inputs_image = processor(clip, return_tensors="pt").to('cuda')

output = model.generate(**inputs_image, max_new_tokens=100, do_sample=False)
print(processor.decode(output[0][2:], skip_special_tokens=True))