import { Component, Element, h, Listen, Prop } from '@stencil/core';

@Component({
  tag: 'jsc-button',
  styleUrl: 'jsc-button.css',
  shadow: true,
})
export class Button {
  @Element() host: HTMLElement;
  @Prop() label: string;
  @Prop() events: string;
  @Prop() name: string;
  @Listen('click', { capture: true })
  handleClick() {}

  linkEvents = (events: JaseciComponent['events']) => {
    Object.keys(events).map((eventName: JaseciEvent) => {
      switch (eventName) {
        case 'click': {
          const actionName = events['click']['fn'];
          const actionArgs = events['click']['args'];
          const elem = this.host.shadowRoot.querySelector(`[name='${this.name}']`);
          elem.addEventListener('click', () => {
            new Function(`${actionName}.apply(this, ${JSON.stringify(actionArgs)})`)();
          });
          break;
        }
        default: {
        }
      }
    });
  };

  componentDidLoad() {
    if (this.events) {
      // attach events to component
      const events = JSON.parse(this.events);
      console.log({ events });
      this.linkEvents(events);
      // remove events
    }
  }

  render() {
    return (
      <button name={this.name} class={`button`}>
        {this.label}
      </button>
    );
  }
}
