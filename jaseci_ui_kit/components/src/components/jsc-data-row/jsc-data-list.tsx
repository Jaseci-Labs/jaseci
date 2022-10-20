import { Component, Element, h, Prop } from '@stencil/core';
import { getProp } from '../../store/propsStore';
import { formatRowContent, getRowValue } from '../../utils/datagrid';
import { setUpEvents } from '../../utils/events';
import { getOperations, renderComponentTree } from '../../utils/utils';

@Component({
  tag: 'jsc-datalist',
  styleUrl: 'jsc-data-list.css',
  shadow: false,
})
export class Datalist {
  @Element() host: HTMLElement;
  @Prop() name: string;
  @Prop() data: [];
  @Prop() css: string = JSON.stringify({});
  @Prop() events: string;
  @Prop() operations: string;
  @Prop() server: string;
  @Prop() walker: string;
  @Prop() layout: 'Column' | 'Row' | 'None' = 'None';
  @Prop() snt: string;
  @Prop() token: string;
  @Prop() template: string;
  @Prop() getters: string;
  @Prop() body: string;
  @Prop({ attribute: 'layoutprops' }) layoutProps: string;

  fetchData() {
    fetch(`${this.server}/js/walker_run`, {
      method: 'POST',
      body: JSON.stringify({
        name: this.walker,
        snt: this.snt,
        ...getProp(this.body, {}),
      }),
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `token ${this.token}`,
      },
    })
      .then(res => res.json())
      .then(res => {
        this.data = res.report[0];
      });
  }

  renderRows(rows: [], getters: { accessor: string; format: string; formatter: 'date' | 'native'; name: string }[], render: []) {
    console.log({ rows, getters, render });
    let data: [] | Record<string, any> = rows;
    if (typeof data === 'undefined' || data === null || (Array.isArray(data) && data.length === 0)) return '<p>No data</p>';
    if (!getters) return '<p>The getters prop is not set</p>';

    if (!Array.isArray(data)) {
      data = [data];
    }

    return data
      .map(row => {
        let markup = `${renderComponentTree(render)}`;

        getters.forEach(getter => {
          const value = getRowValue(getter.accessor, row);
          markup = markup.replaceAll(`{{${getter.name}}}`, formatRowContent({ value, format: getter.format, formatter: getter.formatter }));
        });

        return markup;
      })
      .join('');
  }

  componentDidLoad() {
    setUpEvents(this.host, this.events);
    this.operations = getOperations(this.name);
    this.fetchData();
  }

  getChildren(withChildren: boolean = true) {
    let layoutProps = getProp(this.layoutProps, {});
    layoutProps = Object.keys(layoutProps).map(propName => `${propName}="${layoutProps[propName]}"`);

    const innerHtml = `<div ${withChildren ? 'slot="children"' : ''}>${this.renderRows(this.data, getProp(this.getters), getProp(this.template))}</div>`;

    if (this.layout === 'Column') {
      return `<jsc-column ${layoutProps}>${innerHtml}</jsc-column>`;
    }

    if (this.layout === 'Row') {
      return `<jsc-row ${layoutProps}>${innerHtml}</jsc-row>`;
    }

    if (this.layout === 'None') {
      return innerHtml;
    }
  }

  render() {
    return <div innerHTML={this.getChildren()}></div>;
  }
}
