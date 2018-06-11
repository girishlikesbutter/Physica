def latex_float(f):
    float_str = "{0:.2g}".format(f)
    if "e" in float_str:
        base, exponent = float_str.split("e")
        return r"{0} \times 10^{{{1}}}".format(base, int(exponent))
    else:
        return float_str

def humanize(item):
    if type(item) == uncertainties.core.Variable:
        string = "${} \\pm {}$".format(latex_float(item.n), latex_float(item.s))
    elif type(item) in [int, float, np.float64]:
        string = "{}".format(latex_float(item))
        
    return string

def enter_mathmode(string):
    if("\\" in string):
        x = string.split(" ")
        bits = []
        for bit in x:
            if "\\" in bit:
                # This word contains LaTeX, so enter math mode.
                bit = "${}$".format(bit)
            bits.append(bit)
        # Concatenate everything back together into one word
        return " ".join(bits)
    return string

def FFT(yn, dt, npt, plotter=None, xlim=50):
    """Generates the fast fourier transform of a set of data.
    
    Keyword arguments:
        yn -- the data to transform
        dt -- the time separation of the points on x-axis
        npt -- the number of points on the x-axis
        plotter -- an instance of matplotlib.pyplot (created and returned if None)
        xlim -- an integer representing the maximum x-axis size
    """
    Y = np.fft.fftshift(np.fft.fft(yn))

    t_span=npt*dt

    df=1/t_span
    f_span=1/dt

    f_sample=np.linspace(-npt/2,npt/2,npt,endpoint=False)/npt*f_span
    
    i = len(f_sample / 2)

    ret = False
    if plotter is None:
        ret = True
        plotter = plt
        plotter.figure()
    
    mask = Y>0
    x = f_sample[mask]
    y = np.log(Y[mask])
    
    if xlim is not False:
        k = int(np.floor(len(x) / 2))
        kmin = k-xlim
        kmax = k+xlim+1
        x = x[kmin:kmax]
        y = y[kmin:kmax]
    
    plotter.xticks(rotation=45)
    plotter.plot(x, y, 'g.')
    plotter.xlabel('Frequency [Hz]')
    plotter.ylabel('Power Spectrum')
	
    if ret:
        return plotter