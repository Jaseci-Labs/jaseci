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

export function getProp<T extends any[] | Record<any, any>>(id: string, fallback?: any): T {
  return propsStore.state.props[id] || fallback;
}

export const complexProps: Partial<Record<ComponentTags, Array<string>>> = {
  'jsc-datagrid': ['rows', 'headings'],
  'jsc-datalist': ['getters', 'template', 'layoutProps', 'body'],
  'jsc-tabs': ['tabs'],
  'jsc-dropdown': ['buttonProps', 'items'],
  'jsc-nav-bar': ['links'],
  'jsc-select': ['options'],
  'jsc-radio-group': ['options'],
  'jsc-breadcrumbs': ['links'],
  'jsc-button-group': ['buttons'],
  'jsc-hero': ['action'],
  'jsc-stat': ['stats'],
};
