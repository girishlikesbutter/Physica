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
        table = """\\begin{tabular}{cc}
    \\toprule
    {x} & {y} \\\\
    \\midrule""".format(x=self.__xlabel, y=self.__ylabel, tabular="{tabular}", cc="{cc}")
        for i in range(0, self.__size):
            table = table + """
    {} & {} \\\\""".format(self.__x[i], self.__y[i])
        
        table = table + """
    \\bottomrule
\\end{tabular}"""
        return table
    
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

    def plot(self, fmt="g."):
        xval = [x.n if type(x) == uncertainties.core.Variable else x for x in self.__x]
        yval = [x.n if type(x) == uncertainties.core.Variable else x for x in self.__y]
        uxval = [x.s if type(x) == uncertainties.core.Variable else 0 for x in self.__x]
        uyval = [x.s if type(x) == uncertainties.core.Variable else 0 for x in self.__y]
        
        plt.errorbar(xval, yval, fmt=fmt, xerr=uxval, yerr=uyval)
        
        xstr = self.__xlabel
        if("\\" in self.__xlabel):
            x = self.__xlabel.split(" ")
            bits = []
            for bit in x:
                if "\\" in bit:
                    bit = "${}$".format(bit)
                bits.append(bit)
            xstr = " ".join(bits)
            
        ystr = self.__ylabel
        if("\\" in self.__ylabel):
            y = self.__ylabel.split(" ")
            bits = []
            for bit in y:
                if "\\" in bit:
                    bit = "${}$".format(bit)
                bits.append(bit)
            ystr = " ".join(bits)
        
        plt.xlabel(xstr)
        plt.ylabel(ystr)