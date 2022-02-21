interface JaseciComponent {
  // identifies the component type to render
  component: string;
  props: JaseciComponentProps;
}

interface JaseciComponentProps {
  title?: string;
}
