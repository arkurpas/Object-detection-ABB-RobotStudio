# Object detection with an ABB Robot


<p float="center">
  <img src="https://github.com/arkurpas/Object-detection-ABB-RobotStudio/assets/129556066/c3988a6e-7703-490e-bcae-93ff3a80b005)" width="800" />
  <img src="https://github.com/arkurpas/Object-detection-ABB-RobotStudio/assets/129556066/3d299685-de07-4fe2-ae93-cf3955cd3fe6" width="800" /> 
</p>


## See it in action
https://www.youtube.com/watch?v=YAWKSnbmhUU

## About...
The goal of this project was to implement object detection into robotics station. 

* Model: Single Shot Detector (SSD)
* Library: PyTorch
* Dataset: 60 captured images
* Annotation: Roboflow
* Robots: ABB IRB1200 and ABB IRB2600
* Simulation: ABB RobotStudio
* Hardware: Dell Precision 3581 with NVIDIA RTX 2000 ADA graphics card 

  
## Process description

* a set of random ordered packages come into the station
* a small robot goes above conveyor and  start the camera placed on its gripper
* trained model looks for the manufacturer's logo
* a type of detected object together with coordinates of the center point are sent to robot
* robot picks up the package with vaccum gripper and place it into proper box.
* When a box is filled with 16 packages of specific type of the chips big robot picks up full box and place it on output conveyr.


## Files description
* camera_main.py - main program which needs to be started before starting robotos in RobotStudio. It creates host for socket communication between python and robot code (RAPID language). When the robot send a message to a socket host it starts a camera to detect an object placed in front of the camera.
* model.py - code responsible for training a model. It contains fonction for loading SSD model but also Faster RCNN and mask RCNN.
* k-mean-filtering.py - code responsible for clustering some of input pictures.
* model_evaluation.py - a code to test how model works with unseed images.
* polygon2mask.py - a code which loads an XML file creaded after annotation process and based on polygon coordinates create a mask for each picture. Each mask has its own color in grayscale. This was a preparation step for training mask-RCNN model.
folders:
Robots_programs - contain modules with robots programs
from_camera_image - object detection example
my_pictures.v8i.voc - dataset. Containing images obtained after augmentation process in roboflow.
recorded_simulation - compelete simulation of process.


## insights

### Python Code 
Initially, I aimed to utilize Faster R-CNN for object detection and Mask R-CNN for segmentation. However, due to the computational power limitations of my computer, I decided to opt for SSD (Single Shot Detector) for object detection. It just worked better in the real time object detection.
Communi

### Robotic side
Programs for both robots were created from scratch by me. 


