Lightning App automate the research workflow and production pipeline.
Lightning App is composed of Lightning Work and Lightning Flow.
Wrap existing scripts as Lightning Works.
Exchange data among Lightning Works with Lightning Drives.
Lightning Works send state information to Lighting Flows.
Lightning Flows send run command to Lightning Works.
Distributed states and runs are serialized via event loops in Lightning Flows.

Integrating many components each with it's own scripting tools take time and error pone.
Lighting App is pure Python. 
One language for all tasks.


## Develop Locally and Scale in the Cloud

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

Distributed state changes are serialized and managed by Lightning Flow.  
Lightning Flow then uses `run` to execute tasks.

Locally, Flow(s) and Work(s) run on a same VM.
The diagram below shows state changes.
The runs are omitted from this diagram.

```mermaid
graph TD;
  subgraph Local VM
    LF((App <br><br>Lightning <br>Flow))
    T(Train <br><br>Lighting Work)      -- state <br>changes --> LF
    I(Inference <br><br>Lightning Work) -- state <br>changes --> LF
    D(Diag <br><br>Lightning Work)      -- state <br>changes -->  LF
    LF -- run --> T
    LF -- run --> I
    LF -- run --> D 
    T -- existing script --> TS[train_script.py]
    I -- existing script --> IS[gradio_script.py]
    D -- shell command -->   DS[tensorboard]
  end
```

On the cloud, there is one Lightning Flow VM and many Lightning Work VMs.  
The diagram below shows run and state changes.

```mermaid
graph TD;
  subgraph Cloud
  subgraph Flow VM -- Always one VM
    LF((Orchestrate <br><br>Lightning Flow))
  end
  subgraph Train VMs
    T(Train <br><br>Lighting Work)      <-- state changes --> LF
    LF --run --> T
  end
  subgraph Inference VMs
    I(Inference <br><br>Lightning Work) <-- state changes --> LF
    LF --run --> I
  end
  subgraph Diag VM  
    D(Diag <br><br>Lightning Work)      <-- state changes-->  LF
    LF --run--> D
  end
  end
```

## Data sharing across VMs are managed by Lightning App Drive

Lightning App Drive is available among Lightning Works.
Train, Inference, Diag can share files.

```mermaid
graph TD;
  LD[Lightning App Drive]
  T[Train]     <-- push, get --> LD 
  I[Inference] <-- push, get --> LD
  D[Diag]      <-- push, get --> LD
```

## Interactive workflow with Lightning App
Existing scripts, **unchanged**, are wrapped in as a Lightning App.
Lighting Flow is used to codify orchestration in Python code.
Lighting Work is used to run the script. 
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

## Current State