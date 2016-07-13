__all__ = ['normalize']

def normalize(hist):
    return hist.Scale(1.0/hist.Integral())
