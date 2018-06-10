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