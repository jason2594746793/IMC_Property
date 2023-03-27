import matplotlib.pyplot as plt
import math
import re
import pylab
# Create empty lists to store data
times = []
actions = []
amounts = []
prices = []

# Open the log file
with open("r1algo3.log", "r") as file:
    currentTime = 0
    # Loop through each line in the file
    for line in file:
        # Split the line into its components
        components = line.strip().split()
        # Check if the line contains data
        if len(components) == 4:
            # Add the time, action, amount, and price to their respective lists
            times.append(int(components[0]))
            actions.append(components[1])
            amounts.append(int(components[2][:-1]))
            prices.append(int(components[3]))
            currentTime = int(components[0])
        elif len(components) == 3:
            times.append(currentTime)
            actions.append(components[0])
            amounts.append(int(components[1][:-1]))
            prices.append(int(components[2]))

# Calculate the profit at each time point
profits = []
money_spend = 0
for i in range(len(times)):
    if actions[i] == "BUY":
        money_spend += amounts[i] * prices[i]
    elif actions[i] == "SELL":
        money_spend -= amounts[i] * prices[i]
    profits.append(-money_spend)

# Plot the profit with time graph
new_list = range(math.floor(min(profits)), math.ceil(max(profits))+1)

plt.plot(times, profits)
plt.ylim(-10000000, 10000000)
plt.xlabel("Time")
plt.ylabel("Profit")
plt.title("Profit with Time")
plt.show()
