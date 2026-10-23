"""Unit 7 focus / layer / overlay lifecycle surface.

Re-exports session-owned focus helpers from runtime.jac so companion tests
live in focus.test.jac (OSPUI.md §17, OSPUI-P0-PLAN Unit 7).
"""

import from .runtime {
    OverlayBounds,
    OverlayOpenResult,
    OverlayCloseResult,
    layers_paint_order,
    layers_input_order,
    focus_order,
    advance_focus,
    open_modal_overlay,
    close_overlay,
}
