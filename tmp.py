import matplotlib.pyplot as plt
xs = [0, 1, 2]
ys = [2.5, 4, 3]
plt.plot(xs, ys)
for x, y in zip(xs, ys):
    plt.text(x, y, str(x), color="red", fontsize=12)
plt.show()


# import pandas as pd
# import numpy as np
# array=np.array([(11,12),(21,22)])

# df=pd.DataFrame(array)
# df[2]=[33,66]
# print(df)