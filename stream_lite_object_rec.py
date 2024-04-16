import streamlit as st
from streamlit_webrtc import webrtc_streamer, VideoProcessorBase
from ultralytics import YOLO
import av
import time
import queue
import threading

st.title("OpenCV Filters on Video Stream")
item_to_track = [45, 39, 41]

if "frames" not in st.session_state:
    st.session_state.frames = []

lock = threading.Lock()
class transform(VideoProcessorBase):
    result_queue = []

    def __init__(self) -> None:
        self._model = YOLO('yolov8n.pt')

    def recv(self, frame: av.VideoFrame) -> av.VideoFrame:
        img = frame.to_ndarray(format="bgr24")
        results = self._model.track(img, persist=True)
        img = results[0].plot()
        self.result_queue.append(results[0])
        st.session_state.frames.append(results[0])
        st.write(len(st.session_state.frames))



        return av.VideoFrame.from_ndarray(img, format="bgr24")

webrtc_ctx = webrtc_streamer(
    key="object-detection",
    video_processor_factory=transform,
    sendback_audio=False,
    rtc_configuration={  # Add this line
        "iceServers": [{"urls": ["stun:stun2.l.google.com:19302"]}]},
    media_stream_constraints={"video": True, "audio": False},
)

if "frames" not in st.session_state:
    st.session_state["frames"] = None

if "start_time" not in st.session_state:
    st.session_state['start_time'] = None



def time_calc(webrtc_ctx):
    if webrtc_ctx.state.playing:
        st.session_state.start_time = time.time()
        st.write("IM PLAYING DEEZNUTS")
    elif not webrtc_ctx.state.playing and st.session_state.start_time != None:
        elapsed_time = time.time() - st.session_state.start_time
        st.session_state.start_time = None
        st.write(elapsed_time)
        result = len(webrtc_ctx.video_processor.result_queue)
        st.write(result)
        st.write("HOHOHOHOH")

time_calc(webrtc_ctx)
st.write(webrtc_ctx.state.playing)