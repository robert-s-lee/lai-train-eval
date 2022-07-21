import os
import lightning_app as L
from lit_bashwork import LitBashWork
from lightning.app.storage.drive import Drive
from lightning.app.utilities.state import AppState
from lightning_app.frontend import StreamlitFrontend
import streamlit as st

# command to list modesl that have example.pt for deployment
weights_lightning_logs = """find lightning_logs -name example.pt -type f -maxdepth 2 | xargs -n1 dirname | xargs -n1 basename"""

# ##################################################################################################
# UI 
def main_ui(state:AppState):
  """app's main menu with sidebar for various tasks"""
  st.set_page_config(
     page_title="Lighting App Demo",
     layout="wide",
     initial_sidebar_state="expanded",
  )
  page_names_to_func = {
    'About': about_ui,
    'Train': train_ui,
    'Deploy': select_model_ui,
  }
  page = st.sidebar.selectbox("Main Menu", options=page_names_to_func.keys())
  page_names_to_func[page](state)

def about_ui(state:AppState):
  st.markdown("""
  # Lightning is the "glue" layer of ML.
  - Build models.
  - Research Workflows.
  - Production Pipeline.

  # Research Workflow:
  - Build MNIST models using Lighting Modules, DataLoaders, Trainer, CLI
  - Finetune workflows with Tensorboard, Gradio and Streamlit.
  - "Glue" all using Lightning Flow and Work.
  - Deploy the resulting Lightning App locally or the Cloud.

  # Production Pipeline:
  - [Source Code](https://github.com/robert-s-lee/lai-train-eval)

  - Deploy Locally `lightning run app app.py`

  [![](https://mermaid.ink/img/eyJjb2RlIjoiZ3JhcGggVEQ7XG4gIHN1YmdyYXBoIExvY2FsIFZNXG4gICAgTEYoKEFwcCA8YnI-PGJyPkxpZ2h0bmluZyA8YnI-RmxvdykpXG4gICAgVChUcmFpbiA8YnI-PGJyPkxpZ2h0aW5nIFdvcmspICAgICAgLS0gc3RhdGUgPGJyPmNoYW5nZXMgLS0-IExGXG4gICAgSShJbmZlcmVuY2UgPGJyPjxicj5MaWdodG5pbmcgV29yaykgLS0gc3RhdGUgPGJyPmNoYW5nZXMgLS0-IExGXG4gICAgRChEaWFnIDxicj48YnI-TGlnaHRuaW5nIFdvcmspICAgICAgLS0gc3RhdGUgPGJyPmNoYW5nZXMgLS0-ICBMRlxuICAgIExGIC0tIHJ1biAtLT4gVFxuICAgIExGIC0tIHJ1biAtLT4gSVxuICAgIExGIC0tIHJ1biAtLT4gRCBcbiAgICBUIC0tIGV4aXN0aW5nIHNjcmlwdCAtLT4gVFNbdHJhaW5fc2NyaXB0LnB5XVxuICAgIEkgLS0gZXhpc3Rpbmcgc2NyaXB0IC0tPiBJU1tncmFkaW9fc2NyaXB0LnB5XVxuICAgIEQgLS0gc2hlbGwgY29tbWFuZCAtLT4gICBEU1t0ZW5zb3Jib2FyZF1cbiAgZW5kIiwibWVybWFpZCI6eyJ0aGVtZSI6ImRlZmF1bHQifSwidXBkYXRlRWRpdG9yIjpmYWxzZX0)](https://mermaid-js.github.io/docs/mermaid-live-editor-beta/#/edit/eyJjb2RlIjoiZ3JhcGggVEQ7XG4gIHN1YmdyYXBoIExvY2FsIFZNXG4gICAgTEYoKEFwcCA8YnI-PGJyPkxpZ2h0bmluZyA8YnI-RmxvdykpXG4gICAgVChUcmFpbiA8YnI-PGJyPkxpZ2h0aW5nIFdvcmspICAgICAgLS0gc3RhdGUgPGJyPmNoYW5nZXMgLS0-IExGXG4gICAgSShJbmZlcmVuY2UgPGJyPjxicj5MaWdodG5pbmcgV29yaykgLS0gc3RhdGUgPGJyPmNoYW5nZXMgLS0-IExGXG4gICAgRChEaWFnIDxicj48YnI-TGlnaHRuaW5nIFdvcmspICAgICAgLS0gc3RhdGUgPGJyPmNoYW5nZXMgLS0-ICBMRlxuICAgIExGIC0tIHJ1biAtLT4gVFxuICAgIExGIC0tIHJ1biAtLT4gSVxuICAgIExGIC0tIHJ1biAtLT4gRCBcbiAgICBUIC0tIGV4aXN0aW5nIHNjcmlwdCAtLT4gVFNbdHJhaW5fc2NyaXB0LnB5XVxuICAgIEkgLS0gZXhpc3Rpbmcgc2NyaXB0IC0tPiBJU1tncmFkaW9fc2NyaXB0LnB5XVxuICAgIEQgLS0gc2hlbGwgY29tbWFuZCAtLT4gICBEU1t0ZW5zb3Jib2FyZF1cbiAgZW5kIiwibWVybWFpZCI6eyJ0aGVtZSI6ImRlZmF1bHQifSwidXBkYXRlRWRpdG9yIjpmYWxzZX0)

  - Deploy on the Cloud `lightning run app app.py --cloud`
  [![](https://mermaid.ink/img/eyJjb2RlIjoiZ3JhcGggVEQ7XG4gIHN1YmdyYXBoIENsb3VkXG4gIHN1YmdyYXBoIEZsb3cgVk0gLS0gQWx3YXlzIG9uZSBWTVxuICAgIExGKChPcmNoZXN0cmF0ZSA8YnI-PGJyPkxpZ2h0bmluZyBGbG93KSlcbiAgZW5kXG4gIHN1YmdyYXBoIFRyYWluIFZNc1xuICAgIFQoVHJhaW4gPGJyPjxicj5MaWdodGluZyBXb3JrKSAgICAgIDwtLSBzdGF0ZSBjaGFuZ2VzIC0tPiBMRlxuICAgIExGIC0tcnVuIC0tPiBUXG4gIGVuZFxuICBzdWJncmFwaCBJbmZlcmVuY2UgVk1zXG4gICAgSShJbmZlcmVuY2UgPGJyPjxicj5MaWdodG5pbmcgV29yaykgPC0tIHN0YXRlIGNoYW5nZXMgLS0-IExGXG4gICAgTEYgLS1ydW4gLS0-IElcbiAgZW5kXG4gIHN1YmdyYXBoIERpYWcgVk0gIFxuICAgIEQoRGlhZyA8YnI-PGJyPkxpZ2h0bmluZyBXb3JrKSAgICAgIDwtLSBzdGF0ZSBjaGFuZ2VzLS0-ICBMRlxuICAgIExGIC0tcnVuLS0-IERcbiAgZW5kXG4gIGVuZCIsIm1lcm1haWQiOnsidGhlbWUiOiJkZWZhdWx0In0sInVwZGF0ZUVkaXRvciI6ZmFsc2V9)](https://mermaid-js.github.io/docs/mermaid-live-editor-beta/#/edit/eyJjb2RlIjoiZ3JhcGggVEQ7XG4gIHN1YmdyYXBoIENsb3VkXG4gIHN1YmdyYXBoIEZsb3cgVk0gLS0gQWx3YXlzIG9uZSBWTVxuICAgIExGKChPcmNoZXN0cmF0ZSA8YnI-PGJyPkxpZ2h0bmluZyBGbG93KSlcbiAgZW5kXG4gIHN1YmdyYXBoIFRyYWluIFZNc1xuICAgIFQoVHJhaW4gPGJyPjxicj5MaWdodGluZyBXb3JrKSAgICAgIDwtLSBzdGF0ZSBjaGFuZ2VzIC0tPiBMRlxuICAgIExGIC0tcnVuIC0tPiBUXG4gIGVuZFxuICBzdWJncmFwaCBJbmZlcmVuY2UgVk1zXG4gICAgSShJbmZlcmVuY2UgPGJyPjxicj5MaWdodG5pbmcgV29yaykgPC0tIHN0YXRlIGNoYW5nZXMgLS0-IExGXG4gICAgTEYgLS1ydW4gLS0-IElcbiAgZW5kXG4gIHN1YmdyYXBoIERpYWcgVk0gIFxuICAgIEQoRGlhZyA8YnI-PGJyPkxpZ2h0bmluZyBXb3JrKSAgICAgIDwtLSBzdGF0ZSBjaGFuZ2VzLS0-ICBMRlxuICAgIExGIC0tcnVuLS0-IERcbiAgZW5kXG4gIGVuZCIsIm1lcm1haWQiOnsidGhlbWUiOiJkZWZhdWx0In0sInVwZGF0ZUVkaXRvciI6ZmFsc2V9)
  """)  


