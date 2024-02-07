import paths

import gradio as gr
from aio import run
from process.diff import diff
import os


def zip_files(text, files):
    in_put = os.path.split(files[0].name)

    if files == None or text == "":
        with open("error.txt", "w") as f:
            f.write("please write command here. And upload music file to next block. \n")
        return "writeSomething.txt", "please write command here. And upload music file to next block. \n" + text
    else:
        run("m2s", files[0].name, in_put[0] + "/unf1.png")
        diff(in_put[0] + "/unf2.png", in_put[0] + "/unf1.png", text)
        run("s2m", in_put[0] + "/unf2.png", in_put[0] + "/finish.mp3")
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
