"""Fail if frontend capture APIs run while building/compiling/executing V2."""
from contextlib import ExitStack, contextmanager
import sys
from torch._dynamo.utils import identity
from unittest.mock import patch
import torch
import torch._dynamo as dynamo
import torch._dynamo.convert_frame as convert_frame
# Import the backend before installing probes (not executing/capturing a model).
from torch._inductor.compile_fx import compile_fx  # noqa: F401


@contextmanager
def forbid_frontend_capture():
    calls = []
    backend_symbolic_traces = []
    entries = [(torch, 'compile', 'torch.compile'),
               (dynamo, 'optimize', 'torch._dynamo.optimize'),
               (dynamo, 'optimize_assert', 'torch._dynamo.optimize_assert'),
               (dynamo, 'export', 'torch._dynamo.export'),
               (convert_frame, '_compile', 'torch._dynamo.convert_frame._compile'),
               (torch.export, 'export', 'torch.export.export'),
               (torch.jit, 'trace', 'torch.jit.trace')]
    def blocked(name):
        def fail(*args, **kwargs):
            calls.append(name)
            raise AssertionError('Forbidden frontend capture: ' + name)
        return fail
    with ExitStack() as stack:
        for owner, name, label in entries:
            stack.enter_context(patch.object(owner, name, blocked(label)))
        original_trace = torch.fx.symbolic_trace
        def checked_symbolic_trace(root, *args, **kwargs):
            module = getattr(root, '__module__', type(root).__module__)
            caller = sys._getframe(1).f_globals.get('__name__')
            if root is not identity or caller != 'torch._inductor.loop_body':
                calls.append('torch.fx.symbolic_trace:' + module)
                raise AssertionError('symbolic_trace of non-Inductor frontend is forbidden: ' + module)
            backend_symbolic_traces.append(module + '.' + root.__qualname__ + ' called by ' + caller)
            return original_trace(root, *args, **kwargs)
        stack.enter_context(patch.object(torch.fx, 'symbolic_trace', checked_symbolic_trace))
        report = dict(probed_entries=[label for _, _, label in entries] + ['torch.fx.symbolic_trace frontend roots'],
                      calls=calls, allowed_inductor_internal_symbolic_traces=backend_symbolic_traces)
        yield report
    assert not calls
