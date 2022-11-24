import { Component, Element, Event, EventEmitter, h, Prop, Watch } from '@stencil/core';
import clsx from 'clsx';
import { setUpEvents } from '../../utils/events';
import { speechToText } from '../../utils/events/speech';
import { getOperations } from '../../utils/utils';

@Component({
  tag: 'jsc-speech-input',
  styleUrl: 'jsc-speech-input.css',
  shadow: true,
})
export class SpeechInput {
  @Prop({ reflect: true }) value: string;
  @Prop() css: string = JSON.stringify({});
  @Prop() name: string;
  @Prop() label: string;
  @Prop() altLabel: string;
  @Prop() type: string = 'text';
  @Prop() events: string;
  @Prop() fullwidth: string;
  @Prop() placeholder: string;
  @Prop() operations: string;
  @Prop() palette: 'primary' | 'secondary' | 'accent' | 'ghost' | 'link' | 'info' | 'success' | 'warning' | 'error';
  @Element() host: HTMLElement;

  @Prop() active: boolean;

  private sTT: {
    start: () => void;
    stop: () => void;
  } = speechToText({
    onResult: (text: string) => {
      this.value = text;
    },
    onStart: () => {
      this.active = true;
    },
    onEnd: () => {
      this.active = false;
    },
  });

  @Event() valueChanged: EventEmitter<string>;
  private onInputChangeValue(event: Event) {
    this.value = (event.target as HTMLInputElement).value;
    this.valueChanged.emit(this.value);
  }

  componentDidLoad() {
    setUpEvents(this.host, this.events);
    this.operations = getOperations(this.name);
    this.setFullWidth();
  }

  componentDidRender() {}

  setFullWidth() {
    Object.assign(this.host.style, {
      width: this.fullwidth === 'true' ? '100%' : 'auto',
    });
  }

  @Watch('fullwidth')
  fullwidthChange() {
    this.setFullWidth();
  }

  stopRecognition() {
    this.sTT.stop();
  }

  render() {
    return (
      <div class={clsx('form-control w-full', this.fullwidth !== 'true' && 'max-w-xs')}>
        {this.label && (
          <label class="label">
            <span class="label-text">{this.label}</span>
            {this.altLabel && <span class="label-text-alt">{this.altLabel}</span>}
          </label>
        )}
        <div class="input-group">
          <input
            name={this.name}
            style={{
              ...JSON.parse(this.css),
            }}
            value={this.value}
            type={this.type}
            // use onInput since it's evaluates immediately
            onInput={this.onInputChangeValue.bind(this)}
            class={clsx(
              `input input-bordered w-full`,
              this.fullwidth !== 'true' && 'max-w-xs',
              this.palette && {
                'input-primary': this.palette === 'primary',
                'input-secondary': this.palette === 'secondary',
                'input-accent': this.palette === 'accent',
                'input-success': this.palette === 'success',
                'input-info': this.palette === 'info',
                'input-warning': this.palette === 'warning',
                'input-error': this.palette === 'error',
              },
            )}
            placeholder={this.placeholder}
          ></input>
          <button class={clsx('btn btn-square', this.active && 'btn-error')} onClick={() => (this.active ? this.stopRecognition() : this.sTT.start())}>
            <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
              <path stroke-linecap="round" stroke-linejoin="round" d="M19 11a7 7 0 01-7 7m0 0a7 7 0 01-7-7m7 7v4m0 0H8m4 0h4m-4-8a3 3 0 01-3-3V5a3 3 0 116 0v6a3 3 0 01-3 3z" />
            </svg>
          </button>
        </div>
        {/* register some classes so they aren't purged by daisy-ui */}
        {false && <input class="input-primary input-secondary input-accent input-info input-error input-warning input-success input-sm input-lg input-xs input-xl"></input>}
      </div>
    );
  }
}
