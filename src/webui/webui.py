import paths

import gradio as gr
from src.test.aio import aio
from src.process.diff import run_pipeline, load_model
import os
from paths import NEXTCLOUD_MODEL_DIR


pipe = load_model(NEXTCLOUD_MODEL_DIR / "first-7500")


def zip_files(text, files):
    in_put = os.path.split(files[0].name)

    if files == None or text == "":
        with open("error.txt", "w") as f:
            f.write("please write command here. And upload music file to next block. \n")
        return "writeSomething.txt", "please write command here. And upload music file to next block. \n" + text
    else:
        aio("m2s", files[0].name, in_put[0] + "/unf1.png")
        run_pipeline(pipe, in_put[0] + "/unf1.png", in_put[0] + "/unf2.png", text)
        aio("s2m", in_put[0] + "/unf2.png", in_put[0] + "/finish.mp3")
        return in_put[0] + "/finish.mp3", "SUCCESSFUL!!!" + text


demo = gr.Interface(
    zip_files,
    inputs=[
        gr.Textbox(lines=2, placeholder="please write command here. And upload music file to next block."),
        gr.File(file_count="multiple", file_types=["audio"]),
    ],
    outputs=["file", "text"],
)

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0")
