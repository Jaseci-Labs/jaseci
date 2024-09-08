import { Component, Element, h, Listen, Method, Prop, Watch } from '@stencil/core';
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
    this.open = 'false';
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
      <div onClick={() => this.closeDialog()}>
        <input type="checkbox" id="my-modal-4" checked={this.open === 'true'} class="modal-toggle" />
        <label htmlFor="my-modal-4" class="modal" onClick={e => e.stopPropagation()}>
          <label class="modal-box relative" htmlFor="">
            <label htmlFor="my-modal-3" class="btn btn-sm btn-circle absolute right-2 top-2" onClick={() => this.closeDialog()}>
              ✕
            </label>
            <h3 class="text-lg font-bold mb-2">{this.title}</h3>
            <slot name="contents"></slot>
            {/* <p class="py-4">You've been selected for a chance to get one year of subscription to use Wikipedia for free!</p> */}
          </label>
        </label>

        {/* {this.open === 'true' && (
          <jsc-dialog-container label={this.title} closeDialog={() => this.closeDialog()} ref={el => (this.dialogContainer = el)}>
            <div slot="contents">
            </div>
          </jsc-dialog-container>
        )}
        <div class={clsx('modal-overlay', this.open === 'false' && 'hidden')} onClick={() => this.closeDialog()} data-hidden={!open} /> */}
      </div>
    );
  }
}
