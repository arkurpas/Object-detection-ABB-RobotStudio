# Object detection with an ABB Robot


<p float="center">
  <img src="https://github.com/arkurpas/Object-detection-ABB-RobotStudio/assets/129556066/c3988a6e-7703-490e-bcae-93ff3a80b005)" width="600" />
  <img src="https://github.com/arkurpas/Object-detection-ABB-RobotStudio/assets/129556066/3d299685-de07-4fe2-ae93-cf3955cd3fe6" width="600" /> 
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
* Hardware: Dell Precision 3581 with NVIDIA RTX 2000 ADA graphics card 

  
## Process description

* a set of random ordered packages come into the station
* a small robot goes above conveyor and  start the camera placed on its gripper
* trained model looks for the manufacturer's logo
* a type of detected object together with coordinates of the center point are sent to robot
* robot picks up the package with vaccum gripper and place it into proper box.
* When a box is filled with 16 packages of specific type of the chips big robot picks up full box and place it on output conveyr.


## insights

### Python Code 
The project consist of a  
Initially, I aimed to utilize Faster R-CNN for object detection and Mask R-CNN for segmentation. However, due to the computational power limitations of my computer, I decided to opt for SSD (Single Shot Detector) for object detection. It just worked better in the real time object detection.

### Robotic side
Programs for both robots were created from scratch by me. 


