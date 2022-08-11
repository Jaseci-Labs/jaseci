import { Component, Element, Fragment, h, Prop } from '@stencil/core';
import clsx from 'clsx';
import { getProp } from '../../store/propsStore';
import { setUpEvents } from '../../utils/events';
import { getOperations, renderComponentTree } from '../../utils/utils';

@Component({
  tag: 'jsc-button-group',
  styleUrl: 'jsc-button-group.css',
  shadow: true,
})
export class ButtonGroup {
  @Element() host: HTMLElement;
  @Prop() css: string = JSON.stringify({});
  @Prop({ mutable: true }) events: string;
  @Prop() name: string;
  @Prop() buttons: string;
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
      <div class="btn-group">
        {getProp(this.buttons).map(button => (
          <Fragment>
            {!button.href && <button class={clsx('btn', button.active === 'true' && 'btn-active')}>{button.label}</button>}
            {button.href && (
              <a href={button.href} class={clsx('btn', button.active === 'true' && 'btn-active')}>
                {button.label}
              </a>
            )}
          </Fragment>
        ))}
        {false && <div class="btn-active"></div>}
      </div>
    );
  }
}
