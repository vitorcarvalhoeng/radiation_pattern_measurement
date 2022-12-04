# -----------auxiliary-----------------------

import decimal

def sph2cart(r,elevation,azimuth):
    x = r * np.cos(elevation) * np.cos(azimuth)
    y = r * np.cos(elevation) * np.sin(azimuth)
    z = r * np.sin(elevation)
    return x, y, z


def float_range(start, stop, step):
    while start < stop:
        yield float(start)
        start += decimal.Decimal(step)
  