type ComponentTags = 'jsc-app' | 'jsc-nav-bar' | 'jsc-nav-link' | 'jsc-container' | 'jsc-row' | 'jsc-button' | 'jsc-inputbox' | 'jsc-textbox' | 'jsc-column' | 'jsc-text';
type ComponentNames = 'App' | 'Navbar' | 'NavLink' | 'Container' | 'Row' | 'Column' | 'Button' | 'Inputbox' | 'Textbox' | 'Text';

interface JaseciComponent {
  name?: string;
  // identifies the component type to render
  component: ComponentNames;
  props: JaseciComponentProps;
  sections?: Record<string, Array<JaseciComponent>>;
  events?: Record<JaseciEventName, Array<JaseciAction>>;
  operations?: Record<string, JaseciOperation>;
  css?: Record<string, string>;
}

type JaseciAction = {
  fn: JaseciActionName;
  args: Array<string | number>;
  key?: string;
  // used to specify operation in runOperation
  operation?: string;
  cond?: ActionCondition[];
  onCompleted?: JaseciAction;
} & JaseciCallEndpointAction;

type JaseciCallEndpointAction = {
  endpoint?: string;
};

type JaseciOperation = {
  args: Array<string>;
  run: Array<Record<JaseciEventName, Array<JaseciAction>>>;
};

type JaseciComponentProps = Record<string, unknown>;
type JaseciEventName = 'onClick' | 'onKeyPress' | 'onEnterKeyPress';
type JaseciActionName = 'alert' | 'update' | 'log' | 'append' | 'add' | 'runOperation' | 'callEndpoint';
type ActionConditionName = 'eq' | 'neq' | 'gt' | 'lt';
type ActionCondition = `${string}::#${ActionConditionName}::${string}`;
