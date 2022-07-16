import os
import lightning_app as L
from lit_bashwork import LitBashWork
from lightning.app.storage.drive import Drive
from lightning.app.utilities.state import AppState
from lightning_app.frontend import StreamlitFrontend
import streamlit as st

def select_model_ui(state:AppState):
  model_selection = st.text_input("select model", value=state.model_selection, placeholder=state.model_selection)
  model_button = st.button("submit model", disabled=state.model_start)
  if model_button:
    state.model_selection = model_selection
    state.model_start = True

def train_ui(state:AppState):
  train_args = st.text_area("train_args", value=state.train_args, placeholder=state.train_args)
  train_button = st.button("submit train", disabled=state.train_start)
  if train_button:
    state.train_args = train_args
    state.train_start = True

def app_ui(state:AppState):
  train_ui(state=state)
  select_model_ui(state=state)

class App_UI(L.LightningFlow):
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.train_args = '--trainer.max_epochs=1 --trainer.limit_train_batches=12 --trainer.limit_val_batches=4 --trainer.callbacks=ModelCheckpoint --trainer.callbacks.monitor=val_acc'
    self.train_start = False
    self.model_selection = ""
    self.model_start = False
  def configure_layout(self):
    return(StreamlitFrontend(render_fn=app_ui))

class My_Flow(L.LightningFlow):
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.app_drive = Drive("lit://drive")
    self.trainer = LitBashWork(drive_name="lit://drive")
    self.trainer_diag = LitBashWork(drive_name="lit://drive")
    self.eval_ui = LitBashWork(drive_name="lit://drive")
    self.app_ui = App_UI()

  def run(self, *args, **kwargs):
    self.trainer_diag.run("tensorboard --logdir lightning_logs --host {host} --port {port}", wait_for_exit=False)

    if self.app_ui.train_start:
      self.trainer.run(f"python train_script.py {self.app_ui.train_args}", outputs=['lightning_logs'])
      self.trainer_diag.run(f"python train_script.py {self.app_ui.train_args}", inputs=['lightning_logs'], input_output_only=True)

    if self.app_ui.model_start:
      self.eval_ui.run("python grmnist.py --host {host} --port {port}", wait_for_exit=False, inputs=['lightning_logs'])
      self.app_ui.model_start = False

  def configure_layout(self):
    app_ui = {"name": "App", "content": self.app_ui}
    train_diag = {"name": "Train Diag", "content": self.trainer_diag}
    eval_ui = {"name": "Eval", "content": self.eval_ui}
    return [app_ui, train_diag, eval_ui]
        
app = L.LightningApp(My_Flow())