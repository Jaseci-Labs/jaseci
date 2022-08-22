import { Component, Element, h, Listen, Method, Prop } from '@stencil/core';
import clsx from 'clsx';
import { getComponentByName, setUpEvents } from '../../utils/events';
import { getOperations } from '../../utils/utils';

@Component({
  tag: 'jsc-popover',
  styleUrl: 'jsc-popover.css',
  shadow: false,
})
export class Popover {
  @Element() host: HTMLElement;
  @Prop() css: string = JSON.stringify({});
  @Prop({ mutable: true }) events: string;
  @Prop() name: string;
  @Prop() title: string;
  @Prop() open: string;
  @Prop() left: string;
  @Prop() top: string;
  @Prop() target: string;
  @Prop({ mutable: true }) operations;
  @Prop() listeners: string;

  popoverContainer: HTMLJscPopoverContainerElement;
  contents: HTMLDivElement;

  @Listen('keydown', { target: 'window' })
  onKeyPress(event: KeyboardEvent) {
    if (event.key === 'Escape') {
      this.open && this.closePopover();
    }
  }

  @Method()
  closePopover() {
    this.popoverContainer.playExitAnimation().then(() => {
      this.popoverContainer.classList.add('hidden');
      this.open = 'false';
    });
  }

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

  @Method()
  async openPopover() {
    this.popoverContainer.classList.remove('hidden');
    const contentsHeight = this.contents.getBoundingClientRect().height;
    if (this.popoverContainer) {
      if (this.open === 'true') return;
      this.open = 'true';
      const targetComponent = getComponentByName(this.target);
      console.log({ target: this.target, comp: targetComponent, contentsHeight });
      const targetRect = targetComponent.getBoundingClientRect();
      const offsetY = 220 + 100;

      this.top = `${targetRect.top + window.scrollY - (offsetY + contentsHeight)}px`;
      this.left = `${targetRect.left + window.scrollX}px`;
    }
  }

  @Method()
  togglePopover() {
    if (this.open === 'true') {
      this.closePopover();
    } else {
      this.openPopover();
    }
  }

  render() {
    return (
      <div>
        <jsc-popover-container
          closePopover={() => this.closePopover()}
          label={this.title}
          class={clsx(this.open === 'false' && 'hidden')}
          open={this.open === 'true'}
          top={this.top}
          left={this.left}
          ref={el => (this.popoverContainer = el)}
        >
          <div ref={el => (this.contents = el)} slot="contents">
            <slot name="contents"></slot>
          </div>
        </jsc-popover-container>
      </div>
    );
  }
}
