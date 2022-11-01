import { Component, Event, Element, EventEmitter, h, Method, Prop } from '@stencil/core';
import { renderComponentTree } from '../../utils/utils';
import { configStore, getTheme } from '../../store/configStore';

@Component({
  tag: 'jsc-app',
  styleUrl: 'jsc-app.css',
  shadow: true,
})
export class App {
  @Element() el: HTMLElement;
  @Prop({ mutable: true }) markup: JaseciComponent[];

  isJsonString(str) {
    try {
      JSON.parse(str);
    } catch (e) {
      return false;
    }
    return true;
  }

  @Event() onRender: EventEmitter<string>;

  private onMount() {
    this.onRender.emit('mounted');
  }

  componentWillRender() {
    console.log(this.getGlobalCss());
    // give style the global css
    Object.assign(this.el.style, this.getGlobalCss());
    console.log(this.el.style.cssText);
  }

  componentDidLoad() {
    this.onMount();
  }

  @Method()
  async setMarkup(value) {
    let markup = this.parseValueRef('searchparam', this.parseValueRef('localstorage', this.parseValueRef('config', value)));

    if (!this.isJsonString(value)) {
      alert('NOT JSON');
    }

    this.markup = JSON.parse(markup);
  }

  @Method()
  async setGlobalConfig(config: Record<string, any> & { css: Record<string, string> }) {
    configStore.state.config = { ...configStore.state.config, ...config };
  }

  getGlobalConfig() {
    return configStore.state.config;
  }

  // get global css from a global variable
  getGlobalCss() {
    return this.getGlobalConfig().css;
  }

  parseValueRef(prefix: string, markupString: string) {
    let updatedMarkupString = markupString;
    let matcher = new RegExp(`[{][{]${prefix}[:](.*?)[}][}]`, 'g');
    const configs = markupString.match(matcher);

    console.log({ matcher, configs });

    if (!configs?.length) return updatedMarkupString;

    const configsValueMap = {};

    configs.forEach(configRef => {
      const configName = configRef.split(':')[1].split('}}')[0];

      if (prefix === 'config') {
        configsValueMap[configRef] = this.getGlobalConfig()[configName];
      }

      if (prefix === 'localstorage') {
        configsValueMap[configRef] = localStorage.getItem(configName);
      }

      if (prefix === 'searchparam') {
        configsValueMap[configRef] = new URL(window.location.toString()).searchParams.get(configName);
      }
    });

    Object.keys(configsValueMap).forEach(config => {
      updatedMarkupString = updatedMarkupString.replaceAll(config, configsValueMap[config]);
    });

    console.log({ configsValueMap, configs: this.getGlobalConfig() });

    return updatedMarkupString;
  }

  render() {
    return (
      <div data-theme={getTheme()}>
        <jsc-graph></jsc-graph>
        <div innerHTML={renderComponentTree(this.markup)} class="bg-base-100"></div>
        <jsc-toast></jsc-toast>
      </div>
    );
  }
}
