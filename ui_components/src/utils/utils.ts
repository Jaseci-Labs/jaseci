import { storeProp } from '../store/propsStore';
import { componentMap } from './registry';
let globalOperations = {};
export function format(first: string, middle: string, last: string): string {
  return (first || '') + (middle ? ` ${middle}` : '') + (last ? ` ${last}` : '');
}

const renderTag = (componentTag: ComponentTags, config: { withChildren: Boolean }) => `<${componentTag}>${config.withChildren ? '{children}' : ''}</${componentTag}>`;

// converts props to a string of html attributes to append to the tag
const attachProps = (renderedTag: string, props: JaseciComponent['props']) => {
  const propsString = Object.keys(props)
    .map(key => {
      const prop = storeProp(renderedTag, key, props[key]);
      console.log({ prop });

      return `${key}="${prop}"`;
    })
    .join(' ');

  return renderedTag.replace('>', ` ${propsString}>`);
};

const attachName = (renderedTag: string, name: string) => {
  return name ? renderedTag.replace('>', ` name="${name}">`) : renderedTag;
};

const attachEvents = (renderedTag: string, events: JaseciComponent['events']) => {
  const eventsString = JSON.stringify(events);
  return events ? renderedTag.replace('>', ` events=\'${eventsString}\'>`) : renderedTag;
};

const setOperations = (operations: JaseciComponent['operations'], componentName: string) => {
  if (!globalOperations[componentName]) {
    globalOperations = {
      ...globalOperations,
      [componentName]: operations,
    };
  }
};

export const getOperations = (componentName: string) => {
  return globalOperations[componentName];
};

const attachCSS = (renderedTag: string, css: JaseciComponent['css']) => {
  const styleString = JSON.stringify(css);
  return css ? renderedTag.replace('>', ` css=\'${styleString}\'>`) : renderedTag;
};

// creates a single tag and attaches the props in the correct format
export const renderComponent = (jaseciComponent: JaseciComponent) => {
  console.log({ listeners: jaseciComponent.listeners });
  const renderedTag = renderTag(componentMap[jaseciComponent.component], {
    withChildren: !!jaseciComponent.sections && Object.keys(jaseciComponent.sections).length > 0,
  });
  const componentWithProps = attachProps(
    renderedTag,
    {
      ...jaseciComponent.props,
      listeners: jaseciComponent.listeners,
    } || {},
  );
  const componentWithName = attachName(componentWithProps, jaseciComponent.name);
  const componentWithEvents = attachEvents(componentWithName, jaseciComponent.events);
  setOperations(jaseciComponent.operations, jaseciComponent.name);
  const componentWithCSS = attachCSS(componentWithEvents, jaseciComponent.css || {});

  return componentWithCSS;
};

// generates the html structure that will be rendered
export const renderComponentTree = (jaseciNodes: Array<JaseciComponent>) => {
  let markup = '';

  if (jaseciNodes) {
    jaseciNodes.map(node => {
      markup += renderComponent(node);
      // render child nodes
      if (node.sections) {
        Object.keys(node.sections).map(sectionName => {
          // replace the last children placeholder in the markup with the current node
          // inserts one node into another
          markup = markup.replace(new RegExp('{children}'), `<div slot="${sectionName}">${renderComponentTree(node.sections[sectionName])}</div>`);
        });
      }
    });
  }

  return markup;
};
