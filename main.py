import streamlit as st
import mne
from os.path import join

@st.cache
def load_raw():
    sample_data_folder = mne.datasets.sample.data_path()
    sample_data_raw_file = join(sample_data_folder, 'MEG', 'sample',
                                'sample_audvis_filt-0-40_raw.fif')
    loaded_raw = mne.io.read_raw_fif(sample_data_raw_file, preload=True)

    return loaded_raw


st.title('MNE-Demo')

highpass = st.sidebar.slider('Set Highpass', min_value=0, max_value=75, value=1)
lowpass = st.sidebar.slider('Set Lowpass', min_value=0, max_value=75, value=50)

raw = load_raw()

raw_figure = raw.plot()
st.plotly_chart(raw_figure)

filtering_state = st.text('Filtering data...')
with st.spinner(text='Filtering'):
    raw_filtered = raw.copy().filter(highpass, lowpass)
filtering_state.text('Filtering done!')

figure = raw_filtered.plot_psd(show=False)
st.plotly_chart(figure)

st.balloons()
