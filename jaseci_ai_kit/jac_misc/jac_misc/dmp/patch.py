"""Built in actions for Jaseci"""
import diff_match_patch as dmp_module
from jaseci.jsorc.live_actions import jaseci_action


@jaseci_action(act_group=["patch"], allow_remote=True)
def get_patch(*args):
    """
    Create an array of patch objects
    Param 1 - First text
    Param 2 - Second text
    OR
    Param 1 - Diff array
    OR 
    Param 1 - First text
    Param 2 - Diff array

    Return - Array of patches
    """
    if len(args) == 1:
        dmp = dmp_module.diff_match_patch()
        return dmp.patch_make(args[0])
    elif len(args) == 2 and ((isinstance(args[0], str) and isinstance(args[1], str)) 
                             or (isinstance(args[0], str) and isinstance(args[1], list))):
        dmp = dmp_module.diff_match_patch()
        return dmp.patch_make(args[0], args[1])
    else:
        raise TypeError("Invalid argument types, please check the documentation")


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
def text_to_patch(text: str):
    """
    Convert a block of text to a patch
    Param 1 - String

    Return - Patch array
    """
    dmp = dmp_module.diff_match_patch()
    return dmp.patch_fromText(text)


@jaseci_action(act_group=["patch"], allow_remote=True)
def apply(patch: list, text1: str, threshold: int = 0.5):
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
