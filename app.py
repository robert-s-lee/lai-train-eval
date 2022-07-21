import os
import lightning_app as L
from lit_bashwork import LitBashWork
from lightning.app.storage.drive import Drive
from lightning.app.utilities.state import AppState
from lightning_app.frontend import StreamlitFrontend
import streamlit as st
from  script import ui_script

# command to list modesl that have example.pt for deployment
weights_lightning_logs = """find lightning_logs -name example.pt -type f -maxdepth 2 | xargs -n1 dirname | xargs -n1 basename"""

# UI state
class App_UI(L.LightningFlow):
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    # start training when the app start
    self.train_args = '--trainer.max_epochs=1 --trainer.limit_train_batches=12 --trainer.limit_val_batches=4 --trainer.callbacks=ModelCheckpoint --trainer.callbacks.monitor=val_acc'
    self.train_start = False
    # the menu will be populated by after each training
    self.model_selection_options = []
    # deploy version_0 included with the app when the app starts
    self.model_selection = "base"
    self.model_start = True
  def configure_layout(self):
    return(StreamlitFrontend(render_fn=ui_script.main_ui))

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

    # Run Gradio  Not caching so that model can be redeployed for A/B  
    self.eval_ui = LitBashWork(drive_name="lit://drive", cache_calls=False,
      cloud_build_config=L.BuildConfig(["jsonargparse[signatures]","gradio", "torchvision"])
    )

  def run(self, *args, **kwargs):
    # one time activity
    # 1. start the tensorboard one time
    self.trainer_diag.run("tensorboard --logdir lightning_logs --host $host --port $port", wait_for_exit=False)

    # 2. pull available models from trainer and initialize the  UI
    self.trainer.run(weights_lightning_logs, save_stdout=True)
    if self.trainer.last_args() == weights_lightning_logs:
      # the output is saved in array and don't expect to be very long
      self.app_ui.model_selection_options = self.trainer.last_stdout() 
      # once saved, don't fall back in here
      self.trainer.reset_last_args()  

    if self.app_ui.model_start:
      # 1. indicate the model to use
      cmd = "python script/gradio_script.py --host $host --port $port --model_path lightning_logs/%s/example.pt" % (self.app_ui.model_selection)
      # 2. (re)start the prediction with model selected
      if self.eval_ui.last_args() != cmd:
        self.eval_ui.run(cmd, wait_for_exit=False, kill_pid=True, 
          inputs=['lightning_logs'])  
      # 3. unlock the UI 
      self.app_ui.model_start = False

    if self.app_ui.train_start:
      # 1. start the training
      # the saved_after_run can be hidden by subclassing, but exposing the work to flow hack for now
      cmd = f"python script/train_script.py {self.app_ui.train_args}"
      self.trainer.run(cmd, 
        run_after_run = [weights_lightning_logs],
        outputs=['lightning_logs'])

      # 2. pull the output 
      if self.trainer.last_args() == cmd:
        self.app_ui.model_selection_options = self.trainer.last_stdout()  # already an array
        self.trainer.reset_last_args()  # don't come back here again

      # 3. pull the new tensorboard logs from the trainer
      self.trainer_diag.run(cmd, 
        inputs=['lightning_logs'], input_output_only=True)

      # 4. unlock the UI
      self.app_ui.train_start = False

  def configure_layout(self):
    app_ui = {"name": "App", "content": self.app_ui}
    train_diag = {"name": "Train Diag", "content": self.trainer_diag}
    eval_ui = {"name": "Eval", "content": self.eval_ui}
    return [app_ui, train_diag, eval_ui]
        
app = L.LightningApp(My_Flow())
