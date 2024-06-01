import numpy as np
import matplotlib.pyplot as plt


def plot_series(times: np.ndarray,
                data: np.ndarray,
                ylabel: str,
                plot_quartile: bool = False,
                sample_size: int = None,
                title: str = None,
                xlim: list = None,
                ylim: list = None):

    fig = plt.figure()
    
    if data.ndim > 1:
        
        sample_size = len(data)
        sample_num = len(data[0])
        
        data_medians = np.median(data, axis=0)
        data_95percent = np.percentile(data, 95, axis=0)
        data_5percent = np.percentile(data, 5, axis=0) 
        
    elif sample_size is not None:
    
        sample_num = int(len(data) / sample_size)
         
        data = np.reshape(data[:sample_num * sample_size], (sample_num, sample_size))
        times = np.reshape(times[:sample_num * sample_size], (sample_num, sample_size))
        
        data_medians = np.median(data, axis=1)
        
        times = np.median(times, axis=1)        
        data_95percent = np.percentile(data, 95, axis=1)
        data_5percent = np.percentile(data, 5, axis=1)
        
    else:
        
        plot_quartile = False
        
        data_medians = data
        
    if plot_quartile:
        
        plt.plot(times, data_95percent, linestyle='-', color='orangered', label='5-95 percentile range')
        plt.plot(times, data_5percent, linestyle='-', color='orangered')
        plt.fill_between(times, y1=data_5percent, y2=data_95percent, color='lightsalmon')        
        plt.plot(times, data_medians, linestyle='-', marker='d', color='orangered', label='median')
        
    else:
        
        plt.plot(times, data_medians, linestyle='-', color='orangered')    

    plt.grid('on')        
    plt.xlabel('Time [s]')
    plt.ylabel(ylabel)
    
    if title is not None:
        plt.title(title)
        
    if xlim is not None:    
        plt.xlim(xlim)        
    else:
        plt.xlim((times[0], times[-1]))
        
    if ylim is not None:
        
        plt.xlim(ylim)
    
    fig.tight_layout()
        
        
def plot_multi_series(times_per_element: list,
                      data_per_element: list,
                      label_per_element: list,
                      color_per_element: list,
                      ylabel: str,
                      plot_quartile: bool = False,
                      sample_size: int = None,
                      title: str = None,
                      xlim: list = None,
                      ylim: list = None):

    fig = plt.figure()

    for times, data, label, color in zip(times_per_element, data_per_element, label_per_element, color_per_element):
        
        if data.ndim > 1:
        
            sample_size = len(data)
            sample_num = len(data[0])
            
            data_medians = np.median(data, axis=0)
            data_95percent = np.percentile(data, 95, axis=0)
            data_5percent = np.percentile(data, 5, axis=0)
            
        else:
            
            if sample_size is None:
            
                sample_size = np.max((1, int(len(data) / 100)))        
        
            sample_num = int(len(data) / sample_size)        
            data = np.reshape(data[:sample_num * sample_size], (sample_num, sample_size))
            times = np.reshape(times[:sample_num * sample_size], (sample_num, sample_size))          
            times = np.median(times, axis=1)
            data_medians = np.median(data, axis=1)
            data_95percent = np.percentile(data, 95, axis=1)
            data_5percent = np.percentile(data, 5, axis=1)
        
        if sample_size > 1 and plot_quartile:
            
            plt.plot(times, data_95percent, linestyle='-', color=color, alpha=0.7)
            plt.plot(times, data_5percent, linestyle='-', color=color, alpha=0.7)
            plt.plot(times, data_medians, label=label, linestyle='-', color=color)
            
        else:
        
            plt.plot(times, data_medians, label=label, linestyle='-', color=color)       

    plt.grid('on')        
    plt.xlabel('Time [s]')
    plt.ylabel(ylabel)
    
    plt.legend()
    
    if title is not None:
        plt.title(title)
        
    if xlim is not None:
        plt.xlim(xlim)
    else:
        plt.xlim((times_per_element[0][0], times_per_element[0][-1]))
        
    if ylim is not None:
        plt.ylim(ylim)
        
    fig.tight_layout()
    
    
def plot_ecg_signal(times: np.ndarray,
                    ecg: np.ndarray,
                    ylabel: str,
                    title: str = None):
    
    ax = plt.axes()
    
    ax.set_facecolor('lightyellow')
    
    ax.plot(times, ecg, color='k', linewidth=0.3)    

    ax.grid('on')        
    ax.set_xlabel('Time [s]')
    ax.set_ylabel(ylabel)
    
    if title is not None:
        ax.set_title(title)
        
    ax.set_xlim([times[0], times[-1]])
