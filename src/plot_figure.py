import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import os
import numpy as np


def plot_figure(iv_result, trans_result, lmz_path, _analysis_time):
    fontsize = 14
    title_fontsize = 16
    lmz_path_split = lmz_path.split('\\')
    batch = lmz_path_split[1]
    wafer = lmz_path_split[2]
    date = lmz_path_split[3]
    device_name = lmz_path_split[4].split('.')[0]
    file_name = f"{batch}_{wafer}_{date}_{device_name}.xml"

    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(20, 12))
    fig.suptitle(file_name, fontsize=title_fontsize, weight='bold')

    # --------- Measured Transmission --------- #
    dcbias = trans_result['DCBias']
    trans_l = trans_result['transmission_l']
    trans_il = trans_result['transmission_il']
    ref_l = trans_result['ref_l']
    ref_il = trans_result['ref_il']
    for i in range(len(trans_result['DCBias'])):
        ax1.plot(trans_l[i], trans_il[i], label=dcbias[i])
    ax1.plot(ref_l, ref_il, label='Reference', linestyle='--', color='black')
    ax1.legend(loc='lower center', ncol=4, fontsize=fontsize)
    ax1.set_ylim(-52, -0)
    ax1.set_title('Transmission Spectra - As Measured', fontsize=fontsize)
    ax1.set_xlabel('Wavelength [nm]', fontsize=fontsize)
    ax1.set_ylabel('Measured Transmission [dB]', fontsize=fontsize)
    ax1.tick_params(axis='both', direction='in', labelsize=fontsize)
    ax1.grid(True, linestyle='--', alpha=0.6)

    # ---------- Reference Fit ----------- #
    pred_il = trans_result['ref_pred_il']
    label = trans_result['ref_fit_label']
    r2 = trans_result['ref_r2_score_list']
    for i in range(len(pred_il)):
        ax2.plot(ref_l, pred_il[i], label=label[i])
    ax2.plot(ref_l, ref_il, label='Reference', linestyle='--', color='black')

    ax2.set_title('Reference Spectra - Fitted', fontsize=fontsize)
    ax2.set_xlabel('Wavelength [nm]', fontsize=fontsize)
    ax2.set_ylabel('Measured Transmission [dB]', fontsize=fontsize)
    ax2.tick_params(axis='both', direction='in', labelsize=fontsize)
    ax2.legend(loc="upper left", fontsize=fontsize, ncol=5)
    ax2.set_ylim(np.min(ref_il) - 4, np.max(ref_il) + 4)
    ax2.grid(True, linestyle='--', alpha=0.6)

    # --------- Flattened Transmission --------- #
    ref_model_list = trans_result['ref_model_list']
    flat_trans = trans_result['flat_transmission']
    for i in range(len(trans_result['DCBias'])):
        ax3.plot(trans_l[i], flat_trans[i], label=dcbias[i])
    ax3.plot(ref_l, [0] * len(ref_l), '--', color='black')
    ax3.set_title('Transmission Spectra - Flattened', fontsize=fontsize)
    ax3.set_xlabel('Wavelength [nm]', fontsize=fontsize)
    ax3.set_ylabel('Flat Measured Transmission [dB]', fontsize=fontsize)
    ax3.tick_params(axis='both', direction='in', labelsize=fontsize)
    ax3.legend(loc='lower center', ncol=4, fontsize=fontsize)
    ax3.grid(True, linestyle='--', alpha=0.6)

    # ------------- I-V Characteristics ------------- #
    voltage = iv_result['voltage']
    abs_current = iv_result['abs_current']
    fit_current = iv_result['final current']
    iv_r_squared = iv_result['R_squared']
    ax4.scatter(voltage, abs_current, label='Measured', color='blue')
    ax4.plot(voltage, fit_current, 'r', label='Fitted')

    ax4.annotate(f"R$^2$={iv_r_squared:.4f}", xy=(0.95, 0.95), xycoords='axes fraction', fontsize=fontsize,
                 verticalalignment='top', horizontalalignment='right')
    ax4.set_yscale('log')
    ax4.yaxis.set_major_locator(ticker.LogLocator(base=10, numticks=10))
    ax4.yaxis.set_minor_locator(ticker.LogLocator(base=10, subs='auto', numticks=10))
    ax4.legend(fontsize=fontsize, loc='upper left')
    ax4.set_title('I-V Characteristics', fontsize=fontsize)
    ax4.set_xlabel('Voltage [V]', fontsize=fontsize)
    ax4.set_ylabel('Log Absolute Current [A]', fontsize=fontsize)
    ax4.tick_params(axis='both', direction='in', which='both', labelsize=fontsize)
    ax4.grid(True, which='both', linestyle='--', alpha=0.6)

    plt.tight_layout(rect=(0, 0, 1, 0.96))

    if __name__ == 'src.plot_figure':
        file_path = f'res\\{_analysis_time}\\{batch}\\{wafer}\\{date}\\{device_name}.png'
        if file_path.split('\\')[-1] in os.listdir('res\\'):
            file_path = f'res\\{_analysis_time}\\{batch}\\{wafer}\\{date}\\{device_name}(1).png'
        plt.savefig(file_path)
    else:
        file_path = f'..\\res\\{_analysis_time}\\{batch}\\{wafer}\\{date}\\{device_name}.png'
        if file_path.split('\\')[-1] in os.listdir('..\\res\\'):
            file_path = f'..\\res\\{_analysis_time}\\{batch}\\{wafer}\\{date}\\{device_name}(1).png'
        plt.savefig(file_path)
    plt.close()
