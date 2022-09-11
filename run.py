# Your code goes here.
# You can delete these comments, but do not change the name of this file
# Write your code to expect a terminal of 80 characters wide and 24 rows high

import plotext as pt

SCALE = 0.85

y_vals = [1, 2, 3, 3, 4, 5, 6, 7, 8]
x_vals = [1, 2, 3, 3, 4, 5, 6, 7, 8]

pt.bar(x_vals, y_vals)
pt.title('TEST')

pt.plot_size(80 * SCALE, 24 * SCALE)
pt.show()
# print(pt.ts())
