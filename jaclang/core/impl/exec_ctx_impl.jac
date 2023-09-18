"""Implementation for Jac's Element Abstractions"""
import:py from uuid, UUID, uuid4;

:object:ExecutionContext:a:get_root
() {
    if <self>.master :> type == UUID {
        <self>.master = Master();
    }
    return <self>.master.root_node;
}

:object:ExecutionContext:a:reset {
    <self>.<init>();
}