import { Component, Element, h, Prop, Watch } from '@stencil/core';
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
  @Prop() color: string;
  @Prop() css: string = JSON.stringify({});
  @Prop() operations: string;

  componentDidLoad() {
    setUpEvents(this.host, this.events);
  }

  @Watch('color')
  setColor(newColor: string, _oldValue: string) {
    Object.assign(this.host.style, {
      '--button-color': `var(--${newColor}3)`,
      '--button-bg-color': `var(--${newColor}3)`,
    });
  }

  render() {
    return (
      <button name={this.name} style={JSON.parse(this.css as any)} class={`button`}>
        {this.label}
      </button>
    );
  }
}
