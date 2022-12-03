# Vahper: Valorant helper

### Demo app with use of CV + Pose Estimation 

<img src="/demo/gifs/standing_still.gif?raw=true" width="720px">

<img src="/demo/gifs/v1.gif?raw=true" width="720px">


### Installation:
- Put [model checkpoint](https://download.01.org/opencv/openvino_training_extensions/models/human_pose_estimation/checkpoint_iter_370000.pth) into `vahper\tools\recognition\hpep_cut\weights`
- Install Vahper:
```
git clone https://github.com/codepause/vahper
cd vahper
pip install -r requirements.txt
python setup.py installg
```

### Hotkeys
>- `NUM_1`: `Enable / disable` image processing
>- `NUM_2`: Change rendering mode
>   - `0` - render disable
>   - `1` - head indicator
>   - `2` - head + skeleton
>   - `3` - head + skeleton + bounding box
>- `NUM_3`: `Enable / disable` mouse movement to the closest head indicator
>- `NUM_0`: `Shutdown`
  
### Acknowledgement
- [Daniil-Osokin pytorch pose estimation](https://github.com/Daniil-Osokin/lightweight-human-pose-estimation.pytorch)
- [Easy Pipeline Tools for Automation](https://github.com/antistack/epta)


## P.S
- Vanguard is preventing `WM mouse events`, so this code is _useless_ unless different `mouse driver` is implemented ;)
- I do not support any cheaters. All of this was done for **_educational purposes only_**.
- **Use at your own risk. No responsibilities taken.**