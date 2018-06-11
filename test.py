from physica import dataset

x = np.linspace(0, 50, 100)
yhat = list(3*x**2)
y = list(np.random.normal(3*x**2, 2))
x = list(x)

def fit(x,a,b,c):
    return a*(x+b)**2+c

data = Dataset(x, y)

data.plot(expected=yhat, fitfunc=fit)