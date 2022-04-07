import { Component, Element, h, Prop } from '@stencil/core';
import { setUpEvents } from '../../utils/events';

@Component({
  tag: 'jsc-text',
  styleUrl: 'jsc-text.css',
  shadow: true,
})
export class MyComponent {
  @Prop() variant: 'simple' | 'title' = 'simple';
  @Prop() value: string;
  @Prop() state: string = JSON.stringify({ counterValue: 2 });
  @Prop() operations: string;
  @Prop() css: string = JSON.stringify({});
  @Prop() events: string;

  @Element() host: HTMLElement;

  // try this to add arbitrary state to components
  // setUpState() {
  // this.host['counterValue'] = 200;
  // }

  componentDidLoad() {
    setUpEvents(this.host, this.events);
    // this.setUpState();
  }

  render() {
    return <p style={JSON.parse(this.css)}>{this.value}</p>;
  }
}
