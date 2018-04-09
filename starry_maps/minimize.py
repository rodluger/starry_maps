"""Find the minimum of a polynomial surface map."""
import numpy as np
from scipy.optimize import minimize as scipymin


__all__ = ["minimize"]


def constraint(x):
    """Return zero if on the surface of the unit sphere."""
    return x[0] ** 2 + x[1] ** 2 + x[2] ** 2 - 1


def jacobian(x):
    """Return the jacobian of the constraint."""
    return (2 * x[0], 2 * x[1], 2 * x[2])


def evaluate(x, p):
    """Evaluate the map and its gradient at a point."""
    lmax = int(np.sqrt(len(p)) - 1)
    n = 0
    res = 0
    grad = np.zeros(3)
    for l in range(lmax + 1):
        for m in range(-l, l + 1):
            mu = l - m
            nu = l + m
            if ((nu % 2) == 0):
                res += p[n] * x[0] ** (mu / 2) * x[1] ** (nu / 2)
                if mu == 0:
                    dx = 0
                else:
                    dx = 0.5 * mu * p[n] * x[0] ** (mu / 2 - 1) \
                             * x[1] ** (nu / 2)
                if nu == 0:
                    dy = 0
                else:
                    dy = 0.5 * nu * p[n] * x[0] ** (mu / 2) \
                             * x[1] ** (nu / 2 - 1)
                dz = 0
                grad += np.array([dx, dy, dz])
            else:
                res += p[n] * x[0] ** ((mu - 1) / 2) \
                            * x[1] ** ((nu - 1) / 2) * x[2]
                if mu == 1:
                    dx = 0
                else:
                    dx = 0.5 * (mu - 1) * p[n] * x[0] ** ((mu - 1) / 2 - 1) \
                             * x[1] ** ((nu - 1) / 2) * x[2]
                if nu == 1:
                    dy = 0
                else:
                    dy = 0.5 * (nu - 1) * p[n] * x[0] ** ((mu - 1) / 2) \
                             * x[1] ** ((nu - 1) / 2 - 1) * x[2]
                dz = p[n] * x[0] ** ((mu - 1) / 2) * x[1] ** ((nu - 1) / 2)
                grad += np.array([dx, dy, dz])
            n += 1
    return res, grad


def minimize_brute(p, npts):
    """Find the minimum of the map by brute-force gridding."""
    minpos = (0, 0, 1)
    minval, _ = evaluate(minpos, p)
    res = int(np.ceil(np.sqrt(4 / np.pi * npts)) + 1)
    for x1 in np.linspace(-1, 1, res):
        for x2 in np.linspace(-1, 1, res):
            r2 = x1 ** 2 + x2 ** 2
            if r2 < 1:
                x = 2 * x1 * np.sqrt(1 - r2)
                y = 2 * x2 * np.sqrt(1 - r2)
                z = 1 - 2 * r2
                val, _ = evaluate((x, y, z), p)
                if val < minval:
                    minval = val
                    minpos = (x, y, z)
    return minval, minpos


def minimize(p):
    """Find the global minimum of the map."""
    lmax = int(np.sqrt(len(p)) - 1)
    # A spherical harmonic of degree `l` has at most
    # `lmax^2 - lmax + 2` extrema
    # http://adsabs.harvard.edu/abs/1992SvA....36..220K
    # so let's have at least 2x as many points in each
    # dimension for good sampling
    npts = 4 * (lmax ** 2 - lmax + 2)
    minval, minpos = minimize_brute(p, npts)
    foo = scipymin(evaluate, minpos, args=(p,), method='SLSQP', jac=True,
                   constraints=dict(type='eq', fun=constraint, jac=jacobian))
    return foo.fun
