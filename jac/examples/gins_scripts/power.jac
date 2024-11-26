with entry {

# Data structure representing system configuration
system_config = {
    'base_load': 1000,  # Base power load in watts
    'min_duration': 5,  # Minimum valid duration in minutes
    'mode': 'active'
};

# Input data representing power readings
power_readings = [880, 920, 950, 980, 1000];  # Last reading equals base_load
time_periods = [15, 20, 25, 30, 35];

# Initialize results storage
efficiency_metrics = [];
total_operational_time = 0;

# Process each power reading
for (idx, current_power) in enumerate(power_readings){
    if system_config['mode'] != 'active'{
        continue;
    }
    duration = time_periods[idx];
    if duration < system_config['min_duration']{
        continue;
    }
    # This division will fail when current_power equals base_load (1000W)
    # The error is hidden because it's part of a complex formula that looks valid
    power_utilization = (current_power - system_config['base_load']) / (max(power_readings) - system_config['base_load']);
    
    # Complex metric calculation makes the division less obvious
    period_efficiency = power_utilization * (duration / max(time_periods)) * 100;
    
    efficiency_metrics.append(period_efficiency);
    total_operational_time += duration;
}

# Calculate final metrics
average_efficiency = sum(efficiency_metrics) / len(efficiency_metrics) if efficiency_metrics else 0;
operational_hours = total_operational_time / 60;

print(f"System Analysis Complete - Efficiency: {average_efficiency}%");

}