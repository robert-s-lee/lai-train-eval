import os.path as ops
import lightning_app as L
from lai_bashwork.bashwork import LitBashWork

class My_Flow(L.LightningFlow):
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.trainer = LitBashWork()

  def run(self, *args, **kwargs):
    self.trainer.run("python train_script.py --trainer.max_epochs=1")

app = L.LightningApp(My_Flow())