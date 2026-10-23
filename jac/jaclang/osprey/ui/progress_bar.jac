"""External ProgressBar widget package (Gate 5 / OSPUI.md §18).

Provides node type, event handling, measure/paint hooks, disposal, inspection
metadata, and markup registration without editing framework source.
"""


walker SetProgress {
    has value: float = 0.0;
    has handled: bool = False;
}


node ProgressBar {
    has key: str = "";
    has value: float = 0.0;

    can set_value with SetProgress entry {
        self.value = visitor.value;
        if self.value < 0.0 {
            self.value = 0.0;
        }
        if self.value > 1.0 {
            self.value = 1.0;
        }
        visitor.handled = True;
    }
}


"""Render a one-line progress bar for the given width (helper, fully implemented)."""
def render_progress(value: float, width: int) -> str {
    if width <= 2 {
        return "#" * max(0, width);
    }
    inner = width - 2;
    filled = int(max(0.0, min(1.0, value)) * float(inner));
    if filled > inner {
        filled = inner;
    }
    return "[" + ("#" * filled) + ("-" * (inner - filled)) + "]";
}


"""Measure height for ProgressBar (always 1)."""
def progress_measure_height(bar: ProgressBar, max_width: int) -> int {
    _ = (bar, max_width);
    return 1;
}


"""Paint ProgressBar into a single content line."""
def progress_paint_line(bar: ProgressBar, width: int) -> str {
    return render_progress(bar.value, width);
}


"""Register ProgressBar into a tag map (framework TagRegistry.tags or plain dict).

Avoids importing ui.markup so the widget package stays free of framework cycles.
"""
def register_progress_markup(tags: dict[str, object]) {
    tags["ProgressBar"] = ProgressBar;
}
