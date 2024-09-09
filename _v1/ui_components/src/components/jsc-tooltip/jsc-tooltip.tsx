import { Component, Element, Fragment, h, Prop } from '@stencil/core';
import { getComponentByName, setUpEvents } from '../../utils/events';
import { getOperations } from '../../utils/utils';

@Component({
  tag: 'jsc-tooltip',
  styleUrl: 'jsc-tooltip.css',
  shadow: true,
})
export class Tooltip {
  @Element() host: HTMLElement;
  @Prop() css: string = JSON.stringify({});
  @Prop({ mutable: true }) events: string;
  @Prop() name: string;
  @Prop() label: string;
  @Prop() target: string;
  tooltip: HTMLElement;
  @Prop({ mutable: true }) operations;

  componentDidLoad() {
    const targetComponent = getComponentByName(this.target);
    const targetClone = targetComponent.cloneNode(true);
    const div = document.createElement('div');
    div.click = () => alert('Hmm');
    div.appendChild(targetClone);

    this.tooltip.appendChild(div);
    targetComponent.replaceWith(this.tooltip);

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
        <div ref={el => (this.tooltip = el)} class="tooltip tooltip-right" data-tip={this.label}></div>
      </Fragment>
    );
  }
}
