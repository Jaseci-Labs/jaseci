"""Built in actions for Jaseci"""
import diff_match_patch as dmp_module
from jaseci.actions.live_actions import jaseci_action

@jaseci_action(act_group=["diff"], allow_remote=True)
def get_diff(text1: str, text2: str, timeout: float = 1.0):
    """
    Finds differences between text1 and text2
    Param 1 - First text
    Param 2 - Second text
    Param 3 - Timeout

    Return - Diff array
    """
    dmp = dmp_module.diff_match_patch()
    dmp.Diff_Timeout = timeout
    diff = dmp.diff_main(text1, text2)
    return diff

@jaseci_action(act_group=["diff"], allow_remote=True)
def semantic_clean(diff: list):
    """
    Cleans up the diff to remove coincidental matches
    Param 1 - Diff array

    Return - human-readable diff array
    """
    dmp = dmp_module.diff_match_patch()
    diff = dmp.diff_cleanupSemantic(diff)
    return diff

@jaseci_action(act_group=["diff"], allow_remote=True)
def efficient_clean(diff: list, cost: int = 4):
    """
    Cleans up the diff to be efficient for machine processing
    Param 1 - Diff array
    Param 2 - Edit cost

    Return - Machine-efficient diff array
    """
    dmp = dmp_module.diff_match_patch()
    dmp.Diff_Edit_Cost = cost
    diff = dmp.diff_cleanupEfficiency(diff)
    return diff

@jaseci_action(act_group=["diff"], allow_remote=True)
def get_lvsht(diff: list):
    """
    Gets the Levenshtein distance of a diff
    Param 1 - Diff array

    Return - Levenshtein distance integer
    """
    dmp = dmp_module.diff_match_patch()
    cost = dmp.diff_levenshtein(diff)
    return cost

@jaseci_action(act_group=["diff"], allow_remote=True)
def get_html(diff: list):
    """
    Returns the diff in pretty HTML format
    Param 1 - Diff array

    Return - HTML document
    """
    dmp = dmp_module.diff_match_patch()
    html = dmp.diff_prettyHtml(diff)
    return html

if __name__ == "__main__":
    from jaseci.jsorc.remote_actions import launch_server

    launch_server(port=8000)


    
