# Object detection with an ABB Robot


<p float="center">
  <img src="https://github.com/arkurpas/Object-detection-ABB-RobotStudio/assets/129556066/c3988a6e-7703-490e-bcae-93ff3a80b005)" width="800" />
  <img src="https://github.com/arkurpas/Object-detection-ABB-RobotStudio/assets/129556066/3d299685-de07-4fe2-ae93-cf3955cd3fe6" width="800" /> 
</p>


## See it in action
https://www.youtube.com/watch?v=YAWKSnbmhUU

(a video with a walkthrough is coming)

## About...
The goal of this project was to implement object detection into robotics station. 

* Model: Single Shot Detector (SSD)
* Library: PyTorch
* Dataset: 60 captured images
* Annotation: Roboflow
* Robots: ABB IRB1200 and ABB IRB2600
* Simulation: ABB RobotStudio
* Hardware: Dell Precision 3581 with NVIDIA RTX 2000 ADA graphics card 

  
## Proccess description

* a set of random ordered packages come into the station
* a small robot goes above conveyor and  start the camera placed on its gripper
* trained model looks for the manufacturer's logo
* a type of detected object together with coordinates of the center point are sent to robot
* robot picks up the package with a vaccum gripper and place it into proper box.
* When a box is filled with 16 packages of specific type of the chips big robot picks up full box and place it on output conveyr.


## insights

As a robotics engineer with a passion for AI i wanted to connect both worlds. This led me to an idea of implementing object detection into robotics station. 
By starting a camera_main.py program a server for a socket communication between python code and robot code is created. When a small robot send a "send_to_robot" message a camera is started. Loaded SSD model looks for manufacturer's logo. When an object is detected a type of the object and the coordinates of center point are sent to robot. Then in the robot program the message is converted into appropriate format. Based on that infromation robot drop a pacckage of chips into a proper box.  
Initially, I aimed to utilize Faster R-CNN for object detection and Mask R-CNN for segmentation. However, due to the computational power limitations of my computer, Icided to de opt for SSD (Single Shot Detector) for object detection. It just worked better in the real time object detection. Also I planned to add a functionality for adjusting the robot's pickup position based on the product's position in the box . However, due to the difficulty in demonstrating this using a computer camera, it was not implemented. From robotics perspective the only thing which needs to be done is to change a work object frame according to reciverd coordinates. For sure many more factors must be taken into account when an object is tilted or rotated. It is important to properly process the image.

This project is just an example of deep learning usage, however there are many real world robot application where object detection could be implemented. Fine tunning or transfer learning are incredible for detecting, segmentig anything we want.


## Files description
* camera_main.py - main program which needs to be started before starting robotos in RobotStudio. It creates a host server for socket communication between python and robot code (RAPID language). When the robot send a message to a socket host it starts a camera to detect an object placed in front of the camera.
* model.py - code responsible for training a model. It contains fonction for loading SSD model but also Faster RCNN and mask RCNN.
* k-mean-filtering.py - code responsible for clustering some of input pictures.
* model_evaluation.py - a code to test how model works with unseed images.
* polygon2mask.py - a code which loads an XML file creaded after annotation proccess and based on polygon coordinates create a mask for each picture. Each mask has its own color in grayscale. This was a preparation step for training mask-RCNN model.
folders:
Robots_programs - contain modules with robots programs
from_camera_image - object detection example
my_pictures.v8i.voc - dataset. Containing images obtained after augmentation proccess in roboflow.
recorded_simulation - compelete simulation of proccess.





