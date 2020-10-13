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

  open: function (w) {
    if (!workette_filters.scheduled_now(w)) return false;
    const ctx = w.context;
    if (!ctx.status || ctx.status === "open")
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

  deepMIT: function () {
    const { items } = store.getState().workette;
    const current =
      items[store.getState().workette.days[store.getState().session.cur_date]];
    let ret = [];
    workette_filters.allChildren(current).map((k) => {
      if (
        k.context.is_MIT &&
        workette_filters.open(k) &&
        workette_filters.scheduled_now(k)
      )
        ret.push(k.jid);
    });
    return ret;
  },

  deepRunning: function () {
    const { items } = store.getState().workette;
    const current =
      items[store.getState().workette.days[store.getState().session.cur_date]];
    let ret = [];
    workette_filters.allChildren(current).map((k) => {
      if (workette_filters.running(k)) ret.push(k.jid);
    });
    return ret;
  },

  deepCompleted: function () {
    const { items } = store.getState().workette;
    const current =
      items[store.getState().workette.days[store.getState().session.cur_date]];
    let ret = [];
    workette_filters.allChildren(current).map((k) => {
      if (workette_filters.complete(k)) ret.push(k.jid);
    });
    return ret;
  },

  deepCanceled: function () {
    const { items } = store.getState().workette;
    const current =
      items[store.getState().workette.days[store.getState().session.cur_date]];
    let ret = [];
    workette_filters.allChildren(current).map((k) => {
      if (k.context.status === "canceled") ret.push(k.jid);
    });
    return ret;
  },
};

export { workette_filters };
