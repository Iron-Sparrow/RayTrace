import time
from compyl.compyl import *
from compyl.AntiAliasing import *
import cProfile
import pstats

RayTrace_license = '''This project is currently using the MIT license but this might (and probably will) change in the future.''' #type: ignore
Profile = False

if __name__ == '__main__':
    ot = time.time()
    if Profile:
        with cProfile.Profile() as pr:
            Render()
    else:
        Render()
    print(f"{((time.time() - ot) * 1000):.2f} ms, {(time.time() - ot):.3f} s, {(1/(time.time() - ot)):.3f} Hz")
    if Profile:
        stats = pstats.Stats(pr)
        stats.sort_stats(pstats.SortKey.TIME)
        stats.dump_stats(filename="profilingV2.prof")
        with open("profilingV2.txt", "w") as f:
            stats.stream = f
            stats.print_stats()