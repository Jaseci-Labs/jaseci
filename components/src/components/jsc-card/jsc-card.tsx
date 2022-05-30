import { Component, Element, h, Prop } from '@stencil/core';
import { setUpEvents } from '../../utils/events';
import { getOperations } from '../../utils/utils';
import clsx from 'clsx';

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
  @Prop() shadow: 'sm' | 'md' | 'lg' = 'md';
  @Prop() radius: 'sm' | 'md' | 'lg' | 'full' = 'lg';
  @Prop() variant: 'shadow' | 'outline';
  @Prop() outlineColor: 'red';
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
        style={{ borderColor: '#DBDBDB' }}
        class={clsx(
          ['card'],
          [
            this.variant === 'shadow' && {
              'card-shadow_sm': this.shadow === 'sm',
              'card-shadow_md': this.shadow === 'md',
              'card-shadow_lg': this.shadow === 'lg',
            },
            this.variant === 'outline' && 'card-outline',
          ],
          [
            this.radius === 'sm' && 'card-radius_sm',
            this.radius === 'md' && 'card-radius_md',
            this.radius === 'lg' && 'card-radius_lg',
            this.radius === 'full' && 'card-radius_full',
          ],
        )}
      >
        <slot name="children"></slot>
      </div>
    );
  }
}
