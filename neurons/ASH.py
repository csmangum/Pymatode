
import numpy as np
import matplotlib.pyplot as plt

# Parameters
threshold = 1.0  # Neuron firing threshold
environment_size = 100  # Size of the 1D environment
stimulus_position = 50  # Position of the noxious stimulus
worm_position = 0  # Starting position of the worm
time_steps = 100  # Number of time steps in the simulation

# Initialize ASH neuron and environment
ash_activity = 0.0  # Initial activity level of the ASH neuron

# Simulation
positions = []  # To store the positions of the worm over time
for t in range(time_steps):
    positions.append(worm_position)
    
    # Check for stimulus
    if worm_position == stimulus_position:
        ash_activity += 2.0  # Increase ASH activity due to stimulus
    
    # Update ASH neuron (very simplified)
    if ash_activity >= threshold:
        ash_activity = 0.0  # Reset activity
        worm_position -= 1  # Move worm back (reverse)
    else:
        worm_position += 1  # Move worm forward
    
    # Boundary conditions
    worm_position = max(0, min(worm_position, environment_size - 1))

# Plotting the results
plt.plot(positions)
plt.xlabel("Time")
plt.ylabel("Worm Position")
plt.show()
