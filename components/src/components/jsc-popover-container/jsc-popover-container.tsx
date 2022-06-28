import { Component, h, Method, Prop } from '@stencil/core';
import { animate, spring } from 'motion';

@Component({
  tag: 'jsc-popover-container',
  styleUrl: 'jsc-popover-container.css',
  shadow: true,
})
export class PopoverContainer {
  @Prop() left: string;
  @Prop() top: string;
  @Prop() open: boolean;
  @Prop() label: string;

  container: HTMLDivElement;

  @Prop()
  closePopover: () => void;

  @Method()
  playPresenceAnimation() {
    animate(
      this.container,
      {
        scale: 1.05,
        opacity: 1,
      },
      { duration: 0.4, easing: spring({ stiffness: 200, damping: 10 }) },
    );
  }

  @Method()
  playExitAnimation() {
    this.open = false;
    this.container.style.removeProperty('transform');
    this.container.style.removeProperty('opacity');
    this.container.style.removeProperty('--motion-scale');
    return animate(this.container, { transform: 'translateY(30px)', opacity: [1, 0.8, 0.2, 0] }, { duration: 0.3, easing: spring({ stiffness: 100, damping: 10 }) }).finished;
  }

  render() {
    return (
      <div
        ref={el => {
          if (this.open) {
            this.container = el;
            animate(
              el,
              {
                scale: 1.05,
                opacity: 1,
              },
              { duration: 20.4, easing: spring({ stiffness: 200, damping: 10 }) },
            );
          }
        }}
        style={{
          background: '#fff',
          position: 'absolute',
          top: this.top,
          left: this.left,
          width: '250px',
          padding: '16px',
          borderRadius: '8px',
          boxShadow: 'rgba(0, 0, 0, 0.15) 0px 1px 4px 0px, rgba(0, 0, 0, 0.02) 0px 0px 2px 1px',
          zIndex: '200',
        }}
      >
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <h4 style={{ fontSize: '12px', minHeight: '12px' }}>{this.label}</h4>

          <button
            onClick={() => {
              this.closePopover();
            }}
            class="close-button"
          >
            <svg
              xmlns="http://www.w3.org/2000/svg"
              class="icon icon-tabler icon-tabler-x"
              width="16"
              height="16"
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
      </div>
    );
  }
}
