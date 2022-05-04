import { Component, Element, h, Prop, Watch } from '@stencil/core';
import { setUpEvents } from '../../utils/events';
import { getOperations } from '../../utils/utils';

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
  @Prop() operations: string;
  @Element() host: HTMLElement;

  @Watch('label')
  validateLabel(newLabel: string) {
    if (typeof newLabel !== 'number') {
      throw new Error('Label must be a string.');
    }
  }

  componentDidLoad() {
    setUpEvents(this.host, this.events);
    this.operations = getOperations(this.name);
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
