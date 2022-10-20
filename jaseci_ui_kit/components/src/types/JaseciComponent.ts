type ComponentTags =
  | 'jsc-app'
  | 'jsc-nav-bar'
  | 'jsc-nav-link'
  | 'jsc-container'
  | 'jsc-row'
  | 'jsc-button'
  | 'jsc-inputbox'
  | 'jsc-speech-input'
  | 'jsc-textbox'
  | 'jsc-column'
  | 'jsc-text'
  | 'jsc-card'
  | 'jsc-date-picker'
  | 'jsc-divider'
  | 'jsc-anchor'
  | 'jsc-datagrid'
  | 'jsc-datarow'
  | 'jsc-datalist'
  | 'jsc-dialog'
  | 'jsc-popover'
  | 'jsc-tabs'
  | 'jsc-tab'
  | 'jsc-dropdown'
  | 'jsc-select'
  | 'jsc-tooltip'
  | 'jsc-radio'
  | 'jsc-radio-group'
  | 'jsc-checkbox'
  | 'jsc-toggle'
  | 'jsc-range'
  | 'jsc-alert'
  | 'jsc-collapse'
  | 'jsc-auth-form'
  | 'jsc-avatar'
  | 'jsc-carousel'
  | 'jsc-badge'
  | 'jsc-button-group'
  | 'jsc-progress'
  | 'jsc-rating'
  | 'jsc-drawer'
  | 'jsc-breadcrumbs'
  | 'jsc-hero'
  | 'jsc-stat'
  | 'jsc-chip';

type ComponentNames =
  | 'App'
  | 'Navbar'
  | 'Stat'
  | 'Hero'
  | 'Progress'
  | 'Badge'
  | 'ButtonGroup'
  | 'Drawer'
  | 'AuthForm'
  | 'NavLink'
  | 'Carousel'
  | 'Avatar'
  | 'Collapse'
  | 'Range'
  | 'Checkbox'
  | 'Toggle'
  | 'Container'
  | 'Row'
  | 'Radio'
  | 'RadioGroup'
  | 'Column'
  | 'Button'
  | 'Inputbox'
  | 'SpeechInput'
  | 'Textbox'
  | 'Text'
  | 'Card'
  | 'DatePicker'
  | 'Divider'
  | 'Anchor'
  | 'Datagrid'
  | 'Datarow'
  | 'Datalist'
  | 'Dialog'
  | 'Popover'
  | 'Tabs'
  | 'Tab'
  | 'Breadcrumbs'
  | 'Rating'
  | 'Select'
  | 'Dropdown'
  | 'Alert'
  | 'Tooltip'
  | 'Chip';

interface JaseciComponent {
  name?: string;
  // identifies the component type to render
  component: ComponentNames;
  props: JaseciComponentProps;
  sections?: Record<string, Array<JaseciComponent>>;
  events?: Record<JaseciEventName, Array<JaseciAction>>;
  operations?: Record<string, JaseciOperation>;
  listeners?: Record<string, Record<string, any>>;
  css?: Record<string, string>;
}

type JaseciAction = {
  fn: JaseciActionName;
  args: Array<string | number>;
  key?: string;
  theme?: string;
  // used to specify operation in runOperation
  operation?: string;
  list?: string;
  target?: 'localstorage';
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
type JaseciEventName = 'onClick' | 'onKeyPress' | 'onEnterKeyPress' | 'onMount';
type JaseciActionName =
  | 'alert'
  | 'update'
  | 'log'
  | 'append'
  | 'add'
  | 'runOperation'
  | 'callEndpoint'
  | 'runForEach'
  | 'refreshDatagrid'
  | 'storeValue'
  | 'navigate'
  | 'emit'
  | 'showToast'
  | 'speechToText'
  | 'textToSpeech'
  | 'setTheme';
type ActionConditionName = 'eq' | 'neq' | 'gt' | 'lt';
type ActionCondition = `${string}::#${ActionConditionName}::${string}`;
