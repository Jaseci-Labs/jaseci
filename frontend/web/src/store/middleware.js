const logger = store => next => action => {
    next(action);
}

//Middleware to convert functions to action objects for reducers
const func = ({ dispatch, getState }) => next => action => {
    if (typeof action === 'function') action(dispatch, getState);
    else next(action);
}

export { logger, func };