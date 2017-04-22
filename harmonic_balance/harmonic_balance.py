import scipy as sp
import scipy.fftpack as fftp
# from scipy import pi, sin,cos
# import matplotlib.pyplot as plt


def harmonic_balance_so(sdfunc, x0, omega, method, *kwargs, num_harmonics=1):
    '''Harmonic balance solver for second order ODEs.
    Obtains the solution of a second order differential equation under the
    presumption that the solution is harmonic.

    Returns t (time), x (displacement), v (velocity), and a (acceletation)
    response of a second order linear ordinary differential
    equation defined by
    :math:`\ddot{\mathbf{x}}=f(\mathbf{x},\mathbf{v},\omega)`.
    `

    Parameters
    ----------
    sdfunc: str
        name of function that returns second derivative given omega and
        *kwargs
        :math:`\ddot{\mathbf{x}}=f(\mathbf{x},\mathbf{v},\omega)`
    omega:  float
        assumed fundamental response frequency.
    num_harmonics: int
        number of harmonics to presume. Constant term is always presumed.
    x0: ndarray
        n x m array where n is the number of equations and m is the number of
        values representing the repeating solution.
        It is required that m = 1 + 2 * num_harmonics.
    method: str
        Name of optimization method to be used.

    Returns
    -------
    t, x, v, a : ndarrays
    '''

    '''
    a) define a function that returns errors in time domain as vector
    b) define function to obtain velocity and accelerations from displacement
    and frequencies.
    c)
    '''


def harmonic_deriv(omega, r):
    '''Derivative of a harmonic function using frequency methods
    Returns the derivatives of a harmonic function

    Parameters
    ----------
    omega: float
        Fundamendal frequency, in rad/sec, of repeating signal
    r: ndarray
        | Array of rows of time histories to take the derivative of.
        | The 1 axis (each row) corresponds to a time history.
        | The length of the time histories *must be an odd integer*.

    Returns
    -------
    s: ndarray
        array of function derivatives.
        The 1 axis (each row) corresponds to a time history.

    Notes
    -----
    At this time, the length of the time histories *must be an odd integer*.

    Examples
    --------
    >>> import matplotlib.pyplot as plt
    >>> import scipy as sp
    >>> from scipy import pi,sin,cos
    >>> f = 2
    >>> omega = 2.*pi * f
    >>> numsteps = 11
    >>> t = sp.arange(0,1/omega*2*pi,1/omega*2*pi/numsteps)
    >>> x = sp.array([sin(omega*t)])
    >>> v = sp.array([omega*cos(omega*t)])
    >>> states = sp.append(x,v,axis = 0)
    >>> state_derives = harmonic_deriv(omega,states)
    >>> plt.plot(t,states.T,t,state_derives.T,'x')
    [<matplotlib.line...]
    '''
    n = r.shape[1]
    omega_half = -sp.arange((n-1)/2+1) * omega * 2j/(n-2)
    omega_whole = sp.append(sp.conj(omega_half[-1:0:-1]), omega_half)
    r_freq = fftp.fft(r)
    s_freq = r_freq * omega_whole
    s = fftp.ifft(s_freq)
    return sp.real(s)


if __name__ == "__main__":
    import doctest
    doctest.testmod(optionflags=doctest.ELLIPSIS |
                    doctest.NORMALIZE_WHITESPACE)
    # import vibration_toolbox as vtb

    # doctest.run_docstring_examples(frfest,globals(),optionflags=doctest.ELLIPSIS)
    # doctest.run_docstring_examples(asd,globals(),optionflags=doctest.ELLIPSIS)
    """ What this does.
    python (name of this file)  -v
    will test all of the examples in the help.

    Leaving off -v will run the tests without any output. Success will return
    nothing.

    See the doctest section of the python manual.
    https://docs.python.org/3.5/library/doctest.html
    """
