import { Component, Prop, h, Watch } from '@stencil/core';

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
  @Prop({ mutable: true }) links: string;

  @Watch('label')
  validateLabel(newLabel: string) {
    console.log('label updated');
    if (typeof newLabel !== 'number') {
      throw new Error('Label must be a string.');
    }
  }

  get navLinks(): Array<JaseciComponent> {
    return JSON.parse(this.links);
  }

  render() {
    return (
      <div class="jsc_nav_bar">
        <p class="jsc_nav_bar__label">{this.label}</p>
        <slot name="links"></slot>
      </div>
    );
  }
}
