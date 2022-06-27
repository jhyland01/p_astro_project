"""Script for generating SNRs for the sampled events using bilby. This code is adapted from a bibly tutorial.
Also included in the conversion from SNRs to FARs using the method presented in Lynch et al."""

import numpy as np
import pandas as pd
import bilby
import bilby.gw.utils as ut
from P_astro_project import p_astro_utils
logger = bilby.core.utils.logger
logger.setLevel('WARNING')
bilby.core.utils.log.setup_logger(log_level=0)

# import the samples
samples = pd.read_csv('../outputs/params_for_SNR.csv', index_col=0)
# create detector frame masses
samples = samples.assign(mass_1_det = samples['mass_1']*(1+samples['redshift']))
samples = samples.assign(mass_2_det = samples['mass_2']*(1+samples['redshift']))

# specify other terms
np.random.seed(220222)
N = len(samples['mass_1'])
theta_jn = np.arccos(np.random.uniform(-1,1,N))
psi = np.random.uniform(0,np.pi,N)
phase = np.random.uniform(0,2*np.pi,N)
ra = np.random.uniform(0,2*np.pi,N)
dec = np.random.uniform(-0.5*np.pi,0.5*np.pi,N)
phi_12 = np.random.uniform(0,2*np.pi,N)
phi_jl = np.random.uniform(0,2*np.pi,N)

# initiate snr objects
H1_snr = np.zeros(N)
L1_snr = np.zeros(N)
V1_snr = np.zeros(N)

sampling_frequency = 4096
minimum_frequency = 20

for i in range(0,N,1):
    #  Define injection parameters

    injection_dict = dict(mass_1 = samples['mass_1_det'][i], 
    mass_ratio = samples['mass_ratio'][i], 
    redshift = samples['redshift'][i], 
    theta_jn = theta_jn[i], 
    psi = psi[i], 
    phase = phase[i], 
    geocent_time = 1200000000, 
    ra = ra[i], 
    dec = dec[i], 
    a_1 = samples['a_1'][i], 
    a_2 = samples['a_2'][i], 
    phi_12 = phi_12[i], 
    phi_jl = phi_jl[i], 
    tilt_1 = samples['tilt_1'][i], 
    tilt_2 = samples['tilt_2'][i])


    #  Define time and frequency parameters
    # this function uses lal to estimate the duration of the signal and multiplies it by a safety, 1.1 by default
    # the plus 2 is a safety to ensure the duration in the detector is longer than the signal, alt math.ceil
    duration=np.round(ut.calculate_time_to_merger(minimum_frequency,samples['mass_1_det'][i],samples['mass_2_det'][i], samples['chi_eff'][i])+2,0)
    trigger_time=injection_dict['geocent_time'] #- duration
    
    # Sometimes the duration above 20Hz (or chosen frequency) is zero. In these cases I set the SNR to none.
    if duration == 0:
        H1_snr[i] = L1_snr[i] = V1_snr[i] = None

    else:

        #  Setup waveform generator

        waveform_arguments = dict(waveform_approximant='IMRPhenomPv2',
                                reference_frequency=20., 
                                minimum_frequency = minimum_frequency)
        waveform_generator = bilby.gw.WaveformGenerator(
                duration=duration, 
                sampling_frequency = sampling_frequency,
                frequency_domain_source_model = bilby.gw.source.lal_binary_black_hole,
                waveform_arguments = waveform_arguments,
                parameter_conversion = bilby.gw.conversion.convert_to_lal_binary_black_hole_parameters)


        #  Setup interferometers and inject signal

        ifos = bilby.gw.detector.InterferometerList(['H1', 'L1', 'V1'])
        for ifo in ifos:
            ifo.minimum_frequency = minimum_frequency
            ifo.maximum_frequency = sampling_frequency/2.
            # in controlling the psd, a separate file would need specified for LIGO (aLIGO) and Virgo (AdV)
            #ifo.power_spectral_density = bilby.gw.detector.PowerSpectralDensity(psd_file='AdV_psd.txt')

        ifos.set_strain_data_from_power_spectral_densities(
            sampling_frequency = sampling_frequency, 
            duration = duration,
            start_time = (trigger_time + 2 - duration))
        # try:
        #     ifos.inject_signal(waveform_generator=waveform_generator, parameters=injection_dict)
        # except:
        #     print(injection_dict)
        #     print(duration)
        #     continue
        ifos.inject_signal(waveform_generator = waveform_generator, 
        parameters = injection_dict)

        # Access injection data
        H1_snr[i] = ifos.meta_data['H1']['optimal_SNR']
        L1_snr[i] = ifos.meta_data['L1']['optimal_SNR']
        V1_snr[i] = ifos.meta_data['V1']['optimal_SNR']

        #time.sleep(0.1)

# keep a record of the parameters used
samples = samples.assign(theta_jn = theta_jn,
    psi = psi,
    phase = phase,
    ra = ra,
    dec = dec,
    phi_12 = phi_12,
    phi_jl = phi_jl,
    H1_snr = H1_snr,
    L1_snr = L1_snr,
    V1_snr = V1_snr)
samples['net_snr'] = np.sqrt(samples['H1_snr']**2 + samples['L1_snr']**2 +samples['V1_snr']**2)

# save to file
# samples.to_csv('params_inc_SNR.csv')

# adding on the quick conversion to FARs here
samples['FAR'] = p_astro_utils.SNR_to_FAR(samples['net_snr'])
samples.to_csv('../outputs/params_inc_FAR.csv')