import gradio as gr
import aio.py
import diff.py
def zip_files(text, files):
    in_put = os.path.split(files[0])
    """
    with ZipFile("tmp2222.zip", "w") as zipObj:
        for idx, file in enumerate(files):
            zipObj.write(file.name, file.name.split("/")[-1])
    """
    if files == None or text == "":
        with open("error.txt", "w") as f:
            f.write( "please write command here.And upload music file to next block. \n")
        return "writeSomething.txt","please write command here.And upload music file to next block. \n"+text
    else:
        run("m2s",files[0],in_put[0]+"unf1.png")
        diff(in_put[0]+"unf2.png",in_put[0]+"unf1.png")
        run("s2m",in_put[0]+"unf1.png",in_put[0]+"finish.mp3")
        return "finish.mp3","SUCCESSFUL!!!"+text


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
