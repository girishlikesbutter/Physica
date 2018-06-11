class Dataset:
    def __init__(self, x, y, xlabel="x", ylabel="y"):
        self.__x = x
        self.__y = y
        self.__i = 0
        self.__xlabel = xlabel
        self.__ylabel = ylabel

        if len(x) != len(y):
            raise ValueError("x and y have different dimension")
        self.__size = len(x)
        
    def __str__(self):
        return str([(self.__x[i], self.__y[i]) for i in range(self.__size)])
    
    def __len__(self):
        return self.__size
    
    def __repr__(self):
        return "Dataset(x, y)"
    
    def __getitem__(self, key):
        if type(key) != int:
            raise TypeError
        if key > self.__size:
            raise KeyError
        return self.__y[key]
    
    def __setitem__(self, key, value):
        if type(key) != int or type(value) not in [int, float]:
            raise TypeError
        if key > self.__size:
            raise KeyError
        
        self.__y[key] = value
    
    def __iter__(self):
        return self
    
    def __next__(self):
        if self.__i == self.__size:
            raise StopIteration
        else:
            self.__i += 1
            return (self.__x[self.__i-1], self.__y[self.__i-1])
        
    def latex(self):
        table = """\\begin{tabular}{cc}
    \\toprule
    {x} & {y} \\\\
    \\midrule""".format(x=enter_mathmode(self.__xlabel), y=enter_mathmode(self.__ylabel), tabular="{tabular}", cc="{cc}")
        for i in range(0, self.__size):
            table = table + """
    {} & {} \\\\""".format(humanize(self.__x[i]), humanize(self.__y[i]))
        
        table = table + """
    \\bottomrule
\\end{tabular}"""
        return table

    def plot(self, filename="", deg=None, expected=None, fitfunc=None):
        plt.figure()
        # Separate out uncertainties for anything that has been explicitly declared as ufloat
        xval = [x.n if type(x) == uncertainties.core.Variable else x for x in self.__x]
        yval = [x.n if type(x) == uncertainties.core.Variable else x for x in self.__y]
        uxval = [x.s if type(x) == uncertainties.core.Variable else 0 for x in self.__x]
        uyval = [x.s if type(x) == uncertainties.core.Variable else 0 for x in self.__y]
        
        # Actually plot the data
        plt.errorbar(xval, yval, fmt="g.", xerr=uxval, yerr=uyval, label="observed")
        
        # If requested, fit a polynomial curve of best fit to the data
        # TODO: move away from polyfit
        if deg is not None and fitfunc is not None:
            xhat = np.linspace(min(xval), max(xval), self.__size)
            # To print a covariance matrix, the number of points must be
            # greater than order + 2
            if deg + 2 < self.__size:
                p, cov = np.polyfit(xval, yval, deg, cov=True)
                cov = np.diag(cov)
            else:
                p = np.polyfit(xval, yval, deg, cov=False)
                cov = "not generated"
            f = np.poly1d(p)
            plt.plot(xhat, f(xhat), "r-", label="fit")
            print("covariance: {}".format(cov))
        elif fitfunc is not None:
            popt, pcov = curve_fit(fitfunc, xval, yval)
            plt.plot(xval, fitfunc(xval, *popt), 'r-', label="fit")

        if expected is not None:
            plt.plot(xval, expected, "b.", label="expected")
        
        plt.legend()
            
        # Make any LaTeX in the labels visible
        xstr = enter_mathmode(self.__xlabel)
        ystr = enter_mathmode(self.__ylabel)
        
        plt.xlabel(xstr)
        plt.ylabel(ystr)
        
        plt.savefig(filename)