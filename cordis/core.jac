"""Cordis-style core for Osprey: revertible effects + reactive coeffects.

A compact port of the spatiotemporal composability model (Shi, Zhang, Cui,
"A Programming Paradigm for Spatiotemporal Composability", 2026) to the
Osprey na-harness.

Temporal: every context mutation flows through `set`/`effect`, which record
an explicit inverse in the acting fiber's accumulator. Unloading (or
deactivating) a fiber applies its accumulated inverses LIFO, recovering the
pre-composition state - no restart, no partial cleanup.

Spatial: components declare `inject` (required coeffect keys) and `provide`
(keys they install). After every store change the runtime re-classifies
each fiber's satisfaction and activates / deactivates it reactively, to a
fixpoint (the paper's quiescence).

Simplifications vs the paper (spike scope): fibers and components are one
object; no realms/isolation or interception yet; provisions are unique per
active fiber (enforced lightly); no async/inertia - deactivation is eager.
"""



"""An accumulator element: an inverse action plus the coeffect keys it
retracts when run (used for dependency-notification after recovery)."""
obj Inverse {
    has fn: Callable,
        args: list[any] = [],
        keys: list[str] = [];

    def run -> None {
        self.fn(*self.args);
    }
}


"""A component instantiation: coeffect spec + provision + effect function.

`apply(ctx, fiber)` runs on activation. Everything it does to the context
must go through `ctx.set` (or `ctx.effect`), which is what makes its
complete recovery structural rather than best-effort.
"""
obj Fiber {
    has name: str,
        inject: list[str] = [],
        provide: list[str] = [],
        apply: Callable | None = None,
        active: bool = False,
        parent: str = "root";

    def satisfied(ctx: EffectContext) -> bool {
        for k in self.inject {
            if not ctx.has_key(k) { return False; }
        }
        return True;
    }
}


"""The unified context: coeffect store + per-fiber inverse accumulators."""
obj EffectContext {
    has store: dict[str, object] = {},
         registry: dict[str, Fiber] = {},
         frames: dict[str, list[Inverse]] = {},
         root_frame: list[Inverse] = [],
         current_fiber: str = "",
         verbose: bool = False;

    def has_key(key: str) -> bool {
        return key in self.store;
    }

    def get(key: str) -> object {
        return self.store.get(key);
    }

    def _log(msg: str) -> None {
        if self.verbose { print("  [cordis] " + msg); }
    }

    """set(k, v) is an effect function on the coeffect store (Def. 23):
    it extends the store and returns/tracks the restriction as inverse."""
    def set(key: str, value: object) -> None {
        if key in self.store {
            raise ValueError("coeffect key already provided: " + key);
        }
        self.store[key] = value;
        inv = Inverse(fn=self.unset, args=[key], keys=[key]);
        self._record(inv);
        self._notify([key]);
    }

    """Inverse of set: restrict the store (then notify)."""
    def unset(key: str) -> None {
        self.store.pop(key, None);
        self._notify([key]);
    }

    """Record an inverse into the acting fiber's accumulator (or root)."""
    def _record(inv: Inverse) -> None {
        if self.current_fiber {
            frame: list[Inverse] | None = self.frames.get(self.current_fiber);
            if frame is None {
                frame = [];
                self.frames[self.current_fiber] = frame;
            }
            frame.append(inv);
        } else {
            self.root_frame.append(inv);
        }
    }

    """Generic revertible effect: run fn, track inverse (Alg. 1 shape)."""
    def effect(fn: Callable, args: list[any], inverse: Callable, inv_args: list[any], keys: list[str] = []) -> None {
        fn(*args);
        self._record(Inverse(fn=inverse, args=inv_args, keys=keys));
        if keys { self._notify(keys); }
    }

    """Instantiate a component as a fiber. Registers it; activates only if
    its inject-set is satisfied, else it waits Inactive (Theorem 63: deps
    constrain activation, not registration)."""
    def use(comp: Fiber) -> str {
        if comp.name in self.registry {
            raise ValueError("fiber already registered: " + comp.name);
        }
        for k in comp.provide {
            for other_name in self.registry {
                other = self.registry[other_name];
                if other.active and k in other.provide {
                    raise ValueError(
                        "provision conflict on " + k + ": " + other_name
                    );
                }
            }
        }
        self.registry[comp.name] = comp;
        self._log("registered " + comp.name);
        self._refresh();
        return comp.name;
    }

    """Withdraw a fiber: recover ALL of its effects LIFO, drop it from the
    registry, then let dependents react (they saw it stop providing)."""
    def unload(name: str) -> None {
        fiber = self.registry.get(name);
        if fiber is None { return; }
        del self.registry[name];
        self._recover_frame(name);
        self._refresh();
        self._log("unloaded " + name);
    }

    """Hot swap: dispose old, instantiate new (loader/HMR primitive)."""
    def swap(old_name: str, comp: Fiber) -> str {
        self.unload(old_name);
        return self.use(comp);
    }

    """Apply a fiber's accumulated inverses LIFO; deactivate on the way."""
    def _recover_frame(name: str) -> None {
        frame: list[Inverse] = self.frames.pop(name, []);
        fiber = self.registry.get(name);
        while frame {
            inv: Inverse = frame.pop();
            self._log("  revert " + name + ": " + str(inv.keys));
            inv.run();
        }
        if fiber is not None { fiber.active = False; }
    }

    """Re-classify every fiber's satisfaction to a fixpoint (quiescence)."""
    def _refresh() -> None {
        for _pass in range(32) {
            flipped = False;
            for name in list(self.registry.keys()) {
                fiber = self.registry[name];
                sat = fiber.satisfied(self);
                if sat and not fiber.active {
                    self._activate(name);
                    flipped = True;
                } elif fiber.active and not sat {
                    self._recover_frame(name);
                    flipped = True;
                }
            }
            if not flipped { break; }
        }
    }

    """Run the fiber's effect function under per-fiber tracking."""
    def _activate(name: str) -> None {
        fiber = self.registry.get(name);
        if fiber is None or fiber.apply is None { return; }
        prev = self.current_fiber;
        self.current_fiber = name;
        self.frames[name] = [];
        try {
            fiber.apply(self, fiber);
            fiber.active = True;
            self._log("activated " + name);
        } finally {
            self.current_fiber = prev;
        }
    }

    """Store changed: keys retract/arrive; reactive classification happens
    in _refresh via satisfaction, so notify is just the re-evaluation
    trigger (Alg. 3 collapsed into refresh for the synchronous spike)."""
    def _notify(keys: list[str]) -> None {
        return;
    }

    """Recover everything registered at root level (context reset)."""
    def dispose_all -> None {
        for name in list(self.registry.keys()) {
            self.unload(name);
        }
        while self.root_frame {
            inv: Inverse = self.root_frame.pop();
            inv.run();
        }
    }
}
