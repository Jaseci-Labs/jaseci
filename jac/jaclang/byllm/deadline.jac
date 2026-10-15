import time;
import from jaclang.byllm.exceptions { LLMTimeout }

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

    def allows(delay: float) -> bool {
        left = self.remaining();
        return left is None or left > delay;
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
