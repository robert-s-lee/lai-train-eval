import os
import lightning_app as L
from lightning.app.storage.drive import Drive
from lightning.app.utilities.state import AppState
from lightning_app.components.serve import ServeGradio
import gradio as gr
from functools import partial

class LitGradio(ServeGradio):
    """ ServeGradio run() is blocking."""

    inputs = gr.inputs.Image(type="pil", shape=(28, 28))
    outputs = gr.outputs.Label(num_top_classes=10)

    def __init__(self, *args, drive_name, **kwargs):
      super().__init__(*args, **kwargs)
      self.drive = Drive(drive_name)
      self.start_gradio = True
      self.examples = None

    def get_from_drive(self,inputs):
      for i in inputs:
        print(f"drive get {i}")
        try:                     # file may not be ready 
          self.drive_lpa.get(i)  # Transfer the file from this drive to the local filesystem.
        except:
          pass  
        os.system(f"find {i} -print")

    def put_to_drive(self,outputs):
      for o in outputs:
        print(f"drive put {o}")
        # make sure dir end with / so that put works correctly
        if os.path.isdir(o):
          o = os.path.join(o,"")
        os.system(f"find {o} -print")
        self.drive_lpa.put(o)  

    def run_gradio(self, *args, **kwargs):
      if self._model is None:
          self._model = self.build_model()
      fn = partial(self.predict, *args, **kwargs)
      fn.__name__ = self.predict.__name__
      gr.Interface(fn=fn, inputs=self.inputs, outputs=self.outputs, examples=self.examples).launch(
          server_name=self.host,
          server_port=self.port,
          enable_queue=self.enable_queue,
          prevent_thread_lock=True,
      )    

    def run(self, start_gradio=True, inputs=[], outputs=[]):
      self.get_from_drive(inputs)
      if start_gradio:
        self.examples = [os.path.join(str("./images"), f) for f in os.listdir("./images")]
        self.run_gradio()
      self.put_to_drive(outputs) 

    def predict(self, input_text):
        return self.model(input_text)

    def build_model(self):
        fake_model = lambda x: f"hello {x}"
        return fake_model
