# -*- coding: utf-8 -*-
from maya import cmds, mel

maya_version = int(cmds.about(v=True))
after_maya2022 = maya_version >= 2022
before_maya2020 = not after_maya2022

TWEAK = 'tweak'


def create_poly_tweak_uv_history(mesh):
    cmds.select('{}.map[0]'.format(mesh), r=True)
    cmds.polyEditUV(u=1)
    cmds.polyEditUV(u=-1)
    cmds.select(cl=True)


def delete_non_deformer_history(mesh):
    cmds.select(mesh)
    mel.eval('BakeNonDefHistory')
    cmds.select(cl=True)


def get_history(mesh, sort_type):
    histories = cmds.listHistory(mesh)
    histories = cmds.ls(histories, type=sort_type)
    return histories[0] if histories else None


def has_tweak(mesh):
    tweak = get_history(mesh, TWEAK)
    return tweak is not None


def add_tweak(mesh):
    cmds.select(mesh, r=True)
    mel.eval('AddTweak')
    cmds.select(cl=True)


def delete_tweak(mesh):
    tweak = get_history(mesh, TWEAK)
    cmds.delete(tweak)


def freeze_cv_with_tweak(mesh):
    create_poly_tweak_uv_history(mesh)
    delete_non_deformer_history(mesh)


def freeze_cv_without_tweak(mesh):
    add_tweak(mesh)
    create_poly_tweak_uv_history(mesh)
    delete_non_deformer_history(mesh)
    delete_tweak(mesh)


# TODO: 未バインド(NonDeformer)、BS、などのパターンも網羅する
def freeze_cv():
    mesh = cmds.ls(sl=True)[0]
    _has_tweak = has_tweak(mesh)
    if _has_tweak:
        freeze_cv_with_tweak(mesh)
    else:
        freeze_cv_without_tweak(mesh)
    print(u'CVをフリーズしました。')


# Startup command
# from cv_freezer.cv_freezer import main as cv_freezer_main
# import importlib
# try:
#     importlib.reload(cv_freezer_main)
# except AttributeError:
#     reload(cv_freezer_main)
# cv_freezer_main.freeze_cv()
