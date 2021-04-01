import os
import sys
from os.path import join
from matplotlib.backends.backend_agg import RendererAgg
import numpy as np

import mne
import streamlit as st

# Page Configuration 
st.set_page_config(
    page_title="Filterung von EEG-Daten",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded",
    )

# Streamlit hash is turned off for Raw-Object, maybe if we want to implement reloading after changing some features
# of the raw-object (n_channels, sfreq), we could implement a custom hash-function for that
@st.cache(hash_funcs={mne.io.fiff.raw.Raw: lambda _: None}, allow_output_mutation=True)
def load_raw():
    sample_data_folder = mne.datasets.sample.data_path()
    sample_data_raw_file = join(sample_data_folder, 'MEG', 'sample',
                                'sample_audvis_raw.fif')
    raw = mne.io.read_raw_fif(sample_data_raw_file)

    # All the following methods operate in-Place
    # Reducing data to time window in [s]
    raw.crop(0, 60)

    # QUESTION: Resampling takes quit a long time, maybe filtering the higher sampling-rate is faster than first resampling and then filtering the resampled data?

    # # Resampling data to sampling-frequency in [Hz]
    # st.write('Reducing SampleRate')
    # loaded_raw.resample(200)

    # Picking only Gradiometer-Channels (example for slow drift in this data)
    raw.pick_types(meg=False, eeg=True, stim=False, eog=False)

    # Uncomment this and comment the previous line to see some EKG-Artefacts
    # raw.pick_types(meg='mag', eeg=False, stim=False, eog=False)

    # Load data into memory for filtering afterwards
    raw.load_data()

    return raw


# Streamlit hash is turned off for Raw-Object, should only depend on hp/lp-parameters
@st.cache(hash_funcs={mne.io.fiff.raw.Raw: lambda _: None}, allow_output_mutation=True)
def filter_raw(raw, hp, lp):
    with st.spinner(text='Filtering'):
        raw = raw.copy().filter(hp, lp)
    return raw

# Caching the Plot Figures
@st.cache(allow_output_mutation=True)
def FigureCache():
    return {'EEG-Plot': dict(),
            'PSD-Plot': dict()}

# Load Raw
loaded_raw = load_raw()

# Code Snippet to Hide Burger Menu
#hide_menu_style = """
#        <style>
#       #MainMenu {visibility: hidden;}
#        </style>
#        """
#st.markdown(hide_menu_style, unsafe_allow_html=True)

# Adds Faculty Logo
st.sidebar.image('facultyLogo.jpg', width=150)

# Column-Layout to show graphs horizontally
col1, col2 = st.beta_columns([1,1.4])

# Get Filter-Parameters
highpass = st.sidebar.slider('Hochpass-Filter', min_value=0, max_value=100, value=0)
lowpass = st.sidebar.slider('Tiefpass-Filter', min_value=0, max_value=100, value=100)

# Filter raw
raw_filtered = filter_raw(loaded_raw, highpass, lowpass)

# Get Figure Cache
figure_cache = FigureCache()

# Create a string as hash from the Filter-Parameters
filter_hash = f'{highpass}-{lowpass}'

# Lock functionality used to fix a bug with Matplot which influences multiuser interaction.
_lock = RendererAgg.lock

# Loading cached figure or creating a new one
if filter_hash in figure_cache['EEG-Plot']:
    filtered_image = figure_cache['EEG-Plot'][filter_hash]
else:
    with _lock:
        filtered_fig = raw_filtered.plot(n_channels=20, duration=30, show_scrollbars=False,
                                         show=False, title='Filtern von EEG-Daten', remove_dc=False)
        filtered_fig.canvas.draw()
        filtered_image = np.fromstring(filtered_fig.canvas.tostring_rgb(), dtype=np.uint8)
        filtered_image = filtered_image.reshape(filtered_fig.canvas.get_width_height()[::-1] + (3,))
        figure_cache['EEG-Plot'][filter_hash] = filtered_image

col1.write('EEG-Daten gefiltert:')
col1.image(filtered_image,width=700)

# Loading cached figure or creating a new one
if filter_hash in figure_cache['PSD-Plot']:
    psd_image = figure_cache['PSD-Plot'][filter_hash]
else:
    with _lock:
        psd_fig = raw_filtered.plot_psd(show=False)
        psd_fig.canvas.draw()
        psd_image = np.fromstring(psd_fig.canvas.tostring_rgb(), dtype=np.uint8)
        psd_image = psd_image.reshape(psd_fig.canvas.get_width_height()[::-1] + (3,))
        figure_cache['PSD-Plot'][filter_hash] = psd_image

col2.write('Frequenzspektrum:')
col2.image(psd_image,width=730)

# Shows Cache Memory Usage
#cache_size = sum([sum([sys.getsizeof(figure_cache[plot_type][freq_hash]) for freq_hash in figure_cache[plot_type]])
#                  for plot_type in figure_cache])
#st.write(f'Figure-Cache takes {cache_size} bytes')
