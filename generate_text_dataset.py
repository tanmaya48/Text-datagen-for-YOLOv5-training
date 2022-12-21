import random as rnd
import cv2
import numpy as np
import os
from PIL import Image
import argparse

from text_maker import get_random_string,create_text_image,crop_image,resize_image
from random_placer import place_random,DEFAULT_SIZE

def text_image_generator():
    min_word_len = 2
    max_word_len = 7
    
    word = get_random_string(rnd.randint(min_word_len,max_word_len))
    text_image = create_text_image(word)

    return resize_image(crop_image(text_image)),word


def get_object_class(name=''):
    return 0 # all data label is text/class 0


def save_text_data(placed_data ,text_file_path='data.txt',default_size=DEFAULT_SIZE):

    labels = placed_data['labels']
    positions = placed_data['positions']

    with open(text_file_path,'w') as f:
        for label,position in zip(labels,positions):



            x_min,y_min,width,height = position

            x_mid = x_min + (width/2)
            y_mid = y_min + (height/2)

            norm_x_mid = x_mid/default_size[0]
            norm_y_mid = y_mid/default_size[1]

            norm_width = width/default_size[0]
            norm_height = height/default_size[1]
            
            object_class = 0 # get_object_class(label)

            f.write(f"{object_class} {norm_x_mid} {norm_y_mid} {norm_width} {norm_height}\n")







def parse_opt():
    parser = argparse.ArgumentParser()
    parser.add_argument('-t','--train_count', type=int, default=300)
    parser.add_argument('-v','--val_count', type=str, default=100)
    parser.add_argument('-p','--path', type=str, default='output')
    parser.add_argument('-b','--backgrounds', type=str, default='../background_images')
    return parser.parse_args()
    







def main():
    args = vars(parse_opt())

    BACKGROUNDS_PATH = args['backgrounds']
    BACKGROUNDS = os.listdir(BACKGROUNDS_PATH)


    FOLDER = args['path']
    if not os.path.exists(FOLDER):
        os.mkdir(FOLDER)


    IMAGES_TRAIN = os.path.join(FOLDER,'images/train')
    TEXTS_TRAIN =  os.path.join(FOLDER,'labels/train')

    IMAGES_VAL = os.path.join(FOLDER,'images/val')
    TEXTS_VAL =  os.path.join(FOLDER,'labels/val')


    folders = [[IMAGES_TRAIN,TEXTS_TRAIN],[IMAGES_VAL,TEXTS_VAL]]


    for im_path,tx_path in folders:
        if not os.path.exists(im_path):
            os.makedirs(im_path)
        if not os.path.exists(tx_path):
            os.makedirs(tx_path)


    images_path = IMAGES_TRAIN
    texts_path = TEXTS_TRAIN

    train_count = args['train_count']
    val_count = args['val_count']
    total_images = train_count+val_count

    for index in range(total_images):

        if index >= train_count:
            images_path = IMAGES_VAL
            texts_path = TEXTS_VAL

        

        image_path = os.path.join(images_path,str(index))
        text_path = os.path.join(texts_path,str(index))

        background_path = os.path.join(BACKGROUNDS_PATH,np.random.choice(BACKGROUNDS))
        background_image = cv2.imread(background_path)
        

        background_image = cv2.resize(background_image,DEFAULT_SIZE,interpolation= cv2.INTER_LINEAR)
        
        placed_data = place_random(text_image_generator)
        
        background_image[placed_data['image'][:,:,3]>0] = [0,0,0]
        background_image = background_image+placed_data['image'][:,:,:3]

        cv2.imwrite(f'{image_path}.png',np.array(background_image))

        save_text_data(placed_data,text_file_path=f'{text_path}.txt')

        print(f'index: {index} background: {background_path} count: {placed_data["count"]}')


    

if __name__=='__main__':
    main()
