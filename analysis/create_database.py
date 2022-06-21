"""This script will import the .csv of the samples and turn in into an sqlite3 database. This is mainly for exploring SQL databases, it is not expected to hold any advantage over working with the .csv file."""
import csv, sqlite3

file_path = "../outputs/params_inc_FAR.csv"

con = sqlite3.connect("../outputs/p_astro_events.db") # change to 'sqlite:///your_filename.db'
cur = con.cursor()
cur.execute("CREATE TABLE data (mass_1, mass_ratio, a_1, a_2, cos_tilt_1, cos_tilt_2, redshift, mass_2, chi_eff, tilt_1, tilt_2, sin_tilt_1, sin_tilt_2, chi_p, spin1z, spin2z, spin1x, spin2x, dl, mass_1_det, mass_2_det, H1_snr, L1_snr, V1_snr, theta_jn, psi, phase, ra, dec, phi_12, phi_jl, net_snr, lynch_FAR, FAR);") # use your column names here, this does not yet include p_astro, TAR

with open(file_path,'r') as fin: # `with` statement available in 2.5+
    # csv.DictReader uses first line in file for column headings by default
    dr = csv.DictReader(fin) # comma is default delimiter
    to_db = [(i['mass_1'], i['mass_ratio'], i['a_1'], i['a_2'], i['cos_tilt_1'], i['cos_tilt_2'], i['redshift'], i['mass_2'], i['chi_eff'], i['tilt_1'], i['tilt_2'], i['sin_tilt_1'], i['sin_tilt_2'], i['chi_p'], i['spin1z'], i['spin2z'], i['spin1x'], i['spin2x'], i['dl'], i['mass_1_det'], i['mass_2_det'], i['H1_snr'], i['L1_snr'], i['V1_snr'], i['theta_jn'], i['psi'], i['phase'], i['ra'], i['dec'], i['phi_12'], i['phi_jl'], i['net_snr'], i['lynch_FAR'], i['FAR']) for i in dr]

cur.executemany("INSERT INTO data (mass_1, mass_ratio, a_1, a_2, cos_tilt_1, cos_tilt_2, redshift, mass_2, chi_eff, tilt_1, tilt_2, sin_tilt_1, sin_tilt_2, chi_p, spin1z, spin2z, spin1x, spin2x, dl, mass_1_det, mass_2_det, H1_snr, L1_snr, V1_snr, theta_jn, psi, phase, ra, dec, phi_12, phi_jl, net_snr, lynch_FAR, FAR) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);", to_db)
con.commit()
con.close()