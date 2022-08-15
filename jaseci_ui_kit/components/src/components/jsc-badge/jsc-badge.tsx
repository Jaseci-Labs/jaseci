import { Component, Element, Fragment, h, Prop } from '@stencil/core';
import clsx from 'clsx';
import { getComponentByName, setUpEvents } from '../../utils/events';
import { getOperations } from '../../utils/utils';

@Component({
  tag: 'jsc-badge',
  styleUrl: 'jsc-badge.css',
  shadow: true,
})
export class Badge {
  @Element() host: HTMLElement;
  @Prop() css: string = JSON.stringify({});
  @Prop({ mutable: true }) events: string;
  @Prop() name: string;
  @Prop() label: string;
  @Prop() size: string;
  @Prop() palette: string;
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
        <div
          class={clsx(
            'badge gap-2',
            this.palette && {
              'badge-info': this.palette === 'info',
              'badge-warning': this.palette === 'warning',
              'badge-error': this.palette === 'error',
              'badge-success': this.palette === 'success',
              'badge-primary': this.palette === 'primary',
              'badge-secondary': this.palette === 'secondary',
              'badge-accent': this.palette === 'accent',
              'badge-ghost': this.palette === 'ghost',
            },
            this.size && {
              'badge-xs': this.size === 'xs',
              'badge-sm': this.size === 'sm',
              'badge-md': this.size === 'md',
              'badge-lg': this.size === 'lg',
            },
          )}
        >
          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" class="inline-block w-4 h-4 stroke-current cursor-pointer">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
          </svg>
          {this.label}
        </div>

        {false && (
          <div class="badge-info badge-primary badge-secondary badge-accent badge-ghost badge-info badge-success badge-warning badge-error badge-lg badge-md badge-sm badge-xs"></div>
        )}
      </Fragment>
    );
  }
}
