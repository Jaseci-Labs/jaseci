import { checkCond } from './conditions';
import { renderComponentTree } from './utils';

export function setUpEvents(host: HTMLElement, events: string) {
  if (events) {
    const parsedEvents: JaseciComponent['events'] = JSON.parse(events);
    linkEvents(host, parsedEvents);
  }
}

type ParseArgsConfig = { withOriginal?: boolean };

// determine the value of a variable
export function computeVar(arg: string) {
  if (typeof arg === 'string' && arg.startsWith('var(') && arg.endsWith(')')) {
    const variableName = arg.split('var(')?.[1]?.split(')')[0];
    const [componentName, componentProperty] = variableName.split('.');
    const component = getComponentByName(componentName);
    const variableValue = component[componentProperty];
    return variableValue;
  }

  return arg;
}

// evaluates the value of an arg specified as a variable where the variable is a property name
function parseArgs(args: unknown[], config?: ParseArgsConfig) {
  const originalArgsWithNewArgs = {};
  let newArgs = [...args];
  args.map((arg, index) => {
    if (typeof arg === 'string') {
      const variableValue = computeVar(arg);
      newArgs = [...newArgs.slice(0, index), variableValue, ...newArgs.slice(index + 1)];
      originalArgsWithNewArgs[arg] = variableValue;
    }
  });

  return config?.withOriginal ? originalArgsWithNewArgs : newArgs;
}

function getComponentByName(componentName: string) {
  return window.document.querySelector('jsc-app').shadowRoot.querySelector(`[name='${componentName}']`);
}

/**
 * Evaluates the correct action to be attached to the event handler of the dom element
 */
function runAction(action: JaseciAction) {
  const actionName = action.fn;
  const actionArgs = action.args;
  const parsedActionArgs = parseArgs(action.args);

  checkCond(action.cond || []).run(() => {
    switch (actionName) {
      case 'update':
        // use actions.args because we need a ref instead of the value for the first arg of update
        const componentPropertyRef = actionArgs[0];
        if (typeof componentPropertyRef !== 'string') throw new Error('Component property reference must be a string');
        const [componentName, propertyName] = componentPropertyRef.split('.');
        const component = getComponentByName(componentName);
        const value = parsedActionArgs[1];
        update(component, propertyName, value);
        action?.onCompleted && runAction(action?.onCompleted);
        break;
      case 'append':
        const targetComponentName = actionArgs[0];
        if (typeof targetComponentName !== 'string') throw new Error('Component name must be a string');
        const targetComponent = getComponentByName(targetComponentName);
        let newComponent = actionArgs[1];
        let newComponentString = JSON.stringify(newComponent);

        append(targetComponent, newComponentString);
        action?.onCompleted && runAction(action?.onCompleted);
        break;
      default:
        new Function(`${actionName}.apply(this, ${JSON.stringify(parsedActionArgs)})`)();
    }
  });
}

/**
 * Attach events to the dom element based on the JSON structure
 */
function linkEvents(host: HTMLElement, events: JaseciComponent['events']) {
  Object.keys(events).map((eventName: JaseciEventName) => {
    switch (eventName) {
      case 'onClick': {
        events['onClick'].map(action => {
          host.addEventListener('click', () => {
            runAction(action);
          });
        });

        break;
      }
      case 'onEnter': {
        events['onEnter'].map(action => {
          host.addEventListener('keydown', keyboardEvent => {
            if (keyboardEvent.key === 'Enter') {
              runAction(action);
            }
          });
        });
        break;
      }
      case 'onKeyPress':
        events['onKeyPress'].map(action => {
          host.addEventListener('keydown', keyboardEvent => {
            if (keyboardEvent.key.toLowerCase() === action?.key?.trim().toLowerCase()) {
              runAction(action);
            }
          });
        });
        break;
      default: {
      }
    }
  });
}

// BUILT-IN Actions
function update(element: Element, property: string, value: unknown) {
  element[property] = value;
}

function append(targetComponent: Element, newComponentString: string) {
  // extract vars
  const variables = newComponentString.match(/var[(](.*?)[)]/g);
  const parsedArgs = parseArgs(variables, { withOriginal: true });

  Object.keys(parsedArgs).map(variable => {
    newComponentString = newComponentString.replaceAll(variable, parsedArgs[variable]);
  });

  let newComponent = JSON.parse(newComponentString);

  targetComponent.shadowRoot.innerHTML += renderComponentTree([newComponent] as any);
}
