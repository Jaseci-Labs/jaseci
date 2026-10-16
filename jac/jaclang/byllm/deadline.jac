import contextvars;
import queue;
import threading;
import time;
import from typing { Generator }
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

    def iterate(stream: Iterable[any]) -> Generator[any, None, None] {
        if self.budget is None {
            yield from stream;
            return;
        }
        items: queue.Queue[tuple[any, Exception | None]] = queue.Queue();
        finished = object();

        def pump {
            try {
                for item in stream {
                    items.put((item, None));
                }
                items.put((finished, None));
            } except Exception as e {
                items.put((None, e));
            }
        }
        threading.Thread(
            target=contextvars.copy_context().run, args=(pump, ), daemon=True
        ).start();
        try {
            while True {
                left = self.remaining() or 0.0;
                if left <= 0 {
                    raise self.expired();
                }
                try {
                    (item, error) = items.get(timeout=left);
                } except queue.Empty {
                    raise self.expired() from None;
                }
                if error is not None {
                    raise error;
                }
                if item is finished {
                    return;
                }
                yield item;
            }
        } finally {
            source = stream?.completion_stream or stream;
            close = source?.close;
            if callable(close) {
                try {
                    close();
                } except Exception {}
            }
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
