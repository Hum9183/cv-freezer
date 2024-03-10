# -*- coding: utf-8 -*-
import sys
import unittest

from maya import cmds, mel

from ..cv_freezer import main
from . import test_utils as utils


class CVFreezerTestCase(unittest.TestCase):
    def setUp(self):
        utils.new_scene()

    # TODO: 未バインド、BSなどのパターンも網羅する
    def test_freeze_cv_with_tweak(self):
        deformation_create_tweak_orig_value = None
        if main.after_maya2022:
            # 2022以降はオプションでtweakありかなしかを変更できる
            # このテストケースでは強制的にありにする
            deformation_create_tweak_orig_value = utils.get_deformation_create_tweak_op_var()
            utils.set_deformation_create_tweak_op_var(True)
        cube = utils.create_skin_bound_cube()
        tweak = main.get_history(cube, main.TWEAK)
        utils.set_vtx0_cv(cube, tweak)
        cmds.select(cube)
        main.freeze_cv()
        vtx0_cv = utils.get_vtx0_cv(cube, tweak)
        self.assertEqual(vtx0_cv, 0)
        if main.after_maya2022:
            utils.set_deformation_create_tweak_op_var(deformation_create_tweak_orig_value)

    def test_freeze_cv_without_tweak(self):
        if main.after_maya2022:
            # 2022以降はオプションでtweakありかなしかを変更できる
            # このテストケースでは強制的になしにする
            deformation_create_tweak_orig_value = utils.get_deformation_create_tweak_op_var()
            utils.set_deformation_create_tweak_op_var(False)
        else:
            # 2020以前はtweakは必ずあるため確定でOk
            return
        cube = utils.create_skin_bound_cube()
        tweak = main.get_history(cube, main.TWEAK)
        utils.set_vtx0_cv(cube, tweak)
        cmds.select(cube)
        main.freeze_cv()
        vtx0_cv = utils.get_vtx0_cv(cube, tweak)
        self.assertEqual(vtx0_cv, 0)
        if main.after_maya2022:
            utils.set_deformation_create_tweak_op_var(deformation_create_tweak_orig_value)

    def tearDown(self):
        # self.new_scene()
        pass


def get_test_suite():
    return unittest.TestLoader().loadTestsFromModule(sys.modules[__name__])


def run():
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(get_test_suite())


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
