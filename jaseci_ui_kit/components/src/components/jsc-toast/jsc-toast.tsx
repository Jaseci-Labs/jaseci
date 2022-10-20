import { Component, Element, h, Prop } from '@stencil/core';
import clsx from 'clsx';
import { toastStore } from '../../store/toastStore';
import { setUpEvents } from '../../utils/events';
import { getOperations } from '../../utils/utils';

@Component({
  tag: 'jsc-toast',
  styleUrl: 'jsc-toast.css',
  shadow: true,
})
export class Container {
  @Element() host: HTMLElement;
  @Prop() css: string = JSON.stringify({});
  @Prop({ mutable: true }) events: string;
  @Prop() name: string;
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
        class={clsx(
          'toast shadow-md  text-sm bg-white rounded-md text-justify scale-100 transition-all duration-500 ease-in-out',
          toastStore.get('hidden') && 'scale-0 transition-all',
        )}
      >
        <div class="flex justify-between items-center">
          <div class="w-[200px]">{toastStore.get('config').message}</div>
          <div>
            <button class="ml-4 btn btn-circle btn-xs" onClick={() => toastStore.set('hidden', true)}>
              <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>
        </div>
      </div>
    );
  }
}
