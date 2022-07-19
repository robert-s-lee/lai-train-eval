Lift-and-shift existing training and inference scripts as Lightning App.
Lightning App is the one tool that can automate the research workflow and ML pipeline.
Complexity integrating many components can be simplified with Lighting App.

## Current State  
Lets assume we have existing scripts for training and inference.
Orchestration is typical linear workflow.
Many tools and manual typing results in complex and error prone process.

```mermaid
graph TD;
  U[ssh] -- login to a system --> T[Train with Lighting & Module Trainer];
  T -- scp lightning_log --> D[Diag with Tensorboard]; 
  D -- scp weights.py --> G[Deploy with Gradio];
  G -- scp inference errors --> T;
```

## Target State with Lightning App
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
## Data sharing across VMs are managed by Lightning App Drive

```mermaid
graph TD;
  T[Train]     <-- push, get --> LD[Lightning App Drive]
  I[Inference] <-- push, get --> LD
  D[Diag]]     <-- push, get --> LD
```

## Screenshots
![Train](./assets/../static/train.png)
![Deploy](./assets/../static/deploy.png)
![Diag](./assets/../static/diag.png)
![Inference](./assets/../static/inference.png)

## Explain the code