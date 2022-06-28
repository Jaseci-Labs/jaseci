import { Component, Element, h, Prop } from '@stencil/core';
import { setUpEvents } from '../../utils/events';
import { getOperations } from '../../utils/utils';
import clsx from 'clsx';
import { getTheme } from '../../store/configStore';

@Component({
  tag: 'jsc-card',
  styleUrl: 'jsc-card.css',
  shadow: true,
})
export class Card {
  @Element() host: HTMLElement;
  @Prop() css: string = JSON.stringify({});
  @Prop({ mutable: true }) events: string;
  @Prop() name: string;
  @Prop() title: string;
  @Prop() shadow: 'sm' | 'md' | 'lg' | 'xl' = 'md';
  @Prop() radius: 'sm' | 'md' | 'lg' | 'full' = 'lg';
  @Prop() variant: 'shadow' | 'outline' = 'outline';
  @Prop({ mutable: true }) operations;

  componentDidLoad() {
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
      <div
        data-theme={getTheme()}
        class={clsx(
          ['card bg-base-200'],
          [
            this.variant === 'shadow' && {
              'shadow-sm': this.shadow === 'sm',
              'shadow-md': this.shadow === 'md',
              'shadow-lg': this.shadow === 'lg',
              'shadow-xl': this.shadow === 'xl',
            },
            this.variant === 'outline' && 'card-bordered',
          ],
          // [
          //   this.radius === 'sm' && 'card-radius_sm',
          //   this.radius === 'md' && 'card-radius_md',
          //   this.radius === 'lg' && 'card-radius_lg',
          //   this.radius === 'full' && 'card-radius_full',
          // ],
        )}
      >
        <div class="card-body">
          <h2 class="card-title">{this.title}</h2>
          <slot name="children"></slot>
        </div>
      </div>
    );
  }
}
