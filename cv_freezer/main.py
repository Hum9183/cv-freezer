# -*- coding: utf-8 -*-
from maya import cmds, mel

maya_version = int(cmds.about(v=True))
after_maya2022 = maya_version >= 2022

TWEAK = 'tweak'


def create_poly_tweak_uv_history(mesh):
    """polyTweakUVヒストリを生成する"""
    cmds.select('{}.map[0]'.format(mesh), r=True)   # 0番のUVを選択する
    cmds.polyEditUV(u=1)                            # U軸を1移動する
    cmds.polyEditUV(u=-1)                           # U軸を-1移動する(もとに戻す)
    cmds.select(cl=True)


def delete_history(mesh):
    """「ヒストリ」を削除する"""
    cmds.select(mesh)
    mel.eval('DeleteHistory')
    cmds.select(cl=True)


def delete_non_deformer_history(mesh):
    """「デフォーマ以外のヒストリ」を削除する"""
    cmds.select(mesh)
    mel.eval('BakeNonDefHistory')
    cmds.select(cl=True)


def get_history(mesh, history_type):
    """ヒストリを取得する"""
    histories = cmds.listHistory(mesh)
    histories = cmds.ls(histories, type=history_type)
    return histories[0] if histories else None


def has_tweak(mesh):
    """tweakを持っているかどうか"""
    tweak = get_history(mesh, TWEAK)
    return tweak is not None


def add_tweak(mesh):
    """tweakを追加する"""
    cmds.select(mesh, r=True)
    mel.eval('AddTweak')
    cmds.select(cl=True)


def delete_tweak(mesh):
    """tweakを削除する"""
    tweak = get_history(mesh, TWEAK)
    cmds.delete(tweak)


def has_deformers(mesh):
    deformers = cmds.findDeformers(mesh)
    return deformers is not None


def freeze_cv_with_deformers_and_tweak(mesh):
    """CV値をフリーズする(deformerあり、tweakあり)"""
    create_poly_tweak_uv_history(mesh)
    delete_non_deformer_history(mesh)


def freeze_cv_with_deformers_without_tweak(mesh):
    """CV値をフリーズする(deformerあり、tweakなし)"""
    add_tweak(mesh)
    create_poly_tweak_uv_history(mesh)
    delete_non_deformer_history(mesh)
    delete_tweak(mesh)


def freeze_cv_without_deformers(mesh):
    """CV値をフリーズする(deformerなし)"""
    mel.eval('CreateLattice')
    delete_history(mesh)


def main():
    """ツールの起点"""
    mesh = cmds.ls(sl=True)[0]
    _has_deformers = has_deformers(mesh)
    if _has_deformers:
        _has_tweak = has_tweak(mesh)
        if _has_tweak:
            freeze_cv_with_deformers_and_tweak(mesh)
        else:
            freeze_cv_with_deformers_without_tweak(mesh)
    else:
        freeze_cv_without_deformers(mesh)
    print(u'CV値をフリーズしました。')


# # Startup command
# from cv_freezer.cv_freezer import main as cv_freezer_main
# import importlib
# try:
#     importlib.reload(cv_freezer_main)
# except AttributeError:
#     reload(cv_freezer_main)
# cv_freezer_main.main()
