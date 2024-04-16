import cv2
from ultralytics import YOLO

# Load the YOLOv8 model
model = YOLO('yolov8n.pt')
item_to_track = [45, 39, 41]

# Open the video file
video_path = "vids.mp4"
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

        # Visualize the results on the frame
        annotated_frame = results[0].plot()
        print(type(annotated_frame))

        # Display the annotated frame
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
print(type(result_array[0][0]))
print(fps)
cap.release()
cv2.destroyAllWindows()