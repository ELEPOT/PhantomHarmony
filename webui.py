import gradio as gr


def zip_files(text, files):
    """
    with ZipFile("tmp2222.zip", "w") as zipObj:
        for idx, file in enumerate(files):
            zipObj.write(file.name, file.name.split("/")[-1])
    """

    with open("writeSomething.txt", "w") as f:
        a = files[0]
        a = str(a + "   " + text)
        f.write(a + "\n")
    return "writeSomething.txt"


demo = gr.Interface(
    zip_files,
    inputs=[
        gr.Textbox(lines=2, placeholder="Name Here..."),
        gr.File(file_count="multiple", file_types=["text", ".json", ".csv"]),
    ],
    outputs="file",
)

if __name__ == "__main__":
    demo.launch()
