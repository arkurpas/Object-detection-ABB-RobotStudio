import os
import utils
import torch
import torchvision
from torchvision import tv_tensors
from engine import train_one_epoch, evaluate
from torchvision.io import read_image
from torchvision.ops.boxes import masks_to_boxes
from torchvision.transforms.v2 import functional as F
from torchvision.models.detection import _utils
from torchvision.models.detection import SSDLite320_MobileNet_V3_Large_Weights
from torchvision.models.detection.faster_rcnn import FastRCNNPredictor
from torchvision.models.detection.mask_rcnn import MaskRCNNPredictor
from torchvision.models.detection.ssd import SSDClassificationHead
from torchvision.transforms import v2 as T
from torch.utils.data import Dataset
from torch.utils.tensorboard import SummaryWriter

# Setting up Tensorboard writer
writer = SummaryWriter('../runs/experiment_1')

# Global variables
GLOBAL_VAR = {'TRAIN_DIR': '../my_pictures.v8i.voc/train',
              'VAL_DIR': '../my_pictures.v8i.voc/valid',
              'TEST_DIR': '../my_pictures.v8i.voc/valid',
              'MODEL_PATH': 'model/model_chips.pth'}

num_classes = 3


class ChipsDataset(torch.utils.data.Dataset):
    """
    Custom dataset class for handling image and mask data for chip detection.
    """

    def __init__(self, root, transforms):
        """
        Initialize dataset with root directory and transformations.

        Args:
            root (str): Root directory containing images and masks.
            transforms (callable): Transformations to apply to samples.
        """
        self.root = root
        self.transforms = transforms
        self.imgs = [image for image in sorted(os.listdir(root)) if image[-4:] == '.jpg']
        self.masks = [image for image in sorted(os.listdir(root)) if image[-4:] == '.png']
        self.annot = [image for image in sorted(os.listdir(root)) if image[-4:] == '.xml']
        self.mapping = {0: 0,  # 0 background
                        80: 1,  # 1 = Crunchips
                        255: 2,  # 2 = Lay's
                        }

    def mask_to_class(self, mask):
        """
        Convert mask labels to class labels.

        Args:
            mask (Tensor): Mask tensor.

        Returns:
            Tensor: Converted mask tensor with class labels.
        """
        for k in self.mapping:
            mask[mask == k] = self.mapping[k]
        return mask

    def __getitem__(self, idx):
        """
        Retrieve sample at specified index.

        Args:
            idx (int): Index of sample.

        Returns:
            tuple: Image tensor and target dictionary.
        """
        img_path = os.path.join(self.root, self.imgs[idx])
        mask_path = os.path.join(self.root, self.masks[idx])
        img = read_image(img_path)
        mask = read_image(mask_path)
        mask = self.mask_to_class(mask)
        obj_ids = torch.unique(mask)
        obj_ids = obj_ids[1:]
        num_objs = len(obj_ids)
        masks = (mask == obj_ids[:, None, None]).to(dtype=torch.uint8)
        boxes = masks_to_boxes(masks)
        image_id = idx
        area = (boxes[:, 3] - boxes[:, 1]) * (boxes[:, 2] - boxes[:, 0])
        iscrowd = torch.zeros((num_objs,), dtype=torch.int64)
        img = tv_tensors.Image(img)
        target = {}
        target["boxes"] = tv_tensors.BoundingBoxes(boxes, format="XYXY", canvas_size=F.get_size(img))
        target["masks"] = tv_tensors.Mask(masks)
        target["labels"] = torch.as_tensor(obj_ids, dtype=torch.int64)
        target["image_id"] = image_id
        target["area"] = area
        target["iscrowd"] = iscrowd
        if self.transforms is not None:
            img, target = self.transforms(img, target)
        return img, target

    def __len__(self):
        """
        Get length of dataset.

        Returns:
            int: Length of dataset.
        """
        return len(self.imgs)


