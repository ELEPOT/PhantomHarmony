FROM python:3.9

ARG GRADIO_SERVER_PORT=7860
ENV GRADIO_SERVER_PORT=${GRADIO_SERVER_PORT}

WORKDIR /gradio

ADD   PhantomHarmony/ /gradio/
RUN apt-get update -y
RUN apt-get install ffmpeg -y
RUN python3.9 -m pip install --no-deps -r /gradio/webui_require.txt
#RUN apt-get install ffmpeg
CMD ["python", "/gradio/src/webui/webui.py"]
