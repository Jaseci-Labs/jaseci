import { Component, Element, h, Prop } from '@stencil/core';
import { setUpEvents } from '../../utils/events';
import { getOperations } from '../../utils/utils';

@Component({
  tag: 'jsc-text',
  styleUrl: 'jsc-text.css',
  shadow: true,
})
export class Text {
  @Prop() variant: 'p' | 'h1' | 'h2' | 'h3' | 'h4' | 'h5' | 'h6' = 'p';
  @Prop() value: string;
  @Prop() state: string = JSON.stringify({ counterValue: 2 });
  @Prop() operations: string;
  @Prop() css: string = JSON.stringify({});
  @Prop() events: string;
  @Prop() name: string;

  @Element() host: HTMLElement;

  // try this to add arbitrary state to components
  // setUpState() {
  // this.host['counterValue'] = 200;
  // }

  componentDidLoad() {
    setUpEvents(this.host, this.events);
    this.operations = getOperations(this.name);
    // this.setUpState();
  }

  render() {
    switch (this.variant) {
      case 'p':
        return <span style={JSON.parse(this.css)}>{this.value}</span>;
      case 'h1':
        return <h1 style={JSON.parse(this.css)}>{this.value}</h1>;
      case 'h2':
        return <h2 style={JSON.parse(this.css)}>{this.value}</h2>;
      case 'h3':
        return <h3 style={JSON.parse(this.css)}>{this.value}</h3>;
      case 'h4':
        return <h4 style={JSON.parse(this.css)}>{this.value}</h4>;
      case 'h5':
        return <h5 style={JSON.parse(this.css)}>{this.value}</h5>;
      case 'h6':
        return <h6 style={JSON.parse(this.css)}>{this.value}</h6>;
      default:
        return <span style={JSON.parse(this.css)}>{this.value}</span>;
    }
  }
}
