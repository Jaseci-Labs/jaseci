import { api_actions as api_act } from "./api";
import { time_now, apply_ordering } from "../utils/utils"
import store from './store';

// Action Types
const LOAD_DAY = "load_day";
// const LOAD_MITs = "load_deep_mits";
// const LOAD_WORKETTE = "load_workette";
const SET_WORKETTE = "update_workette";
const MOVE_WORKETTE = "move_workette";
const CREATE_WORKETTE = "create_workette";
const DELETE_WORKETTE = "delete_workette";
const DUMMY_DATA = "generate_dummy_data";
const ERROR = "workette_op_error";
const WKT_LOGOUT = "workette_log_out";


// Action Creators
const workette_actions = {
    load_day: (date) => {
        const { session } = store.getState();
        return api_act.call({
            url: "/jac/prime_run",
            status: "Loading Day",
            method: "post",
            data: { name: "get_gen_day", snt: session.sentinel, nd: session.graph, ctx: { date: date } },
            success_action: LOAD_DAY,
            error_action: ERROR
        });
    },
    // load_mits: (w_id) => {
    //     const { session } = store.getState();
    //     return api_act.call({
    //         url: "/jac/prime_run",
    //         method: "post",
    //         data: { name: "deep_mits", snt: session.sentinel, nd: w_id, ctx: {} },
    //         success_action: LOAD_MITs,
    //         error_action: ERROR,
    //         pass_through: { w_id: w_id }
    //     });
    // },
    // load_workette: (w_id) => {
    //     const { session } = store.getState();
    //     return api_act.call({
    //         url: "/jac/prime_run",
    //         method: "post",
    //         data: { name: "load_workette", snt: session.sentinel, nd: w_id, ctx: {} },
    //         success_action: LOAD_WORKETTE,
    //         error_action: ERROR
    //     });
    // },
    set_workette: (w_id, ctx) => {
        return api_act.call({
            url: "/jac/set_node_context",
            status: "Updating Workette",
            method: "post",
            data: { nd: w_id, ctx: ctx },
            success_action: SET_WORKETTE,
            error_acmion: ERROR
        });
    },
    move_workette: (w_id, dest_node) => {
        const { session } = store.getState();
        return api_act.call({
            url: "/jac/prime_run",
            status: "Moving Workette",
            method: "post",
            data: { name: "move_workette", snt: session.sentinel, nd: w_id, ctx: { dest_node: dest_node } },
            success_action: MOVE_WORKETTE,
            error_action: ERROR,
            pass_through: { w_id: w_id, dest_node: dest_node }
        });
    },
    create_workette: (w_id, ctx) => {
        const { session } = store.getState();
        return api_act.call({
            url: "/jac/prime_run",
            status: "Creating Workette",
            method: "post",
            data: { name: "create_workette", snt: session.sentinel, nd: w_id, ctx: ctx },
            success_action: CREATE_WORKETTE,
            error_action: ERROR,
            pass_through: { w_id: w_id }
        });
    },
    delete_workette: (w_id, parent_id) => {
        const { session } = store.getState();
        return api_act.call({
            url: "/jac/prime_run",
            status: "Deleting Workette",
            method: "post",
            data: { name: "delete_workette", snt: session.sentinel, nd: w_id, ctx: {} },
            success_action: DELETE_WORKETTE,
            error_action: ERROR,
            pass_through: { w_id: w_id, parent_id: parent_id }
        });
    },
    dummy_data: () => {
        const { session } = store.getState();
        return api_act.call({
            url: "/jac/prime_run",
            method: "post",
            data: { name: "gen_rand_life", snt: session.sentinel, nd: session.graph, ctx: {} },
            success_action: DUMMY_DATA,
            error_action: ERROR
        })
    },
    logout: () => ({
        type: WKT_LOGOUT
    }),
}




