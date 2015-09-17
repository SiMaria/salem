from __future__ import division

import unittest
import shutil
import os
import time
from matplotlib.pyplot import plot

import numpy as np
from numpy.testing import assert_allclose
import shapely.geometry as shpg
import geopandas as gpd

from salem import utils


# Globals
current_dir = os.path.dirname(os.path.abspath(__file__))
testdir = os.path.join(current_dir, 'tmp')
if not os.path.exists(testdir):
    os.makedirs(testdir)


def create_dummy_shp(fname):

    e_line = shpg.LinearRing([(1.5, 1), (2., 1.5), (1.5, 2.), (1, 1.5)])
    i_line = shpg.LinearRing([(1.4, 1.4), (1.6, 1.4), (1.6, 1.6), (1.4, 1.6)])
    p1 = shpg.Polygon(e_line, [i_line])
    p2 = shpg.Polygon([(2.5, 1.3), (3., 1.8), (2.5, 2.3), (2, 1.8)])
    p3 = shpg.Point(0.5, 0.5)
    p4 = shpg.Point(1, 1)
    df = gpd.GeoDataFrame()
    df['name'] = ['Polygon', 'Line']
    df['geometry'] = gpd.GeoSeries([p1, p2])
    of = os.path.join(testdir, fname)
    df.to_file(of)
    return of


def delete_test_dir():
    if os.path.exists(testdir):
        shutil.rmtree(testdir)


class TestUtils(unittest.TestCase):

    def setUp(self):
        if not os.path.exists(testdir):
            os.makedirs(testdir)

    def tearDown(self):
        delete_test_dir()

    def test_cache_working(self):

        f1 = 'f1.shp'
        f1 = create_dummy_shp(f1)
        cf1 = utils.cached_path(f1)
        self.assertFalse(os.path.exists(cf1))
        _ = utils.read_shapefile(f1)
        self.assertFalse(os.path.exists(cf1))
        _ = utils.read_shapefile(f1, cached=True)
        self.assertTrue(os.path.exists(cf1))
        # nested calls
        self.assertTrue(cf1 == utils.cached_path(cf1))

        # wait a bit
        time.sleep(0.1)
        f1 = create_dummy_shp(f1)
        cf2 = utils.cached_path(f1)
        self.assertFalse(os.path.exists(cf1))
        _ = utils.read_shapefile(f1, cached=True)
        self.assertFalse(os.path.exists(cf1))
        self.assertTrue(os.path.exists(cf2))
        df = utils.read_shapefile(f1, cached=True)
        np.testing.assert_allclose(df.min_x, [1., 2.])
        np.testing.assert_allclose(df.max_x, [2., 3.])
        np.testing.assert_allclose(df.min_y, [1., 1.3])
        np.testing.assert_allclose(df.max_y, [2., 2.3])

        self.assertRaises(ValueError, utils.read_shapefile, 'f1.sph')
        self.assertRaises(ValueError, utils.cached_path, 'f1.splash')
        
    def test_mercatorgrid(self):

        grid = utils.local_mercator_grid(center_ll=(11.38, 47.26),
                                                   extent=(2000000, 2000000))
        lon1, lat1 = grid.center_grid.ll_coordinates
        e1 = grid.extent
        grid = utils.local_mercator_grid(center_ll=(11.38, 47.26),
                                                   extent=(2000000, 2000000),
                                                   order='ul')
        lon2, lat2 = grid.center_grid.ll_coordinates
        e2 = grid.extent

        assert_allclose(e1, e2)
        assert_allclose(lon1, lon2[::-1, :])
        assert_allclose(lat1, lat2[::-1, :])

        grid = utils.local_mercator_grid(center_ll=(11.38, 47.26),
                                                   extent=(2000, 2000),
                                                   nx=100)
        lon1, lat1 = grid.pixcorner_ll_coordinates
        e1 = grid.extent
        grid = utils.local_mercator_grid(center_ll=(11.38, 47.26),
                                                   extent=(2000, 2000),
                                                   order='ul',
                                                   nx=100)
        lon2, lat2 = grid.pixcorner_ll_coordinates
        e2 = grid.extent

        assert_allclose(e1, e2)
        assert_allclose(lon1, lon2[::-1, :])
        assert_allclose(lat1, lat2[::-1, :])

        grid = utils.local_mercator_grid(center_ll=(11.38, 47.26),
                                                   extent=(2000, 2000),
                                                   nx=10)
        e1 = grid.extent
        grid = utils.local_mercator_grid(center_ll=(11.38, 47.26),
                                                   extent=(2000, 2000),
                                                   order='ul',
                                                   nx=9)
        e2 = grid.extent
        assert_allclose(e1, e2)

    def test_demofiles(self):

        self.assertTrue(os.path.exists(utils.get_demo_file('dem_wgs84.nc')))
        self.assertTrue(utils.get_demo_file('dummy') is None)