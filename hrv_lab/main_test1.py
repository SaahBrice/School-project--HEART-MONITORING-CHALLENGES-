import argparse
import os
import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objs as go
import plotly.express as px
from plotly.subplots import make_subplots
from plot import plot_series, plot_ecg_signal

parser = argparse.ArgumentParser()

parser.add_argument('-epoch_folder', '--epoch_folder', type=str, default='./epoch_1/')
parser.add_argument('-window_duration', '--window_duration', type=float, default=240.0)
parser.add_argument('-window_shift', '--window_shift', type=float, default=60.0)
parser.add_argument('-extract_ecg', '--extract_ecg', dest='extract_ecg', action='store_true')
parser.add_argument('-compute_nni', '--compute_nni', dest='compute_nni', action='store_true')
parser.add_argument('-compute_hrv', '--compute_hrv', dest='compute_hrv', action='store_true')
parser.add_argument('-plot_ecg', '--plot_ecg', dest='plot_ecg', action='store_true')
parser.add_argument('-plot_nni', '--plot_nni', dest='plot_nni', action='store_true')
parser.add_argument('-plot_hrv', '--plot_hrv', dest='plot_hrv', action='store_true')
parser.add_argument('-plot_comparison', '--plot_comparison', dest='plot_comparison', action='store_true')

if __name__ == '__main__':
    
    args = vars(parser.parse_args())
    
    epoch_folder = args['epoch_folder']
    window_duration = args['window_duration']
    window_shift = args['window_shift']
    extract_ecg = args['extract_ecg']
    compute_nni = args['compute_nni']   
    compute_hrv = args['compute_hrv']
    plot_ecg = args['plot_ecg']
    plot_nni = args['plot_nni']  
    plot_hrv = args['plot_hrv']
    plot_comparison = args['plot_comparison']
        
    if plot_ecg:
        ecg_times_path = os.path.join(epoch_folder, 'ecg_times.npz')
        ecg_path = os.path.join(epoch_folder, 'ecg.npz')
        
        if os.path.exists(ecg_times_path) and os.path.exists(ecg_path):
            ecg_times = np.load(ecg_times_path)['data']
            ecg = np.load(ecg_path)['data']
            plot_ecg_signal(ecg_times, ecg, 'ECG [mV]')
        else:
            print("ECG data files not found.")
        
    if compute_nni:
        qrs_peak_times_path = os.path.join(epoch_folder, 'qrs_peak_times.npz')
        
        if os.path.exists(qrs_peak_times_path):
            qrs_peak_times = np.load(qrs_peak_times_path)['data']        
            nn_intervals = qrs_peak_times[1:] - qrs_peak_times[:-1]
            nni_times = qrs_peak_times[:-1]
            
            # Save original NN intervals
            original_nn_intervals = nn_intervals.copy()
            original_nni_times = nni_times.copy()
            
            # Filter out NN intervals larger than 1.5 seconds
            nni_times = nni_times[nn_intervals <= 1.5]
            nn_intervals = nn_intervals[nn_intervals <= 1.5]
            
            subsequent_differences = np.abs(nn_intervals[1:] - nn_intervals[:-1])
            sd_times = nni_times[:-1]
            
            np.savez_compressed(os.path.join(epoch_folder, 'nni_times.npz'), data=nni_times)
            np.savez_compressed(os.path.join(epoch_folder, 'nni.npz'), data=nn_intervals)
            np.savez_compressed(os.path.join(epoch_folder, 'sd_times.npz'), data=sd_times)
            np.savez_compressed(os.path.join(epoch_folder, 'sd.npz'), data=subsequent_differences)
        else:
            print("QRS peak times file not found.")
        
