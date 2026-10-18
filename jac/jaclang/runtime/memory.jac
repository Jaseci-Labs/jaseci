import logging;
import threading;
import from collections.abc { Generator }
import from uuid { UUID }

glob logger = logging.getLogger(__name__),
     __all__ = ['Memory'];


obj Memory {
    has base_path: (str | None) = None,
        target_path: (str | None) = None,
        __mem__: dict[UUID, Anchor] postinit,
        _dirty: dict[UUID, None] postinit,
        _deleted: set[UUID] postinit,
        _on_commit: list[Callable] postinit,
        _lock: threading.RLock postinit;

    has store: (any | None) {
        getter {
            return None;
        }
    }

    def postinit;
    def _init_memory;
    def new_session(target_path: str) -> Memory;
    def is_available -> bool;
    def data_location -> (str | None);
    def get(id: UUID) -> (Anchor | None);
    def put(anchor: Anchor);
    def mark_dirty(anchor: Anchor);
    def delete(id: UUID);
    def `has(id: UUID) -> bool;
    def query(
        filter: (Callable[[Anchor], bool] | None) = None
    ) -> Generator[Anchor, None, None];

    def get_roots -> Generator[Root, None, None];
    def find(
        ids: (UUID | Iterable[UUID]), filter: (Callable[[Anchor], Anchor] | None) = None
    ) -> Generator[Anchor, None, None];

    def find_one(
        ids: (UUID | Iterable[UUID]), filter: (Callable[[Anchor], Anchor] | None) = None
    ) -> (Anchor | None);

    def batch_get(ids: list[UUID]) -> dict[UUID, Anchor];
    def commit(anchor: (Anchor | None) = None);
    def abort;
    def get_mem -> dict[UUID, Anchor];
    def quarantine_ref(referrer: (Anchor | None), stub: Anchor);
    def preserve_unresolved_ref(id: UUID) -> bool;
    async def aget(id: UUID) -> (Anchor | None);
    async def aput(anchor: Anchor);
    async def adelete(id: UUID);
    async def ahas(id: UUID) -> bool;
    async def acommit(anchor: (Anchor | None) = None);
    def on_commit(callback: Callable);
    def _fire_on_commit;
    def read_barrier;
    def seal_scan;
    def unseal_scan;
    def flush(full: bool = False);
    def reset_fetch_count;
    def get_fetch_count -> int;
    def unit_enter(key: (str | None) = None);
    def unit_exit;
    def unit_depth -> int;
    def read_scope_enter;
    def read_scope_exit;
    def run_request(body: Callable) -> any;
    def close;
}

impl Memory.postinit {
    self._init_memory();
}

impl Memory._init_memory {
    self._lock = threading.RLock();
    self.__mem__ = {};
    self._dirty = {};
    self._deleted = set();
    self._on_commit = [];
}

impl Memory.new_session(target_path: str) -> Memory {
    return self;
}

impl Memory.is_available -> bool {
    return True;
}

impl Memory.data_location -> (str | None) {
    return None;
}

impl Memory.get(id: UUID) -> (Anchor | None) {
    if id in self._deleted {
        return None;
    }
    return self.__mem__.get(id);
}

impl Memory.put(anchor: Anchor) {
    aid = anchor.ensure_id();
    with self._lock {
        self.__mem__[aid] = anchor;
        self._dirty[aid] = None;
        self._deleted.discard(aid);
    }
}

impl Memory.mark_dirty(anchor: Anchor) {
    if anchor.id in self.__mem__ {
        self._dirty[anchor.id] = None;
    }
}

impl Memory.delete(id: UUID) {
    with self._lock {
        self.__mem__.pop(id, None);
        self._dirty.pop(id, None);
        self._deleted.add(id);
    }
}

impl Memory.`has(id: UUID) -> bool {
    if id in self._deleted {
        return False;
    }
    return id in self.__mem__;
}

impl Memory.query(
    filter: (Callable[[Anchor], bool] | None) = None
) -> Generator[Anchor, None, None] {
    for anchor in list(self.__mem__.values()) {
        if filter is None or filter(anchor) {
            yield anchor;
        }
    }
}

impl Memory.get_roots -> Generator[Root, None, None] {
    for anchor in list(self.__mem__.values()) {
        if isinstance(anchor.archetype, Root) {
            yield anchor.archetype;
        }
    }
}

impl Memory.find(
    ids: (UUID | Iterable[UUID]), filter: (Callable[[Anchor], Anchor] | None) = None
) -> Generator[Anchor, None, None] {
    id_list = [ids] if isinstance(ids, UUID) else list(ids);
    for id in id_list {
        if (anchor := self.get(id)) {
            if filter is None or filter(anchor) {
                yield anchor;
            }
        }
    }
}

impl Memory.find_one(
    ids: (UUID | Iterable[UUID]), filter: (Callable[[Anchor], Anchor] | None) = None
) -> (Anchor | None) {
    return next(self.find(ids, filter), None);
}

impl Memory.batch_get(ids: list[UUID]) -> dict[UUID, Anchor] {
    out: dict[UUID, Anchor] = {};
    for i in ids {
        if i in self._deleted {
            continue;
        }
        if (hit := self.__mem__.get(i)) is not None {
            out[i] = hit;
        }
    }
    return out;
}

impl Memory.commit(anchor: (Anchor | None) = None) {
    with self._lock {
        self._dirty.clear();
        self._deleted.clear();
    }
    self._fire_on_commit();
}

impl Memory.abort {
    self._dirty.clear();
    self._deleted.clear();
    self._on_commit = [];
}

impl Memory.get_mem -> dict[UUID, Anchor] {
    return self.__mem__;
}

impl Memory.quarantine_ref(referrer: (Anchor | None), stub: Anchor) {
    self.__mem__.pop(stub.ensure_id(), None);
}

impl Memory.preserve_unresolved_ref(id: UUID) -> bool {
    return False;
}

impl Memory.aget(id: UUID) -> (Anchor | None) {
    return self.get(id);
}

impl Memory.aput(anchor: Anchor) {
    self.put(anchor);
}

impl Memory.adelete(id: UUID) {
    self.delete(id);
}

impl Memory.ahas(id: UUID) -> bool {
    return self.`has(id);
}

impl Memory.acommit(anchor: (Anchor | None) = None) {
    self.commit(anchor);
}

impl Memory.on_commit(callback: Callable) {
    self._on_commit.append(callback);
}

impl Memory._fire_on_commit {
    fired = self._on_commit;
    self._on_commit = [];
    if not fired {
        return;
    }
    self.unseal_scan();
    try {
        for cb in fired {
            try {
                cb();
            } except Exception as e {
                logger.warning(f"on_commit callback failed: {type(e).__name__}: {e}");
            }
        }
    } finally {
        self.unseal_scan();
    }
}

impl Memory.read_barrier {}

impl Memory.seal_scan {}

impl Memory.unseal_scan {}

impl Memory.flush(full: bool = False) {}

impl Memory.reset_fetch_count {}

impl Memory.get_fetch_count -> int {
    return 0;
}

impl Memory.unit_enter(key: (str | None) = None) {}

impl Memory.unit_exit {}

impl Memory.unit_depth -> int {
    return 0;
}

impl Memory.read_scope_enter {}

impl Memory.read_scope_exit {}

impl Memory.run_request(body: Callable) -> any {
    result = body();
    self.commit();
    return result;
}

impl Memory.close {
    self.commit();
    self.__mem__.clear();
    self._dirty.clear();
    self._deleted.clear();
}
