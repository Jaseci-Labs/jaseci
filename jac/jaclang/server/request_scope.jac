import logging;
import from contextvars { Token }
import from types { TracebackType }

glob logger: logging.Logger = logging.getLogger('jaclang.serve');


obj RequestScope {
    has context: ExecutionContext,
        _token: Token[(ExecutionContext | None)],
        _aborted: bool = False;

    static def open(
        base_path_dir: (str | None) = None, full_target_path: (str | None) = None
    ) -> RequestScope;

    static def current -> ExecutionContext;
    def abort;
    def _discard;
    def close;
    def __enter__ -> ExecutionContext;
    def __exit__(
        exc_type: (type[BaseException] | None),
        exc: (BaseException | None),
        tb: (TracebackType | None)
    ) -> bool;
}

impl RequestScope.open(
    base_path_dir: (str | None) = None, full_target_path: (str | None) = None
) -> RequestScope {
    context = JacRuntime.create_j_context(
        user_root=None, base_path_dir=base_path_dir, full_target_path=full_target_path
    );
    return RequestScope(
        context=context, _token=JacRuntime.push_request_context(context)
    );
}

impl RequestScope.current -> ExecutionContext {
    context = JacRuntime.request_context();
    if context is None {
        raise RuntimeError(
            'No request scope is open. A walker or function is executed '
            'inside RequestScope.open(), which gives the call a context and '
            'session of its own; the process-global context is not a '
            'request context.'
        );
    }
    return context;
}

impl RequestScope.abort {
    self._aborted = True;
    self._discard();
}

impl RequestScope._discard {
    self.context.mem.abort();
    self.context.pending_effects.clear();
}

impl RequestScope.close {
    try {
        if self._aborted {
            self._discard();
        }
        self.context.close();
    } except Exception as e {
        logger.warning(f"Failed to close request context: {e}", exc_info=True);
    } finally {
        JacRuntime.reset_request_context(self._token);
    }
}

impl RequestScope.__enter__ -> ExecutionContext {
    return self.context;
}

impl RequestScope.__exit__(
    exc_type: (type[BaseException] | None),
    exc: (BaseException | None),
    tb: (TracebackType | None)
) -> bool {
    self.close();
    return False;
}
