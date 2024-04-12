from pathlib import Path

import paths

import gradio as gr
from src.test.aio import aio
from src.test.diff import run_pipeline, load_model
from src.webui.webui_spleeter import separate_to_file
import os
from paths import NEXTCLOUD_MODEL_DIR
from pydub import AudioSegment
import numpy as np

from src.process.mark_beat import mark_beat

# pipe = load_model(NEXTCLOUD_MODEL_DIR / "fp16_lr1e-5-best")
mods = os.listdir(NEXTCLOUD_MODEL_DIR)
mods_need_beat_mark = ["第三代", "第三代 - 開放基底模型"]
pipe = ""
same = ""


def segment_to_sr_ndarray(segment: AudioSegment):
    return segment.frame_rate, np.array(segment.split_to_mono()[0].get_array_of_samples())


def zip_files(mo, text, file, steps, spl):
    global same, pipe
    if file == None or text == "" or str(type(steps)) != "<class 'int'>":
        with open("error.txt", "w") as f:
            f.write(
                "please write command here. And upload music file to next block. Don't input float type in times block."
            )

        return (
            "error.txt",
            "error.txt",
            "error.txt",
            "please write command here. And upload music file to next block.Don't input float type in times block",
        )

    in_put = Path(file)
    root_dir = in_put.parent
    filename = in_put.stem

    print(root_dir)

    print("in_put")
    if same != mo:
        pipe = load_model(NEXTCLOUD_MODEL_DIR / mo)
        same = mo
    # pipe = load_model(NEXTCLOUD_MODEL_DIR / mo)

    if spl:
        separate_to_file(in_put, root_dir)
        aio("m2s", root_dir / filename / "vocals.wav", root_dir / "unf1.png")
        if mo in mods_need_beat_mark:
            mark_beat(root_dir / "unf1.png", in_put, root_dir / "unf1.png")
        run_pipeline(pipe, root_dir / "unf1.png", root_dir / "unf2.png", text, steps)
        aio("s2m", root_dir / "unf2.png", root_dir / "finish.wav")
        sound1 = AudioSegment.from_wav(root_dir / filename / "vocals.wav")  # mp3 load wav
        sound2 = AudioSegment.from_file(root_dir / "finish.wav")
        output = sound1.overlay(sound2)
        return (
            segment_to_sr_ndarray(sound2),
            segment_to_sr_ndarray(sound1),
            segment_to_sr_ndarray(output),
            "SUCCESSFUL!!!",
        )

    else:
        print("aio")
        aio("m2s", in_put, root_dir / "unf1.png")
        if mo in mods_need_beat_mark:
            mark_beat(root_dir / "unf1.png", in_put, root_dir / "unf1.png")
        print("run pipeline")
        run_pipeline(pipe, root_dir / "unf1.png", root_dir / "unf2.png", text, steps)
        print("aio")
        aio("s2m", root_dir / "unf2.png", root_dir / "finish.wav")
        sound1 = AudioSegment.from_file(in_put)
        sound2 = AudioSegment.from_file(root_dir / "finish.wav")
        output = sound1.overlay(sound2)
        print("finish")
        return (
            segment_to_sr_ndarray(sound2),
            segment_to_sr_ndarray(sound1),
            segment_to_sr_ndarray(output),
            "SUCCESSFUL!!!",
        )


demo = gr.Interface(
    zip_files,
    inputs=[
        gr.Dropdown(mods, label="模型", value="第三代 - 開放基底模型", info="選模型，用於比較不同模型生成結果，建議第三代 - 開放基底模型"),
        gr.Textbox(lines=2, label="文字敘述", placeholder="輸入想要的文字敘述"),
        gr.Audio(type="filepath", label="上傳音檔或直接錄音", show_label=True),
        gr.Slider(2, 50, value=20, label="步數", step=1, info="選擇執行步數，一般來說，少可以加快速度，多可以增加生成結果品質，但超過一定數值就不會再有更明顯的改善了"),
        gr.Checkbox(label="使用spleeter", info="如果上傳的音檔有伴奏，勾選使用spleeter"),
    ],
    outputs=[gr.Audio(label="AI生成伴奏"), gr.Audio(label="原人聲"), gr.Audio(label="合成結果"), gr.Textbox(label="訊息")],
)

if __name__ == "__main__":
    demo.queue().launch(share=True, inline=False, server_name="localhost")
