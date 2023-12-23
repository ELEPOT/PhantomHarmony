import gradio as gr


def zip_files(text, files):
    """
    with ZipFile("tmp2222.zip", "w") as zipObj:
        for idx, file in enumerate(files):
            zipObj.write(file.name, file.name.split("/")[-1])
    """

    with open("writeSomething.txt", "w") as f:
        a = files[0]
<<<<<<< HEAD
        a = str(a + "   " + text)
        f.write(a + "\n")
=======
        a = str(a)
        f.write(a)
>>>>>>> 516eec6fa789593cbb795b7d6698a6fc11b8676a
    return "writeSomething.txt"


demo = gr.Interface(
    zip_files,
    inputs=[
        gr.Textbox(lines=2, placeholder="Name Here..."),
        gr.File(file_count="multiple", file_types=["text", ".json", ".csv"]),
    ],
<<<<<<< HEAD
    outputs="file",
=======
    outputs="text",
>>>>>>> 516eec6fa789593cbb795b7d6698a6fc11b8676a
)

if __name__ == "__main__":
    demo.launch()
