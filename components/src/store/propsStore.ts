import { nanoid } from 'nanoid';
import { createStore } from '@stencil/store';

export const propsStore = createStore({
  props: {},
});

export function storeProp(renderedTag: string, propName: string, value: any) {
  let result: string = value;

  Object.keys(complexProps).forEach(tagName => {
    if (propName === 'listeners') {
      const id = nanoid();
      propsStore.state.props[id] = value;

      result = id;
    } else {
      if (renderedTag.includes(tagName)) {
        if (complexProps[tagName].includes(propName)) {
          const id = nanoid();
          propsStore.state.props[id] = value;

          result = id;
        }
      }
    }
  });

  return result;
}

export function getProp(id: string, fallback?: any) {
  return propsStore.state.props[id] || fallback;
}

export const complexProps: Partial<Record<ComponentTags, Array<string>>> = {
  'jsc-datagrid': ['rows', 'headings'],
  'jsc-datalist': ['getters', 'template', 'layoutProps', 'body'],
  'jsc-tabs': ['tabs'],
};
