1. Please, copy local_config_exemple.json --> local_config.json and adapt value to your local machine...

2. For each simulation, you are expected to increment the variable "id" in scan_lenth.m
3. To plot the result using python, use the module "load_simu.py":
   	from load_simu import load
	simu = load(id)
	simu.plot(legend=['roc_depth', 'input_waist'])