"""Implementation for Jac's Element Abstractions"""
import:py from uuid, UUID, uuid4;

:obj:ExecutionContext:c:get_root
() {
    if <self>.master :> type == UUID {
        <self>.master = Master();
    }
    return <self>.master.root_node;
}

:obj:ExecutionContext:c:reset {
    <self>.<init>();
}