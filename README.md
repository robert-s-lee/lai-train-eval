A lift-and-shift tutorial of Lightning App, Flow, Work.  
- interactive UI
- training
- training diag
- eval

Integrations:
- Streamlit
- Gradio
- Tensorboard

Lightning App:
- Drive


<table>
<tr>
<th align="center">
<img width="441" height="1">
<p> 
<small>
Current Simple Workflow
</small>
</p>
</th>
<th align="center">
<img width="441" height="1">
<p> 
<small>
Flexible Workflow with Lightning App
</small>
</p>
</th>
</tr>
<tr>
<td>
<!-- REMOVE THE BACKSLASHES -->
```mermaid
graph TD;
  T[Train with Lighting & Module Trainer] -- Send lightning_log --> D[Diag with Tensorboard]; 
  D -- Send weights.py --> G[Deploy with Gradio];
  G -- Retrain --> T;
```
</td>
<td>
<!-- REMOVE THE BACKSLASHES -->
```mermaid
graph TD;
  L[Lightning App] --> U[UI with Streamlit]
  U -- start Training --> T[Train with Lighting & Module Trainer];
  U -- deploy model --> G[Deploy with Gradio];
  T -- Send lightning_log --> D[Diag with Tensorboard];
  T -- Send weights.py --> G;
  G -- Retrain --> T;
```
</td>
</tr>







```
train_script.py --trainer.max_epochs=1 --trainer.limit_train_batches=12 --trainer.limit_val_batches=4 --trainer.callbacks=ModelCheckpoint --trainer.callbacks.monitor=val_acc
``` 