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


def zip_files(mo, text, files, times, spl):
    in_put = os.path.split(files[0].name)

    if files == None or text == "":
        with open("error.txt", "w") as f:
            f.write("please write command here. And upload music file to next block. \n")
        return "error.txt", "error.txt",  "error.txt","please write command here. And upload music file to next block. \n" + text
    else:
        if spl:
            separate_to_file(files[0].name, in_put[0])
            aio("m2s", in_put[0] + f"/{in_put[1].split('.')[0]}/vocals.wav", in_put[0] + "/unf1.png")
            run_pipeline(pipe, in_put[0] + "/unf1.png", in_put[0] + "/unf2.png", text, times)
            aio("s2m", in_put[0] + "/unf2.png", in_put[0] + "/finish.mp3")
            sound1 = AudioSegment.from_mp3(in_put[0] + f"/{in_put[1].split('.')[0]}/vocals.wav")
            sound2 = AudioSegment.from_mp3(in_put[0] + "/finish.mp3")
            output = sound1.overlay(sound2)
            output.export("output.wav", format="wav")
            return (
                in_put[0] + "/finish.mp3",
                f"/{in_put[1].split('.')[0]}/vocals.wav",
                "output.wav",
                "SUCCESSFUL!!!",
            )
        else:
            aio("m2s", files[0].name, in_put[0] + "/unf1.png")
            run_pipeline(pipe, in_put[0] + "/unf1.png", in_put[0] + "/unf2.png", text, times)
            aio("s2m", in_put[0] + "/unf2.png", in_put[0] + "/finish.mp3")
            sound1 = AudioSegment.from_mp3(files[0].name)
            sound2 = AudioSegment.from_mp3(in_put[0] + "/finish.mp3")
            output = sound1.overlay(sound2)
            output.export("output.wav", format="wav")
            return in_put[0] + "/finish.mp3", files[0].name, "output.wav", "SUCCESSFUL!!!" 


demo = gr.Interface(
    zip_files,
    inputs=[
        gr.Dropdown(mods, label="models", info="Which models do you want to use?"),
        gr.Textbox(lines=2, placeholder="please write command here. And upload music file to next block."),
        gr.File(file_count="multiple", file_types=["audio"]),
        gr.Slider(2, 50, value=20, label="times", info="How many times do you want to run?", step = 1),
        gr.Checkbox(label="spleeter", info="Do you need spleeter?"),
        
    ],
    outputs=["file", "file", "file", "text"],
)

if __name__ == "__main__":
    demo.launch(share=True)
