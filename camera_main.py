import time
import cv2
import torch
from model import GLOBAL_VAR, get_model_object_detection, LabelConverter
from torchvision.transforms import v2 as T
import socket
from queue import Queue

# Path to the model
MODEL_PATH = GLOBAL_VAR['MODEL_PATH']
# Host address and port
HOST = "127.0.0.1"
PORT = 8000

class ObjectDetector:
    """Class implementing object detection."""
    def __init__(self, model_path, num_classes=3):
        """Initialize the object detector."""
        self.model_path = model_path
        self.num_classes = num_classes
        self.model = self.load_model()

        # The model was trained on RGB images loaded via torchvision.io.read_image,
        # so incoming frames must be converted from OpenCV's BGR before this runs.
        self.transform = T.Compose([
            T.ToImage(),
            T.ToDtype(torch.float32, scale=True),
        ])

    def load_model(self):
        """Load the object detection model."""
        model = get_model_object_detection(num_classes=self.num_classes)
        model.load_state_dict(torch.load(self.model_path, map_location="cpu"))
        model.eval()
        return model

    def detect_and_segment(self, image):
        """Detect and segment objects in an RGB image."""
        input_tensor = self.transform(image).unsqueeze(0)
        with torch.no_grad():
            output = self.model(input_tensor)
        return output


def start_camera(q_out, detector, label_converter):
    """Function to start the camera and perform object detection."""
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Could not open camera.")
        return
    time.sleep(1)
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        cv2.imshow('Camera Feed', frame)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        output = detector.detect_and_segment(rgb_frame)
        for box, score, label in zip(output[0]['boxes'], output[0]['scores'], output[0]['labels']):
            if score > 0.8:
                cv2.rectangle(frame, (int(box[0]), int(box[1])), (int(box[2]), int(box[3])), (0, 255, 0), 2)

                center_point = (int((box[0] + box[2]) / 2), int((box[1] + box[3]) / 2))
                cv2.circle(frame, center_point, 5, (0, 255, 0), thickness=-1)
                cv2.putText(frame, f"{center_point}", center_point, cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)

                class_name = label_converter.label_to_name(label.item())
                class_score = f"{score:.2f}"
                cv2.putText(frame, f"{class_name} {class_score}", (int(box[0]), int(box[1]) - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 0), 2)

                data = str(f"{label.item()}{center_point[0]}-{center_point[1]}").encode()
                q_out.put(data)
                cv2.destroyWindow('Camera Feed')
                cv2.imwrite("from_camera_image/camera_save.jpg", frame)
                saved_image = cv2.imread("from_camera_image/camera_save.jpg",1)
                cv2.imshow('saved_image', saved_image)
                cv2.waitKey(2000)
                cv2.destroyWindow("saved_image")

                return


        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

def main():
    """Main function of the program."""
    q = Queue()

    detector = ObjectDetector(MODEL_PATH)
    label_converter = LabelConverter()

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print(f"Server listening on {HOST}:{PORT}")
        conn, addr = s.accept()
        print(f"Connected by {addr}")
        with conn:
            while True:
                try:
                    message = conn.recv(1024).decode()
                    if not message:
                        print("Client disconnected.")
                        break
                    print(message)

                    if message == 'send_to_robot':
                        start_camera(q, detector, label_converter)
                        if q.empty():
                            print("No object detected, nothing sent to the robot.")
                            continue
                        data_to_send = q.get()
                        print(data_to_send)
                        conn.send(data_to_send)
                except (ConnectionResetError, BrokenPipeError) as exc:
                    print(f"Connection lost: {exc}")
                    break
                finally:
                    time.sleep(2)

if __name__ == "__main__":
    main()
