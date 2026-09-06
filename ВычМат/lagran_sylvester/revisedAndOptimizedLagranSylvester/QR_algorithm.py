#QR_algorithm.py
import numpy as np
import HouseholderTransformation as hh
#import GivensTransformation as gv
import QR_decomposition as qr
import initsyalizatsyaMatristy as im

def calculate(A,iterations=30):
    _,H = hh.transform(A)
    for _ in range(iterations):
        Q,R = qr.transform(H)
        H = R @ Q
    return H

#"""
orig = im.A
H = calculate(orig.copy())
print(H)
indx = [i for i in range(H.shape[0])]
print(np.diag(H))
print(np.linalg.eigvals(orig))
#"""