import { Component, Element, h, Prop } from '@stencil/core';
import { setUpEvents } from '../../utils/events';
import { getOperations } from '../../utils/utils';

@Component({
  tag: 'jsc-auth-form',
  styleUrl: 'jsc-auth-form.css',
  shadow: true,
})
export class JscAuthForm {
  @Element() host: HTMLElement;
  @Prop() css: string = JSON.stringify({});
  @Prop({ mutable: true }) events: string;
  @Prop() name: string;
  @Prop({ attribute: 'hidenamefield' }) hideNameField: string = 'false';
  @Prop({ mutable: true }) operations;
  @Prop() mode: 'signup' | 'login' = 'login';
  @Prop({ attribute: 'serverurl' }) serverURL: string;
  @Prop() redirectURL: string;
  @Prop() requireActivation: 'true' | 'false' = 'false';
  @Prop({ attribute: 'tokenkey' }) tokenKey: string = 'token';

  fullName: string;
  email: string;
  password: string;

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

  signUp() {
    fetch(`${this.serverURL}/user/create/`, {
      method: 'POST',
      body: JSON.stringify({
        name: this.fullName,
        email: this.email,
        password: this.password,
        is_activated: this.requireActivation === 'false',
      }),
      headers: { 'Content-Type': 'application/json' },
    }).then(async res => {
      const data = await res.json();

      if (data?.token) {
        localStorage.setItem(this.tokenKey, data.token);
      }

      if (this.redirectURL) {
        window.location.href = this.redirectURL;
      }
    });
  }

  logIn() {
    fetch(`${this.serverURL}/user/token/`, {
      method: 'POST',
      body: JSON.stringify({ email: this.email, password: this.password }),
      headers: { 'Content-Type': 'application/json' },
    }).then(async res => {
      const data = await res.json();

      if (data?.token) {
        localStorage.setItem(this.tokenKey, data.token);
      }

      if (this.redirectURL) {
        window.location.href = this.redirectURL;
      }
    });
  }

  render() {
    return (
      <div style={{ display: 'flex', flexDirection: 'column', gap: '20px' }}>
        {this.mode === 'signup' && this.hideNameField !== 'true' && (
          <jsc-inputbox onValueChanged={e => (this.fullName = e.detail)} label={'Full Name'} placeholder={'Enter your full name'}></jsc-inputbox>
        )}
        <jsc-inputbox onValueChanged={e => (this.email = e.detail)} label={'Email'} placeholder={'Enter your email'}></jsc-inputbox>
        <jsc-inputbox onValueChanged={e => (this.password = e.detail)} label={'Password'} type="password" placeholder={'Enter your password'}></jsc-inputbox>
        <div>
          <jsc-button label={this.mode === 'signup' ? 'Sign Up' : 'Login'} onClick={() => (this.mode === 'signup' ? this.signUp() : this.logIn())}></jsc-button>
        </div>
      </div>
    );
  }
}
