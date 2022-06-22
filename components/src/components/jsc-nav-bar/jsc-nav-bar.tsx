import { Component, Element, h, Prop, Watch } from '@stencil/core';
import { configStore, getTheme } from '../../store/configStore';
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
      <div data-theme={getTheme()} class="navbar bg-neutral text-neutral-content" style={JSON.parse(this.css)}>
        <div class="flex-1">
          <a class="btn btn-ghost normal-case text-xl">{this.label}</a>
        </div>
        <div class="flex-none pr-2">
          <ul class="menu menu-horizontal p-0">
            <slot name="links"></slot>
          </ul>
        </div>
      </div>
    );
  }
}
