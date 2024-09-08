import { Component, Element, h, Listen, Method, Prop, Watch } from '@stencil/core';
import { setUpEvents } from '../../utils/events';
import { getOperations } from '../../utils/utils';

@Component({
  tag: 'jsc-drawer',
  styleUrl: 'jsc-drawer.css',
  shadow: true,
})
export class Container {
  @Element() host: HTMLElement;
  @Prop() css: string = JSON.stringify({});
  @Prop({ mutable: true }) events: string;
  @Prop() name: string;
  @Prop() title: string;
  @Prop() open: string = 'true';
  @Prop({ mutable: true }) operations;
  @Prop() listeners: string;

  @Watch('open')
  watchDrawer(open: string) {
    if (open === 'false') this.closeDrawer();
  }

  @Listen('keydown', { target: 'window' })
  onKeyPress(event: KeyboardEvent) {
    if (event.key === 'Escape') {
      this.open && this.closeDrawer();
    }
  }

  @Method()
  async closeDrawer() {
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
      // <div class="drawer drawer-end">
      //   <div onClick={() => this.closeDrawer()}>
      //     <input type="checkbox" id="my-drawer-4" checked={this.open === 'true'} class="drawer-toggle" />
      //     <div class="drawer-side">
      //       <label htmlFor="my-drawer-4" class="drawer-overlay" onClick={e => e.stopPropagation()}></label>
      //       <h3 class="text-lg font-bold mb-2">{this.title}</h3>
      //       <slot name="contents"></slot>
      //     </div>
      //   </div>
      // </div>
      <div class="drawer drawer-end">
        <input id="my-drawer-4" type="checkbox" value={'true'} class="drawer-toggle" />
        <div class="drawer-content">
          <label htmlFor="my-drawer-4" class="drawer-button btn btn-primary">
            Open drawer
          </label>
        </div>
        <div class="drawer-side">
          <label htmlFor="my-drawer-4" class="drawer-overlay"></label>
          <ul class="menu p-4 overflow-y-auto w-80 bg-base-100 text-base-content">
            <li>
              <a>Sidebar Item 1</a>
            </li>
            <li>
              <a>Sidebar Item 2</a>
            </li>
          </ul>
        </div>
      </div>
    );
  }
}
