import { Component, Element, h, Method, Prop } from '@stencil/core';
import { renderComponentTree } from '../../utils/utils';
import serialize from 'serialize-javascript';

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

  componentDidRender() {
    console.log(this.getGlobalCss());
    // give style the global css
    Object.assign(this.el.style, this.getGlobalCss());
    console.log(this.el.style.cssText);
  }

  componentDidLoad() {
    this.setGlobalConfig({});
  }

  @Method()
  async setMarkup(value) {
    // clear local storage to reset operations for each comp
    localStorage.clear();

    let markup = this.parseConfig(value);

    if (!this.isJsonString(value)) {
      alert('NOT JSON');
    }

    this.markup = JSON.parse(markup);
  }

  @Method()
  async setGlobalConfig(config: Record<string, any>) {
    (window as any).global = window;
    global.__JSC_WEBKIT_CONFIG__ = config;
    global.__JSC_WEBKIT_OPERATIONS__ = {};
  }

  getGlobalConfig() {
    return global.__JSC_WEBKIT_CONFIG__;
  }

  // get global css from a global variable
  getGlobalCss() {
    return this.getGlobalConfig().css;
  }

  parseConfig(markupString: string) {
    let updatedMarkupString = markupString;

    const configs = markupString.match(/config[(](.*?)[)]/g);
    if (!configs?.length) return updatedMarkupString;

    const configsValueMap = {};

    configs.forEach(configRef => {
      const configName = configRef.split('config(')?.[1]?.split(')')[0];
      configsValueMap[configRef] = this.getGlobalConfig()[configName];
    });

    Object.keys(configsValueMap).forEach(config => {
      updatedMarkupString = updatedMarkupString.replaceAll(config, configsValueMap[config]);
    });

    console.log({ configsValueMap });

    return updatedMarkupString;
  }

  render() {
    return (
      <div>
        <div innerHTML={renderComponentTree(this.markup)}></div>
      </div>
    );
  }
}
