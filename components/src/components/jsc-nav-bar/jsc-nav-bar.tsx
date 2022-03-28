import { Component, Element, h, Prop, Watch } from '@stencil/core';
import { setUpEvents } from '../../utils/events';

@Component({
  tag: 'jsc-nav-bar',
  styleUrl: 'jsc-nav-bar.css',
  shadow: true,
})
export class NavBar {
  /**
   * The title of the app bar.
   */
  @Prop({ mutable: true }) label: string;
  @Prop() css: string = JSON.stringify({});
  @Prop() name: string;
  @Prop() events: string;
  @Element() host: HTMLElement;

  @Watch('label')
  validateLabel(newLabel: string) {
    console.log('label updated');
    if (typeof newLabel !== 'number') {
      throw new Error('Label must be a string.');
    }
  }

  componentDidLoad() {
    setUpEvents(this.host, this.events);
  }

  render() {
    return (
      <div class="jsc_nav_bar" style={JSON.parse(this.css)}>
        <p class="jsc_nav_bar__label">{this.label}</p>
        <slot name="links"></slot>
      </div>
    );
  }
}
