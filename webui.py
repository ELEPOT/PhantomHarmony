import gradio as gr


def zip_files(text, files):
    """
    with ZipFile("tmp2222.zip", "w") as zipObj:
        for idx, file in enumerate(files):
            zipObj.write(file.name, file.name.split("/")[-1])
    """
    if files == None or text == None:
        with open("writeSomething.txt", "w") as f:
            
            
            f.write( "please write command here.And upload music file to next block. \n")
        return "writeSomething.txt","please write command here.And upload music file to next block. \n"+text
    else:
        with open("writeSomething.txt", "w") as f:
            a = files[0]
            a = str(a + "   " + text)
            f.write(a + "\n")
        return "writeSomething.txt","SUCCESSFUL!!!"+text


demo = gr.Interface(
    zip_files,
    inputs=[
        gr.Textbox(lines=2, placeholder="please write command here.And upload music file to next block."),
        gr.File(file_count="multiple", file_types=["text", ".json", ".csv"]),
    ],
    outputs=["file","text"]
)

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0")
