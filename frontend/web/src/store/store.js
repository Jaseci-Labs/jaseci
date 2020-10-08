import { createStore, combineReducers, applyMiddleware, compose } from 'redux';
import { workette_reducer } from './workette';
import { session_reducer } from './session';
import { logger /*, func*/ } from './middleware';
import { api_middleware, api_reducer } from './api';

const enhancers = compose(applyMiddleware(logger, /*func,*/ api_middleware),
    window.__REDUX_DEVTOOLS_EXTENSION__ ? window.__REDUX_DEVTOOLS_EXTENSION__() : f => f);


const reducers = combineReducers({
    workette: workette_reducer,
    session: session_reducer,
    api: api_reducer,
});

const store = createStore(reducers, enhancers);

export default store;