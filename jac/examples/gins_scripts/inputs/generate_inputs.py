import numpy as np
import os
import random

current_directory = os.path.dirname(os.path.abspath(__file__))
output_file = os.path.join(current_directory,'test_predict.txt')


# mean = 92
# std_dev = 9
# num_samples = 100
# skewness = 5
# random_numbers = list(np.random.normal(mean,std_dev, num_samples))
# w_str = "\n".join(str(round(num,3)) for num in random_numbers)

num_samples = 1000
start_value = 99
end_avg = 105

# Initialize storage for sensor data
sensor_data = []

# Calculate the amount to increment each value to reach the desired average
increment = (end_avg - start_value) / num_samples

current_value = start_value
for _ in range(num_samples):
    # Add some noise to make the data more realistic
    noise = random.uniform(-0.7, 0.5)
    sensor_value = current_value + noise
    sensor_data.append(sensor_value)
    
    # Update current value towards the end_avg
    current_value += increment

# Write data to output file
with open(output_file, 'w') as file:
    for value in sensor_data:
        file.write(f"{value:.2f}\n")