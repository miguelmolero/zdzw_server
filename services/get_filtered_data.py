from typing import List
from models.record_data import InspectionData, RecordData, StripData
from models.defects_data import DefectsData, DefectItem
from scipy.signal import savgol_filter
import numpy as np

def apply_savgol_filter(strip: StripData) -> StripData:
    window_size = 199  
    poly_order = 1 
    amplitude_filtered = []
    tof_filtered = []

    amplitude_filtered = savgol_filter(strip.amplitude, window_size, poly_order).tolist()
    tof_filtered = savgol_filter(strip.tof, window_size, poly_order).tolist()
    strip.amp_damages = amplitude_filtered
    strip.tof_damages = tof_filtered

    return strip

def get_defects(strip: StripData, feature: str) -> List[DefectItem]:
    below_indexes = []
    below_x_values = []
    below_y_values = []

    if feature == "amplitude":
        below_indexes = np.where(np.array(strip.amplitude) < np.array(strip.amp_damages))
        below_x_values = below_indexes[0]
        below_y_values = [strip.amplitude[i] for i in below_x_values]
        below_x_values = below_x_values.tolist()
    elif feature == "tof":
        below_indexes = np.where(np.array(strip.tof) < np.array(strip.tof_damages))
        below_x_values = below_indexes[0]
        below_y_values = [strip.tof[i] for i in below_x_values]
        below_x_values = below_x_values.tolist()

    defects : List[DefectItem] = []
    counter = 0
    start_index = below_x_values[0]
    last_index = below_x_values[0]

    for index in below_x_values[1:]:
        if index ==  last_index + 1:
            last_index = index
        else:
            start_index = below_x_values.index(start_index)
            last_index = below_x_values.index(last_index)
            defect = DefectItem(
                name=feature + str(counter), 
                start_index=start_index, 
                end_index=last_index, 
                start_feature_value=below_y_values[start_index], 
                end_feature_value=below_y_values[last_index], 
                risk_level=1
            )
            defects.append(defect)
            counter += 1
            start_index = index
            last_index = index

    start_index = below_x_values.index(start_index)
    last_index = below_x_values.index(last_index)
    defect = DefectItem(
        name=feature + str(counter), 
        start_index=start_index, 
        end_index=last_index, 
        start_feature_value=below_y_values[start_index], 
        end_feature_value=below_y_values[last_index], 
        risk_level=1
    )
    defects.append(defect)
    return defects

def get_filtered_data(json_data : InspectionData) -> InspectionData:
    defects_amp : List[DefectItem] = []
    defects_tof : List[DefectItem] = []

    for strip in json_data.payload_data.strip_data:
        strip = apply_savgol_filter(strip)
        if strip.defects_data is None:
            strip.defects_data = DefectsData(defects_amp=[], defects_tof=[])
        try:
            defects_amp = get_defects(strip, "amplitude")
            defects_tof = get_defects(strip, "tof")
            strip.defects_data = DefectsData(defects_amp=defects_amp, defects_tof=defects_tof)
        except Exception as e:
            print("Error", e)

    return json_data


