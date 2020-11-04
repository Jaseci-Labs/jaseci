import { api_actions as api_act } from "./api";
import { todays_date } from "../utils/utils"

//Action Types
const LOGIN = "user_log_in"
const LOGOUT = "user_log_out"
const CREATE = "user_created"
const CHANGE_DATE = "change_date"
const LOAD_JAC = "load_jac_code"
const ERROR = "user_session_error"

//Action Creators
const session_actions = {
    create: ({ email, pass, full_name }) =>
        api_act.call({
            url: "/user/create/",
            method: "post",
            data: { email, password: pass, name: full_name },
            success_action: CREATE,
            error_action: ERROR
        }),
    login: ({ email, pass }) =>
        api_act.call({
            url: "/user/token/",
            method: "post",
            data: { email, password: pass },
            success_action: LOGIN,
            error_action: ERROR
        }),
    load_jac: (code) =>
        api_act.call({
            url: "/jac/load_application",
            method: "post",
            data: { name: "lifelogify", code },
            success_action: LOAD_JAC,
            error_action: ERROR
        }),
    change_date: (date) => ({
        type: CHANGE_DATE,
        payload: { date }
    }),
    logout: () => ({
        type: LOGOUT
    }),
    error: (pl) => ({
        type: ERROR,
        payload: pl
    }),
}

//Reducers
const init_state = {
    error: {}, logged_in: false, token: "",
    cur_date: todays_date(),
    jac_loaded: false, sentinel: null, graph: null
}
const session_reducer = (state = init_state, action) => {
    switch (action.type) {
        case LOGIN:
            return {
                ...state, error: {}, token: action.payload.token,
                logged_in: true
            };
        case LOGOUT:
            return {
                ...init_state
            };
        case CREATE:
            return { ...state, error: {}, token: "user_created", logged_in: false };
        case CHANGE_DATE:
            return { ...state, cur_date: action.payload.date.toISOString().split("T")[0] };
        case LOAD_JAC:
            //Check first that LL Jac code compiled on server
            let active_error = state.error;
            const { sentinel, graph, active } = action.payload;
            if (!active)
                active_error.messages = "CRITICAL: LL JAC NOT ACTIVE";
            return {
                ...state, error: active_error, jac_loaded: active,
                sentinel: sentinel.split(":")[2], graph: graph.split(":")[2]
            };
        case ERROR:
            return { ...state, error: action.payload };
        default:
            return state;
    }
}

export { session_actions, session_reducer };