# -*- coding: utf-8 -*-
from maya import cmds, mel

TEST_CV_VALUE = -2
DEFORMATION_CREATE_TWEAK = 'deformationCreateTweak'


def get_deformation_create_tweak_op_var():
    return cmds.optionVar(q=DEFORMATION_CREATE_TWEAK)


def set_deformation_create_tweak_op_var(value):
    cmds.optionVar(intValue=(DEFORMATION_CREATE_TWEAK, value))


def create_skin_bound_cube():
    cube = cmds.polyCube()[0]
    cmds.select(cl=True)
    joint = cmds.joint()
    cmds.select(cl=True)
    sel = [cube, joint]
    cmds.select(sel, r=True)
    mel.eval('SmoothBindSkin')
    return cube


def set_vtx0_cv(mesh, tweak):
    """頂点番号0のx座標にCV値-2を設定"""
    if tweak is None:
        cmds.setAttr('{}.pnts[0].pntx'.format(mesh), TEST_CV_VALUE)
    else:
        cmds.setAttr('{}.vlist[0].vertex[0].xVertex'.format(tweak), TEST_CV_VALUE)


def get_vtx0_cv(mesh, tweak):
    """頂点番号0のX座標のCV値を取得"""
    if tweak is None:
        vtx0_cv = cmds.getAttr('{}.pnts[0].pntx'.format(mesh))
    else:
        vtx0_cv = cmds.getAttr('{}.vlist[0].vertex[0].xVertex'.format(tweak))
    return vtx0_cv


def new_scene():
    cmds.file(force=True, new=True)
