from model import GLOBAL_VAR, get_transform, get_model_instance_segmentation, get_model_object_detection
import torch
import matplotlib.pyplot as plt
from torchvision.io import read_image

from torchvision.utils import draw_bounding_boxes, draw_segmentation_masks

num_classes = 3
device = torch.device('cuda') if torch.cuda.is_available() else torch.device('cpu')


# model = get_model_instance_segmentation(num_classes=num_classes)
model = get_model_object_detection(num_classes=num_classes)
model.load_state_dict(torch.load(GLOBAL_VAR['MODEL_PATH']))

model.to(device)

model.eval()

image = read_image("../show/iCloud-Photos/onion/IMG_8351.JPEG")
eval_transform = get_transform(train=False)

with torch.no_grad():
    x = eval_transform(image)
    # convert RGBA -> RGB and move to device
    x = x[:3, ...].to(device)
    predictions = model([x, ])
    pred = predictions[0]


box_threshold = 0.8
image = (255.0 * (image - image.min()) / (image.max() - image.min())).to(torch.uint8)
image = image[:3, ...]
pred_labels = [f"{label}+{score:.3f}" for label, score in zip(pred["labels"], pred["scores"]) if score > box_threshold]
pred_boxes = pred["boxes"][pred['scores'] > box_threshold].long()
output_image = draw_bounding_boxes(image, pred_boxes, pred_labels, colors="red")

# proba_threshold = 0.9
# score_threshold = 0.5
# masks = (pred["masks"][pred['scores'] > score_threshold] > proba_threshold).squeeze(1)
# output_image = draw_segmentation_masks(output_image, masks, alpha=0.5, colors="blue")
print(pred["scores"])
print(pred["labels"])
plt.figure(figsize=(12, 12))
plt.imshow(output_image.permute(1, 2, 0))
plt.show()