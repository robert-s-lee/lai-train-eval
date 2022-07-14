import os.path as ops
import lightning_app as L
from lai_bashwork.bashwork import LitBashWork
from lightning_app.frontend import StreamlitFrontend
from lightning.app.utilities.state import AppState
import streamlit as st

def train_ui(state:AppState):
  train_args = st.text_input("train_args", value=state.train_args, placeholder=state.train_args)
  train_button = st.button("submit", disabled=state.train_start)
  if train_button:
    state.train_args = train_args
    state.train_start = True

def app_ui(state:AppState):
  train_ui(state=state)

class App_UI(L.LightningFlow):
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.train_args = "--trainer.max_epochs=1"
    self.train_start = False
  def configure_layout(self):
    return(StreamlitFrontend(render_fn=app_ui))

class My_Flow(L.LightningFlow):
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.trainer = LitBashWork()
    self.app_ui = App_UI()
  def run(self, *args, **kwargs):
    if self.app_ui.train_start:
      self.trainer.run(f"python train_script.py {self.app_ui.train_args}")
      self.app_ui.train_start = False

app = L.LightningApp(My_Flow())