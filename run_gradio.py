import os
import lightning_app as L
from lai_bashwork.bashwork import LitBashWork
from lightning.app.storage.drive import Drive
from lightning.app.utilities.state import AppState
from lightning_app.components.serve import ServeGradio
import gradio as gr
from functools import partial
import torch
import torchvision.transforms as T

class LitGradio(LitBashWork):
    """ ServeGradio run() is blocking."""


    grtransform = T.Compose([T.Resize((28, 28)), T.ToTensor()])

    def __init__(self, *args, drive_name, **kwargs):
      super().__init__(*args, **kwargs)
      self.drive = Drive(drive_name)
      self.start_gradio = True
      self.examples = None
      self.labels = {idx: str(idx) for idx in range(10)}
      # variable starting with _ is not saved.  so it can be more complex type
      self._model = None
      self.enable_queue = False

    def run_gradio(self, *args, **kwargs):
      inputs = gr.inputs.Image(type="pil", shape=(28, 28))
      outputs = gr.outputs.Label(num_top_classes=10)
      if self._model is None:
          self._model = self.build_model()
      fn = partial(self.predict, *args, **kwargs)
      fn.__name__ = self.predict.__name__
      gr.Interface(fn=fn, inputs=inputs, outputs=outputs, examples=self.examples).launch(
          server_name=self.host,
          server_port=self.port,
          enable_queue=self.enable_queue,
          prevent_thread_lock=True,
      )    

    def run(self, start_gradio=True, restart_gradio=False, inputs=[], outputs=[]):
      self.get_from_drive(inputs)
      if start_gradio:
        self.examples = [os.path.join(str("./images"), f) for f in os.listdir("./images")]
        self.run_gradio()
      self.put_to_drive(outputs) 

    def predict(self, img):
      # 1. Receive an image and transform it into a tensor
      imgs = self.grtransform(img)
      img = imgs[0]
      img = img.unsqueeze(0).unsqueeze(0)

      # 2. Apply the model on the image and convert the logits into probabilities
      prediction = torch.exp(self._model(img))

      # 3. Return the data in the `gr.outputs.Label` format
      return {self.labels[i]: prediction[0][i].item() for i in range(10)}

    def build_model(self, best_model_path="./example.pt"):
        model = torch.jit.load(best_model_path)
        model.eval()
        return model
