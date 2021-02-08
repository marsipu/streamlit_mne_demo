from os.path import join

import mne
import streamlit as st


# cache is turned off for Raw-Object, maybe if we want to implement reloading after changing some features
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

    # Resampling takes quit a long time, maybe filtering the higher sampling-rate is faster than first resampling
    #   and then resampling the resampled data

    # # Resampling data to sampling-frequency in [Hz]
    # st.write('Reducing SampleRate')
    # loaded_raw.resample(200)

    # Picking only Gradiometer-Channels (example for slow drift in this data)
    raw.pick_types(meg=False, eeg=True, stim=False, eog=False)

    # Data has to be loaded into memory for filtering afterwards
    raw.load_data()

    return raw


# cache is turned off for Raw-Object, should only depend on hp/lp-parameters
@st.cache(hash_funcs={mne.io.fiff.raw.Raw: lambda _: None}, allow_output_mutation=True)
def filter_raw(raw, hp, lp):
    with st.spinner(text='Filtering'):
        raw = raw.copy().filter(hp, lp)

    return raw


st.title('EEG-Filter Demo')

st.sidebar.write('<Erklär-Text>')

loaded_raw = load_raw()
# Get Filter-Parameters
highpass = st.sidebar.slider('Hochpass-Filter', min_value=0, max_value=100, value=0)
lowpass = st.sidebar.slider('Tiefpass-Filter', min_value=0, max_value=100, value=100)

# Filter raw
raw_filtered = filter_raw(loaded_raw, highpass, lowpass)

st.write('EEG-Daten gefiltert:')
filtered_fig = raw_filtered.plot(n_channels=10, duration=60, show_scrollbars=False,
                                 show=False, title='Filtern von EEG-Daten', remove_dc=False)
st.write(filtered_fig)

st.write('Frequenzspektrum:')
psd_fig = raw_filtered.plot_psd(show=False)
st.write(psd_fig)
