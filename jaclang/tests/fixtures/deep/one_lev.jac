import:jac from .deeper, snd_lev as snd_lev;
import:jac from ..deep, deeper;

can olprint -> str {
    # deeper.snd_lev.slprint(); FIXME:
    return "one level deeper" + snd_lev.slprint();
}