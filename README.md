Usage:
```sudo python render.py "HI!"```

If this is running with plain Python 2.7 somewhere, will print out:

```
XX  XX   XXXX      XX   00000000
XX  XX    XX      XXXX  00000000
XX  XX    XX      XXXX  00000000
XXXXXX    XX       XX   00000000
XX  XX    XX       XX   00000000
XX  XX    XX            00000000
XX  XX   XXXX      XX   00000000
                        00000000
```

If you have this hooked up to a BeagleBone Black + LogiBone 
running (at least) a 16x32 RGB LED matrix, the 8x8 "HI!" message
should also show up your panel.

NOTE: Remember to load the `logibone_mat.bit` file using the `logi_load` command!
