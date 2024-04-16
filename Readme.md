
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
