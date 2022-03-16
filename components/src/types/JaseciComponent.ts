type ComponentTags = 'jsc-app' | 'jsc-nav-bar' | 'jsc-nav-link' | 'jsc-container' | 'jsc-row' | 'jsc-button' | 'jsc-inputbox' | 'jsc-textbox' | 'jsc-column' | 'jsc-text';
type ComponentNames = 'App' | 'Navbar' | 'NavLink' | 'Container' | 'Row' | 'Column' | 'Button' | 'Inputbox' | 'Textbox' | 'Text';

interface JaseciComponent {
  name?: string;
  // identifies the component type to render
  component: ComponentNames;
  props: JaseciComponentProps;
  slots?: Record<string, Array<JaseciComponent>>;
  events?: Record<JaseciEventName, Array<JaseciAction>>;
}

type JaseciAction = {
  fn: JaseciActionName;
  args: Array<string | number>;
  key?: string;
  cond?: ActionCondition[];
  onCompleted?: JaseciAction;
};
type JaseciComponentProps = Record<string, unknown>;
type JaseciEventName = 'onClick' | 'onKeyPress' | 'onEnter';
type JaseciActionName = 'alert' | 'update' | 'log' | 'append';
type ActionConditionName = 'eq' | 'neq' | 'gt';
type ActionCondition = `${string}::#${ActionConditionName}::${string}`;
