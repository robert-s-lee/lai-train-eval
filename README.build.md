
# ex of resume from chekcheckpoint

- resume
- resume will remove lightning_logs/version_0/checkpoints/epoch=57-step=108750.ckpt
- version_1 will be created
```
python train_script.py --trainer.resume_from_checkpoint lightning_logs/version_0/checkpoints/epoch=57-step=108750.ckpt
```


# dirname that has example.pt file
cd lightning_logs; find . -name example.pt -type f -depth 2 -exec bash -c 'echo $(basename $(dirname {}))' \;; cd ..
version_1


