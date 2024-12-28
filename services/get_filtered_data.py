from typing import List
from models.record_data import RecordData, RecordRawData
from scipy.signal import savgol_filter

def get_filtered_data(json_data : RecordRawData) -> RecordRawData:
    # Filtrar los datos de entrada
    window_size = 199  
    poly_order = 1 
    amplitude_filtered = []
    tof_filtered = []

    for strip in json_data.payload_data.strip_data: 
        amplitude_filtered = savgol_filter(strip.amplitude, window_size, poly_order).tolist()
        tof_filtered = savgol_filter(strip.tof, window_size, poly_order).tolist()
        strip.amp_damages = amplitude_filtered
        strip.tof_damages = tof_filtered

    return json_data