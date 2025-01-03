from taipy.gui import Gui
from tensorflow.keras import models
from PIL import Image
import numpy as np

class_names = {
    0: 'airplane',
    1: 'automobile',
    2: 'bird',
    3: 'cat',
    4: 'deer',
    5: 'dog',
    6: 'frog',
    7: 'horse',
    8: 'ship',
    9: 'truck',
}

model = models.load_model("baseline.keras")

def predict_image(model, path_to_img):
    img = Image.open(path_to_img)
    img = img.convert("RGB")
    img = img.resize((32, 32))
    data = np.asarray(img) # in tensor form now
    
    #process to normalize image
    

    
    data = data / 255

    probs = model.predict(np.array([data])[:1])

    top_prob = probs.max()
    top_pred = class_names[np.argmax(probs)]
    
    return top_prob, top_pred
    
    
    
    
img_path = "placeholder_image.png" 
prob = 0
pred = ""
content = ""

index = """
<|text-center|
<|{"logo.png"}|image|width=25vw|>

<|{content}|file_selector|extensions = .png|>
Select and Image from your file 
system

<|{img_path}|image|> 

<|{pred}|>

<|{prob}|indicator|value = {prob}|min = 0|max = 100|width=25vw|> 
>
 """

def on_change(state, var_name, var_val):
    if var_name == "content":
        state.img_path = var_val
        top_prob, top_pred = predict_image(model, var_val)
        state.prob = round(top_prob * 100)
        article = "a "
        if top_pred[0] in set(['a','e','o','u','i']):
            article = "an "
        
        state.pred = "this is " + article + top_pred
        state.img_path = var_val
#    print(var_name, var_val)

app = Gui(page = index)
if __name__ == "__main__":
    app.run(use_reloader=True, port = 5001)