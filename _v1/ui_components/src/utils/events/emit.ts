import { getProp } from '../../store/propsStore';
import { getComponentByName } from '../events';

export const emit = (targetListener: string) => {
  // get the component
  const [targetComponentName, listenerName] = targetListener.split('.');
  if (typeof targetComponentName !== 'string') throw new Error('Component name must be a string');
  const targetComponent = getComponentByName(targetComponentName);

  // read listner
  if (targetComponent) {
    const listeners = targetComponent.getAttribute('listeners');
    const listenersValue = getProp(listeners, {});
    const listener = listenersValue[listenerName];

    // send changes
    Object.keys(listener).forEach(attribute => {
      if (attribute === '$call') {
        const calls = listener[attribute];
        calls.forEach(call => {
          const method = call['method'];
          if (method) {
            targetComponent[method]();
          }
        });
      } else {
        targetComponent.setAttribute(attribute, listener[attribute]);
      }
    });
  }
};
