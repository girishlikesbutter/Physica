from physica import dataset

data = Dataset([ufloat(1, 0.5),2,3], [4,ufloat(5,3),6], xlabel="\\lambda [m per mile]", ylabel="\\Omega [ohms per steradian]")

data.plot(fmt="r.")