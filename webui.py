import gradio as gr
import os

def zip_files(files):
    '''
    with ZipFile("tmp2222.zip", "w") as zipObj:
        for idx, file in enumerate(files):
            zipObj.write(file.name, file.name.split("/")[-1])
    '''

    with open('writeSomething.txt', 'w') as f:
        f.write('hello\n')
    return "writeSomething.txt"

demo = gr.Interface(
    zip_files,
    gr.File(file_count="multiple", file_types=["text", ".json", ".csv"]),
    "file",
)

if __name__ == "__main__":
    demo.launch()