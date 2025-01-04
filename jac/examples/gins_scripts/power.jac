import:py from math { exp }
import:py from time { sleep }
# Data structure representing system configuration
glob system_config: Dict[str, Union[int, str, float]] = {
    'base_load': 1000,    # Base power load in watts
    'min_duration': 10,   # Minimum valid duration in minutes
    'mode': 'active',
    'time_step': 0,       # Track progression of simulation
    'reference_delta': 200 # Reference power delta for normalization
};

# Function to generate declining power readings
with entry {
    # Create gradually converging power readings
    base: float = system_config['base_load'];
    power_readings: list[float] = [];
    time_periods: list[int] = [];
    reference_power: float = base + 200;# Reference power for normalization

    # Generate 200 readings that gradually approach base_load
    for i in range(200) {
        # Power gradually approaches base_load (1000W)
        delta: float = 200.0 * exp(-0.5 * i);# Slower decay for better visualization
        current_power: float = base + delta;
        power_readings.append(current_power);

        # Time periods increase linearly
        time_periods.append(15 + i * 2);
    }

    # Initialize results storage

    efficiency_metrics: list = [];
    total_operational_time: int = 0;

    PROGRAM_INPUT = power_readings;

    # Process each power reading with different execution paths
    for (idx, current_power) in enumerate(power_readings) {
        if system_config['mode'] != 'active' {
            continue;
        }

        duration: int = time_periods[idx];
        if duration < system_config['min_duration'] {
            continue;
        }

        # Track simulation progression

        system_config['time_step'] += 1;

        power_delta: float = current_power - system_config['base_load'];

        # Introduce different execution paths based on time_step
        if system_config['time_step'] > 50 {
            diminishing_reference: float = power_delta * 2;  # Reference point approaches zero with power_delta
            power_utilization: float = power_delta / diminishing_reference;  # Approaches 0.5, then unstable
        } else {
            # Original calculation path for first 10 steps
            power_utilization: float = power_delta / system_config['reference_delta'];
        }
        period_efficiency: float = power_utilization * (duration / max(time_periods)) * 100;

        efficiency_metrics.append(period_efficiency);
        total_operational_time += duration;

        # Print current state
        print(
            f"Step {system_config['time_step']}: Power={current_power}W, " + f"Delta from base={current_power - system_config['base_load']}W"
        );
        sleep(0.25);
    }

    # Calculate final metrics if no error occurred

    average_efficiency: float = sum(efficiency_metrics) / len(efficiency_metrics) if efficiency_metrics else 0;
    operational_hours: float = total_operational_time / 60;
    print(
        f"System Analysis Complete - Efficiency: {average_efficiency}%"
    );

}
