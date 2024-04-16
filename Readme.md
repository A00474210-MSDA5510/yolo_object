# Directory Guide
Here is going to simple guide you what each file is and which one is important!


## [app.py](https://github.com/A00474210-MSDA5510/yolo_object/blob/main/app.py)
___
This is the only file you needs to look at, I put most of my work it to it, it uses streamlit for the UI and interaction.
It was not deployed on the streamlit cloud is because OpenCV does not work well with streamlit, espcially when it try
to access local camera when it's on the cloud.

The code is well documented, I uses pre trained yolov8n.pt for my model(the newest one), uses opencv to access webcam, however the function/API 
call about the model mostly are the new ones, updated two month ago.

> To run app, type `streamlit run app.py` in console

