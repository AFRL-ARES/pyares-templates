#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# *** Simple Random With Exclusion Planner ***
"""
This planner implements a random with exclusion search method.

The main functionality involves finding "Nearest Neighbors" in order to calculate a radius at which we want to exclude any new points.
The script will find N (5 by default) defined nearest neighbors and use the distances to find the radius. This in the 2d case, creates a circle of sorts
around all existing points that are "exclusion" zones for new randomly generated points.

The specific calculation checks for the closest existing point to the newly generated point, and uses this distance to compare with the exclusion radius.
every 100 points generated that fail this check will continue to reduce the radius requirement. This allows for greater experiment count to first attempt
do adequate random exploration over the experiment space.
"""
# -----------------------------------------------------------------------------
# 1. Import Necessary Modules
# -----------------------------------------------------------------------------
from PyAres import AresPlannerService, PlanRequest, PlanResponse, AresDataType, Outcome # Required for the PyAres Service
from scipy.spatial.distance import cdist
from sklearn.neighbors import NearestNeighbors
import numpy as np
import traceback

# -----------------------------------------------------------------------------
# 2. Define Your Service Details 
# -----------------------------------------------------------------------------
name = "Random_w/_excl_Planner"
description = "Generates random values within specificed bounds outside of regions of exlclusion"
version = "1.0.0" # Planner version numbering that will be reported to ARES OS.
port =	7306 # The network port your Planner will use to communicate with ARES OS.
local = True # Whether to use localhost or not

# ----------------------------------------------------------------------------- 
# 3. Define the Planning Logic
# -----------------------------------------------------------------------------
# Normalization functions can be predefined to make repeated use easier.
def normalize(value, min_val, max_val):
	if (max_val - min_val) == 0:
		return 0.5 # Avoid division by zero if min and max are the same
	return (value - min_val) / (max_val - min_val)

def denormalize(norm_value, min_val, max_val):
	return norm_value * (max_val - min_val) + min_val
	
# The main "math" behind the planning process. In this case we have a nearest neighbors algorithm, as well as the planning portion to calculate the next value
def find_nearest_neighbors(points, n_neighbors):
	num_points = len(points)
	if num_points <= 1:
		return 1.0 # Default radius if only one point or none

	# Ensure n_neighbors is not more than the number of points available to compare against
	if num_points <= n_neighbors:
		n_neighbors = num_points - 1

	if n_neighbors <= 0:
		# Fallback if we only have 1 or 2 points
		return np.mean(cdist(points, points)) if num_points > 1 else 1.0
	
	# n_neighbors+1 because a point's nearest neighbor is itself
	distances, _ = NearestNeighbors(n_neighbors=int(n_neighbors + 1)).fit(points).kneighbors(points)
	# Exclude the first column (distance to self, which is 0)
	return distances[:, 1:].mean()

def plan(sorted_matrix, seed, n_neighbors):
	sphere_radius = find_nearest_neighbors(sorted_matrix, n_neighbors) / 2
	rng = np.random.default_rng(seed=seed)
	num_params = sorted_matrix.shape[1]

	# Handle the very first run where there is no matrix
	if num_params == 0:
		return rng.uniform(0, 1, size=len(request.parameters)) # This part is illustrative, size needs to be known

	for i in range(10000):
		random_point = rng.uniform(0, 1, size=num_params)
		# If no points to compare against or if point is outside exclusion zone
		if len(sorted_matrix) == 0 or min(cdist(sorted_matrix, [random_point])) >= sphere_radius:
			break
		# Periodically reduce radius to prevent getting stuck
		if i > 0 and i % 100 == 0:
			sphere_radius *= 0.90 # Exponential decay

	return random_point

# -----------------------------------------------------------------------------
# 4. Define Planner Function.
# -----------------------------------------------------------------------------
# This function handles the "plumbing" of passing data to an from the ARES PlanRequest to the actual planning logic
def planner(request: PlanRequest) -> PlanResponse:
	param_names, param_vals, all_values_matrix = [], [], []
	try:
		seed = int(request.settings.get('Seed'))
		n_neighbors = request.settings.get('N Nearest Neighbors')
		rng = np.random.default_rng(seed=seed)
		
		for param in request.parameters:
			if param.is_result or not param.is_planned:
				continue
			param_names.append(param.name)
			
			# Compiling all previously stored histoy
			planned_history = [v.planned_value for v in param.param_history]
			
			# If there is no planned history, generate a random value within the bounds and returns that
			if len(planned_history) == 0:
				param_vals.append(rng.uniform(param.minimum_value,param.maximum_value))
			else:
				# Data is pre-normalized and then added to the matrix in order to make the math easier later.
				values = [normalize(v, param.minimum_value, param.maximum_value) for v in planned_history]
				all_values_matrix.append(values)
		if all_values_matrix:
			sorted_matrix = np.vstack(all_values_matrix).T
			plan_seed = rng.integers(0, 2*32 - 1)
			param_vals_norm = plan(sorted_matrix,plan_seed, n_neighbors)
		
			for i, param in enumerate(request.parameters):
				if param.is_result or not param.is_planned:
					continue
				param_vals.append(denormalize(param_vals_norm[i], param.minimum_value, param.maximum_value))
		
		response = PlanResponse(parameter_names=param_names, parameter_values=param_vals ,outcome=Outcome.SUCCESS)
		# NOTE: PyAres versions > 0.4.0 support assigning values using a dictionary structure, e.g., PlanResponse(parameter_data={param1_key:param1_value,...})
	except Exception as e:
		# This forces the full error stack to print in your terminal
		print("\n--- PLANNER CRASHED ---")
		traceback.print_exc() 
		print("-----------------------\n")
		
		# This safely passes the error string back to the ARES OS UI
		return PlanResponse(parameter_names=parameter_names,parameter_values=[-1]*len(parameter_names),outcome=Outcome.FAILURE)
		
	return response

# -----------------------------------------------------------------------------
# 4. Configure and Start Analyzer Service.
# -----------------------------------------------------------------------------
if __name__ == "__main__":

	planner_service = AresPlannerService(planner,
										 name,
										 version,
										 description, 
										 use_localhost=local, 
										 port=port)


	planner_service.add_supported_type(AresDataType.NUMBER)

	# Note that setting names are case sensitive in this example
	planner_service.add_setting("Seed", AresDataType.NUMBER, default_value=1111) 
	planner_service.add_setting("N Nearest Neighbors", AresDataType.NUMBER, default_value=5) 
	try:
		planner_service.start()
	except Exception as e:
		print(f"An Exception Occured: {e}")
	except KeyboardInterrupt:
		print(f"\nShutting Down PyAres Service...")
	finally: # Use the finally block for things like saving/closing any active data files, closing remote connections, etc.
		pass