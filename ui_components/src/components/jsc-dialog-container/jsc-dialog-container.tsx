import { Component, h, Method, Prop } from '@stencil/core';
import clsx from 'clsx';
import { animate, spring } from 'motion';

@Component({
  tag: 'jsc-dialog-container',
  styleUrl: 'jsc-dialog-container.css',
  shadow: true,
})
export class DialogContainer {
  @Prop({ mutable: true })
  label?: string;

  @Prop()
  closeDialog: () => void;

  modalContainer!: HTMLDivElement;

  componentDidRender() {
    animate(
      this.modalContainer,
      {
        scale: 1.05,
        opacity: 1,
      },
      { duration: 0.4, easing: spring({ stiffness: 200, damping: 10 }) },
    );
  }

  @Method()
  async setLabel(label: string) {
    this.label = label;
  }

  @Method()
  playExitAnimation() {
    return animate(this.modalContainer, { transform: 'translateY(30px)', opacity: [1, 0.8, 0.2, 0] }, { duration: 0.3, easing: spring({ stiffness: 100, damping: 10 }) }).finished;
  }

  render() {
    return (
      <div id="modal-container" class={clsx('modal-container')} ref={el => (this.modalContainer = el as HTMLDivElement)}>
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
          <h3 class={'modal-title'}>{this.label}</h3>
          <button
            onClick={() => {
              this.closeDialog();
            }}
            class="close-button"
          >
            <svg
              xmlns="http://www.w3.org/2000/svg"
              class="icon icon-tabler icon-tabler-x"
              width="18"
              height="18"
              viewBox="0 0 24 24"
              stroke-width="1.5"
              stroke="#0569DB"
              fill="none"
              stroke-linecap="round"
              stroke-linejoin="round"
            >
              <path stroke="none" d="M0 0h24v24H0z" fill="none" />
              <line x1="18" y1="6" x2="6" y2="18" />
              <line x1="6" y1="6" x2="18" y2="18" />
            </svg>
          </button>
        </div>
        <slot name="contents"></slot>
        <p>yo</p>
      </div>
    );
  }
}
