import time
from compyl.compyl import *

RayTrace_license = '''This project is currently using the MIT license but this might (and probably will) change in the future.''' #type: ignore


if __name__ == '__main__':
    ot = time.time()
    Render()
    print(f"{((time.time() - ot) * 1000):.2f} ms, {(time.time() - ot):.3f} s, {(1/(time.time() - ot)):.3f} Hz")