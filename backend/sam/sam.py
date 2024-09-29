from segment_anything import SamPredictor, sam_model_registry
import numpy as np
import matplotlib.pyplot as plt
import cv2
import time
import warnings
warnings.filterwarnings("ignore")

def run_sam(x_coord, y_coord):
    start_time = time.time()
    
    image = cv2.imread('static/input.jpg')

    sam_checkpoint = "sam/sam_vit_l_0b3195.pth"
    model_type = "vit_l"
    sam = sam_model_registry[model_type](checkpoint=sam_checkpoint)
    predictor = SamPredictor(sam)

    predictor.set_image(image)
    input_point = np.array([[x_coord, y_coord]])
    input_label = np.array([1])
    masks, scores, logits = predictor.predict(
        point_coords=input_point,
        point_labels=input_label,
        multimask_output=False,
    )
    mask = masks[0]
    plt.figure(figsize=(10,10))
    plt.imshow(image)
    image[mask < 0.5] = [255, 255, 255]
    plt.gca().imshow(image)
    cv2.imwrite("static/mask.jpg", image)

    print("--- %s seconds ---" % (time.time() - start_time))