def get_model_object_detection_fasterrcnn():
    """
    Retrieve a Faster R-CNN model for object detection.

    Returns:
        torchvision.models.detection.FasterRCNN: Faster R-CNN model.
    """
    model = torchvision.models.detection.fasterrcnn_resnet50_fpn(weights="DEFAULT")
    num_classes = 3
    in_features = model.roi_heads.box_predictor.cls_score.in_features
    model.roi_heads.box_predictor = FastRCNNPredictor(in_features, num_classes)
    return model


def get_model_object_detection(num_classes=3, size=320):
    """
    Retrieve an SSD model for object detection.

    Args:
        num_classes (int): Number of classes.
        size (int): Input image size.

    Returns:
        torchvision.models.detection.SSD: SSD model.
    """
    model = torchvision.models.detection.ssdlite320_mobilenet_v3_large(weights=SSDLite320_MobileNet_V3_Large_Weights.DEFAULT)
    in_channels = _utils.retrieve_out_channels(model.backbone, (size, size))
    num_anchors = model.anchor_generator.num_anchors_per_location()
    model.head.classification_head = SSDClassificationHead(
        in_channels=in_channels,
        num_anchors=num_anchors,
        num_classes=num_classes,
    )
    model.transform.min_size = (size,)
    model.transform.max_size = size
    return model


def get_model_instance_segmentation(num_classes):
    """
    Retrieve a Mask R-CNN model for instance segmentation.

    Args:
        num_classes (int): Number of classes.

    Returns:
        torchvision.models.detection.MaskRCNN: Mask R-CNN model.
    """
    model = torchvision.models.detection.maskrcnn_resnet50_fpn_v2(weights="DEFAULT")
    in_features = model.roi_heads.box_predictor.cls_score.in_features
    model.roi_heads.box_predictor = FastRCNNPredictor(in_features, num_classes)
    in_features_mask = model.roi_heads.mask_predictor.conv5_mask.in_channels
    hidden_layer = 256
    model.roi_heads.mask_predictor = MaskRCNNPredictor(
        in_features_mask,
        hidden_layer,
        num_classes
    )
    return model


def get_transform(train):
    """
    Retrieve transformations for training or evaluation.

    Args:
        train (bool): True if training, False if evaluation.

    Returns:
        torchvision.transforms.Compose: Transformation pipeline.
    """
    transforms = []
    if train:
        pass
    transforms.append(T.ToDtype(torch.float, scale=True))
    transforms.append(T.ToPureTensor())
    return T.Compose(transforms)


def train_model():
    """
    Train the model.
    """
    device = torch.device('cuda') if torch.cuda.is_available() else torch.device('cpu')
    dataset = ChipsDataset(GLOBAL_VAR['TRAIN_DIR'], get_transform(train=True))
    dataset_test = ChipsDataset(GLOBAL_VAR['VAL_DIR'], get_transform(train=False))
    data_loader = torch.utils.data.DataLoader(
        dataset,
        batch_size=10,
        shuffle=True,
        collate_fn=utils.collate_fn
    )
    data_loader_test = torch.utils.data.DataLoader(
        dataset_test,
        batch_size=10,
        shuffle=False,
        collate_fn=utils.collate_fn
    )
    model = get_model_object_detection()
    model.to(device)
    params = [p for p in model.parameters() if p.requires_grad]
    optimizer = torch.optim.SGD(
        params,
        lr=0.001,
        momentum=0.9,
        weight_decay=0.0005
    )
    lr_scheduler = torch.optim.lr_scheduler.StepLR(
        optimizer,
        step_size=5,
        gamma=0.1
    )
    num_epochs = 30
    for epoch in range(num_epochs):
        train_one_epoch(model, optimizer, data_loader, device, epoch, print_freq=3)
        lr_scheduler.step()
        evaluate(model, data_loader_test, device=device)
    print("That's it!")
    torch.save(model.state_dict(), GLOBAL_VAR['MODEL_PATH'])


# train_model()
