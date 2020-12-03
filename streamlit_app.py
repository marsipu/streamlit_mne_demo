import streamlit as st
import mne
import matplotlib
from matplotlib import pyplot as plt
from os.path import join

# Pyplot somehow needs to be imported to initialize Matplotlib-Backend and make use of matplotlib.figure.Figure possible
_ = plt


@st.cache(hash_funcs={mne.io.fiff.raw.Raw: lambda _: None}, allow_output_mutation=True)
def load_raw():
    sample_data_folder = mne.datasets.sample.data_path()
    sample_data_raw_file = join(sample_data_folder, 'MEG', 'sample',
                                'sample_audvis_raw.fif')
    raw = mne.io.read_raw_fif(sample_data_raw_file, preload=True)

    return raw


@st.cache(hash_funcs={mne.io.fiff.raw.Raw: lambda _: None}, allow_output_mutation=True)
def pick_channels(raw, channels):
    raw_picked = raw.copy().pick_channels(channels)

    return raw_picked


@st.cache(hash_funcs={mne.io.fiff.raw.Raw: lambda _: None}, allow_output_mutation=True)
def filter_raw(raw, hp, lp):
    with st.spinner(text='Filtering'):
        raw_filtered = raw.copy().filter(hp, lp)

    return raw_filtered


@st.cache(hash_funcs={matplotlib.figure.Figure: lambda _: None})
def plot_raw(raw, n_channels, duration, start):
    raw_fig = raw.plot(n_channels=n_channels, duration=duration, start=start, show_scrollbars=True, show=False)

    return raw_fig


st.title('MNE-Demo')

senseless_button = st.sidebar.button('Does nothing')

raw = load_raw()
rounded_sfreq = int(raw.info['sfreq'])
st.write(f'Loaded raw with a sampling-frequency of {rounded_sfreq}')

# Pick channels as selected
channels = st.sidebar.multiselect('Channel-Selection', raw.ch_names, default=list())
raw_picked = pick_channels(raw, channels)

# Get Filter-Parameters
highpass = st.sidebar.slider('Set Highpass-Filter', min_value=0, max_value=int(rounded_sfreq / 2), value=1)
lowpass = st.sidebar.slider('Set Lowpass-Filter', min_value=0, max_value=int(rounded_sfreq / 2), value=50)

# Set time slider-maximum to length of sample-recording (n time-points/sampling-frequency)
start = st.sidebar.slider('Time[s]', min_value=0, max_value=int(raw.n_times / raw.info['sfreq']), value=0)
duration = st.sidebar.number_input('Set Time-Window[s] (max. 100 s)', min_value=1, max_value=100, value=10)
n_channels = st.sidebar.number_input('Set number of channels to display (max. 50)', min_value=1, max_value=50, value=10)

# Filter raw
raw_filtered = filter_raw(raw_picked, highpass, lowpass)

# Plot-Checkboxes
show_raw = st.sidebar.checkbox('Show MEG/EEG-Data (unfiltered)')
show_filt_raw = st.sidebar.checkbox('Show MEG/EEG-Data (filtered)')
show_psd = st.sidebar.checkbox('Show Power-Spectrum-Density')

if show_raw:
    st.write('This is the unfiltered MEG/EEG-Data')
    raw_fig = plot_raw(raw, n_channels=n_channels, duration=duration, start=start)
    st.write(raw_fig)
    # Add plot-buttons
    raw_col1, raw_col2, raw_col3, raw_col4 = st.beta_columns(4)
    with raw_col1:
        if st.button('up'):
            raw_fig.canvas.key_press_event('up')
    with raw_col2:
        if st.button('down'):
            raw_fig.canvas.key_press_event('down')
    with raw_col3:
        if st.button('left'):
            raw_fig.canvas.key_press_event('left')
    with raw_col4:
        if st.button('right'):
            raw_fig.canvas.key_press_event('right')
else:
    st.write('Check "Show MEG/EEG-Data (unfiltered)" to plot something')

if show_filt_raw:
    st.write('This is the filtered MEG/EEG-Data')
    raw_filt_fig = raw_filtered.plot(n_channels=n_channels, duration=duration, start=start, show_scrollbars=False,
                                     show=False)
    st.write(raw_filt_fig)
    # Add plot-buttons
    raw_filt_col1, raw_filt_col2, raw_filt_col3, raw_filt_col4 = st.beta_columns(4)
    with raw_filt_col1:
        if st.button('up'):
            raw_filt_fig.canvas.key_press_event('up')
    with raw_filt_col2:
        if st.button('down'):
            raw_filt_fig.canvas.key_press_event('down')
    with raw_filt_col3:
        if st.button('left'):
            raw_filt_fig.canvas.key_press_event('left')
    with raw_filt_col4:
        if st.button('right'):
            raw_filt_fig.canvas.key_press_event('right')
else:
    st.write('Check "Show MEG/EEG-Data (filtered)" to plot something')

if show_psd:
    st.write('This is the Power-Spectrum-Density of MEG/EEG-Data')
    psd_fig = raw_filtered.plot_psd(show=False)
    st.write(psd_fig)
else:
    st.write('Check "Show Power-Spectrum-Density" to plot something')
