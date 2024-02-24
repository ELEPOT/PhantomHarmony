from pathlib import Path

import paths

import gradio as gr
from src.test.aio import aio
from src.test.diff import run_pipeline, load_model
from src.webui.webui_spleeter import separate_to_file
import os
from paths import NEXTCLOUD_MODEL_DIR
from pydub import AudioSegment

# pipe = load_model(NEXTCLOUD_MODEL_DIR / "fp16_lr1e-5-best")
mods = os.listdir(NEXTCLOUD_MODEL_DIR)
pipe = ""
same = ""


def zip_files(mo, text, files, times, spl):
    #    in_put = os.path.split(in_put)
    global same, pipe
    if files == None or text == "" or str(type(times)) != "<class 'int'>":
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
        in_put = Path(files[0].name)
        root_dir = in_put.parent.resolve()
        filename = in_put.stem

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
            output.export(root_dir / "output.wav", format="wav")
            return (
                root_dir / "finish.wav",
                root_dir / filename / "vocals.wav",
                root_dir / "output.wav",
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
            return root_dir / "finish.wav", in_put, root_dir / "output.wav", "SUCCESSFUL!!!"


demo = gr.Interface(
    zip_files,
    inputs=[
        gr.Dropdown(
            mods, label="models", value="fp16_lr1e-5_train_base-61000", info="Which models do you want to use?"
        ),
        gr.Textbox(lines=2, placeholder="please write command here. And upload music file to next block."),
        gr.File(file_count="multiple", file_types=["audio"]),
        gr.Slider(2, 50, value=20, label="times", info="How many times do you want to run?", step=1),
        gr.Checkbox(label="spleeter", info="Do you need spleeter?"),
    ],
    outputs=["audio", "audio", "audio", "text"],
)

if __name__ == "__main__":
    demo.queue().launch(share=True, inline=False)
