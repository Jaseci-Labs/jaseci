export function format(first: string, middle: string, last: string): string {
  return (first || '') + (middle ? ` ${middle}` : '') + (last ? ` ${last}` : '');
}

export const componentMap: Record<Exclude<ComponentNames, 'App'>, ComponentTags> = {
  Navbar: 'jsc-nav-bar',
  NavLink: 'jsc-nav-link',
  Container: 'jsc-container',
  Row: 'jsc-row',
  Column: 'jsc-column',
  Button: 'jsc-button',
  Inputbox: 'jsc-inputbox',
  Textbox: 'jsc-textbox',
  Text: 'jsc-text',
};

const renderTag = (componentTag: ComponentTags, config: { withChildren: Boolean }) => `<${componentTag}>${config.withChildren ? '{children}' : ''}</${componentTag}>`;

// converts props to a string of html attributes to append to the tag
const attachProps = (renderedTag: string, props: JaseciComponent['props']) => {
  const propsString = Object.keys(props)
    .map(key => `${key}="${props[key]}"`)
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
  if (!global.__JSC_WEBKIT_OPERATIONS__[componentName]) {
    // TODO: make this private
    global.__JSC_WEBKIT_OPERATIONS__ = {
      ...global.__JSC_WEBKIT_OPERATIONS__,
      [componentName]: operations,
    };
  }
};

export const getOperations = (componentName: string) => {
  return global.__JSC_WEBKIT_OPERATIONS__[componentName];
};

const attachCSS = (renderedTag: string, css: JaseciComponent['css']) => {
  const styleString = JSON.stringify(css);
  return css ? renderedTag.replace('>', ` css=\'${styleString}\'>`) : renderedTag;
};

// creates a single tag and attaches the props in the correct format
export const renderComponent = (jaseciComponent: JaseciComponent) => {
  const renderedTag = renderTag(componentMap[jaseciComponent.component], {
    withChildren: !!jaseciComponent.sections && Object.keys(jaseciComponent.sections).length > 0,
  });
  const componentWithProps = attachProps(renderedTag, jaseciComponent.props || {});
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
