import cv2
from ultralytics import YOLO
import json

class parse_result:
    def __init__(self, result):
        self.json_file = json.loads(result.tojson())
        self.name = [i["name"] for i in self.json_file]
        self.obj_class = [i["class"] for i in self.json_file]

# Load the YOLOv8 model
model = YOLO('yolov8n.pt')
model.classes = [45, 39, 41]
item_to_track = [45, 39, 41]

# Open the video file
cap = cv2.VideoCapture(0)
fps = cap.get(cv2.CAP_PROP_FPS)
result_array = []
# Loop through the video frames
while cap.isOpened():
    # Read a frame from the video
    success, frame = cap.read()

    if success:
        # Run YOLOv8 tracking on the frame, persisting tracks between frames
        print(type(frame))
        results = model.track(frame, persist=True)
        result_array.append(results)
        annotated_frame = frame
        if any(same_item in parse_result(results[0]).obj_class for same_item in item_to_track):
            print("LOLOLOLOLOLOLOLOLOLOL")
            annotated_frame = results[0].plot()
        cv2.imshow("YOLOv8 Tracking", annotated_frame)
        print(len(results))

        # Break the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
    else:
        # Break the loop if the end of the video is reached
        break

# Release the video capture object and close the display window
for i in model.names:
    print(i, model.names[i])
for i in result_array:
    print("LOL")
    print(parse_result(i[0]).name)
print(fps)
cap.release()
cv2.destroyAllWindows()