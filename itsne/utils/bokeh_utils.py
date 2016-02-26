"""
Bokeh utility functions
"""
from PIL import Image
import numpy as np


def convert_to_RGBA(img, alpha=None):
    """Converts input PIL Image or nparray to RGBA. Returns ndarray of shape
    (H, W, 4), where the last channel dimension is `alpha`, the transparency"""
    try:
        if img.mode != "RGBA":
            img = np.array(img.convert("RGBA"))
    except AttributeError:
        img = Image.fromarray(img)
        if img.mode != "RGBA":
            img = np.array(img.convert("RGBA"))
    # reconvert back to npy. we converted ^ to make sure any array is converted
    # to a standard color mode, RGBA, so we can manpipualate easily
    if alpha is not None:
        if alpha >= 0 and alpha <= 255:
            img[:, :, 3] = int(alpha)
        else:
            raise RuntimeError("alpha must be between [0, 255]")

    return np.array(img)


def preproc_img(img, flip_ud=True, alpha=None):
    """ Preprocess a image arr (numpy or PIL.Image) to be absorbed bokeh's
    plotting."""
    # convert to RGBA if it's not, depending on whether ndarr/PIL.Image
    img = convert_to_RGBA(img, alpha=alpha)

    # traditional image conventions refer to top left corner as 0,0.
    # however, bokeh has bottom left (0,0).
    if flip_ud:
        img = np.flipud(img)

    # convert img to be 2d arr (M x N) with dtype = uint32 -- for bokeh
    bimg = np.squeeze(img.astype(np.uint8).view(np.uint32))
    return bimg
