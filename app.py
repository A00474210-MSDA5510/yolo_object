import streamlit as st
import cv2
from ultralytics import YOLO
import time
import json

ITEMS_TO_TRACK = [45, 39, 41]  # 45: bowl, 39: bottle, 41: cup
MODEL_PATH = "yolov8n.pt"


class ParseSingleResult:
    """
    Made this To be able to found one specific item in one frame easier.
    Usually I would put this in my helper directory, but leave it here
    so you don't have to go digging.
    """

    def __init__(self, result):
        """
        made ez to get json
        result.names only give you a list of all names @_@
        """
        self.data = json.loads(result.tojson())
        self.names = [item["name"] for item in self.data]
        self.classes = [item["class"] for item in self.data]

    def included_in_frame(self, match_list):
        """
        return True: if one or more items in list matches one item in frame --> object class
        return False: if no item matches
        """
        return any(match_cls in self.classes for match_cls in match_list)


def toggle_scanning():
    """
    For Toggle button --> streamlit official doc shows this is the way
    """
    st.session_state.toggle_button = not st.session_state.toggle_button


def load_model():
    return YOLO(MODEL_PATH)


def clear_data_and_reset():
    """
    Delete all data to refresh data
    """
    st.session_state.clear()
    st.experimental_rerun()


def setup_page():
    """
    All setup goes here.
    """
    st.title("Webcam Display Streamlit App")
    st.caption("Powered by OpenCV and Streamlit")
    if "toggle_button" not in st.session_state:
        st.session_state.toggle_button = False
    if "total_time" not in st.session_state:
        st.session_state.total_time = 0.0
    st.button("Toggle Scanning", on_click=toggle_scanning)
    if st.button("Reset Data"):
        clear_data_and_reset()


def main():
    setup_page()
    model = load_model()  # Initialize the YOLO model
    camera = cv2.VideoCapture(0)  # Start the webcam
    frame_placeholder = st.empty()  # Placeholder for displaying frames

    if "frames" not in st.session_state:
        st.session_state['frames'] = []

    if st.session_state.toggle_button:
        if "start_time" not in st.session_state:
            st.session_state['start_time'] = time.time()  # For Tracking time

        while camera.isOpened():
            success, frame = camera.read()
            if not success:
                st.error("Failed to capture video.")
                break

            results = model.track(frame, persist=True)
            parsed_results = ParseSingleResult(results[0])
            annotated_frame = results[0].plot() if parsed_results.included_in_frame(ITEMS_TO_TRACK) else frame
            st.session_state.frames.append(results[0])
            display_frame = cv2.cvtColor(annotated_frame, cv2.COLOR_BGR2RGB)
            frame_placeholder.image(display_frame)

    else:
        if "start_time" in st.session_state:
            update_total_run_time()
            display_results()

    camera.release()
    cv2.destroyAllWindows()


def update_total_run_time():
    elapsed_time = time.time() - st.session_state.start_time
    st.session_state.total_time += elapsed_time
    del st.session_state['start_time']  # Clean up start time
    st.write(f"Total scanning time: {st.session_state.total_time:.2f}s")  # Recording time

    # Total frame/fps = video time
    st.write(f"video time based on fps: "
             f"{len(st.session_state.frames) / cv2.VideoCapture(0).get(cv2.CAP_PROP_FPS):.2f}s")


def display_results():
    for item_id in [45, 39, 41]:
        # for each ID display it's number of frame
        count = sum(1 for frame in st.session_state.frames if ParseSingleResult(frame).included_in_frame([item_id]))
        st.write(f"The video contains {YOLO('yolov8n.pt').names[item_id]} for {count} frames")
    st.write(f"The ML model processed: {len(st.session_state.frames)} frame")


if __name__ == "__main__":
    main()
