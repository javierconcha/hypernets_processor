"""
Tests for TemplateUtil class
"""

import unittest
import xarray
from hypernets_processor.data_io.template_util import TemplateUtil
from hypernets_processor.version import __version__


'''___Authorship___'''
__author__ = "Sam Hunt"
__created__ = "21/2/2020"
__version__ = __version__
__maintainer__ = "Sam Hunt"
__email__ = "sam.hunt@npl.co.uk"
__status__ = "Development"

# todo - add variable properties to dictionaries and test
# todo - improve metadata tests to fully check metadata

COMMON_VARIABLES = {"wavelength": {},
                    "bandwidth": {},
                    "viewing_angle_azimuth": {},
                    "viewing_angle_zenith": {},
                    "sun_angle_azimuth": {},
                    "sun_angle_zenith": {},
                    "quality_flags": {},
                    "acquisition_time": {}}

L1A_RAD_VARIABLES = {"u_random_radiance": {},
                    "u_systematic_radiance": {},
                    "cov_random_radiance": {},
                    "cov_systematic_radiance": {},
                    "radiance": {}}

L1A_IRR_VARIABLES = {"u_random_irradiance": {},
                    "u_systematic_irradiance": {},
                    "cov_random_irradiance": {},
                    "cov_systematic_irradiance": {},
                    "irradiance": {}}

L2A_VARIABLES = {"u_random_reflectance": {},
                 "u_systematic_reflectance": {},
                 "cov_random_reflectance": {},
                 "cov_systematic_reflectance": {},
                 "reflectance": {}}

L2B_VARIABLES = {"u_random_reflectance": {},
                 "u_systematic_reflectance": {},
                 "cov_random_reflectance": {},
                 "cov_systematic_reflectance": {},
                 "reflectance": {}}


def test_dataset(self, ds, variables):
    self.assertEqual(len(variables.keys()), len(ds.data_vars) + len(ds.coords))

    for var in variables.keys():
        self.assertIsNotNone(ds.variables[var])


class TestTemplateUtil(unittest.TestCase):

    def test_add_common_variables(self):
        dataset = xarray.Dataset()

        TemplateUtil.add_common_variables(dataset, 271, 10)

        test_dataset(self, dataset, COMMON_VARIABLES)

    def test_add_l1a_rad_variables(self):
        dataset = xarray.Dataset()

        TemplateUtil.add_l1a_rad_variables(dataset, 271, 10)

        test_dataset(self, dataset, L1A_RAD_VARIABLES)

    def test_add_l1a_irr_variables(self):
        dataset = xarray.Dataset()

        TemplateUtil.add_l1a_irr_variables(dataset, 271, 10)

        test_dataset(self, dataset, L1A_IRR_VARIABLES)

    def test_add_l2a_variables(self):
        dataset = xarray.Dataset()

        TemplateUtil.add_l2a_variables(dataset, 271, 10)

        test_dataset(self, dataset, L2A_VARIABLES)

    def test_add_l2b_variables(self):
        dataset = xarray.Dataset()

        TemplateUtil.add_l2b_variables(dataset, 271, 10)

        test_dataset(self, dataset, L2B_VARIABLES)

    def test_add_common_metadata(self):
        dataset = xarray.Dataset()

        TemplateUtil.add_common_metadata(dataset)

        self.assertEqual("English", dataset.attrs["language"])

    def test_add_l1a_rad_metadata(self):
        dataset = xarray.Dataset()

        TemplateUtil.add_l1a_rad_metadata(dataset)

        self.assertEqual("HYPSTAR dataset of radiance",
                         dataset.attrs["title"])

    def test_add_l1_irr_metadata(self):
        dataset = xarray.Dataset()

        TemplateUtil.add_l1a_irr_metadata(dataset)

        self.assertEqual("HYPSTAR dataset of irradiance",
                         dataset.attrs["title"])

    def test_add_l_l1b_metadata(self):
        dataset = xarray.Dataset()

        TemplateUtil.add_l_l1b_metadata(dataset)

        self.assertEqual("HYPSTAR Land network dataset of radiance and irradiance",
                         dataset.attrs["title"])

    def test_add_w_l1b_metadata(self):
        dataset = xarray.Dataset()

        TemplateUtil.add_w_l1b_metadata(dataset)

        self.assertEqual("HYPSTAR Water network dataset of downwelling irradiance, upwelling and downwelling"
                         " radiance and water leaving radiance",
                         dataset.attrs["title"])

    def test_add_l_l2a_metadata(self):
        dataset = xarray.Dataset()

        TemplateUtil.add_l_l2a_metadata(dataset)

        self.assertEqual("HYPSTAR Land network dataset of spectral surface reflectance",
                         dataset.attrs["title"])

    def test_add_w_l2a_metadata(self):
        dataset = xarray.Dataset()

        TemplateUtil.add_w_l2a_metadata(dataset)

        self.assertEqual("HYPSTAR Water network dataset of spectral surface reflectance",
                         dataset.attrs["title"])

    def test_add_land_network_metadata(self):
        dataset = xarray.Dataset()

        TemplateUtil.add_land_network_metadata(dataset)

        self.assertEqual("Hunt Sam", dataset.attrs["creator_name"])

    def test_add_water_network_metadata(self):
        dataset = xarray.Dataset()

        TemplateUtil.add_water_network_metadata(dataset)

        self.assertEqual("Goyens Clémence", dataset.attrs["creator_name"])


if __name__ == '__main__':
    unittest.main()
