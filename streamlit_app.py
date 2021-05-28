import os
import sys
import streamlit as st

import matplotlib.pyplot as plt
import numpy as np 
import wave
import sys

st.set_option('deprecation.showPyplotGlobalUse', False)

# Page Configuration 
st.set_page_config(
    page_title="Audio Demo",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded",
    )

# Adds Faculty Logo
st.sidebar.image(r'facultyLogo.jpg', width=150)

col1, col2 = st.beta_columns([1,1])
col3, col4 = st.beta_columns([1,1])
col5, col6 = st.beta_columns([1,1])
col7, col8 = st.beta_columns([1,1])


col1.write('Ieee0105 Speech')
col1.audio(r'DemoAudiofiles\ieee0105_Speech.wav')
col2.write('8Bit Low Amp')
col2.audio(r'DemoAudiofiles\speaker_8bit_low_amp.wav')
col3.write('8Bit')
col3.audio(r'DemoAudiofiles\speaker_8bit.wav')
col4.write('SR1500')
col4.audio(r'DemoAudiofiles\speaker_SR1500.wav')
col5.write('SR3000')
col5.audio(r'DemoAudiofiles\speaker_SR3000.wav')
col6.write('SR6000')
col6.audio(r'DemoAudiofiles\speaker_SR6000.wav')
col7.write('SR12000')
col7.audio(r'DemoAudiofiles\speaker_SR12000.wav')
col8.write('SR24000')
col8.audio(r'DemoAudiofiles\speaker_SR24000.wav')

def visualize(path: str):
    raw = wave.open(path)

    signal = raw.readframes(-1)
    signal = np.frombuffer(signal, dtype='int16')

    f_rate = raw.getframerate()
    time = np.linspace(0, len(signal)/f_rate, num= len(signal))

    plt.figure(1)
    plt.title(path.split('\\')[1])
    plt.xlabel("Time")
    plt.plot(time,signal)


col1.pyplot(visualize(r'DemoAudiofiles\ieee0105_Speech.wav'))
col2.pyplot(visualize(r'DemoAudiofiles\speaker_8bit_low_amp.wav'))
col3.pyplot(visualize(r'DemoAudiofiles\speaker_8bit.wav'))
col4.pyplot(visualize(r'DemoAudiofiles\speaker_SR1500.wav'))
col5.pyplot(visualize(r'DemoAudiofiles\speaker_SR3000.wav'))
col6.pyplot(visualize(r'DemoAudiofiles\speaker_SR6000.wav'))
col7.pyplot(visualize(r'DemoAudiofiles\speaker_SR12000.wav'))
col8.pyplot(visualize(r'DemoAudiofiles\speaker_SR24000.wav'))

