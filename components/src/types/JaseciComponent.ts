type ComponentTags = 'jsc-app' | 'jsc-nav-bar' | 'button';
type ComponentNames = 'App' | 'Button' | 'Navbar';

interface JaseciComponent {
  // identifies the component type to render
  component: ComponentNames;
  props: JaseciComponentProps;
  slots?: Record<string, Array<JaseciComponent>>;
}

type JaseciComponentProps = Record<string, unknown>;
