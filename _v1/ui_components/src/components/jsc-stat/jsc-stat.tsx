import { Component, Element, h, Prop } from '@stencil/core';
import { getProp } from '../../store/propsStore';
import { setUpEvents } from '../../utils/events';
import { getOperations } from '../../utils/utils';

@Component({
  tag: 'jsc-stat',
  styleUrl: 'jsc-stat.css',
  shadow: true,
})
export class Stat {
  @Element() host: HTMLElement;
  @Prop() css: string = JSON.stringify({});
  @Prop({ mutable: true }) events: string;
  @Prop() name: string;
  @Prop() label: string;
  @Prop() value: string;
  @Prop() stats: string;
  @Prop() total: string;
  @Prop() description: string;
  @Prop({ mutable: true }) operations;

  componentDidLoad() {
    // const childrenSlot = this.host.shadowRoot.querySelector('slot[name=children]') as HTMLSlotElement;

    // childrenSlot.assignedNodes().map(node => {
    Object.assign(this.host.style, {
      'box-sizing': 'border-box',
      // 'overflowX': 'auto',
      ...JSON.parse(this.css),
    });

    setUpEvents(this.host, this.events);
    this.operations = getOperations(this.name);
  }

  render() {
    return (
      <div class="stats shadow">
        {getProp(this.stats).map(stat => (
          <div class="stat">
            <div class="stat-title">{stat.label}</div>
            <div class="stat-value">{stat.value}</div>
            <div class="stat-desc">{stat.description}</div>
          </div>
        ))}
      </div>
    );
  }
}
