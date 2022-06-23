"""This script was produced by the LVK and it used for formating plots."""

from warnings import warn
from cycler import cycler
import matplotlib as mpl
mpl.use("Agg")
import matplotlib.pyplot as plt

# Standardized figure widths in inches.
# These are based on the output of `\the\textwidth` and `\the\columnwidth` in
# the LaTeX document.  If we change our LaTeX template, we should double-check
# that they do not change.
# NOTE: If LaTeX displays a number in `pt` units, divide by 72 to get inches.
widths = {
    'textwidth' : 7.0,
    'columnwidth' : 3.0,
}


def limit_ax_oom(
        ax, n_oom: int, x_or_y: str,
        measure_from: str="upper", base: float=10.0,
    ) -> None:
    r"""
    Takes a :class:`matplotlib.axes._subplots.AxesSubplot` object, and limits
    its limits to ``n_oom`` orders of magnitude (in the logarithmic base set by
    the ``base`` parameter, ``10.0`` by default) from either the upper or lower
    data limit (set with ``measure_from`` argument, "upper" by default).  Either
    operates on x- or y-axis, set by passing "x" or "y" for ``x_or_y`` argument.

    If the data limits are already within the specified orders of magnitude, no
    changes will be made.
    """
    import math
    import numpy

    # Validate inputs.
    if x_or_y not in {"x", "y"}:
        raise KeyError("Invalid choice for 'x_or_y', must be either 'x' or 'y'")
    if measure_from not in {"upper", "lower"}:
        raise KeyError(
            "Invalid choice for 'measure_from', must be either 'upper' or "
            "'lower'"
        )

    # Get data limits along specified axis.
    if x_or_y == "x":
        data_lo, data_hi = ax.dataLim.x0, ax.dataLim.x1
    else:
        data_lo, data_hi = ax.dataLim.y0, ax.dataLim.y1

    # Convert data limits to log-scale, rounding to the next integer.
    data_log_lo = numpy.floor(numpy.log(data_lo) / numpy.log(base))
    data_log_hi = numpy.ceil(numpy.log(data_hi) / numpy.log(base))

    # Do nothing if data limits already close enough.
    if data_log_hi - data_log_lo <= n_oom:
        return

    # Determine the new bound to set.
    if measure_from == "upper":
        data_lo = base ** (data_log_hi - n_oom)
    else:
        data_hi = base ** (data_log_lo + n_oom)

    # Alter the specified axis limits.
    if x_or_y == "x":
        ax.set_xlim([data_lo, data_hi])
    else:
        ax.set_ylim([data_lo, data_hi])


