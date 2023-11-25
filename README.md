# RayTrace

RayTace.py is a project to write a ray tracer in Python3.

## What are the differences ?

### V1

The V1 is a modified version of the code from the Medium arcticle. It's currently deprecated as we decided to work on the V2 and a possible V3.

### V2

The V2 is an upgraded V1, it adds multiple features including but not limited to:

* Using a faster method using .pyc files.
* Having a better material system.
* Using numba to make the code faster.

### V3 - Not ready yet, only project

The V3 will be a complete rewrite to use the GPU instead of the CPU, currently Glumpy but it might (probably) change.

## How does it work ?

### V1

The V1 one is a copy of the medium article code using another system for the materials: no dictionary.

### V2

The V2 is an upgrade to the V1.
It uses a simpler and better material system and proposes more features with a faster runtime thanks to numba.

### V2.1

The V2.1 is a complete rewrite from scratch that is trying to be realtime.
