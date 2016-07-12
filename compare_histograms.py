from subprocess import check_output

import ROOT

import atlas_utils

__all__ = ['from_ttrees', 'from_hists']

# initialization code
ROOT.gROOT.SetBatch(True)
atlas_utils.set_atlas_style()

def from_ttrees(ttrees, labels, varexp, output, title=';;', condition=None,
                dim=(600, 600), log=False, xlims=None):

    n_hist = len(ttrees)

    if isinstance(varexp, str):
        varexp = [varexp] * n_hist
    if isinstance(condition, str):
        condition = [condition] * n_hist

    assert(
        n_hist == len(labels) and
        n_hist == len(varexp) and
        (condition is None or n_hist == len(condition))
    )

    uuid = check_output('uuidgen')

    exprs = ['{}>>hist{}{}'.format(n, i, uuid) for i,n in enumerate(varexp)]

    hists = []

    for i, (tree, exp) in enumerate(zip(ttrees, exprs)):
        if condition is None:
            tree.Draw(exp)
        else:
            tree.Draw(exp, condition[i])
        hists.append(ROOT.gROOT.FindObject('hist{}{}'.format(i, uuid)))

    from_hists(hists, labels, output, title, dim, log, xlims)


MAX_ = -float('inf')

def from_hists(hists, labels, output, title=';;', dim=(600, 600), log=False,
               xlims=None):

    canvas = ROOT.TCanvas("canvas", "canvas", 0, 0, dim[0], dim[1])
    canvas.SetLogy(log)

    stk = ROOT.THStack("stk", "")

    for i, (hist, color) in enumerate(zip(hists, range(1,50))):
        hist.SetLineColor(color)
        stk.Add(hist)

    stk.SetTitle(title)
    stk.SetMaximum(stk.GetMaximum('nostack')*(10 if log else 1.5))
    stk.Draw('nostack')

    legend = ROOT.TLegend(0.8, 0.8, 0.9, 0.9)
    legend.SetBorderSize(0)
    for i, (hist, lbl) in enumerate(zip(hists,labels)):
        legend.AddEntry(hist, lbl, 'L')
    legend.Draw()

    txt = ROOT.TText()
    txt.SetNDC()
    txt.DrawText(0.36, 0.87, 'Internal')
    atlas_utils.atlas_label(0.2, 0.87)

    canvas.SaveAs(output)
