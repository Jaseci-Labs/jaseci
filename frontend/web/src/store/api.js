import axios from 'axios';

// Action Types
const API_CALL = "api_call";
const API_SUCCESS = "api_success";
const API_FAIL = "api_failed";
const JSCI_BASE_URL = process.env.REACT_APP_JASECI_URL

// Action Creators
const api_actions = {
    call: ({ url, status, method, data, success_action, error_action, pass_through }) => ({
        type: API_CALL,
        payload: {
            url,
            status,
            method: (method) ? method : "get",
            data: (data) ? data : {},
            success_action,
            error_action,
            pass_through
        }
    }),
    success: (pl) => ({
        type: API_SUCCESS,
        payload: pl
    }),
    failed: (pl) => ({
        type: API_FAIL,
        payload: pl
    }),
}

//Middleware for API calls that will hit store
const api_middleware = ({ dispatch, getState }) => next => async action => {
    if (action.type !== "api_call") return next(action);
    next(action);

    const { url, method, data, success_action, error_action, pass_through }
        = action.payload;

    try {
        const response = await axios.request({
            baseURL: JSCI_BASE_URL,
            url,
            method,
            data
        });
        response.data.pass_through = pass_through
        dispatch(api_actions.success(response.data))
        if (success_action)
            dispatch({ type: success_action, payload: response.data })
    } catch (error) {
        const report = {};
        if (error.message) report.messages = error.message;
        if (error.response) report.response = error.response;
        dispatch(api_actions.failed(report));
        if (error_action)
            dispatch({ type: error_action, payload: report })
    }
}

// Reducers
const init_state = { is_loading: false }
const api_reducer = (state = init_state, action) => {
    switch (action.type) {
        case API_CALL:
            const status = action.payload.status ? action.payload.status : "Working"
            return { ...state, is_loading: status }
        case API_FAIL:
            return { ...state, is_loading: false }
        case API_SUCCESS:
            return { ...state, is_loading: false }
        default:
            return state;
    }
}


export { api_actions, api_middleware, api_reducer };