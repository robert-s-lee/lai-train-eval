import os.path as ops
import lightning_app as L
from lai_bashwork.bashwork import LitBashWork
from lightning_app.frontend import StreamlitFrontend
from lightning_app.components.serve import ServeGradio
import streamlit as st
from lightning_app.components.serve import ServeGradio
import gradio as gr

class LitGradio(ServeGradio):
    inputs = gr.inputs.Textbox(default='lightning', label='name input')
    outputs = gr.outputs.Textbox(label='output')
    examples = [["hello lightning"]]

    def predict(self, input_text):
        return self.model(input_text)

    def build_model(self):
        fake_model = lambda x: f"hello {x}"
        return fake_model

def train_ui(state):
  train_args = st.text_input("train_args", value=state.train_args, placeholder=state.train_args)
  train_button = st.button("submit", disabled=state.train_start)
  if train_button:
    state.train_args = train_args
    state.train_start = True

class Train_UI(L.LightningFlow):
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.train_args = "--trainer.max_epochs=1"
    self.train_start = False
  def configure_layout(self):
    return(StreamlitFrontend(render_fn=train_ui))

class My_Flow(L.LightningFlow):
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.trainer = LitBashWork()
    self.trainer_param = Train_UI()
    self.trainer_diag = LitBashWork(parallel=True)
    self.eval_param = LitGradio()

  def run(self, *args, **kwargs):
    self.eval_param.run()
    self.trainer_diag.run("tensorboard --logdir lightning_logs --host {host} --port {port}")
    self.eval_param.run()
    if self.trainer_param.train_start:
      self.trainer.run(f"python train_script.py {self.trainer_param.train_args}")
      self.trainer_param.train_start = False

  def configure_layout(self):
    train_param = {"name": "Train Param", "content": self.trainer_param}
    train_diag = {"name": "Train Diag", "content": self.trainer_diag}
    eval_param = {"name": "Eval Param", "content": self.eval_param}
    eval_ui = {"name": "Eval", "content": self.eval_param}
    return [train_param, train_diag, eval_ui]
        
app = L.LightningApp(My_Flow())