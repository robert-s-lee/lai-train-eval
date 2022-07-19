import os
import lightning_app as L
from lit_bashwork import LitBashWork
from lightning.app.storage.drive import Drive
from lightning.app.utilities.state import AppState
from lightning_app.frontend import StreamlitFrontend
import streamlit as st

# ##################################################################################################
# UI 
def main_ui(state:AppState):
  page_names_to_func = {
    'Train': train_ui,
    'Deploy': select_model_ui,
  }
  page = st.sidebar.selectbox("Main Menu", options=page_names_to_func.keys())
  page_names_to_func[page](state)
  
def select_model_ui(state:AppState):
  model_selection = st.text_input("Select Model", 
    value=state.model_selection, placeholder=state.model_selection, disabled=state.model_start)
  model_button = st.button("Deploy Model", disabled=state.model_start)
  if model_button:
    state.model_selection = model_selection
    state.model_start = True
  if state.model_start:
    st.info("Please go to Eval tab to use the model")

def train_ui(state:AppState):
  train_args = st.text_area("Train Arguments", 
    value=state.train_args, placeholder=state.train_args, disabled=state.train_start)
  train_button = st.button("Start Training", disabled=state.train_start)
  if train_button:
    state.train_args = train_args
    state.train_start = True
  if state.train_start:
    st.info("Please go to Train Diag tab to evalute the training")

# UI state
class App_UI(L.LightningFlow):
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    # start training when the app start
    self.train_args = '--trainer.max_epochs=1 --trainer.limit_train_batches=12 --trainer.limit_val_batches=4 --trainer.callbacks=ModelCheckpoint --trainer.callbacks.monitor=val_acc'
    self.train_start = True
    # deploy version_0 included with the app when the app starts
    self.model_selection = "version_0"
    self.model_start = True
  def configure_layout(self):
    return(StreamlitFrontend(render_fn=main_ui))

# ##################################################################################################
# Main App
class My_Flow(L.LightningFlow):
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)

    self.app_drive = Drive("lit://drive")
    self.app_ui = App_UI()

    # Run Training with Lightning Modules and Trainer
    self.trainer = LitBashWork(drive_name="lit://drive",
      cloud_build_config=L.BuildConfig(["jsonargparse[signatures]", "pytorch-lightning","torchvision"]))

    # Run Tensorboard
    self.trainer_diag = LitBashWork(drive_name="lit://drive", parallel=True,
      cloud_build_config=L.BuildConfig(["tensorflow", "tensorboard", "setuptools==59.5.0"]))

    # Run Gradio  
    self.eval_ui = LitBashWork(drive_name="lit://drive",
      cloud_build_config=L.BuildConfig(["jsonargparse[signatures]","gradio", "torchvision"])
    )

  def run(self, *args, **kwargs):
    self.trainer_diag.run("tensorboard --logdir lightning_logs --host {host} --port {port}", wait_for_exit=False)

    if self.app_ui.model_start:
      # 1. indicate the model to use
      cmd = "python grmnist.py --host {host} --port {port} --model_path lightning_logs/%s/example.pt" % (self.app_ui.model_selection)
      
      # 2. (re)start the prediction with model selected
      self.eval_ui.run(cmd, wait_for_exit=False, kill_pid=True, 
        inputs=['lightning_logs'])
      
      # 3. unlock the UI 
      self.app_ui.model_start = False

    if self.app_ui.train_start:
      # 1. start the training
      self.trainer.run(f"python train_script.py {self.app_ui.train_args}", 
        outputs=['lightning_logs'])

      # 2. pull the new tensorboard logs from the trainer
      self.trainer_diag.run(f"python train_script.py {self.app_ui.train_args}", 
        inputs=['lightning_logs'], input_output_only=True)

      # 3. unlock the UI
      self.app_ui.train_start = False

  def configure_layout(self):
    app_ui = {"name": "App", "content": self.app_ui}
    train_diag = {"name": "Train Diag", "content": self.trainer_diag}
    eval_ui = {"name": "Eval", "content": self.eval_ui}
    return [app_ui, train_diag, eval_ui]
        
app = L.LightningApp(My_Flow())
