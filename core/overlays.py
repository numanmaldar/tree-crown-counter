import cv2
import numpy as np
from PIL import Image


def draw_boxes_on_image(image_path, boxes_df, output_path=None):
    """
    Draws bounding boxes from DeepForest predictions onto the source image.
    Returns the annotated image as a numpy array (RGB).
    Optionally saves to output_path.
    """
    img = cv2.imread(image_path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    for _, row in boxes_df.iterrows():
        xmin, ymin, xmax, ymax = int(row["xmin"]), int(row["ymin"]), int(row["xmax"]), int(row["ymax"])
        score = row.get("score", 1.0)

        # Green boxes, thicker for higher confidence
        color = (0, 255, 0)
        thickness = 2

        cv2.rectangle(img, (xmin, ymin), (xmax, ymax), color, thickness)

        # Optional: label with score
        label = f"{score:.2f}"
        cv2.putText(img, label, (xmin, max(ymin - 5, 0)),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.4, color, 1)

    if output_path:
        Image.fromarray(img).save(output_path)

    return img