//Reducer Helpers
const load_workettes_from_payload = (pl) => {
    let additions = {}
    pl.map(x => {
        additions[x[1].jid] = x[1];
        additions[x[1].jid].children = [];
        const parent_id = 'urn:uuid:' + x[0];
        additions[x[1].jid].parent = parent_id;
        if (parent_id in additions)
            additions[parent_id].children.push(x[1].jid)
    });
    for (const i in additions) {
        const item = additions[i];
        if (item.children)
            item.children = apply_ordering(item.context.order, [...item.children])
    }
    return additions;
}



// Reducers
const init_state = { error: "", status: "", days: {}, items: {} }
const workette_reducer = (state = init_state, action) => {
    switch (action.type) {
        case LOAD_DAY:
            {
                const pl = action.payload;
                const additions = load_workettes_from_payload(pl);
                return {
                    ...state,
                    //DB of workettes for session
                    items: { ...state.items, ...additions },
                    days: { ...state.days, [pl[0][1].context.day.split('T')[0]]: pl[0][1].jid }
                };

            }
        // case LOAD_MITs:
        //     {
        //         const pl = action.payload;
        //         const { w_id } = action.payload.pass_through;
        //         let additions = {}
        //         let mit_list = [];
        //         pl.map(x => { additions[x.jid] = x; mit_list.push(x.jid); });
        //         additions[w_id] = state.items[w_id];
        //         additions[w_id].deep_mits = mit_list;
        //         return {
        //             ...state,
        //             //DB of workettes for session
        //             items: { ...state.items, ...additions },
        //         };
        //     }
        // case LOAD_WORKETTE:
        //     {
        //         const pl = action.payload;
        //         const additions = load_workettes_from_payload(pl);
        //         return {
        //             ...state,
        //             //DB of workettes for session
        //             items: { ...state.items, ...additions },
        //         };
        //     }
        case SET_WORKETTE:
            {
                let new_items = { ...state.items };
                const kids = new_items[action.payload.jid].children
                const parent = new_items[action.payload.jid].parent
                new_items[action.payload.jid] = action.payload;
                new_items[action.payload.jid].children =
                    apply_ordering(action.payload.context.order, kids);
                new_items[action.payload.jid].parent = parent;
                new_items[action.payload.jid].context.last_written = time_now()

                return {
                    ...state,
                    items: { ...new_items },
                }
            }
        case MOVE_WORKETTE:
            {
                let new_items = { ...state.items };
                const kids = new_items[action.payload[0].jid].children
                const old_parent = new_items[action.payload[0].jid].parent;
                const new_parent = action.payload.pass_through.dest_node;
                new_items[action.payload[0].jid] = action.payload[0];
                new_items[action.payload[0].jid].children =
                    apply_ordering(action.payload[0].context.order, kids);
                new_items[action.payload[0].jid].parent = new_parent;
                new_items[old_parent].children = new_items[old_parent].children.filter(v => v !== action.payload[0].jid)
                new_items[new_parent].children.push(action.payload[0].jid)
                return {
                    ...state,
                    items: { ...new_items },
                }
            }
        case CREATE_WORKETTE:
            {
                action.payload[0].children = []
                action.payload[0].parent = action.payload.pass_through.w_id
                let new_items = { ...state.items, [action.payload[0].jid]: action.payload[0] };
                new_items[action.payload.pass_through.w_id].children.push(action.payload[0].jid)
                return {
                    ...state,
                    items: { ...new_items },
                };
            }
        case DELETE_WORKETTE:
            {
                let new_items = { ...state.items };
                delete new_items[action.payload.pass_through.w_id];
                const d_idx = new_items[action.payload.pass_through.parent_id].children.indexOf(action.payload.pass_through.w_id);
                new_items[action.payload.pass_through.parent_id].children.splice(d_idx, 1);
                return {
                    ...state,
                    items: { ...new_items },
                };
            }
        case ERROR:
            return { ...state, error: action.payload }
        case WKT_LOGOUT:
            return { ...init_state }
        default:
            return state;
    }
}

export { workette_reducer, workette_actions };