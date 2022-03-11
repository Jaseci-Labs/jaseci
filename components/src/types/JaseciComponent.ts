type ComponentTags = 'jsc-app' | 'jsc-nav-bar' | 'jsc-nav-link' | 'jsc-container' | 'jsc-row' | 'jsc-button' | 'jsc-inputbox' | 'jsc-textbox' | 'jsc-column';
type ComponentNames = 'App' | 'Navbar' | 'NavLink' | 'Container' | 'Row' | 'Column' | 'Button' | 'Inputbox' | 'Textbox';

interface JaseciComponent {
  name?: string;
  // identifies the component type to render
  component: ComponentNames;
  props: JaseciComponentProps;
  slots?: Record<string, Array<JaseciComponent>>;
  events?: Record<JaseciEvent, { fn: JaseciAction; args: Array<string | number> }>;
}

type JaseciComponentProps = Record<string, unknown>;

type JaseciEvent = 'click';
type JaseciAction = 'alert' | 'log';
