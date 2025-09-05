from scipy.optimize import curve_fit
import json
import math
import matplotlib.pyplot as plt
import numpy as np

# load the json data from ../data/isoflops_curves.json
with open('../data/isoflops_curves.json', 'r') as f:
    data = json.load(f)
    # load it into a dictionary 


# Data is a list of dictionaries with the following keys:
# - parameters: int
# - compute_budget: float
# - final_loss: float

# Now we'll go through the dictionary and we will build out a training set
# of x = parameters that achieved minimal loss., y = compute budget

# Thus each compute budget can appear at most once
# and we will only keep the pair that achieves minimal loss. 

# let's first build a dictionary of compute budget to (params, min_loss)
compute_budget_to_min_loss_dict = {}
for item in data:
    if item["compute_budget"] not in compute_budget_to_min_loss_dict:
        compute_budget_to_min_loss_dict[item["compute_budget"]] = []
    compute_budget_to_min_loss_dict[item["compute_budget"]].append((item["parameters"], item["final_loss"]))

# Now we sort so that the min loss is the first element
for key in compute_budget_to_min_loss_dict:
    compute_budget_to_min_loss_dict[key].sort(key=lambda x: x[1])

training_set_parameters = []
print("Training set (N, C):")
for key in compute_budget_to_min_loss_dict:
    training_set_parameters.append((math.log(key), math.log(compute_budget_to_min_loss_dict[key][0][0])))
    print(key,compute_budget_to_min_loss_dict[key][0][0])

def log_log_fit(x, a, b):
    return a * x + b

popt_parameters, pcov_parameters = curve_fit(log_log_fit, [x[0] for x in training_set_parameters], [x[1] for x in training_set_parameters])
print("N = b*C^a")
print(f"N = {math.exp(popt_parameters[1])}*C^{popt_parameters[0]}")
print("Optimal exponent: ", popt_parameters[0])
print("Multiplicative factor: ", math.exp(popt_parameters[1]))
print("Predicted optimal dataset size for $10^{23}$ FLOPs: ", math.exp(popt_parameters[1]) * (10**(24* popt_parameters[0]))/10**9, "T")
print("Predicted optimal dataset size for $10^{24}$ FLOPs: ", math.exp(popt_parameters[1]) * (10**(24* popt_parameters[0]))/10**9, "T")

training_set_data = []
print("Training set (D, C):")
for key in compute_budget_to_min_loss_dict:
    training_set_data.append((math.log(key),math.log(key/6/compute_budget_to_min_loss_dict[key][0][0])))
    print(key,key/6/compute_budget_to_min_loss_dict[key][0][0]) # D = N/6C
popt_data, pcov_data = curve_fit(log_log_fit, [x[0] for x in training_set_data], [x[1] for x in training_set_data])
print("D = b*C^a")
print(f"D = {math.exp(popt_data[1])}*C^{popt_data[0]}")
print("Optimal exponent: ", popt_data[0])
print("Multiplicative factor: ", math.exp(popt_data[1]))
print("Predicted optimal dataset size for $10^{23}$ FLOPs: ", math.exp(popt_data[1]) * (10**(24* popt_data[0]))/10**9, "B")
print("Predicted optimal dataset size for $10^{24}$ FLOPs: ", math.exp(popt_data[1]) * (10**(24* popt_data[0]))/10**9, "B")



fig, axs = plt.subplots(1, 2, figsize=(10, 8))
axs[0].set_title("Chinchilla Isoflops Curves (Parameters)")
axs[0].set_xlabel("Compute Budget")
axs[0].set_ylabel("Parameters")
axs[0].set_xlim(min([math.exp(x[0]) for x in training_set_parameters]),  np.float64(1e24))


# Create extended x range from min training data to 1e24
x_min = min([x[0] for x in training_set_parameters])
x_max = np.log(1e24)
x_range = np.linspace(x_min, x_max, 100)
log_log_curve_y_parameters = popt_parameters[0] * x_range + popt_parameters[1]

axs[0].scatter([math.exp(x[0]) for x in training_set_parameters], [math.exp(x[1]) for x in training_set_parameters])
axs[0].loglog(np.exp(x_range), np.exp(log_log_curve_y_parameters))


# Create extended x range from min training data to 1e24
x_min_data = min([x[0] for x in training_set_data])
x_max_data = np.log(1e24)
x_range_data = np.linspace(x_min_data, x_max_data, 100)
log_log_curve_y_data = popt_data[0] * x_range_data + popt_data[1]

axs[1].scatter([math.exp(x[0]) for x in training_set_data], [math.exp(x[1]) for x in training_set_data])
axs[1].loglog(np.exp(x_range_data), np.exp(log_log_curve_y_data))
axs[1].set_title("Chinchilla Isoflops Curves (Data)")
axs[1].set_xlabel("log(Compute Budget)")
axs[1].set_ylabel("log(Data)")
axs[1].set_xlim(math.exp(x_min_data),  np.float64(1e24))

plt.show()

