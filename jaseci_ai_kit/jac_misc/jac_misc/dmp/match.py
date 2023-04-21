"""Built in actions for Jaseci"""
import diff_match_patch as dmp_module
from jaseci.jsorc.live_actions import jaseci_action


@jaseci_action(act_group=["match"], allow_remote=True)
def get_match(
    text: str, pattern: str, loc: int, dist: int = 1000, threshold: float = 0.5
):
    """
    Finds occurences in text near loc that match pattern
    Param 1 - Input text
    Param 2 - Pattern to match
    Param 3 - Expected location
    Param 4 - Match distance
    Param 5 - Match accuracy threshold

    Return - Location of closest match
    """
    dmp = dmp_module.diff_match_patch()
    dmp.Match_Distance = dist
    dmp.Match_Threshold = threshold
    return dmp.match_main(text, pattern, loc)
