from random import randint

import numba
@numba.njit(fastmath=True)
def Clamp(x:float, mi_ma:tuple[float, float] = (0., 1.)) -> float:
    return x * (mi_ma[0] < x) * (mi_ma[1] > x) + mi_ma[0] * (mi_ma[0] >= x) + mi_ma[1] * (mi_ma[1] <= x)

@numba.njit(fastmath=True)
def Clampint(x:int, mi_ma:tuple[int, int] = (0, 1)) -> int:
    return x * (mi_ma[0] < x) * (mi_ma[1] > x) + mi_ma[0] * (mi_ma[0] >= x) + mi_ma[1] * (mi_ma[1] <= x)

@numba.jit(fastmath=True, nopython=False)
def Clamplist(x:list, mi_ma:tuple[int|float, int|float] = (0,1)) -> list[float|int]:
    for i in range(len(x)):
        x[i] = x[i] * (mi_ma[0] < x[i]) * (mi_ma[1] > x[i]) + mi_ma[0] * (mi_ma[0] >= x[i]) + mi_ma[1] * (mi_ma[1] <= x[i])
    return x
