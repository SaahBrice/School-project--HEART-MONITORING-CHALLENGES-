import argparse
import numpy as np
import matplotlib.pyplot as plt
from plot import plot_series, plot_ecg_signal


parser = argparse.ArgumentParser()

parser.add_argument('-epoch_folder', '--epoch_folder', type=str, default='./epoch_0/')
parser.add_argument('-window_duration', '--window_duration', type=float, default=240.0)
parser.add_argument('-window_shift', '--window_shift', type=float, default=60.0)
parser.add_argument('-extract_ecg', '--extract_ecg', dest='extract_ecg', action='store_true')
parser.add_argument('-compute_nni', '--compute_nni', dest='compute_nni', action='store_true')
parser.add_argument('-compute_hrv', '--compute_hrv', dest='compute_hrv', action='store_true')
parser.add_argument('-plot_ecg', '--plot_ecg', dest='plot_ecg', action='store_true')
parser.add_argument('-plot_nni', '--plot_nni', dest='plot_nni', action='store_true')
parser.add_argument('-plot_hrv', '--plot_hrv', dest='plot_hrv', action='store_true')

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
        
    if plot_ecg:
        
        ecg_times = np.load(epoch_folder + 'ecg_times.npz')['data']
        ecg = np.load(epoch_folder + 'ecg.npz')['data']
        
        plot_ecg_signal(ecg_times, ecg, 'ECG [mV]')
        
    if compute_nni:
        
        qrs_peak_times = np.load(epoch_folder + 'qrs_peak_times.npz')['data']        
        nn_intervals = qrs_peak_times[1:] - qrs_peak_times[:-1]
        nni_times = qrs_peak_times[:-1]
        
        nni_times = np.asarray([qrs_peak_times[x] for x in range(len(nn_intervals)) if nn_intervals[x] < 1.5])
        nn_intervals = np.asarray([nn_intervals[x] for x in range(len(nn_intervals)) if nn_intervals[x] < 1.5])
        
        subsequent_differences = np.abs(nn_intervals[1:] - nn_intervals[:-1])
        sd_times = nni_times[:-1]
        
        np.savez_compressed(epoch_folder + 'nni_times.npz', data=nni_times)
        np.savez_compressed(epoch_folder + 'nni.npz', data=nn_intervals)
        
        np.savez_compressed(epoch_folder + 'sd_times.npz', data=sd_times)
        np.savez_compressed(epoch_folder + 'sd.npz', data=subsequent_differences)
        
    if plot_nni:
        
        nn_intervals = np.load(epoch_folder + 'nni.npz')['data']
        subsequent_differences = np.load(epoch_folder + 'sd.npz')['data']
        nni_times = np.load(epoch_folder + 'nni_times.npz')['data']
        sd_times = np.load(epoch_folder + 'sd_times.npz')['data']
        
        plot_series(nni_times, nn_intervals, 'NNI [s]')        
        plot_series(sd_times, subsequent_differences, 'SD [s]')
        
    if compute_hrv:
        
        nn_intervals = np.load(epoch_folder + 'nni.npz')['data']
        nni_times = np.load(epoch_folder + 'nni_times.npz')['data']
        
        window_times = []    
        avg_nn_intervals = []
        std_nn_intervals = []
        
        last_time = nni_times[-1]
        
        current_time = 0
        next_time = window_duration
        
        while next_time < last_time:
            
            window_times.append(current_time)
            
            current_time_index = np.argmin(np.abs(current_time-nni_times))
            next_time_index = np.argmin(np.abs(next_time-nni_times))
            
            window_nn_intervals = nn_intervals[current_time_index:next_time_index]
            
            avg_nn_intervals.append(np.mean(window_nn_intervals))
            std_nn_intervals.append(np.std(window_nn_intervals))
            
            current_time += window_shift
            next_time += window_shift
            
        np.savez_compressed(epoch_folder + 'window_times.npz', data=window_times)
        np.savez_compressed(epoch_folder + 'avg_nn_intervals.npz', data=avg_nn_intervals)
        np.savez_compressed(epoch_folder + 'std_nn_intervals.npz', data=std_nn_intervals)
    
        
    if plot_hrv:
        
        window_times = np.load(epoch_folder + 'window_times.npz')['data']
        avg_nn_intervals = np.load(epoch_folder + 'avg_nn_intervals.npz')['data']
        std_nn_intervals = np.load(epoch_folder + 'std_nn_intervals.npz')['data']

        plot_series(window_times, 60 / np.asarray(avg_nn_intervals), 'HR [beat/min]')
        plot_series(window_times, avg_nn_intervals, 'AVNN [s]')
        plot_series(window_times, std_nn_intervals, 'SDNN [s]')

    plt.show()
