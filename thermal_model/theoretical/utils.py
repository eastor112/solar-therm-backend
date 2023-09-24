import numpy as np
import cmath
import math


def acosd(x):
  acos_result = cmath.acos(x)
  return complex(math.degrees(acos_result.real), math.degrees(acos_result.imag))


def interpolate_nan_inf(arr):
  finite_indices = np.isfinite(arr)

  nan_inf_indices = ~finite_indices

  arr[nan_inf_indices] = np.interp(
      np.where(nan_inf_indices)[0],
      np.where(finite_indices)[0],
      arr[finite_indices]
  )

  return arr
