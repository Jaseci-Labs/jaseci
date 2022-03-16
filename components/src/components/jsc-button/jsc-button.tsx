import { Component, Element, h, Prop } from '@stencil/core';
import { setUpEvents } from '../../utils/events';

@Component({
  tag: 'jsc-button',
  styleUrl: 'jsc-button.css',
  shadow: true,
})
export class Button {
  @Element() host: HTMLElement;
  @Prop() label: string;
  @Prop() events: string;
  @Prop() name: string;

  componentDidLoad() {
    setUpEvents(this.host, this.events);
  }

  render() {
    return (
      <button name={this.name} class={`button`}>
        {this.label}
      </button>
    );
  }
}
