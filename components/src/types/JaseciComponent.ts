type ComponentTags = 'jsc-app' | 'jsc-nav-bar' | 'jsc-nav-link' | 'jsc-container' | 'jsc-row';
type ComponentNames = 'App' | 'Navbar' | 'NavLink' | 'Container' | 'Row';

interface JaseciComponent {
  // identifies the component type to render
  component: ComponentNames;
  props: JaseciComponentProps;
  slots?: Record<string, Array<JaseciComponent>>;
}

type JaseciComponentProps = Record<string, unknown>;
