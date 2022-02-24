export function format(first: string, middle: string, last: string): string {
  return (first || '') + (middle ? ` ${middle}` : '') + (last ? ` ${last}` : '');
}

export const componentMap: Record<Exclude<ComponentNames, 'App'>, ComponentTags> = {
  Navbar: 'jsc-nav-bar',
  Button: 'button',
};

const renderTag = (componentTag: ComponentTags) => `<${componentTag}></${componentTag}>`;

// converts props to a string of html attributes to append to the tag
const attachProps = (renderedTag: string, props: Record<string, unknown>) => {
  const propsString = Object.keys(props)
    .map(key => `${key}="${props[key]}"`)
    .join(' ');

  return renderedTag.replace('>', ` ${propsString}>`);
};

export const renderComponent = (componentName: ComponentNames, props: Record<string, unknown>) => {
  return attachProps(renderTag(componentMap[componentName]), props);
};

export const renderComponentTree = (jaseciNodes: Array<JaseciComponent>) => {
  let markup = '<div>';

  jaseciNodes.map(node => {
    markup += renderComponent(node.component, node.props);
  });

  markup += '</div>';
  return markup;
};
