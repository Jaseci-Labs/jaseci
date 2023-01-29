import { Component, Element, Fragment, h, Prop } from '@stencil/core';
import { getProp } from '../../store/propsStore';
import { setUpEvents } from '../../utils/events';
import { getOperations } from '../../utils/utils';

@Component({
  tag: 'jsc-dropdown',
  styleUrl: 'jsc-dropdown.css',
  shadow: true,
})
export class Dropdown {
  @Element() host: HTMLElement;
  @Prop() css: string = JSON.stringify({});
  @Prop({ mutable: true }) events: string;
  @Prop() name: string;
  @Prop() label: string;
  @Prop() items: string;
  @Prop({ attribute: 'buttonprops' }) buttonProps: string;
  @Prop({ mutable: true }) operations;

  componentDidLoad() {
    // const childrenSlot = this.host.shadowRoot.querySelector('slot[name=children]') as HTMLSlotElement;

    // childrenSlot.assignedNodes().map(node => {
    Object.assign(this.host.style, {
      ...JSON.parse(this.css),
    });

    setUpEvents(this.host, this.events);
    this.operations = getOperations(this.name);
  }

  render() {
    return (
      <Fragment>
        <div class="dropdown dropdown-click">
          <jsc-button tabindex="0" label={this.label} {...getProp(this.buttonProps)}></jsc-button>
          <ul tabindex="0" class="dropdown-content menu p-2 shadow bg-base-100 rounded-box w-52">
            {getProp(this.items).map(item => (
              <li>
                <a href={item.href} target={item.target}>
                  {item.label}
                </a>
              </li>
            ))}
            {/* <slot name="contents"></slot> */}
          </ul>
        </div>
      </Fragment>
    );
  }
}
