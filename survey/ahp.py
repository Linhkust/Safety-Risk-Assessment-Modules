import numpy as np
from pyrepo_mcda.mcda_methods import AHP
from fractions import Fraction
import random

def int_fraction(string):
    try:
        return int(string)
    except Exception:
        return Fraction(string)

def ahp_analysis(pc_result):
    n = pc_result.shape[1]
    RI = [0, 0, 0.58, 0.90, 1.12, 1.24, 1.32, 1.41, 1.45, 1.49]
    lambdamax = np.amax(np.linalg.eigvals(pc_result).real)
    CI = (lambdamax - n) / (n - 1)
    CR = CI / RI[n - 1]

    ahp = AHP()
    weights = ahp._calculate_eigenvector(pc_result)
    return CR, weights


def generate_random_str(len=15):
    str = ""
    for i in range(len):
        str += random.choice('abcdefghijklmnopqrstuvwxyz')
    return str