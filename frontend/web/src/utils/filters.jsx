import store from "../store/store";

const workette_filters = {
  scheduled_now: function (w) {
    const { session } = store.getState();
    const ctx = w.context;
    if (
      ctx.is_ritual &&
      !ctx.is_ritual[new Date(store.getState().session.cur_date).getDay()]
    )
      if (ctx.status === "done") return true;
      else return false;

    if (ctx.snooze_till) {
      let d1 = new Date(ctx.snooze_till);
      let d2 = new Date(session.cur_date);
      if (ctx.snooze_till && d1 > d2) return false;
    }
    return true;
  },

  active_workette: function (w) {
    if (!workette_filters.scheduled_now(w)) return false;
    const ctx = w.context;
    if (!ctx.wtype || ctx.wtype === "workette" || ctx.wtype == "none")
      return true;
    return false;
  },

  active_ritual: function (w) {
    const ctx = w.context;
    return workette_filters.scheduled_now(w) && ctx.is_ritual;
  },

  open: function (w) {
    if (!workette_filters.scheduled_now(w)) return false;
    const ctx = w.context;
    if (!ctx.status || ctx.status === "open" || ctx.status === "running")
      if (!ctx.wtype || ctx.wtype === "workette" || ctx.wtype == "none")
        return true;
    return false;
  },

  complete: function (w) {
    const ctx = w.context;
    if (ctx.status === "done") return true;
    return false;
  },

  running: function (w) {
    const ctx = w.context;
    if (ctx.status === "running") return true;
    return false;
  },

  canceled: function (w) {
    const ctx = w.context;
    if (ctx.status === "canceled") return true;
    return false;
  },

  allChildren: function (w) {
    const { items } = store.getState().workette;
    let ret = [];
    if (!w || !w.children) return ret;
    w.children.map((x) => {
      ret.push(...workette_filters.allChildren(items[x]));
    });
    ret.push(w);
    return ret;
  },

  deepMIT: function (w_id = null) {
    const { items } = store.getState().workette;
    let current =
      items[store.getState().workette.days[store.getState().session.cur_date]];
    if (w_id) current = items[w_id];
    let ret = [];
    workette_filters.allChildren(current).map((k) => {
      if (
        k.context.is_MIT &&
        workette_filters.open(k) &&
        workette_filters.scheduled_now(k) &&
        !workette_filters.running(k)
      )
        ret.push(k.jid);
    });
    return ret;
  },

  deepActiveRituals: function (w_id = null) {
    const { items } = store.getState().workette;
    let current =
      items[store.getState().workette.days[store.getState().session.cur_date]];
    if (w_id) current = items[w_id];
    let ret = [];
    workette_filters.allChildren(current).map((k) => {
      if (workette_filters.active_ritual(k)) ret.push(k.jid);
    });
    return ret;
  },

  deepRunning: function (w_id = null) {
    const { items } = store.getState().workette;
    let current =
      items[store.getState().workette.days[store.getState().session.cur_date]];
    if (w_id) current = items[w_id];
    let ret = [];
    workette_filters.allChildren(current).map((k) => {
      if (workette_filters.running(k)) ret.push(k.jid);
    });
    return ret;
  },

  deepCompleted: function (w_id = null) {
    const { items } = store.getState().workette;
    let current =
      items[store.getState().workette.days[store.getState().session.cur_date]];
    if (w_id) current = items[w_id];
    let ret = [];
    workette_filters.allChildren(current).map((k) => {
      if (workette_filters.complete(k)) ret.push(k.jid);
    });
    return ret;
  },

  deepCanceled: function (w_id = null) {
    const { items } = store.getState().workette;
    let current =
      items[store.getState().workette.days[store.getState().session.cur_date]];
    if (w_id) current = items[w_id];
    let ret = [];
    workette_filters.allChildren(current).map((k) => {
      if (k.context.status === "canceled") ret.push(k.jid);
    });
    return ret;
  },

  // Get total number of items inside workette thats available
  // self_call is used internally to prevent counting the head workette
  countDeepChildren: function (w, self_call = false) {
    const { items } = store.getState().workette;
    let count = self_call && workette_filters.active_workette(w) ? 1 : 0;
    w.children.map((i) => {
      count += workette_filters.countDeepChildren(items[i], true);
    });
    return count;
  },

  // Get total number of items that has been closed
  // self_call is used to prevent counting the head workette
  countDeepChildrenClosed: function (w, self_call = false) {
    const { items } = store.getState().workette;
    let count =
      self_call &&
      workette_filters.active_workette(w) &&
      (workette_filters.complete(w) || workette_filters.canceled(w))
        ? 1
        : 0;
    w.children.map((i) => {
      count += workette_filters.countDeepChildrenClosed(items[i], true);
    });
    return count;
  },
};

export { workette_filters };
