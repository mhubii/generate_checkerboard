# Generate Checkerboard
Generate a checkerboard for camera calibration with

```shell
python gen.py --format A4 --size 0.05 # units of m
```

Saves resulting height, width, and square size in param.yaml. **Please assure that the printed version is not scaled**. Call help with

```shell
python gen.py -h
```

The generated checkerboard can then for example be used with a [stereo calibration](https://github.com/sourishg/stereo-calibration). 
