import { Component, Element, h, Prop } from '@stencil/core';
import { setUpEvents } from '../../utils/events';
import { getOperations } from '../../utils/utils';

@Component({
  tag: 'jsc-dropdown-item',
  styleUrl: 'jsc-dropdown-item.css',
  shadow: false,
})
export class NavLink {
  @Prop() name: string;
  @Prop() label: string;
  @Prop() href: string;
  @Prop() target: string;
  @Prop() css: string = JSON.stringify({});
  @Prop() events: string;
  @Prop() operations: string;
  @Element() host: HTMLElement;

  componentDidLoad() {
    setUpEvents(this.host, this.events);
    this.operations = getOperations(this.name);
  }

  render() {
    return (
      <li>
        <a href={this.href} target={this.target} style={JSON.parse(this.css)}>
          {this.label}
        </a>
      </li>
    );
  }
}
