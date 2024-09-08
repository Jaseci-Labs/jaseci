import { Component, Element, Fragment, h, Prop } from '@stencil/core';
import clsx from 'clsx';
import { setUpEvents } from '../../utils/events';
import { getOperations } from '../../utils/utils';

@Component({
  tag: 'jsc-avatar',
  styleUrl: 'jsc-avatar.css',
  shadow: true,
})
export class Avatar {
  @Element() host: HTMLElement;
  @Prop() css: string = JSON.stringify({});
  @Prop({ mutable: true }) events: string;
  @Prop() name: string;
  @Prop() variant: string;
  @Prop() src: string;
  @Prop() size: string;
  @Prop() placeholder: string;
  tooltip: HTMLElement;
  @Prop({ mutable: true }) operations;

  componentDidLoad() {
    // childrenSlot.assignedNodes().map(node => {
    Object.assign(this.host.style, {
      'box-sizing': 'border-box',
      'overflowX': 'auto',
      ...JSON.parse(this.css),
    });

    setUpEvents(this.host, this.events);
    this.operations = getOperations(this.name);
  }

  render() {
    return (
      <Fragment>
        <div class={clsx('avatar', this.placeholder && 'placeholder')}>
          <div
            class={clsx(
              'w-24 bg-neutral text-neutral-content relative',
              this.size && {
                'w-8': this.size === 'xs',
                'w-12': this.size === 'sm',
                'w-16': this.size === 'md',
                'w-24': this.size === 'lg',
              },
              this.variant && {
                'rounded-md': this.variant === 'rounded',
                'rounded-full': this.variant === 'circle',
              },
            )}
          >
            <img src={this.src} style={{ position: 'absolute', zIndex: '4' }} />
            <span style={{ position: 'absolute', zIndex: '2' }}>{this.placeholder}</span>
          </div>
        </div>
        {false && <div class="rounded rounded-full"></div>}
      </Fragment>
    );
  }
}
