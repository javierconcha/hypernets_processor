"""
Contains main class for orchestrating hypernets data processing jobs
"""

from hypernets_processor.version import __version__
from hypernets_processor.calibration.calibrate import Calibrate
from hypernets_processor.surface_reflectance.surface_reflectance import SurfaceReflectance
from hypernets_processor.interpolation.interpolate import InterpolateL1c
from hypernets_processor.data_io.hypernets_writer import HypernetsWriter

import xarray as xr
import numpy as np


'''___Authorship___'''
__author__ = "Sam Hunt"
__created__ = "26/3/2020"
__version__ = __version__
__maintainer__ = "Sam Hunt"
__email__ = "sam.hunt@npl.co.uk"
__status__ = "Development"


class HypernetsProcessor:
    """
    Class to orchestrate Hypernets data processing jobs

    :type logger: logging.logger
    :param logger: logger
    """

    def __init__(self, logger=None):
        """
        Constructor method
        """

        self.logger = logger

    def run(self):
        """
        Runs hypernets data processing jobs
        """
        ds_irr = xr.open_dataset('../examples/HYPERNETS_W_VFFR_L0_IRR_20200715T133429_v0.0.nc')
        ds_rad = xr.open_dataset('../examples/HYPERNETS_W_VFFR_L0_RAD_20200715T133429_v0.0.nc')
        ds_bla = xr.open_dataset('../examples/HYPERNETS_W_VFFR_L0_BLA_20200715T133429_v0.0.nc')
        #ds_bla = ds_bla.rename({"digital_number":"dark_signal"})
        ds_bla["digital_number"].values= ds_bla["digital_number"].values/10.

        cal=Calibrate(MCsteps=100)
        intp=InterpolateL1c(MCsteps=100)
        surf=SurfaceReflectance(MCsteps=100)



        calibration_data={}
        calibration_data["gains"] = np.ones(len(ds_rad["wavelength"]))
        calibration_data["temp"] = 20*np.ones(len(ds_rad["wavelength"]))
        calibration_data["u_random_gains"] = 0.1*np.ones(len(ds_rad["wavelength"]))
        calibration_data["u_random_dark_signal"] = np.zeros(len(ds_rad["wavelength"]))
        calibration_data["u_random_temp"] = 1*np.ones(len(ds_rad["wavelength"]))
        calibration_data["u_systematic_gains"] = 0.05*np.ones(len(ds_rad["wavelength"]))
        calibration_data["u_systematic_dark_signal"] = np.zeros(len(ds_rad["wavelength"]))
        calibration_data["u_systematic_temp"] = 1*np.ones(len(ds_rad["wavelength"]))

        L1a_rad=cal.calibrate_l1a("radiance",ds_rad,ds_bla,calibration_data,measurement_function='StandardMeasurementFunction')
        L1a_irr=cal.calibrate_l1a("irradiance",ds_irr,ds_bla,calibration_data,measurement_function='StandardMeasurementFunction')
        # L1a_rad=xr.open_dataset("../examples/test_L1a_rad.nc")
        # L1a_irr=xr.open_dataset("../examples/test_L1a_irr.nc")
        L1b_rad=cal.average_l1b("radiance",L1a_rad)
        L1b_irr=cal.average_l1b("irradiance",L1a_irr)
        L1c=intp.interpolate_l1c(L1b_rad,L1b_irr,"LandNetworkInterpolationIrradianceLinear")
        L2a=surf.process(L1c,"LandNetworkProtocol")

        HypernetsWriter.write(L1a_rad,"../examples/test_L1a_rad.nc",overwrite=True)
        HypernetsWriter.write(L1a_irr,"../examples/test_L1a_irr.nc",overwrite=True)
        HypernetsWriter.write(L1b_rad,"../examples/test_L1b_rad.nc",overwrite=True)
        HypernetsWriter.write(L1b_irr,"../examples/test_L1b_irr.nc",overwrite=True)
        HypernetsWriter.write(L1c,"../examples/test_L1c.nc",overwrite=True)
        HypernetsWriter.write(L2a,"../examples/test_L2a.nc",overwrite=True)
        return None


if __name__ == "__main__":
    hp=HypernetsProcessor()
    hp.run()
    pass