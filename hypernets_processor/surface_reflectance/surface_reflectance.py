"""
Surface reflectance class
"""

from hypernets_processor.version import __version__
from hypernets_processor.data_io.hypernets_ds_builder import HypernetsDSBuilder
from hypernets_processor.surface_reflectance.measurement_functions.protocol_factory import ProtocolFactory
import punpy
import numpy as np

'''___Authorship___'''
__author__ = "Pieter De Vis"
__created__ = "12/04/2020"
__version__ = __version__
__maintainer__ = "Pieter De Vis"
__email__ = "Pieter.De.Vis@npl.co.uk"
__status__ = "Development"


class SurfaceReflectance:
    def __init__(self,MCsteps=1000,parallel_cores=1):
        self._measurement_function_factory = ProtocolFactory()
        self.prop= punpy.MCPropagation(MCsteps,parallel_cores=parallel_cores)

    def process(self,dataset_l1c,measurement_function):
        dataset_l1c = self.perform_checks(dataset_l1c)
        l1tol2_function = self._measurement_function_factory.get_measurement_function(measurement_function)
        input_vars = l1tol2_function.get_argument_names()
        input_qty = self.find_input(input_vars,dataset_l1c)
        u_random_input_qty = self.find_u_random_input(input_vars,dataset_l1c)
        u_systematic_input_qty = self.find_u_systematic_input(input_vars,dataset_l1c)
        dataset_l2 = self.l2_from_l1c_dataset(dataset_l1c)
        dataset_l2 = self.process_measurement_function("reflectance",dataset_l2,l1tol2_function.function,input_qty,
                                                       u_random_input_qty,u_systematic_input_qty)
        return dataset_l2

    def find_input(self,variables,dataset):
        """
        returns a list of the data for a given list of input variables

        :param variables:
        :type variables:
        :param dataset:
        :type dataset:
        :return:
        :rtype:
        """
        inputs = []
        for var in variables:
            inputs.append(dataset[var].values)
        return inputs

    def find_u_random_input(self,variables,dataset):
        """
        returns a list of the random uncertainties on the data for a given list of input variables

        :param variables:
        :type variables:
        :param dataset:
        :type dataset:
        :return:
        :rtype:
        """
        inputs = []
        for var in variables:
            inputs.append(dataset["u_random_"+var].values)
        return inputs

    def find_u_systematic_input(self,variables,dataset):
        """
        returns a list of the systematic uncertainties on the data for a given list of input variables

        :param variables:
        :type variables:
        :param dataset:
        :type dataset:
        :return:
        :rtype:
        """
        inputs = []
        for var in variables:
            inputs.append(dataset["u_systematic_"+var].values)
        return inputs

    def perform_checks(self,dataset_l1):
        """
        Identifies and removes faulty measurements (e.g. due to cloud cover).

        :param dataset_l0:
        :type dataset_l0:
        :return:
        :rtype:
        """
        return dataset_l1

    def l2_from_l1c_dataset(self,datasetl1c):
        """
        Makes a L2 template of the data, and propagates the appropriate keywords from L1.

        :param datasetl0:
        :type datasetl0:
        :return:
        :rtype:
        """
        l2a_dim_sizes_dict = {"wavelength":len(datasetl1c["wavelength"]),
                              "series":len(datasetl1c['series'])}
        l2a = HypernetsDSBuilder.create_ds_template(l2a_dim_sizes_dict,"L_L2A")

        return l2a

    def process_measurement_function(self,measurandstring,dataset,measurement_function,input_quantities,u_random_input_quantities,
                                     u_systematic_input_quantities):
        measurand = measurement_function(*input_quantities)
        u_random_measurand = self.prop.propagate_random(measurement_function,input_quantities,u_random_input_quantities)
        u_systematic_measurand,corr_systematic_measurand = self.prop.propagate_systematic(measurement_function,
                                                                                          input_quantities,
                                                                                          u_systematic_input_quantities,
                                                                                          return_corr=True,corr_axis=0)
        dataset[measurandstring].values = measurand
        dataset["u_random_"+measurandstring].values = u_random_measurand
        dataset["u_systematic_"+measurandstring].values = u_systematic_measurand
        dataset["corr_random_"+measurandstring].values = np.eye(len(u_random_measurand))
        dataset["corr_systematic_"+measurandstring].values = corr_systematic_measurand

        return dataset










