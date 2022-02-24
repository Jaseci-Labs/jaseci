import { Component, Prop, h } from '@stencil/core';

@Component({
  tag: 'jsc-nav-link',
  styleUrl: 'jsc-nav-link.css',
  shadow: true,
})
export class NavLink {
  @Prop() label: string;

  render() {
    return <a class="jsc_nav_link">{this.label}</a>;
  }
}
