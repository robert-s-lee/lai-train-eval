from pathlib import Path
import gradio as gr
import torch
import torchvision.transforms as T
from jsonargparse import CLI

transform = T.Compose([T.Resize((28, 28)), T.ToTensor()])
labels = {idx: str(idx) for idx in range(10)}
model = None

def build_model(model_path="../example.pt"):
    global model
    model = torch.jit.load(model_path)
    model.eval()

def predict(img):
    # 1. Receive an image and transform it into a tensor
    imgs = transform(img)
    img = imgs[0]
    img = img.unsqueeze(0).unsqueeze(0)

    # 2. Apply the model on the image and convert the logits into probabilities
    prediction = torch.exp(model(img))

    # 3. Return the data in the `gr.outputs.Label` format
    return {labels[i]: prediction[0][i].item() for i in range(10)}

def greet(name):
    return "Hello " + name + "!!"

def run(
  model_path="lightning_logs/version_0/example.pt", 
  image_dir="./images",
  host:str=None,
  port:int=None,
  ):
  """Run gradio
    Args:
        model_path: Path to model.pt file.
        image_dir: Dir with examples images.  
  """ 
  inputs = gr.inputs.Image(type="pil", shape=(28, 28))
  outputs = gr.outputs.Label(num_top_classes=10)
  # does not take ../images nor absolute path
  examples = [str(x) for x in Path(image_dir).rglob("*")]
  build_model(model_path=model_path)

  demo = gr.Interface(fn=predict, inputs=inputs, outputs=outputs, examples=examples)
  demo.launch(server_name=host, server_port=port)

if __name__ == "__main__":
  CLI(run)  