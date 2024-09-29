from segment_anything import SamPredictor, sam_model_registry
import numpy as np
import torch
import matplotlib.pyplot as plt
import cv2
import time
import warnings
warnings.filterwarnings("ignore")

def run_sam():
    start_time = time.time()
    image = cv2.imread('sam/alex.jpg')

    sam_checkpoint = "sam/sam_vit_l_0b3195.pth"
    model_type = "vit_l"
    sam = sam_model_registry[model_type](checkpoint=sam_checkpoint)
    predictor = SamPredictor(sam)

    predictor.set_image(image)
    input_point = np.array([[1000, 2500]])
    input_label = np.array([1])
    masks, scores, logits = predictor.predict(
        point_coords=input_point,
        point_labels=input_label,
        multimask_output=True,
    )

    outstr = ""
    for i, (mask, score) in enumerate(zip(masks, scores)):
        plt.figure(figsize=(10,10))
        plt.imshow(image)
        image_cpy = image.copy()
        image_cpy[mask < 0.5] = [255, 255, 255]
        plt.gca().imshow(image_cpy)
        cv2.imwrite("static/image"+str(i)+".png", image_cpy)
        outstr += "<img src='static/image"+str(i)+".png' height='600px'>"

    print("--- %s seconds ---" % (time.time() - start_time))
    return outstr