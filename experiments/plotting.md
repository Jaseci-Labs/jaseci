## Load Test Results Analysis

This script analyzes load test results stored in JSON files and generates bar plots for different metrics.

### Prerequisites

- Python 3.x
- NumPy
- Matplotlib

### Usage

1. Place the load test result JSON files in a folder.
    ### Input Data Format

    The load test result JSON files should follow the following structure:

    ```json
    {
        "restaurant_chatbot": {
            "evaluation-mem-4096": {
                "walker_level": {
                    // JSON data specific to the "evaluation-mem-4096" configuration and "walker_level" metric
                }
            },
            "all_remote": {
                "walker_level": {
                    // JSON data specific to the "all_remote" configuration and "walker_level" metric
                }
            },
            "all_local": {
                "walker_level": {
                    // JSON data specific to the "all_local" configuration and "walker_level" metric
                }
            }
        }
    }
2. The folder structure should follow the following format:

```
<folder_path>/
├── <application_name>/
│ ├── run1/
│ │ └── <application_name>-<node_mem>.json
│ ├── run2/
│ │ └── <application_name>-<node_mem>.json
│ └── ...
├── <application_name>/
│ ├── run1/
│ │ └── <application_name>-<node_mem>.json
│ ├── run2/
│ │ └── <application_name>-<node_mem>.json
│ └── ...
└── ...
```

3. Run the script with the folder path as a command-line argument:

    ```
    python load_test_analysis.py <folder_path>
    ```

    Replace `<folder_path>` with the path to the folder containing the load test result JSON files.

4. The script will process the files and generate average bar plots for each metric and application.
5. The plots will be saved as PDF files in the master folder.

### Files

- `plot_money.py`: The main script that analyzes load test results and generates plots.

### Metrics

The script generates bar plots for the following metrics:

- Average Latency Speedup (X)
- Throughput Speedup (X)
- 99th Latency Speedup (X)

## Applications

The script analyzes load test results for the following applications:

### Local, Remote, and Eval Config:

- Sentence Pairing
- Discussion Analysis
- Restaurant Chatbot

### Remote and Eval Config Only:

- Flight Chatbot
- Zeroshot FAQ Bot
- Flow Analysi.
- Virtual Assistant

Please note that the script analyzes load test results for different configurations, including local, remote, and eval. The applications listed under "Local, Remote, and Eval Config" were tested in all configurations, while the applications listed under "Remote and Eval Config Only" were tested only in the remote and eval configurations.

### Output

The script generates bar plots for each metric and application. The plots are saved as PDF files with the following naming convention:
```
<folder_path>/
├── <application_name>/
    ├── <application_name>_<metric_name>.pdf
└── ...
```

