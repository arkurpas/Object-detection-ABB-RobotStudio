# Object detection with an ABB Robot


<p float="center">
  <img src="https://github.com/arkurpas/Object-detection-ABB-RobotStudio/assets/129556066/c3988a6e-7703-490e-bcae-93ff3a80b005)" width="500" />
  <img src="https://github.com/arkurpas/Object-detection-ABB-RobotStudio/assets/129556066/3d299685-de07-4fe2-ae93-cf3955cd3fe6" width="500" /> 
</p>


## See it in action
youtube_link

## About...
The goal of this project was to implement object detection into robotics station. 

* Model: Single Shot Detector (SSD)
* Library: PyTorch
* Dataset: 60 captured images
* Annotation: Roboflow
* Robots: ABB IRB1200 and ABB IRB2600
* Simulation: ABB RobotStudio
* Communication: Sockets

## Process description

1. a set of random ordered packages come into the station
2. a small robot goes above conveyor and  start the camera placed on its gripper
3. trained model looks for the manufacturer's logo
4. a type of detected object together with coordinates of the center point are sent to robot
5. robot picks up the package with vaccum gripper and place it into proper box.
6. When a box is filled with 16 packages of specific type of the chips big robot picks up full box and place it on output conveyr. 

## Process description
