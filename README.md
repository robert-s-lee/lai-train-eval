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


```mermaid
graph TD;
  U[UI] -- start Training --> T[Train with Lighting Module Trainer];
  U -- deploy model --> G[Deploy with Gradio];
  T -- Send lightning_log --> D[Diag with Tensorboard];
  T -- Send weights.py --> G;
```    



```
train_script.py --trainer.max_epochs=1 --trainer.limit_train_batches=12 --trainer.limit_val_batches=4 --trainer.callbacks=ModelCheckpoint --trainer.callbacks.monitor=val_acc
``` 