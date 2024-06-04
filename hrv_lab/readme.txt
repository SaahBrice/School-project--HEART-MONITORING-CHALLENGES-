# ECG Analysis and HRV Computation Script

## Overview

This project is is a homework given where i am to analyze ECG data and compute Heart Rate Variability (HRV) metrics and detect possible instances of seizures. 
The script offers various functionalities such as extracting ECG signals, computing NN intervals, analyzing HRV metrics, and visualizing the results. 
The script is modular, allowing users to specify which operations to perform using command-line arguments. This script was given as homework file and modifications was carried out by me to
enable seizure detection and possiby, represent in a plot.


## Dependencies

The script requires the following Python packages:
- `argparse`
- `os`
- `numpy`
- `matplotlib`
- `plotly`


## Usage

To run the script, use the command line with appropriate arguments. Below are the arguments you can specify:


- `-epoch_folder, --epoch_folder`: The folder containing epoch data files (default: './epoch_1/').
- `-window_duration, --window_duration`: Duration of the window for HRV computation in seconds (default: 240.0).
- `-window_shift, --window_shift`: Shift duration between windows for HRV computation in seconds (default: 60.0).
- `-extract_ecg, --extract_ecg`: Flag to extract and plot ECG signals.
- `-compute_nni, --compute_nni`: Flag to compute NN intervals from QRS peak times.
- `-compute_hrv, --compute_hrv`: Flag to compute HRV metrics from NN intervals.
- `-plot_ecg, --plot_ecg`: Flag to plot ECG signals.
- `-plot_nni, --plot_nni`: Flag to plot NN intervals and detect potential seizures.
- `-plot_hrv, --plot_hrv`: Flag to plot HRV metrics.
- `-plot_comparison, --plot_comparison`: Flag to plot a comparison of original and filtered NN intervals.

## Example Commands

```sh
python script.py --compute_nni --plot_nni
```


### Seizure Detection

As earlier mentionned, the script includes a feature to detect potential seizures based on the NN intervals (NNI).
Seizure detection is performed by identifying unusually short NN intervals, which can be indicative of abnormal heart activity.

#### Algorithm Explanation

The algorithm for seizure detection works as follows:

1. **Compute NN Intervals**: NN intervals are calculated as the time difference between consecutive QRS peaks.
2. **Calculate Mean and Standard Deviation**: The mean (average) and standard deviation of the NN intervals are computed.
3. **Set a Threshold**: A threshold is defined as the mean NN interval minus a multiple of the standard deviation. This threshold helps in identifying intervals that are significantly shorter than the average.
4. **Identify Seizure Points**: NN intervals that fall below the threshold are flagged as potential seizure points.


#### Modifying the Threshold

The threshold for seizure detection is calculated as:

\[ \text{threshold} = \text{mean\_nni} - k \times \text{std\_nni} \]

where \( k \) is a multiplicative factor. 
In the provided code, \( k \) is set to 4 by default. To modify the sensitivity of the seizure detection, you can change this multiplicative factor:

- **Increase \( k \)**: To make the seizure detection more stringent (fewer false positives), increase the value of \( k \). 
    This will lower the threshold, resulting in fewer intervals being flagged as potential seizures.
- **Decrease \( k \)**: To make the seizure detection more sensitive (more potential seizures detected), decrease the value of \( k \). 
    This will raise the threshold, resulting in more intervals being flagged as potential seizures.

#### Example

To modify the multiplicative factor from 4 to 3, change the following line of code:
```python
threshold = mean_nni - 4 * std_nni  # Original line
```
to
```python
threshold = mean_nni - 3 * std_nni  # Modified line
```

This change will make the seizure detection algorithm more sensitive, potentially detecting more seizure events. 
Adjusting the multiplicative factor allows you to tailor the detection sensitivity based on your specific requirements and the characteristics of your dataset.

##Conclusion

Conclusion
This script serve many functions amongst which it can detect potential seizures, leveraging abnormal NN intervals to identify critical events in cardiac activity, as was requested in the assignment.

By employing a thresholding algorithm based on the mean and standard deviation of NN intervals, the script highlights intervals significantly shorter than the norm,
 indicative of potential seizure activity. 
Moreover, the script's flexibility allows users to fine-tune the sensitivity of the seizure detection algorithm by adjusting the multiplicative factor in the threshold calculation. 