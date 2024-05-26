
import xml.etree.ElementTree as ET
import numpy as np
from decimal import Decimal
from lmfit import Parameters, Minimizer


def vi(lmz_path):
    # Parse the XML file
    tree = ET.parse(lmz_path)
    root = tree.getroot()

    # Extract voltage and current values
    voltage_str = root.find('.//Voltage').text
    voltage_values = np.array([float(v) for v in voltage_str.split(',')])
    current_str = root.find('.//Current').text
    current_values = np.array([float(v) for v in current_str.split(',')])
    abs_current = np.abs(current_values)

    # Define the model function
    def mob(params, x, data=None):
        Is = params['Is']
        Vt = params['Vt']
        n = params['n']

        # Fit a polynomial to the negative part of the data
        negative_indices = x < 0
        if np.any(negative_indices):
            poly_coeff = np.polyfit(x[negative_indices], data[negative_indices], deg=2)
            model_negative = np.polyval(poly_coeff, x[negative_indices])
        else:
            model_negative = np.array([])

        # Model the positive part with an exponential function
        positive_indices = x >= 0
        model_positive = Is * (np.exp(x[positive_indices] / (n * Vt)) - 1) if np.any(positive_indices) else np.array([])

        # Concatenate the models
        model = np.concatenate((model_negative, model_positive))

        if data is None:
            return model
        else:
            return model - data

    # Set initial parameters
    pars = Parameters()
    pars.add('Is', value=10 ** -8)
    pars.add('Vt', value=0.026)
    pars.add('n', value=1, vary=False)

    # Perform the minimization
    fitter = Minimizer(mob, pars, fcn_args=(voltage_values, current_values))
    result = fitter.minimize()
    final = abs_current + result.residual

    # Calculate R-squared
    RSS = np.sum(result.residual ** 2)
    mean_current = np.mean(current_values)
    TSS = np.sum((current_values - mean_current) ** 2)
    R_squared = 1 - (Decimal(RSS) / Decimal(TSS))

    return {'voltage': voltage_values, 'abs_current': abs_current, 'final current': final, 'R_squared': R_squared}


