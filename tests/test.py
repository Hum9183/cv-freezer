# -*- coding: utf-8 -*-
import sys
import unittest

from maya import cmds, mel

from ..cv_freezer import main

TEST_CV_VALUE = -2      # テスト時に設定するCV値。-2でなくてもよい
FROZEN_CV_VALUE = 0     # フリーズ後のCV値。assertEqual()で比較する
DEFORMATION_CREATE_TWEAK = 'deformationCreateTweak'


def get_deformation_create_tweak_op_var():
    """optionVar「deformationCreateTweak」の値を取得する"""
    return cmds.optionVar(q=DEFORMATION_CREATE_TWEAK)


def set_deformation_create_tweak_op_var(value):
    """optionVar「deformationCreateTweak」の値を設定する"""
    cmds.optionVar(intValue=(DEFORMATION_CREATE_TWEAK, value))


def create_skin_bound_cube():
    """スキンバインドされたCubeを生成する"""
    cube = cmds.polyCube()[0]
    cmds.select(cl=True)
    joint = cmds.joint()
    cmds.select(cl=True)
    sel = [cube, joint]
    cmds.select(sel, r=True)
    mel.eval('SmoothBindSkin')
    return cube


def set_vtx0_cv(mesh, tweak, value):
    """0番の頂点のx座標にCV値を設定する"""
    if tweak is None:
        cmds.setAttr('{}.pnts[0].pntx'.format(mesh), value)
    else:
        cmds.setAttr('{}.vlist[0].vertex[0].xVertex'.format(tweak), value)


def get_vtx0_cv(mesh, tweak):
    """0番の頂点のx座標にCV値を取得する"""
    if tweak is None:
        vtx0_cv = cmds.getAttr('{}.pnts[0].pntx'.format(mesh))
    else:
        vtx0_cv = cmds.getAttr('{}.vlist[0].vertex[0].xVertex'.format(tweak))
    return vtx0_cv


def new_scene():
    """新規シーンを開く"""
    cmds.file(force=True, new=True)


class CVFreezerTestCase(unittest.TestCase):
    def setUp(self):
        """テストメソッドの実行前に呼ばれる"""
        new_scene()

    def test_freeze_cv_with_deformers_and_tweak(self):
        """freeze_cv_with_deformers_and_tweakのテストメソッド"""
        deformation_create_tweak_orig_value = None
        if main.after_maya2022:
            # 2022以降はオプションでtweakありかなしかを変更できる
            # このテストケースでは強制的にありにする
            deformation_create_tweak_orig_value = get_deformation_create_tweak_op_var()
            set_deformation_create_tweak_op_var(True)
        cube = create_skin_bound_cube()
        tweak = main.get_history(cube, main.TWEAK)
        set_vtx0_cv(cube, tweak, TEST_CV_VALUE)
        main.freeze_cv_with_deformers_and_tweak(cube)
        vtx0_cv = get_vtx0_cv(cube, tweak)
        self.assertEqual(vtx0_cv, FROZEN_CV_VALUE)
        if main.after_maya2022:
            set_deformation_create_tweak_op_var(deformation_create_tweak_orig_value)

    def test_freeze_cv_with_deformers_without_tweak(self):
        """freeze_cv_without_tweakのテストメソッド"""
        if main.after_maya2022:
            # 2022以降はオプションでtweakありかなしかを変更できる
            # このテストケースでは強制的になしにする
            deformation_create_tweak_orig_value = get_deformation_create_tweak_op_var()
            set_deformation_create_tweak_op_var(False)
        else:
            # 2020以前はtweakは必ずあるため確定でOk
            return
        cube = create_skin_bound_cube()
        tweak = main.get_history(cube, main.TWEAK)
        set_vtx0_cv(cube, tweak, TEST_CV_VALUE)
        main.freeze_cv_with_deformers_without_tweak(cube)
        vtx0_cv = get_vtx0_cv(cube, tweak)
        self.assertEqual(vtx0_cv, FROZEN_CV_VALUE)
        if main.after_maya2022:
            set_deformation_create_tweak_op_var(deformation_create_tweak_orig_value)

    def test_freeze_cv_without_deformers(self):
        """freeze_cv_without_deformersのテストメソッド"""
        cube = cmds.polyCube()[0]
        tweak = None
        set_vtx0_cv(cube, tweak, TEST_CV_VALUE)
        main.freeze_cv_without_deformers(cube)
        vtx0_cv = get_vtx0_cv(cube, tweak)
        self.assertEqual(vtx0_cv, FROZEN_CV_VALUE)

    def tearDown(self):
        """テストメソッドの実行後に呼ばれる"""
        new_scene()


def run():
    """テストの起点"""
    test_suite = unittest.TestLoader().loadTestsFromModule(sys.modules[__name__])
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(test_suite)


# Startup command
# from cv_freezer.cv_freezer import main as cv_freezer_main
# from cv_freezer.tests import test as cv_freezer_test
# import importlib
# try:
#     importlib.reload(cv_freezer_main)
#     importlib.reload(cv_freezer_test)
# except AttributeError:
#     reload(cv_freezer_main)
#     reload(cv_freezer_test)
# cv_freezer_test.run()
