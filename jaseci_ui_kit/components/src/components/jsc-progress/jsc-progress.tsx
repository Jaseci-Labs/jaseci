import { Component, Element, Fragment, h, Prop } from '@stencil/core';
import clsx from 'clsx';
import { setUpEvents } from '../../utils/events';
import { getOperations } from '../../utils/utils';

@Component({
  tag: 'jsc-progress',
  styleUrl: 'jsc-progress.css',
  shadow: true,
})
export class Progress {
  @Element() host: HTMLElement;
  @Prop() css: string = JSON.stringify({});
  @Prop({ mutable: true }) events: string;
  @Prop() name: string;
  @Prop() max: number = 100;
  @Prop() size: string;
  @Prop() value: number = 0;
  @Prop() palette: string;
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
        <progress
          value={this.value}
          max={this.max}
          class={clsx(
            'progress w-56 gap-2',
            this.palette && {
              'progress-info': this.palette === 'info',
              'progress-warning': this.palette === 'warning',
              'progress-error': this.palette === 'error',
              'progress-success': this.palette === 'success',
              'badge-primary': this.palette === 'primary',
              'progress-secondary': this.palette === 'secondary',
              'progress-accent': this.palette === 'accent',
              'progress-ghost': this.palette === 'ghost',
            },
            this.size && {
              'progress-xs': this.size === 'xs',
              'progress-sm': this.size === 'sm',
              'progress-md': this.size === 'md',
              'progress-lg': this.size === 'lg',
            },
          )}
        ></progress>

        {false && (
          <div class="progress-ghost progress-lg progress-primary progress-secondary progress-accent progress-info progress-info progress-success progress-warning progress-error"></div>
        )}
      </Fragment>
    );
  }
}
