"""Built in actions for Jaseci"""
import diff_match_patch as dmp_module
from jaseci.actions.live_actions import jaseci_action

@jaseci_action(act_group=["patch"], allow_remote=True)
def get_patch(text1: str, text2: str):
    """
    Create an array of patch objects
    Param 1 - First text
    Param 2 - Second text

    Return - Array of patches
    """
    dmp = dmp_module.diff_match_patch()
    return dmp.patch_make(text1, text2)

@jaseci_action(act_group=["patch"], allow_remote=True)
def get_patch(diff: list):
    """
    Create an array of patch objects
    Param 1 - Diff array

    Return - Array of patches
    """
    dmp = dmp_module.diff_match_patch()
    return dmp.patch_make(diff)

@jaseci_action(act_group=["patch"], allow_remote=True)
def get_patch(text1: str, diff: list):
    """
    Create an array of patch objects
    Param 1 - First text
    Param 2 - Diff array

    Return - Array of patches
    """
    dmp = dmp_module.diff_match_patch()
    return dmp.patch_make(text1, diff)

@jaseci_action(act_group=["patch"], allow_remote=True)
def get_text(patch: list):
    """
    Convert patch list to a block of text
    Param 1 - Patch array

    Return - String
    """
    dmp = dmp_module.diff_match_patch()
    return dmp.patch_toText(patch)

@jaseci_action(act_group=["patch"], allow_remote=True)
def text_toPatch(text: str):
    """
    Convert a block of text to a patch
    Param 1 - String

    Return - Patch array
    """
    dmp = dmp_module.diff_match_patch()
    return dmp.patch_fromText(text)

@jaseci_action(act_group=["patch"], allow_remote=True)
def apply(patch: list, text1: str, threshold: 0.5):
    """
    Apply a patch list to a text
    Param 1 - Patch array
    Param 2 - First text
    Param 3 - Deletion threshold

    Return - [Second text, Results]
    """
    dmp = dmp_module.diff_match_patch()
    dmp.Patch_DeleteThreshold = threshold
    return dmp.patch_apply(patch, text1)