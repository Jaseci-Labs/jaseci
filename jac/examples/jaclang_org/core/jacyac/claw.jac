import from "react" { useEffect }
import from "@jac/runtime" { BridgeError }

obj ClawModel {
    has activity: Activity | None,
        job: JobView | None,
        tutorials: list[TutorialCard],
        tutorial: TutorialView | None,
        loading: bool,
        error: str,
        refresh: Callable[[], None];
}

glob CLAW_POLL_MS: int = 3000;

def:pub useClaw(view: str, focus: str) -> ClawModel;

impl useClaw(view: str, focus: str) -> ClawModel {
    has activity: Activity | None = None,
        job: JobView | None = None,
        tutorials: list[TutorialCard] = [],
        tutorial: TutorialView | None = None,
        loading: bool = False,
        error: str = "";

    async def refresh {
        try {
            if view == "ninjaclaw" {
                activity = await ninjaclaw_activity();
                if focus {
                    job = await ninjaclaw_job(job_id=focus);
                } else {
                    job = None;
                }
            } elif view == "tutorials" {
                if focus {
                    tutorial = await ninjaclaw_tutorial(slug=focus);
                } else {
                    tutorial = None;
                }
                tutorials = await ninjaclaw_tutorials();
            }
            error = "";
        } except BridgeError {
            error = "Can't reach ninjaclaw right now. Try again in a moment.";
        } finally {
            loading = False;
        }
    }

    async can with (view, focus) entry {
        if view == "ninjaclaw" or view == "tutorials" {
            loading = True;
            await refresh();
        }
    }

    useEffect(
        lambda {
            if view != "ninjaclaw" {
                return lambda {};
            }
            interval = setInterval(lambda { refresh(); }, CLAW_POLL_MS);
            return lambda { clearInterval(interval); };
        },
        [view, focus]
    );

    return ClawModel(
        activity=activity,
        job=job,
        tutorials=tutorials,
        tutorial=tutorial,
        loading=loading,
        error=error,
        refresh=refresh
    );
}
