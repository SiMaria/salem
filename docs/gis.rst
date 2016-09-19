.. _gis:

Georeferencing
==============

A point on earth can be defined unambiguously in two ways:

DATUM (lon, lat, datum)
    longitudes and latitudes are angular coordinates of a point on an
    ellipsoid (datum)
PROJ (x, y, projection)
    x (eastings) and y (northings) are cartesian coordinates of a point in a
    map projection (the unit of x, y is usually meter)

Transformations between datums and projections is handled by several tools
in the python ecosystem, for example `GDAL`_ or the more lightweight
`pyproj`_. Salem adds a third coordinate reference system (crs) to this list:

GRID (i, j, Grid)
    on a structured grid, the (x, y) coordinates are distant of a
    constant (dx, dy) step. The (x, y) coordinates are therefore equivalent
    to a new reference frame (i, j) proportional to the projection's (x, y)
    frame.

Transformations between datum and projections are handled by the pyproj
library. Since most datasets nowadays are defined in the WGS 84 datum,
from now on we will only be concerned about projections [#]_.

The concept of Grid added by Salem is useful when transforming data between
two structured datasets, or from an unstructured dataset to a structured one.

.. _GDAL: https://pypi.python.org/pypi/GDAL/
.. _pyproj: https://jswhit.github.io/pyproj/



.. [#] in pyproj, the two concepts are often interchangeable:
       (lon, lat) coordinates are equivalent to cartesian
       (lon, lat) coordinates in the plate carree projection.

Grids
-----

A :py:class:`~salem.Grid` is defined by a projection, a reference point in
this projection, a grid spacing and a number of grid points:

.. ipython:: python

    import numpy as np
    import salem
    from salem import wgs84

    grid = salem.Grid(nxny=(3, 2), dxdy=(1, 1), ll_corner=(6, 49), proj=wgs84)
    x, y = grid.xy_coordinates
    x
    y

Here, the grid is defined on the plate caree projection, so that the longitudes
and latitudes are the same as the eastings and northings:

.. ipython:: python

    lon, lat = grid.ll_coordinates
    lon
    lat

But it won't be the case for other projections, for example:

.. ipython:: python

    from pyproj import Proj
    utm = Proj("+proj=utm +zone=35 +datum=WGS84 +units=m")
    utmgrid = salem.Grid(nxny=(3, 2), dxdy=(50000, 50000), ll_corner=(0, 60000), proj=utm)
    x, y = utmgrid.xy_coordinates
    lon, lat = utmgrid.ll_coordinates
    y
    lat
