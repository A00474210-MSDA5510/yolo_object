import streamlit as st
from streamlit_webrtc import webrtc_streamer
from ultralytics import YOLO
import av
import time
import threading
from queue import Queue



def transform(frame):
    img = frame.to_ndarray(format="bgr24")
    results = model.track(img, persist=True)
    with lock:
        img_container["img"] = results[0]
    img = results[0].plot()
    return av.VideoFrame.from_ndarray(img, format="bgr24")




def time_calc(webrtc_ctx):
    if webrtc_ctx.state.playing:
        st.session_state.start_time = time.time()
        with lock:
            img = img_container["img"]
            st.session_state.frames.put(img)
            st.session_state.queue_size += 1
        if img is None:
            pass
    elif not webrtc_ctx.state.playing and st.session_state.start_time != None:
        elapsed_time = time.time() - st.session_state.start_time
        st.session_state.start_time = None
        st.write(f"elapsed time {elapsed_time:.2f}")





if __name__ == "__main__":

    st.title("OpenCV Filters on Video Stream")
    model = YOLO('yolov8n.pt')
    item_to_track = [45, 39, 41]

    lock = threading.Lock()
    img_container = {"img": None}
    if "frames" not in st.session_state:
        st.session_state.frames = Queue()

    webrtc_ctx = webrtc_streamer(
        key="object-detection",
        video_frame_callback=transform,
        sendback_audio=False,
        rtc_configuration={  # Add this line
            "iceServers": [{"urls": ["stun:stun2.l.google.com:19302"]}]},
        media_stream_constraints={"video": True, "audio": False},
    )

    if "frames" not in st.session_state:
        st.session_state["frames"] = None

    if "start_time" not in st.session_state:
        st.session_state['start_time'] = None

    if "queue_size" not in st.session_state:
        st.session_state.queue_size = 0

    time_calc(webrtc_ctx)