def select_model_ui(state:AppState):
  """select model to deploy"""
  # current model is the default (default to 0 when Work is not up yet)
  try:
    index=state.model_selection_options.index(state.model_selection)
  except:
    index=0
  # show the options
  model_selection = st.selectbox("Select Model", 
    options=state.model_selection_options, 
    index=index,
    disabled=state.model_start)
  model_button = st.button("Deploy Model", disabled=state.model_start)
  # process the submit
  if model_selection != "" and model_button:
    state.model_selection = model_selection
    state.model_start = True
  # after screenlock, show the next step
  if state.model_start:
    st.info("Please go to Eval tab to use the model")

def train_ui(state:AppState):
  """enter parameters for training"""
  train_args = st.text_area("Train Arguments", 
    value=state.train_args, placeholder=state.train_args, disabled=state.train_start)
  train_button = st.button("Start Training", disabled=state.train_start)
  # process the submit
  if train_button:
    state.train_args = train_args
    state.train_start = True
  # after screenlock, show the next step
  if state.train_start:
    st.info("Please go to Train Diag tab to evalute the training")

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
      cmd = "python gradio_script.py --host $host --port $port --model_path lightning_logs/%s/example.pt" % (self.app_ui.model_selection)
      # 2. (re)start the prediction with model selected
      if self.eval_ui.last_args() != cmd:
        self.eval_ui.run(cmd, wait_for_exit=False, kill_pid=True, 
          inputs=['lightning_logs'])  
      # 3. unlock the UI 
      self.app_ui.model_start = False

    if self.app_ui.train_start:
      # 1. start the training
      # the saved_after_run can be hidden by subclassing, but exposing the work to flow hack for now
      cmd = f"python train_script.py {self.app_ui.train_args}"
      self.trainer.run(f"python train_script.py {self.app_ui.train_args}", 
        run_after_run = [weights_lightning_logs],
        outputs=['lightning_logs'])

      # 2. pull the output 
      if self.trainer.last_args() == cmd:
        self.app_ui.model_selection_options = self.trainer.last_stdout()  # already an array
        self.trainer.reset_last_args()  # don't come back here again

      # 3. pull the new tensorboard logs from the trainer
      self.trainer_diag.run(f"python train_script.py {self.app_ui.train_args}", 
        inputs=['lightning_logs'], input_output_only=True)

      # 4. unlock the UI
      self.app_ui.train_start = False

  def configure_layout(self):
    app_ui = {"name": "App", "content": self.app_ui}
    train_diag = {"name": "Train Diag", "content": self.trainer_diag}
    eval_ui = {"name": "Eval", "content": self.eval_ui}
    return [app_ui, train_diag, eval_ui]
        
app = L.LightningApp(My_Flow())
