import os.path as ops
import lightning_app as L
from lai_bashwork.bashwork import LitBashWork
from lightning_app.frontend import StreamlitFrontend
from lightning.app.utilities.state import AppState
import streamlit as st

def select_model_ui(state:AppState):
  model_args = st.text_input("select model", value=state.model_selection, placeholder=state.model_selection)
  model_button = st.button("submit model", disabled=state.model_start)
  if model_button:
    state.model_args = model_args
    state.model_button = True

def train_ui(state:AppState):
  train_args = st.text_input("train_args", value=state.train_args, placeholder=state.train_args)
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
    self.train_args = "--trainer.max_epochs=1"
    self.train_start = False
    self.model_selection = ""
    self.model_start = False
  def configure_layout(self):
    return(StreamlitFrontend(render_fn=app_ui))

class My_Flow(L.LightningFlow):
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.trainer = LitBashWork()
    self.app_ui = App_UI()
    self.trainer_diag = LitBashWork(parallel=True)

  def run(self, *args, **kwargs):
    self.trainer_diag.run("tensorboard --logdir lightning_logs --host {host} --port {port}")
    if self.app_ui.train_start:
      self.trainer.run(f"python train_script.py {self.app_ui.train_args}")
      self.app_ui.train_start = False

  def configure_layout(self):
    train_ui = {"name": "App", "content": self.app_ui}
    train_diag = {"name": "Train Diag", "content": self.trainer_diag}
    return [train_ui, train_diag]
        
app = L.LightningApp(My_Flow())