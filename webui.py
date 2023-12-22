import gradio as gr

def zip_files(files):
    '''
    with ZipFile("tmp2222.zip", "w") as zipObj:
        for idx, file in enumerate(files):
            zipObj.write(file.name, file.name.split("/")[-1])
    '''

    with open('writeSomething.txt', 'w') as f:
        a=files[0]
        a=str(a)
        f.write(a)
    return "writeSomething.txt"

demo = gr.Interface(
    zip_files,
    gr.File(file_count="multiple", file_types=["text", ".json", ".csv"]),
    "file",
)

if __name__ == "__main__":
    demo.launch()