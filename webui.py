import shutil

import gradio as gr


def process_file(fileobj):
    path = "F:\temp"
    shutil.copyfile(fileobj.name, path)
    return do_something_to_file(path)


demo = gr.Interface(
    fn=process_file,
    inputs=[
        "file",
    ],
    outputs="file",
)

demo.launch()
