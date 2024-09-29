from ultralytics import SAM
import cv2
import time
import warnings
import numpy as np
warnings.filterwarnings("ignore")

def run_sam(x_coord, y_coord):
    start_time = time.time()
    
    source = 'static/input.jpg'
    image = cv2.imread(source)

    model = SAM("sam_b.pt")
    results = model(source, points=[[int(x_coord), int(y_coord)]], labels=[1])
    mask = results[0].masks.data.detach().numpy().squeeze()
    print("--- %s seconds ---" % (time.time() - start_time))

    np.savetxt('static/bitmask.txt', mask.astype(int), fmt='%d')

    image[mask < 0.5] = [255, 255, 255]
    cv2.imwrite('static/mask.jpg', image)

    print("--- %s seconds ---" % (time.time() - start_time))