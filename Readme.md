
# Directory Guide

This guide provides a simple overview and highlights the important one.

## [app.py](https://github.com/A00474210-MSDA5510/yolo_object/blob/main/app.py) The Three object this app reconize are
---
* bowl
* bottle
* cup

## Overview
___
This file is the primary focus of the project. It contains the majority of my work and utilizes Streamlit for user interface and interaction functionalities. The application was not deployed on Streamlit Cloud due to compatibility issues with OpenCV, especially regarding access to the local camera when hosted in the cloud.

The code is well-documented and employs the pre-trained `yolov8n.pt` model, using OpenCV for webcam access. Note that the function/API calls related to the model are mostly the latest ones, updated two months ago.



> **To run the application, type the following command in your console:**
> ```
> streamlit run app.py
> ```

* The reset data button will remove all the saved data in the streamlit application
* Toggle scanning will start the camera, toggle it again it will pause and display result.


## [stream_lite_object_rec.py](https://yoloobject-9t7mrcbkzl7p5bzmilbkfl.streamlit.app/)
___
This is a link to streamlit link, I have build this one on streamlit, using streamlit_webrtc, however streamlit is quite single threaded and the only thing I can do is draw the bounding box over the video, and please don't judge me based on the code in this file, it's more of a scratch file, but it's quite neat
* Access webcam over internet. 
