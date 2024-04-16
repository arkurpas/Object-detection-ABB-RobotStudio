# Object detection with an ABB Robot


<p float="center">
  <img src="https://github.com/arkurpas/Object-detection-ABB-RobotStudio/assets/129556066/c3988a6e-7703-490e-bcae-93ff3a80b005)" width="800" />
  <img src="https://github.com/arkurpas/Object-detection-ABB-RobotStudio/assets/129556066/c5d11642-ac5e-401a-9426-c4e48bf7508b" width="800" /> 
</p>


## See it in action
https://www.youtube.com/watch?v=YAWKSnbmhUU

(The  walkthrough video will be available soon.)

## In short
The objective of this project was to deploy object detection and recognition models in robotics through the application of computer vision techniques.

* Model: Single Shot Detector (SSD)
* Library: PyTorch
* Dataset: 60 captured images
* Annotation: Roboflow
* Robots: ABB IRB1200 and ABB IRB2600
* Simulation: ABB RobotStudio
* Hardware: Dell Precision 3581 with NVIDIA RTX 2000 ADA graphics card 

  
## Process description
  
* Randomly ordered packages arrive at the robotics station.
* A small robot approaches the conveyor and activates the camera mounted on its gripper.
* The trained model enables the detection of the manufacturer's logo.
* The type and coordinates of the detected object's center point are transmitted to the robot.
* The robot picks up the package with a vacuum gripper and places it into the appropriate box.
* When a box is filled with 16 packages of a specific type of chips, the large robot picks it up and places it on the output conveyor.


## Insights

  As a robotics engineer with a passion for AI, I aimed to bridge both domains. This led to the idea of implementing object detection within the robotics station.

  By initiating the camera_main.py program, a server for socket communication between Python code and robot code is established. When a small robot sends a "send_to_robot" message, the camera activates. The loaded SSD model searches for the manufacturer's logo. Upon detecting an object, the type of the object and its center point coordinates are sent to the robot. Subsequently, in the robot's program, the message is converted into an appropriate format. Based on this information, the robot places a package of chips into the correct box.

  Initially, I intended to use Faster R-CNN for object detection and Mask R-CNN for segmentation. However, due to the computational limitations of my computer, I opted for SSD (Single Shot Detector) for object detection, as it performed better in real-time object detection. Additionally, I planned to incorporate functionality to adjust the robot's pickup position based on the product's position in the box. However, due to the difficulty in demonstrating this using a computer camera, it was not implemented. From a robotics perspective, the only necessary adjustment is to change the work object frame according to the received coordinates. Certainly, additional considerations must be made for tilted or rotated objects. Proper image processing is crucial.

  This project serves as an example of deep learning application. However, there are numerous real-world robot applications where object detection could be implemented. Fine-tuning or transfer learning are invaluable for detecvting and segmenting various objects.


## Files description

* camera_main.py - the main program that needs to be launched before starting robots in RobotStudio. It establishes a host server for socket communication between Python and robot code (RAPID language). When the robot sends a message to a socket host, the camera activates to detect an object placed in front of it.
* model.py - code responsible for model training. It includes functions for loading the SSD model as well as Faster R-CNN and Mask R-CNN.
* k-mean-filtering.py - code responsible for clustering some input pictures.
* model_evaluation.py - code to evaluate the model's performance with unseen images.
* polygon2mask.py - code that loads an XML file created after the annotation process and, based on polygon coordinates, generates a mask for each image. Each mask is represented with its own grayscale color. This step was preparatory for training the Mask R-CNN model.
  
folders

* Robots_programs - contain modules with robots programs
* from_camera_image - object detection example
* my_pictures.v8i.voc - dataset. Containing images obtained after augmentation process in roboflow.
* recorded_simulation - compelete simulation of process.





