import streamlit as st
import mne
from os.path import join


@st.cache
def load_raw():
    sample_data_folder = mne.datasets.sample.data_path()
    sample_data_raw_file = join(sample_data_folder, 'MEG', 'sample',
                                'sample_audvis_raw.fif')
    loaded_raw = mne.io.read_raw_fif(sample_data_raw_file, preload=True)

    return loaded_raw


@st.cache
def filter_raw(rw, hp, lp):
    with st.spinner(text='Filtering'):
        rw_filt = rw.copy().filter(hp, lp)

    return rw_filt


st.title('MNE-Demo')

raw = load_raw()
rounded_sfreq = int(raw.info['sfreq'])
st.write(f'Loaded raw with a sampling-frequency of {rounded_sfreq}')

# Get Filter-Parameters
highpass = st.sidebar.slider('Set Highpass-Filter', min_value=0, max_value=int(rounded_sfreq/2), value=1)
lowpass = st.sidebar.slider('Set Lowpass-Filter', min_value=0, max_value=int(rounded_sfreq/2), value=50)

# Set time slider-maximum to length of sample-recording (n time-points/sampling-frequency)
start = st.sidebar.slider('Time[s]', min_value=0, max_value=int(raw.n_times / raw.info['sfreq']), value=0)
duration = st.sidebar.number_input('Set Time-Window[s] (max. 100 s)', min_value=1, max_value=100, value=10)
n_channels = st.sidebar.number_input('Set number of channels to display (max. 50)', min_value=1, max_value=50, value=10)
channels = st.sidebar.multiselect('Channel-Selection', raw.ch_names, default=raw.ch_names[:20])

# Pick channels as selected
raw_picked = raw.copy().pick_channels(channels)

# Filter raw
raw_filtered = filter_raw(raw_picked, highpass, lowpass)

# Plot-Checkboxes
show_raw = st.sidebar.checkbox('Show MEG/EEG-Data (unfiltered)')
show_filt_raw = st.sidebar.checkbox('Show MEG/EEG-Data (filtered)')
show_psd = st.sidebar.checkbox('Show Power-Spectrum-Density')

if show_raw:
    st.write('This is the unfiltered MEG/EEG-Data')
    raw_fig = raw_picked.plot(n_channels=n_channels, duration=duration, start=start, show_scrollbars=False, show=False)
    st.write(raw_fig)
else:
    st.write('Check "Show MEG/EEG-Data (unfiltered)" to plot something')

if show_filt_raw:
    st.write('This is the filtered MEG/EEG-Data')
    raw_filt_fig = raw_filtered.plot(n_channels=n_channels, duration=duration, start=start, show_scrollbars=False,
                                     show=False)
    st.write(raw_filt_fig)
else:
    st.write('Check "Show MEG/EEG-Data (filtered)" to plot something')

if show_psd:
    st.write('This is the Power-Spectrum-Density of MEG/EEG-Data')
    psd_fig = raw_filtered.plot_psd(show=False)
    st.write(psd_fig)
else:
    st.write('Check "Show Power-Spectrum-Density" to plot something')
