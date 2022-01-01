import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import statistics


with open("./data/hv.txt", "r", encoding="utf-8") as f:
    data = [float(i.rstrip("\n")) for i in f]

data = [i for i in data if not i > 100]

median = statistics.median(data2)
mean = statistics.mean(data2)

fig = plt.figure()
gs = gridspec.GridSpec(2, 1, height_ratios=[1, 5])

# Box plot
ax = plt.subplot(gs[0])
ax.set_xticks([i for i in range(0, 101, 10)])
ax.set_title("Historical Volatility(HV) Distribution")
ax.boxplot(data2, vert=False, sym="-")
ax.axes.yaxis.set_visible(False)

# Histgram
ax = plt.subplot(gs[1])
ax.set_ylabel("Frequency")
ax.set_xlabel("HV(%)")
ax.set_yticks([i for i in range(0, 251, 25)])
ax.set_xticks([])
ax.hist(data2, bins=80, histtype="step")
ax.axvline(median, color="k", linestyle="dashed", linewidth=1, label="median")
ax.axvline(mean, color="k", linestyle="dotted", linewidth=1, label="mean")
ax.tick_params(length=0)
ax.legend()
ax.grid()

# plt.show()
fig.savefig("./images/historical_volatility_distribution.png")
