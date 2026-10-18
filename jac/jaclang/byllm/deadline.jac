import time;
import from contextvars { ContextVar }

glob _active_deadline: ContextVar[CallDeadline | None] = ContextVar(
         "byllm_call_deadline", `default=None
     );

obj CallDeadline {
    has budget: float | None = None,
        model: str = "",
        started_at: float = 0.0;

    def postinit {
        if not self.started_at {
            self.started_at = time.monotonic();
        }
    }

    def remaining -> float | None {
        if self.budget is None {
            return None;
        }
        return self.budget - (time.monotonic() - self.started_at);
    }

    def bound(seconds: float) -> float {
        left = self.remaining();
        if left is None {
            return seconds;
        }
        return max(0.0, min(seconds, left));
    }

    def check {
        left = self.remaining();
        if left is not None and left <= 0 {
            raise self.expired();
        }
    }

    def expired -> LLMTimeout {
        return LLMTimeout(
            message=(
                f"by llm() call to {self.model} did not finish within its "
                f"{self.budget:g}s timeout"
            ),
            model=self.model
        );
    }
}

def start_deadline(budget: float | None, model: str) -> CallDeadline {
    outer = _active_deadline.get();
    left = outer.remaining() if outer is not None else None;
    if left is not None {
        left = max(0.0, left);
        budget = left if budget is None else min(budget, left);
    }
    return CallDeadline(budget=budget, model=model);
}
