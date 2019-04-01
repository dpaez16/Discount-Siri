import cv2

def gen_trash_meme(image):
	trash_template = cv2.imread('./trash_template.jpg')
	trash_person = cv2.imread(image)
	height, width = trash_template.shape[:2]
	height_, width_ = int(height/2), int(width/2)
	resized_trash_person = cv2.resize(trash_person, (height_, width_), interpolation=cv2.INTER_NEAREST)
	
	trash_template[:height_, width_:, :] = resized_trash_person
	cv2.imwrite("./trash_meme_output.jpg", trash_template)