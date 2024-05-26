import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

fontsize = 12


def plot_figure(iv_result, trans_result, lmz_path):
    device_name = lmz_path.split('\\')[-1].split('.')[0]
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 9))
    # ax1: Measured transmission
    # ax2: Fitted transmission reference
    # ax3: Processed transmission reference
    # ax4: Measured and fitted I-V characteristics

    """
    transmission 부분 제작중
    """
    voltage = iv_result['voltage']
    abs_current = iv_result['abs_current']
    fit_current = iv_result['final current']
    iv_r_squared = iv_result['R_squared']
    ax4.scatter(voltage, abs_current, label='Measured')
    ax4.plot(voltage, fit_current, 'r', label=f'Fitted')

    ax4.annotate(f"R$^2$={iv_r_squared}", xy=[-2.0, 1e-4], fontsize=fontsize)
    ax4.annotate(f"-1V={abs_current[4]}A", xy=[-2.0, 1e-5], fontsize=fontsize)
    ax4.annotate(f"+1V={abs_current[12]}A", xy=[-2.0, 1e-6], fontsize=fontsize)

    ax4.set_yscale('log')
    ax4.yaxis.set_major_locator(ticker.LogLocator(base=10, numticks=10))
    ax4.yaxis.set_minor_locator(
        ticker.LogLocator(base=10, subs=(0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9), numticks=10))
    ax4.legend(fontsize=fontsize)
    ax4.set_title('I-V Characteristics', fontsize=fontsize)
    ax4.set_xlabel('Voltage [V]', fontsize=fontsize)
    ax4.set_ylabel('Log Absolute Current [A]', fontsize=fontsize)
    ax4.tick_params(axis='both', direction='in', which='both', labelsize=fontsize)

    plt.tight_layout()

    if __name__ == 'src.plot_figure':
        plt.savefig(f'res\\{device_name}.png')
    else:
        plt.savefig(f'..\\res\\{device_name}.png')
    # plt.show()
