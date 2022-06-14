import { Component, Element, h, Listen, Method, Prop, Watch } from '@stencil/core';
import clsx from 'clsx';
import { setUpEvents } from '../../utils/events';
import { getOperations } from '../../utils/utils';

@Component({
  tag: 'jsc-dialog',
  styleUrl: 'jsc-dialog.css',
  shadow: true,
})
export class Container {
  @Element() host: HTMLElement;
  @Prop() css: string = JSON.stringify({});
  @Prop({ mutable: true }) events: string;
  @Prop() name: string;
  @Prop() title: string;
  @Prop() open: string;
  @Prop({ mutable: true }) operations;
  @Prop() listeners: string;

  dialogContainer: any;

  @Watch('open')
  watchOpen(open: string) {
    if (open === 'false') this.closeDialog();
  }

  @Listen('keydown', { target: 'window' })
  onKeyPress(event: KeyboardEvent) {
    if (event.key === 'Escape') {
      this.open && this.closeDialog();
    }
  }

  @Method()
  async closeDialog() {
    if (this.open === 'true') {
      this.dialogContainer.playExitAnimation().then(() => (this.open = 'false'));
    }
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

  render() {
    return (
      <div>
        {this.open === 'true' && (
          <jsc-dialog-container label={this.title} closeDialog={() => this.closeDialog()} ref={el => (this.dialogContainer = el)}>
            <div slot="contents">
              <slot name="contents"></slot>
            </div>
          </jsc-dialog-container>
        )}
        <div class={clsx('modal-overlay', this.open === 'false' && 'hidden')} onClick={() => this.closeDialog()} data-hidden={!open} />
      </div>
    );
  }
}
