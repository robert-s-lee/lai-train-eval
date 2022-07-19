Lift-and-shift existing training and inference scripts as Lightning App.
Lightning App is the one tool that can automate the research workflow and ML pipeline.
Integrating many components each with it's own scripting tools take time and error pone.
Lighting App is pure Python. 
One language for all tasks.


## Test Locally and Scale in the Cloud

Develop locally on a single box and deploy on distributed on the cloud without any code change
  
- Develop and test locally
```bash
lightning app run app.py
```
- Deploy on the cloud

```bash
lightning app run app.py --cloud
```

## Lighting App is Composed of Lightning Flow(s) and Lightning Work(s)

On the cloud, there is one Lightning Flow VM and many Lightning Work VMs.  
Locally, Flow(s) and Work(s) run on a same VM.
Distributed state changes are serialized and managed by Lightning Flow.

```mermaid
graph TD;
  T[Train Lighting Work]      <-- state changes --> LF[Orchestrate Lightning Flow]
  I[Inference Lightning Work] <-- state changes --> LF
  D[Diag Lightning Work]      <-- state changes-->  LF
```

## Data sharing across VMs are managed by Lightning App Drive

```mermaid
graph TD;
  T[Train]     <-- push, get --> LD[Lightning App Drive]
  I[Inference] <-- push, get --> LD
  D[Diag]      <-- push, get --> LD
```

## Interactive workflow with Lightning App
Same existing scripts are wrapped in as a Lightning App.
Lighting Flow is used to codify orchestration in Python code.
Lighting Work is used to run the script in the cloud. 
Interactive workflow is enabled with Lightning App.

```mermaid
graph TD;
  L[Lightning App] --> U[UI with Streamlit]
  U -- start Training --> T[Train with Lighting & Module Trainer];
  U -- deploy model --> G[Deploy with Gradio];
  T -- Send lightning_log --> D[Diag with Tensorboard];
  T -- Send weights.py --> G;
  G -- Retrain --> T;
```

## Screenshots of Lighting App

- Enter Training Parameter
![Train](./assets/../static/train.png)
- Enter Model to Deploy
![Deploy](./assets/../static/deploy.png)
- Evaluate Training
![Diag](./assets/../static/diag.png)
- Inference on a Model
![Inference](./assets/../static/inference.png)
