# Object detection with an ABB Robot


<p float="center">
  <img src="https://github.com/arkurpas/Object-detection-ABB-RobotStudio/assets/129556066/c3988a6e-7703-490e-bcae-93ff3a80b005)" width="500" />
  <img src="https://github.com/arkurpas/Object-detection-ABB-RobotStudio/assets/129556066/3d299685-de07-4fe2-ae93-cf3955cd3fe6" width="500" /> 
</p>


## See it in action
youtube_link

## About...
The goal of this project was to implement object detection into robotics station. 

* Model: fine tunned Single Shot Detector (SSD)
* Library: PyTorch
* Dataset: 60 captured images
* Annotation: Roboflow
* Robots: ABB IRB1200 and ABB IRB2600
* Simulation: ABB RobotStudio
* Communication: Sockets

  ## Process description

A small robot goes above conveyor where boxes with chips in come. In that posstion robot starts camera (for simulation purpose it was a computer webcamera). Loaded neural network looks for object it was trained for. If the object is found robot reccive information regarding type of detected object and its center point. 
