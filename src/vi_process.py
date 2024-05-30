
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
        poly_coeff = np.polyfit(x[x < 2], data[x < 2], deg=12)
        model_negative = np.polyval(poly_coeff, x[x < 2])
        model_positive = Is * (np.exp(x[x >= 2] / (n * Vt)) - 1)
        model = np.concatenate((model_negative, model_positive))
        if data is None:
            return model
        else:
            return model - data

    pars = Parameters()
    pars.add('Is', value=10 ** -8)
    pars.add('Vt', value=0.026)
    pars.add('n', value=1, vary=False)

    fitter = Minimizer(mob, pars, fcn_args=(voltage_values, current_values))
    result = fitter.minimize()
    final = abs_current + result.residual

    # Calculate R-squared
    RSS = np.sum(result.residual ** 2)
    mean_current = np.mean(current_values)
    TSS = np.sum((current_values - mean_current) ** 2)
    R_squared = 1 - (Decimal(RSS) / Decimal(TSS))

    return {'voltage': voltage_values, 'abs_current': abs_current, 'final current': final, 'R_squared': R_squared}

print(vi('..\\dat\\HY202103\\D24\\20190531_151815\\HY202103_D24_(2,-3)_LION1_DCM_LMZO.xml'))
