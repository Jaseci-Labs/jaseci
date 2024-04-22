if last_run is None {
    here.user_level_buddy_schedule[
        "d1_reminder"
    ]["last_run"] = now_tz.isoformat();
    self.user_root_node.messages["web"].append(
        {"type": "mid_day_nudge", "message": res["response"]}
    );
}