if plot_nni:
    nni_path = os.path.join(epoch_folder, 'nni.npz')
    sd_path = os.path.join(epoch_folder, 'sd.npz')
    nni_times_path = os.path.join(epoch_folder, 'nni_times.npz')
    sd_times_path = os.path.join(epoch_folder, 'sd_times.npz')
    
    if os.path.exists(nni_path) and os.path.exists(sd_path) and os.path.exists(nni_times_path) and os.path.exists(sd_times_path):
        nn_intervals = np.load(nni_path)['data']
        subsequent_differences = np.load(sd_path)['data']
        nni_times = np.load(nni_times_path)['data']
        sd_times = np.load(sd_times_path)['data']
        
        fig = make_subplots(
            rows=3, cols=2, 
            column_widths=[0.8, 0.2],
            subplot_titles=('NN Intervals', 'Subsequent Differences', 'Seizure Detection')
        )

        fig.add_trace(go.Scatter(x=nni_times, y=nn_intervals, mode='lines', name='NNI'), row=1, col=1)
        fig.add_trace(go.Scatter(x=sd_times, y=subsequent_differences, mode='lines', name='SD'), row=2, col=1)

        mean_nni = np.mean(nn_intervals)
        std_nni = np.std(nn_intervals)
        threshold = mean_nni - 4 * std_nni

        seizure_indices = np.where(nn_intervals < threshold)[0]
        seizure_times = nni_times[seizure_indices]

        

        fig.add_trace(go.Scatter(x=nni_times, y=nn_intervals, mode='lines', name='NNI'), row=3, col=1)
        for index in seizure_indices:
            fig.add_trace(go.Scatter(x=[nni_times[index]], y=[nn_intervals[index]], mode='markers', marker=dict(color='red'), showlegend=False), row=3, col=1)



        fig.update_layout(height=900, width=1200, title_text="NN Intervals and Seizure Detection")
        fig.update_xaxes(title_text="Time [s]", row=1, col=1)
        fig.update_xaxes(title_text="Time [s]", row=2, col=1)
        fig.update_xaxes(title_text="Time [s]", row=3, col=1)
        fig.update_yaxes(title_text="NNI [s]", row=1, col=1)
        fig.update_yaxes(title_text="SD [s]", row=2, col=1)
        fig.update_yaxes(title_text="NNI [s]", row=3, col=1)

        fig.show()
    else:
        print("NNI or SD data files not found.")

        
    if compute_hrv:
        nni_path = os.path.join(epoch_folder, 'nni.npz')
        nni_times_path = os.path.join(epoch_folder, 'nni_times.npz')
        
        if os.path.exists(nni_path) and os.path.exists(nni_times_path):
            nn_intervals = np.load(nni_path)['data']
            nni_times = np.load(nni_times_path)['data']
            
            window_times = []    
            avg_nn_intervals = []
            std_nn_intervals = []
            
            last_time = nni_times[-1]
            
            current_time = 0
            next_time = window_duration
            
            while next_time < last_time:
                window_times.append(current_time)
                
                current_time_index = np.argmin(np.abs(current_time - nni_times))
                next_time_index = np.argmin(np.abs(next_time - nni_times))
                
                window_nn_intervals = nn_intervals[current_time_index:next_time_index]
                
                avg_nn_intervals.append(np.mean(window_nn_intervals))
                std_nn_intervals.append(np.std(window_nn_intervals))
                
                current_time += window_shift
                next_time += window_shift
                
            np.savez_compressed(os.path.join(epoch_folder, 'window_times.npz'), data=window_times)
            np.savez_compressed(os.path.join(epoch_folder, 'avg_nn_intervals.npz'), data=avg_nn_intervals)
            np.savez_compressed(os.path.join(epoch_folder, 'std_nn_intervals.npz'), data=std_nn_intervals)
        else:
            print("NNI data files not found. Please compute NNI first.")
    
        
    if plot_hrv:
        window_times_path = os.path.join(epoch_folder, 'window_times.npz')
        avg_nn_intervals_path = os.path.join(epoch_folder, 'avg_nn_intervals.npz')
        std_nn_intervals_path = os.path.join(epoch_folder, 'std_nn_intervals.npz')
        
        if os.path.exists(window_times_path) and os.path.exists(avg_nn_intervals_path) and std_nn_intervals_path:
            window_times = np.load(window_times_path)['data']
            avg_nn_intervals = np.load(avg_nn_intervals_path)['data']
            std_nn_intervals = np.load(std_nn_intervals_path)['data']
            
            fig = make_subplots(rows=3, cols=1, subplot_titles=('HR [beat/min]', 'AVNN [s]', 'SDNN [s]'))

            fig.add_trace(go.Scatter(x=window_times, y=60 / np.asarray(avg_nn_intervals), mode='lines', name='HR'), row=1, col=1)
            fig.add_trace(go.Scatter(x=window_times, y=avg_nn_intervals, mode='lines', name='AVNN'), row=2, col=1)
            fig.add_trace(go.Scatter(x=window_times, y=std_nn_intervals, mode='lines', name='SDNN'), row=3, col=1)

            fig.update_layout(height=900, width=1200, title_text="HRV Metrics")
            fig.update_xaxes(title_text="Time [s]")
            fig.update_yaxes(title_text="HR [beat/min]", row=1, col=1)
            fig.update_yaxes(title_text="AVNN [s]", row=2, col=1)
            fig.update_yaxes(title_text="SDNN [s]", row=3, col=1)

            fig.show()
        else:
            print("HRV data files not found. Please compute HRV first.")
    
    if plot_comparison and compute_nni:
        # Identify and filter out noise
        noise_threshold = 0.9
        filtered_indices = [i for i, interval in enumerate(original_nn_intervals) if interval <= noise_threshold]
        
        filtered_nni_times = original_nni_times[filtered_indices]
        filtered_nn_intervals = original_nn_intervals[filtered_indices]

        removed_indices = [i for i, interval in enumerate(original_nn_intervals) if interval > noise_threshold]
        removed_nni_times = original_nni_times[removed_indices]
        removed_nn_intervals = original_nn_intervals[removed_indices]

        # Calculate statistics for filtered NN intervals
        filtered_mean_nni = np.mean(filtered_nn_intervals)
        filtered_std_nni = np.std(filtered_nn_intervals)
        

        plt.figure()

        # Plot original NN intervals
        plt.subplot(3, 1, 1)
        plt.plot(original_nni_times, original_nn_intervals, label='Original NNI')
        plt.xlabel('Time [s]')
        plt.ylabel('NNI [s]')
        plt.legend()
        plt.title('Original NN Intervals')

        # Plot filtered NN intervals
        plt.subplot(3, 1, 2)
        plt.plot(filtered_nni_times, filtered_nn_intervals, label='Filtered NNI', color='green')
        plt.xlabel('Time [s]')
        plt.ylabel('NNI [s]')
        plt.legend()
        plt.title('Filtered NN Intervals')

        # Plot removed NN intervals
        plt.subplot(3, 1, 3)
        plt.plot(removed_nni_times, removed_nn_intervals, label='Removed NNI', color='red')
        plt.xlabel('Time [s]')
        plt.ylabel('NNI [s]')
        plt.legend()
        plt.title('Removed NN Intervals')

        plt.tight_layout()
        plt.show()
