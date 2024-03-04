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

# pipe = load_model(NEXTCLOUD_MODEL_DIR / "fp16_lr1e-5-best")
mods = os.listdir(NEXTCLOUD_MODEL_DIR)
pipe = ""
same = ""


def segment_to_sr_ndarray(segment: AudioSegment):
    return segment.frame_rate, np.array(segment.split_to_mono()[0].get_array_of_samples())


def zip_files(mo, text, file, times, spl):
    #    in_put = os.path.split(in_put)
    global same, pipe
    if file == None or text == "" or str(type(times)) != "<class 'int'>":
        with open("error.txt", "w") as f:
            f.write(
                "please write command here. And upload music file to next block.Don't input float type in times block. \n"
            )
        return (
            "error.txt",
            "error.txt",
            "error.txt",
            "please write command here. And upload music file to next block.Don't input float type in times block \n",
        )
    else:
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
            print("spl finish")
            aio("m2s", root_dir / filename / "vocals.wav", root_dir / "unf1.png")
            print("aio")
            run_pipeline(pipe, root_dir / "unf1.png", root_dir / "unf2.png", text, times)
            print("pipe")
            aio("s2m", root_dir / "unf2.png", root_dir / "finish.wav")
            sound1 = AudioSegment.from_wav(root_dir / filename / "vocals.wav")  # mp3 load wav
            sound2 = AudioSegment.from_wav(root_dir / "finish.wav")
            output = sound1.overlay(sound2)
            return (
                segment_to_sr_ndarray(sound2),
                segment_to_sr_ndarray(sound1),
                segment_to_sr_ndarray(output),
                "SUCCESSFUL!!!",
            )

        else:
            aio("m2s", in_put, root_dir / "unf1.png")
            run_pipeline(pipe, root_dir / "unf1.png", root_dir / "unf2.png", text, times)
            aio("s2m", root_dir / "unf2.png", root_dir / "finish.wav")
            sound1 = AudioSegment.from_file(in_put)
            sound2 = AudioSegment.from_mp3(root_dir / "finish.wav")
            output = sound1.overlay(sound2)
            output.export(root_dir / "output.wav", format="wav")
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
        gr.Dropdown(mods, label="models", value="第三代 (無敘述比例 = 0.1)-61000", info="Which models do you want to use?"),
        gr.Textbox(lines=2, placeholder="先選模型，輸入音樂類型，上傳音檔或直接錄音，如果上船的音檔有伴奏，勾選spleeter，選擇執行步數，少可以快，多可以品質增加"),
        gr.Audio(type="filepath"),
        gr.Slider(2, 50, value=20, label="times", step=1),
        gr.Checkbox(label="spleeter",),
    ],
    outputs=["audio", "audio", "audio", "text"],
)

if __name__ == "__main__":
    demo.queue().launch(share=True, inline=False)
