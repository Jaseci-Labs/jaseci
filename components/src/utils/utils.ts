export function format(first: string, middle: string, last: string): string {
  return (first || '') + (middle ? ` ${middle}` : '') + (last ? ` ${last}` : '');
}

export const componentMap: Record<Exclude<ComponentNames, 'App'>, ComponentTags> = {
  Navbar: 'jsc-nav-bar',
  NavLink: 'jsc-nav-link',
  Container: 'jsc-container',
  Row: 'jsc-row',
};

const renderTag = (componentTag: ComponentTags, config: { withChilren: Boolean }) => `<${componentTag}>${config.withChilren ? '{children}' : ''}</${componentTag}>`;

// converts props to a string of html attributes to append to the tag
const attachProps = (renderedTag: string, props: Record<string, unknown>) => {
  const propsString = Object.keys(props)
    .map(key => `${key}="${props[key]}"`)
    .join(' ');

  return renderedTag.replace('>', ` ${propsString}>`);
};

// creates a single tag and attaches the props in the correct format
export const renderComponent = (jaseciComponent: JaseciComponent) => {
  return attachProps(
    renderTag(componentMap[jaseciComponent.component], {
      withChilren: !!jaseciComponent.slots && Object.keys(jaseciComponent.slots).length > 0,
    }),
    jaseciComponent.props,
  );
};

// generates the html structure that will be rendered
export const renderComponentTree = (jaseciNodes: Array<JaseciComponent>) => {
  let markup = '';

  if (jaseciNodes) {
    jaseciNodes.map(node => {
      markup += renderComponent(node);
      // render child nodes
      if (node.slots) {
        Object.keys(node.slots).map(slotName => {
          // replace the last children placeholder in the markup with the current node
          // inserts one node into another
          markup = markup.replace(new RegExp('{children}'), `<div slot="${slotName}">${renderComponentTree(node.slots[slotName])}</div>`);
        });
      }
    });
  }

  return markup;
};