rc_params = {
    '_internal.classic_mode': False,
    'agg.path.chunksize': 0,
    'axes.autolimit_mode': 'data',
    'axes.axisbelow': 'line',
    'axes.edgecolor': 'black',
    'axes.facecolor': 'white',
    'axes.formatter.limits': [-5, 6],
    'axes.formatter.min_exponent': 0,
    'axes.formatter.offset_threshold': 4,
    'axes.formatter.use_locale': False,
    'axes.formatter.use_mathtext': False,
    'axes.formatter.useoffset': True,
    'axes.grid': True,
    'axes.grid.axis': 'both',
    'axes.grid.which': 'major',
    'axes.labelcolor': 'black',
    'axes.labelpad': 4.0,
    'axes.labelsize': 16,
    'axes.labelweight': 'normal',
    'axes.linewidth': 0.8,
    'axes.prop_cycle': cycler(
        'color',
        [
            '#1f77b4', '#ff7f0e',
            '#2ca02c', '#d62728',
            '#9467bd', '#8c564b',
            '#e377c2', '#7f7f7f',
            '#bcbd22', '#17becf',
        ]
    ),
    'axes.spines.bottom': True,
    'axes.spines.left': True,
    'axes.spines.right': True,
    'axes.spines.top': True,
    'axes.titlecolor': 'auto',
    'axes.titlelocation': 'center',
    'axes.titlepad': 6.0,
    'axes.titlesize': 'large',
    'axes.titleweight': 'normal',
    'axes.titley': None,
    'axes.unicode_minus': True,
    'axes.xmargin': 0.05,
    'axes.ymargin': 0.05,
    'axes.zmargin': 0.05,
    'axes3d.grid': True,
    'backend': 'agg',
    'backend_fallback': True,
    'boxplot.bootstrap': None,
    'boxplot.boxprops.color': 'black',
    'boxplot.boxprops.linestyle': '-',
    'boxplot.boxprops.linewidth': 1.0,
    'boxplot.capprops.color': 'black',
    'boxplot.capprops.linestyle': '-',
    'boxplot.capprops.linewidth': 1.0,
    'boxplot.flierprops.color': 'black',
    'boxplot.flierprops.linestyle': 'none',
    'boxplot.flierprops.linewidth': 1.0,
    'boxplot.flierprops.marker': 'o',
    'boxplot.flierprops.markeredgecolor': 'black',
    'boxplot.flierprops.markeredgewidth': 1.0,
    'boxplot.flierprops.markerfacecolor': 'none',
    'boxplot.flierprops.markersize': 6.0,
    'boxplot.meanline': False,
    'boxplot.meanprops.color': 'C2',
    'boxplot.meanprops.linestyle': '--',
    'boxplot.meanprops.linewidth': 1.0,
    'boxplot.meanprops.marker': '^',
    'boxplot.meanprops.markeredgecolor': 'C2',
    'boxplot.meanprops.markerfacecolor': 'C2',
    'boxplot.meanprops.markersize': 6.0,
    'boxplot.medianprops.color': 'C1',
    'boxplot.medianprops.linestyle': '-',
    'boxplot.medianprops.linewidth': 1.0,
    'boxplot.notch': False,
    'boxplot.patchartist': False,
    'boxplot.showbox': True,
    'boxplot.showcaps': True,
    'boxplot.showfliers': True,
    'boxplot.showmeans': False,
    'boxplot.vertical': True,
    'boxplot.whiskerprops.color': 'black',
    'boxplot.whiskerprops.linestyle': '-',
    'boxplot.whiskerprops.linewidth': 1.0,
    'boxplot.whiskers': 1.5,
    'contour.corner_mask': True,
    'contour.linewidth': None,
    'contour.negative_linestyle': 'dashed',
    'date.autoformatter.day': '%Y-%m-%d',
    'date.autoformatter.hour': '%m-%d %H',
    'date.autoformatter.microsecond': '%M:%S.%f',
    'date.autoformatter.minute': '%d %H:%M',
    'date.autoformatter.month': '%Y-%m',
    'date.autoformatter.second': '%H:%M:%S',
    'date.autoformatter.year': '%Y',
    'date.converter': None,
    'date.epoch': '1970-01-01T00:00:00',
    'date.interval_multiples': None,
    'docstring.hardcopy': False,
    'errorbar.capsize': 0.0,
    'figure.autolayout': False,
    'figure.constrained_layout.h_pad': 0.04167,
    'figure.constrained_layout.hspace': 0.02,
    'figure.constrained_layout.use': True,
    'figure.constrained_layout.w_pad': 0.04167,
    'figure.constrained_layout.wspace': 0.02,
    'figure.dpi': 100.0,
    'figure.edgecolor': 'white',
    'figure.facecolor': 'white',
    'figure.figsize': [6.4, 4.8],
    'figure.frameon': True,
    'figure.max_open_warning': 20,
    'figure.raise_window': True,
    'figure.subplot.bottom': 0.11,
    'figure.subplot.hspace': 0.2,
    'figure.subplot.left': 0.125,
    'figure.subplot.right': 0.9,
    'figure.subplot.top': 0.88,
    'figure.subplot.wspace': 0.2,
    'figure.titlesize': 'large',
    'figure.titleweight': 'normal',
    'font.family': ['serif'],
    'font.monospace': ['Computer Modern Typewriter'],
    'font.sans-serif': ['Computer Modern Sans Serif'],
    'font.serif': ['Computer Modern'],
    'font.size': 10.0,
    'font.stretch': 'normal',
    'font.style': 'normal',
    'font.variant': 'normal',
    'font.weight': 'normal',
    'grid.alpha': 0.6,
    'grid.color': 'black',
    'grid.linestyle': '-',
    'grid.linewidth': 1.0,
    'hatch.color': 'black',
    'hatch.linewidth': 1.0,
    'hist.bins': 10,
    'image.aspect': 'equal',
    'image.cmap': 'viridis',
    'image.composite_image': True,
    'image.interpolation': 'antialiased',
    'image.lut': 256,
    'image.origin': 'upper',
    'image.resample': True,
    'interactive': False,
    'legend.borderaxespad': 0.5,
    'legend.borderpad': 0.4,
    'legend.columnspacing': 2.0,
    'legend.edgecolor': '0.8',
    'legend.facecolor': 'inherit',
    'legend.fancybox': True,
    'legend.fontsize': 15,
    'legend.framealpha': 0.8,
    'legend.frameon': True,
    'legend.handleheight': 0.7,
    'legend.handlelength': 2.0,
    'legend.handletextpad': 0.8,
    'legend.labelspacing': 0.5,
    'legend.loc': 'best',
    'legend.markerscale': 1.0,
    'legend.numpoints': 1,
    'legend.scatterpoints': 1,
    'legend.shadow': False,
    'legend.title_fontsize': None,
    'lines.antialiased': True,
    'lines.color': 'C0',
    'lines.dash_capstyle': 'butt',
    'lines.dash_joinstyle': 'round',
    'lines.dashdot_pattern': [6.4, 1.6, 1.0, 1.6],
    'lines.dashed_pattern': [3.7, 1.6],
    'lines.dotted_pattern': [1.0, 1.65],
    'lines.linestyle': '-',
    'lines.linewidth': 1.5,
    'lines.marker': 'None',
    'lines.markeredgecolor': 'auto',
    'lines.markeredgewidth': 1.0,
    'lines.markerfacecolor': 'auto',
    'lines.markersize': 6.0,
    'lines.scale_dashes': True,
    'lines.solid_capstyle': 'projecting',
    'lines.solid_joinstyle': 'round',
    'markers.fillstyle': 'full',
    'mathtext.bf': 'sans:bold',
    'mathtext.cal': 'cursive',
    'mathtext.default': 'it',
    'mathtext.fallback': 'cm',
    'mathtext.fallback_to_cm': None,
    'mathtext.fontset': 'dejavusans',
    'mathtext.it': 'sans:italic',
    'mathtext.rm': 'sans',
    'mathtext.sf': 'sans',
    'mathtext.tt': 'monospace',
    'patch.antialiased': True,
    'patch.edgecolor': 'black',
    'patch.facecolor': 'C0',
    'patch.force_edgecolor': False,
    'patch.linewidth': 1.0,
    'path.effects': [],
    'path.simplify': True,
    'path.simplify_threshold': 0.111111111111,
    'path.sketch': None,
    'path.snap': True,
    'pcolor.shading': 'flat',
    'pcolormesh.snap': True,
    'pdf.compression': 6,
    'pdf.fonttype': 3,
    'pdf.inheritcolor': False,
    'pdf.use14corefonts': False,
    'pgf.preamble': '',
    'pgf.rcfonts': True,
    'pgf.texsystem': 'xelatex',
    'polaraxes.grid': True,
    'ps.distiller.res': 6000,
    'ps.fonttype': 3,
    'ps.papersize': 'letter',
    'ps.useafm': False,
    'ps.usedistiller': None,
    'savefig.bbox': None,
    'savefig.directory': '~',
    'savefig.dpi': 'figure',
    'savefig.edgecolor': 'auto',
    'savefig.facecolor': 'auto',
    'savefig.format': 'png',
    'savefig.orientation': 'portrait',
    'savefig.pad_inches': 0.1,
    'savefig.transparent': False,
    'scatter.edgecolors': 'face',
    'scatter.marker': 'o',
    'svg.fonttype': 'path',
    'svg.hashsalt': None,
    'svg.image_inline': True,
    'text.antialiased': True,
    'text.color': 'black',
    'text.hinting': 'force_autohint',
    'text.hinting_factor': 8,
    'text.kerning_factor': 0,
    'text.latex.preamble': '',
    'text.usetex': True,
    'timezone': 'UTC',
    'tk.window_focus': False,
    'toolbar': 'toolbar2',
    'webagg.address': '127.0.0.1',
    'webagg.open_in_browser': True,
    'webagg.port': 8988,
    'webagg.port_retries': 50,
    'xaxis.labellocation': 'center',
    'xtick.alignment': 'center',
    'xtick.bottom': True,
    'xtick.color': 'black',
    'xtick.direction': 'in',
    'xtick.labelbottom': True,
    'xtick.labelcolor': 'inherit',
    'xtick.labelsize': 14,
    'xtick.labeltop': False,
    'xtick.major.bottom': True,
    'xtick.major.pad': 3.5,
    'xtick.major.size': 3.5,
    'xtick.major.top': True,
    'xtick.major.width': 0.8,
    'xtick.minor.bottom': True,
    'xtick.minor.pad': 3.4,
    'xtick.minor.size': 2.0,
    'xtick.minor.top': True,
    'xtick.minor.visible': False,
    'xtick.minor.width': 0.6,
    'xtick.top': False,
    'yaxis.labellocation': 'center',
    'ytick.alignment': 'center_baseline',
    'ytick.color': 'black',
    'ytick.direction': 'in',
    'ytick.labelcolor': 'inherit',
    'ytick.labelleft': True,
    'ytick.labelright': False,
    'ytick.labelsize': 14,
    'ytick.left': True,
    'ytick.major.left': True,
    'ytick.major.pad': 3.5,
    'ytick.major.right': True,
    'ytick.major.size': 3.5,
    'ytick.major.width': 0.8,
    'ytick.minor.left': True,
    'ytick.minor.pad': 3.4,
    'ytick.minor.right': True,
    'ytick.minor.size': 2.0,
    'ytick.minor.visible': False,
    'ytick.minor.width': 0.6,
    'ytick.right': False,
}

for param, value in rc_params.items():
    try:
        mpl.rcParams[param] = value
    except Exception as e:
        warn(f'Failed to set parameter {param}.  It is probably deprecated')
