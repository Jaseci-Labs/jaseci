type ComponentTags = 'jsc-app' | 'jsc-nav-bar' | 'jsc-nav-link' | 'jsc-container' | 'jsc-row' | 'jsc-button' | 'jsc-inputbox' | 'jsc-textbox' | 'jsc-column';
type ComponentNames = 'App' | 'Navbar' | 'NavLink' | 'Container' | 'Row' | 'Column' | 'Button' | 'Inputbox' | 'Textbox';

interface JaseciComponent {
  name?: string;
  // identifies the component type to render
  component: ComponentNames;
  props: JaseciComponentProps;
  slots?: Record<string, Array<JaseciComponent>>;
  events?: Record<JaseciEventName, Array<JaseciAction>>;
}

type JaseciAction = { fn: JaseciActionName; args: Array<string | number>; key?: string };
type JaseciComponentProps = Record<string, unknown>;
type JaseciEventName = 'onClick' | 'onKeyPress' | 'onEnter';
type JaseciActionName = 'alert' | 'update' | 'log';
