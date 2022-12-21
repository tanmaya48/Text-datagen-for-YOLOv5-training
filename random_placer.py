import numpy as np
import cv2
import random

import os

BACKGROUND_PATH='../background_images/'

BACKGROUNDS = os.listdir(BACKGROUND_PATH)

DEFAULT_SIZE = (640,640)


def load_background_image(resize=True, size=DEFAULT_SIZE) -> np.array:
    
    background = random.choice(BACKGROUNDS)

    background_image = cv2.imwrite(BACKGROUND_PATH+background)
    if resize:
        background_image=cv2.resize(background_image, size, interpolation=cv2.INTER_LINEAR)

    return background_image



def place_random(image_generator, background_size = [], max_placed_count=10,min_placed_count=2, max_placing_attempts=50, postion_attempts=5) -> dict:
    
    if len(background_size)<1:
        background_size = list(DEFAULT_SIZE)
        background_size.append(4)
    
    background= np.zeros(background_size, dtype=np.uint8)

    curent_attempt = 0

    list_label_data=[]
    list_placing_postions=[]
    
    placed_count =0

    to_place_count = random.randint(min_placed_count,max_placed_count)

    while curent_attempt < max_placing_attempts:
        
        if placed_count >= to_place_count:
            break

        image, label_data = image_generator()
        
        h,w,_ = image.shape
        
        placing_success = False
        for i in range(postion_attempts):

            x = np.random.randint( (background_size[0]-w) )
            y = np.random.randint( (background_size[1]-h) )


            if np.sum(background[y:y+h,x:x+w,:]) > 0: # if something is placed in the region
                continue

            
            placing_success = True
            break

        if not placing_success:
            continue

        background[y:y+h,x:x+w,:] = image
        list_label_data.append(label_data)
        list_placing_postions.append( (x,y,w,h) )
        
        placed_count+=1
    
    random_placed_dict={
        'image':background,
        'labels':list_label_data,
        'positions':list_placing_postions,
        'count':placed_count}

    return random_placed_dict


    

    
