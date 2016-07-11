import glob
import os

import ROOT

__all__ = ['set_atlas_style', 'atlas_label']


DIR_ = glob.glob(
    '{}/atlasstyle-*'.format(
        os.path.dirname(os.path.realpath(__file__))
    )
)[0]

ROOT.gROOT.LoadMacro('{}/AtlasStyle.C'.format(DIR_))
ROOT.gROOT.LoadMacro('{}/AtlasUtils.C'.format(DIR_))


def set_atlas_style():
    ROOT.SetAtlasStyle()


def atlas_label(x_coord, y_coord):
    ROOT.ATLAS_LABEL(x_coord, y_coord)
