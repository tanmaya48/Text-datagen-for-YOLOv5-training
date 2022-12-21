import numpy as np
import cv2

letters:str = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'



def resize_image(image,min_ratio=0.3,max_ratio=1):
    scale_ratio = np.random.uniform(min_ratio,max_ratio) # percent of original size
    width = int(image.shape[1] * scale_ratio)
    height = int(image.shape[0] * scale_ratio)
    dim = (width, height)
    
    # resize image
    image = cv2.resize(image, dim, interpolation = cv2.INTER_AREA)
    return image


def get_random_string(word_length=4) -> str:
    word:str = ''
    for index in range(word_length):
        letter_index = np.random.randint(len(letters))
        word = word + letters[letter_index]
    return word



def random_color():
    color = np.random.randint(low=0,high=255,size=3).tolist()
    color.append(255)
    return color
    
    





def create_text_image(text:str='word') -> np.array:
    text_image: np.array = np.zeros((500,500,4),np.uint8)
    cv2.putText(text_image,text,(10,70),cv2.FONT_HERSHEY_SIMPLEX,3,random_color(),thickness=4)
    return text_image




def crop_image(image:np.array, pad:int = 3):
    coords = cv2.findNonZero(image[:,:,3])
    x,y,w,h = cv2.boundingRect(coords)

    return image[y-3:y+h+3,x-3:x+w+3,:]










def main():
    text = get_random_string()
    text_image = create_text_image(text)
    cv2.imwrite('text_image.png',crop_image(text_image))
    

if __name__ == '__main__':
    main()
