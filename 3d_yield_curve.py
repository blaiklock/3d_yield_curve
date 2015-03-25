import Quandl
import numpy as np
from mpl_toolkits.mplot3d import axes3d
import matplotlib.dates as dates
import matplotlib.ticker as ticker
import matplotlib.pyplot as plt

def format_date(x, pos=None):
    return dates.num2date(x).strftime('%Y-%m-%d')

data = Quandl.get('USTREASURY/YIELD', returns='numpy', trim_start="2009-01-02")

header = []
for name in data.dtype.names[1:]:
    maturity = float(name.split(" ")[0])
    if name.split(" ")[1] == 'Mo':
        maturity = maturity / 12
    header.append(maturity)

x_data = []
y_data = []
z_data = []

for dt in data.Date:
    dt_num = dates.date2num(dt)
    x_data.append([dt_num for i in range(len(data.dtype.names)-1)])

for row in data:
    y_data.append(header)
    z_data.append(list(row.tolist()[1:]))

x = np.array(x_data, dtype='f')
y = np.array(y_data, dtype='f')
z = np.array(z_data, dtype='f')

fig = plt.figure(figsize=(15, 10))
ax = fig.add_subplot(111, projection='3d')
ax.plot_surface(x, y, z, rstride=10, cstride=1, cmap='Blues', vmin=np.nanmin(z), vmax=np.nanmax(z))
ax.set_title('US Treasury Yield Curve')
ax.set_ylabel('Maturity')
ax.set_zlabel('Yield')

ax.w_xaxis.set_major_formatter(ticker.FuncFormatter(format_date))
for tl in ax.w_xaxis.get_ticklabels():
    tl.set_ha('right')
    tl.set_rotation(15)

plt.show()
