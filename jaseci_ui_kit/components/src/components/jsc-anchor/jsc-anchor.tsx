import { Component, Element, Fragment, h, Prop } from '@stencil/core';
import clsx from 'clsx';
import { setUpEvents } from '../../utils/events';
import { getOperations } from '../../utils/utils';

@Component({
  tag: 'jsc-anchor',
  styleUrl: 'jsc-anchor.css',
  shadow: true,
})
export class NavLink {
  @Prop() name: string;
  @Prop() label: string;
  @Prop() href: string;
  @Prop() target: string;
  @Prop() css: string = JSON.stringify({});
  @Prop() events: string;
  @Prop() hover: 'true' | 'false' = 'false';
  @Prop() palette: 'primary' | 'secondary' | 'accent' | 'neutral';
  @Prop() operations: string;
  @Element() host: HTMLElement;

  componentDidLoad() {
    setUpEvents(this.host, this.events);
    this.operations = getOperations(this.name);
  }

  render() {
    return (
      <Fragment>
        <a
          class={clsx(
            'link',
            {
              'link-primary': this.palette === 'primary',
              'link-secondary': this.palette === 'secondary',
              'link-accent': this.palette === 'accent',
              'link-neutral': this.palette === 'neutral',
            },
            this.hover === 'true' && 'link-hover',
          )}
          href={this.href}
          target={this.target}
          style={JSON.parse(this.css)}
        >
          {this.label}
        </a>
        {false && <a class="link-primary link-secondary link-accent link-hover link-neutral"></a>}
      </Fragment>
    );
  }
}
