import { Component, Element, h, Prop } from '@stencil/core';
import clsx from 'clsx';
import { getProp } from '../../store/propsStore';
import { setUpEvents } from '../../utils/events';
import { getOperations } from '../../utils/utils';

@Component({
  tag: 'jsc-hero',
  styleUrl: 'jsc-hero.css',
  shadow: true,
})
export class Hero {
  @Element() host: HTMLElement;
  @Prop() css: string = JSON.stringify({});
  @Prop({ mutable: true }) events: string;
  @Prop() name: string;
  @Prop() action: string;
  @Prop() description: string;
  @Prop({ attribute: 'backgroundimage' }) backgroundImage: string;
  @Prop({ reflect: false }) label: string;
  @Prop({ mutable: true }) operations;

  componentDidLoad() {
    // const childrenSlot = this.host.shadowRoot.querySelector('slot[name=children]') as HTMLSlotElement;

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
      <div
        class="hero min-h-screen bg-base-200"
        style={{
          backgroundImage: this.backgroundImage ? `url(${this.backgroundImage})` : undefined,
        }}
      >
        {this.backgroundImage && <div class={clsx('hero-overlay', this.backgroundImage && 'bg-opacity-60')}></div>}
        <div class={clsx('hero-content text-center', this.backgroundImage && 'text-neutral-content')}>
          <div class="max-w-md">
            <h1 class="text-5xl font-bold">{this.label}</h1>
            <p class="py-6">{this.description}</p>
            <button class="btn btn-primary text-primary-content">{(getProp(this.action) as { label: string }).label}</button>
          </div>
        </div>
      </div>
    );
  }
}
