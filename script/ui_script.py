import streamlit as st

# ##################################################################################################
# UI 
def main_ui(state):
  """app's main menu with sidebar for various tasks"""
  # st page defaults
  st.set_page_config(
     page_title="Lighting App Demo",
     layout="wide",
     initial_sidebar_state="expanded",
  )
  # menu item
  page_names_to_func = {
    'About': about_ui,
    'Train': train_ui,
    'Deploy': select_model_ui,
  }
  page = st.sidebar.radio("Main Menu", options=page_names_to_func.keys())
  page_names_to_func[page](state)

def about_ui(state):
  st.markdown("""
  # Lightning is the "glue" layer of ML.
  - Build models.
  - Research Workflows.
  - Production Pipeline.

  # Wrap existing code to get started fast
  - Take the existing code
  - Wrap it with Lightning Work
  - Run it with Lightning Flow
  - Lightning App created.
  [![](https://mermaid.ink/img/eyJjb2RlIjoiZ3JhcGggUkw7XG4gIEFQKEFwcCA8YnI-PGJyPkxpZ2h0bmluZyA8YnI-QXBwKVxuICBzdWJncmFwaCBTdGF0ZSBUcmFuc2l0aW9uIHZpYSBFdmVudCBMb29wXG4gICAgTEYoKE9yY2hlc3RyYXRlIDxicj48YnI-TGlnaHRuaW5nIDxicj5GbG93KSlcbiAgICBMV1tSdW4gPGJyPjxicj5MaWdodG5pbmcgPGJyPldvcmtdXG4gICAgQVAgLS0gcnVuIC0tPiBMRlxuICAgIExGIC0tIHJ1biAtLT4gTFdcbiAgICBMVyAtLSBzdGF0ZSBjaGFuZ2VzIC0tPiBMRlxuICBlbmQgIFxuICBzdWJncmFwaCBleGlzdGluZyBzY3JpcHRzXG4gICAgU1tleGlzdGluZyAucHkgLnNoIC4uIGNvZGVdXG4gIGVuZFxuICBMVyAtLS0-IFNcbiIsIm1lcm1haWQiOnsidGhlbWUiOiJkZWZhdWx0In0sInVwZGF0ZUVkaXRvciI6ZmFsc2V9)](https://mermaid-js.github.io/docs/mermaid-live-editor-beta/#/edit/eyJjb2RlIjoiZ3JhcGggUkw7XG4gIEFQKEFwcCA8YnI-PGJyPkxpZ2h0bmluZyA8YnI-QXBwKVxuICBzdWJncmFwaCBTdGF0ZSBUcmFuc2l0aW9uIHZpYSBFdmVudCBMb29wXG4gICAgTEYoKE9yY2hlc3RyYXRlIDxicj48YnI-TGlnaHRuaW5nIDxicj5GbG93KSlcbiAgICBMV1tSdW4gPGJyPjxicj5MaWdodG5pbmcgPGJyPldvcmtdXG4gICAgQVAgLS0gcnVuIC0tPiBMRlxuICAgIExGIC0tIHJ1biAtLT4gTFdcbiAgICBMVyAtLSBzdGF0ZSBjaGFuZ2VzIC0tPiBMRlxuICBlbmQgIFxuICBzdWJncmFwaCBleGlzdGluZyBzY3JpcHRzXG4gICAgU1tleGlzdGluZyAucHkgLnNoIC4uIGNvZGVdXG4gIGVuZFxuICBMVyAtLS0-IFNcbiIsIm1lcm1haWQiOnsidGhlbWUiOiJkZWZhdWx0In0sInVwZGF0ZUVkaXRvciI6ZmFsc2V9)

  # Research Workflow:
  - Build MNIST models using Lighting Modules, DataLoaders, Trainer, CLI
  - Finetune workflows with Tensorboard, Gradio and Streamlit.
  - "Glue" all using Lightning Flow and Work.
  - Deploy Locally `lightning run app app.py`
[![](https://mermaid.ink/img/eyJjb2RlIjoiZ3JhcGggQlQ7XG4gIHN1YmdyYXBoIExvY2FsIFZNXG4gICAgTEYoKEFwcCA8YnI-PGJyPkxpZ2h0bmluZyA8YnI-RmxvdykpXG4gICAgVChUcmFpbiA8YnI-PGJyPkxpZ2h0aW5nIFdvcmspICAgICAgLS0gc3RhdGUgPGJyPmNoYW5nZXMgLS0-IExGXG4gICAgSShJbmZlcmVuY2UgPGJyPjxicj5MaWdodG5pbmcgV29yaykgLS0gc3RhdGUgPGJyPmNoYW5nZXMgLS0-IExGXG4gICAgRChEaWFnIDxicj48YnI-TGlnaHRuaW5nIFdvcmspICAgICAgLS0gc3RhdGUgPGJyPmNoYW5nZXMgLS0-IExGXG4gICAgVShVSSA8YnI-PGJyPkxpZ2h0bmluZyBGTG93KSAgICAgICAgLS0gc3RhdGUgPGJyPmNoYW5nZXMgLS0-IExGICBcbiAgICBMRiAtLSBydW4gLS0-IFRcbiAgICBMRiAtLSBydW4gLS0-IElcbiAgICBMRiAtLSBydW4gLS0-IEQgXG4gICAgTEYgLS0gcnVuIC0tPiBVIFxuICAgIHN1YmdyYXBoIGV4aXN0aW5nIHNjcmlwdHNcbiAgICAgIFRTW3RyYWluX3NjcmlwdC5weV1cbiAgICAgIElTW2dyYWRpb19zY3JpcHQucHldXG4gICAgICBEU1t0ZW5zb3Jib2FyZF1cbiAgICAgIFVTW3VpX3NjcmlwdC5weV1cbiAgICBlbmRcbiAgICBzdWJncmFwaCB3cmFwcGVyIGNvZGVcbiAgICAgIFQgLS0tPiBUU1xuICAgICAgSSAtLS0-IElTXG4gICAgICBEIC0tLT4gRFNcbiAgICAgIFUgLS0tPiBVUyAgXG4gICAgZW5kXG4gIGVuZCIsIm1lcm1haWQiOnsidGhlbWUiOiJkZWZhdWx0In0sInVwZGF0ZUVkaXRvciI6ZmFsc2V9)](https://mermaid-js.github.io/docs/mermaid-live-editor-beta/#/edit/eyJjb2RlIjoiZ3JhcGggQlQ7XG4gIHN1YmdyYXBoIExvY2FsIFZNXG4gICAgTEYoKEFwcCA8YnI-PGJyPkxpZ2h0bmluZyA8YnI-RmxvdykpXG4gICAgVChUcmFpbiA8YnI-PGJyPkxpZ2h0aW5nIFdvcmspICAgICAgLS0gc3RhdGUgPGJyPmNoYW5nZXMgLS0-IExGXG4gICAgSShJbmZlcmVuY2UgPGJyPjxicj5MaWdodG5pbmcgV29yaykgLS0gc3RhdGUgPGJyPmNoYW5nZXMgLS0-IExGXG4gICAgRChEaWFnIDxicj48YnI-TGlnaHRuaW5nIFdvcmspICAgICAgLS0gc3RhdGUgPGJyPmNoYW5nZXMgLS0-IExGXG4gICAgVShVSSA8YnI-PGJyPkxpZ2h0bmluZyBGTG93KSAgICAgICAgLS0gc3RhdGUgPGJyPmNoYW5nZXMgLS0-IExGICBcbiAgICBMRiAtLSBydW4gLS0-IFRcbiAgICBMRiAtLSBydW4gLS0-IElcbiAgICBMRiAtLSBydW4gLS0-IEQgXG4gICAgTEYgLS0gcnVuIC0tPiBVIFxuICAgIHN1YmdyYXBoIGV4aXN0aW5nIHNjcmlwdHNcbiAgICAgIFRTW3RyYWluX3NjcmlwdC5weV1cbiAgICAgIElTW2dyYWRpb19zY3JpcHQucHldXG4gICAgICBEU1t0ZW5zb3Jib2FyZF1cbiAgICAgIFVTW3VpX3NjcmlwdC5weV1cbiAgICBlbmRcbiAgICBzdWJncmFwaCB3cmFwcGVyIGNvZGVcbiAgICAgIFQgLS0tPiBUU1xuICAgICAgSSAtLS0-IElTXG4gICAgICBEIC0tLT4gRFNcbiAgICAgIFUgLS0tPiBVUyAgXG4gICAgZW5kXG4gIGVuZCIsIm1lcm1haWQiOnsidGhlbWUiOiJkZWZhdWx0In0sInVwZGF0ZUVkaXRvciI6ZmFsc2V9)

  # Production Pipeline:
  - Deploy on the Cloud `lightning run app app.py --cloud`
[![](https://mermaid.ink/img/eyJjb2RlIjoiZ3JhcGggVEQ7XG4gIHN1YmdyYXBoIENsb3VkXG4gIHN1YmdyYXBoIEZsb3cgVk0gLS0gQWx3YXlzIG9uZSBWTVxuICAgIExGKChPcmNoZXN0cmF0ZSA8YnI-PGJyPkxpZ2h0bmluZyBGbG93KSlcbiAgZW5kXG4gIHN1YmdyYXBoIFRyYWluIFZNc1xuICAgIFQoVHJhaW4gPGJyPjxicj5MaWdodGluZyBXb3JrKSAgICAgIDwtLSBzdGF0ZSBjaGFuZ2VzIC0tPiBMRlxuICAgIExGIC0tcnVuIC0tPiBUXG4gIGVuZFxuICBzdWJncmFwaCBJbmZlcmVuY2UgVk1zXG4gICAgSShJbmZlcmVuY2UgPGJyPjxicj5MaWdodG5pbmcgV29yaykgPC0tIHN0YXRlIGNoYW5nZXMgLS0-IExGXG4gICAgTEYgLS1ydW4gLS0-IElcbiAgZW5kXG4gIHN1YmdyYXBoIERpYWcgVk0gIFxuICAgIEQoRGlhZyA8YnI-PGJyPkxpZ2h0bmluZyBXb3JrKSAgICAgIDwtLSBzdGF0ZSBjaGFuZ2VzLS0-ICBMRlxuICAgIExGIC0tcnVuLS0-IERcbiAgZW5kXG4gIGVuZCIsIm1lcm1haWQiOnsidGhlbWUiOiJkZWZhdWx0In0sInVwZGF0ZUVkaXRvciI6ZmFsc2V9)](https://mermaid-js.github.io/docs/mermaid-live-editor-beta/#/edit/eyJjb2RlIjoiZ3JhcGggVEQ7XG4gIHN1YmdyYXBoIENsb3VkXG4gIHN1YmdyYXBoIEZsb3cgVk0gLS0gQWx3YXlzIG9uZSBWTVxuICAgIExGKChPcmNoZXN0cmF0ZSA8YnI-PGJyPkxpZ2h0bmluZyBGbG93KSlcbiAgZW5kXG4gIHN1YmdyYXBoIFRyYWluIFZNc1xuICAgIFQoVHJhaW4gPGJyPjxicj5MaWdodGluZyBXb3JrKSAgICAgIDwtLSBzdGF0ZSBjaGFuZ2VzIC0tPiBMRlxuICAgIExGIC0tcnVuIC0tPiBUXG4gIGVuZFxuICBzdWJncmFwaCBJbmZlcmVuY2UgVk1zXG4gICAgSShJbmZlcmVuY2UgPGJyPjxicj5MaWdodG5pbmcgV29yaykgPC0tIHN0YXRlIGNoYW5nZXMgLS0-IExGXG4gICAgTEYgLS1ydW4gLS0-IElcbiAgZW5kXG4gIHN1YmdyYXBoIERpYWcgVk0gIFxuICAgIEQoRGlhZyA8YnI-PGJyPkxpZ2h0bmluZyBXb3JrKSAgICAgIDwtLSBzdGF0ZSBjaGFuZ2VzLS0-ICBMRlxuICAgIExGIC0tcnVuLS0-IERcbiAgZW5kXG4gIGVuZCIsIm1lcm1haWQiOnsidGhlbWUiOiJkZWZhdWx0In0sInVwZGF0ZUVkaXRvciI6ZmFsc2V9)

  # Source Code:
  - [Source Code](https://github.com/robert-s-lee/lai-train-eval)
  """)  


def select_model_ui(state):
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
    st.info("""Please go to Eval tab to use the model""")  

  st.info("""The Eval Tab may show `Gateway Error` while the old model is being replaced with the new model.
    Please wait couple of seconds and refresh the page""")

def train_ui(state):
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

if __name__ == "__main__":
  from dotmap import DotMap
  state = DotMap()
  state.train_args = '--trainer.max_epochs=1 --trainer.limit_train_batches=12 --trainer.limit_val_batches=4 --trainer.callbacks=ModelCheckpoint --trainer.callbacks.monitor=val_acc'
  state.train_start = False
  # the menu will be populated by after each training
  state.model_selection_options = []
  # deploy version_0 included with the app when the app starts
  state.model_selection = "base"
  state.model_start = True
  main_ui(state)