import { Component, Element, h, Method, Prop, Watch } from '@stencil/core';
import clsx from 'clsx';
import { getProp } from '../../store/propsStore';
import { formatRowContent, getRowValue, renderRow } from '../../utils/datagrid';
import { setUpEvents } from '../../utils/events';
import { getOperations } from '../../utils/utils';
import { sort } from 'fast-sort';

@Component({
  tag: 'jsc-datagrid',
  styleUrl: 'jsc-data-grid.css',
  shadow: true,
})
export class JscDatagrid {
  @Element() host: HTMLElement;
  @Prop() css: string = JSON.stringify({});
  @Prop({ mutable: true }) events: string;
  @Prop() name: string;
  @Prop() variant: 'striped' | 'default';
  @Prop() server: string;
  @Prop() walker: string;
  @Prop() snt: string;
  @Prop() token: string;
  @Prop() headings: string;
  @Prop({ mutable: true }) rows: { context: any }[];
  @Prop({ mutable: true }) operations;
  @Prop() rowData: [][] = [];
  @Prop({ mutable: true }) sortOrder: {} = {};
  @Prop({ attribute: 'itemsperpage' }) itemsPerPage: number = 2;
  @Prop() currentPage: number = 1;
  @Prop() maxPages: number = 1;

  @Method()
  async refetchData() {
    this.fetchData();
  }

  fetchData() {
    fetch(`${this.server}/js/walker_run`, {
      method: 'POST',
      body: JSON.stringify({
        name: this.walker,
        snt: this.snt,
      }),
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `token ${this.token}`,
      },
    })
      .then(res => res.json())
      .then(res => {
        this.rows = res.report[0];
        this.maxPages = Math.ceil(this.rows.length / this.itemsPerPage);
        this.rowData = this.getRowData(this.rows);
      });
  }

  componentDidLoad() {
    Object.assign(this.host.style, {
      'box-sizing': 'border-box',
      'overflowX': 'auto',
      ...JSON.parse(this.css),
    });

    setUpEvents(this.host, this.events);
    this.operations = getOperations(this.name);

    this.fetchData();
  }

  calculateRowData() {
    return sort(this.getRowData(this.rows)).by(
      Object.keys(this.sortOrder).map(heading => ({
        [this.sortOrder[heading]]: i => i[getProp(this.headings).findIndex(sourceHeading => sourceHeading.accessor === heading)],
      })) as any,
    );
  }

  @Watch('rows')
  watchRows() {
    this.rowData = this.calculateRowData();
  }

  @Watch('sortOrder')
  watchSortOrder() {
    this.rowData = this.calculateRowData();
  }

  @Watch('currentPage')
  watchCurrentPage() {
    this.rowData = this.calculateRowData();
  }

  getRowData(rows: any[]) {
    // build the 2d array of data
    // get the headings
    const headings = getProp(this.headings);

    const rowData = rows.map(row => {
      let result = headings.map(heading =>
        formatRowContent({
          value: getRowValue(heading.accessor, row),
          format: heading.format,
          formatter: heading.formatter,
        }),
      );
      return result;
    });

    const start = this.currentPage === 1 ? 0 : this.itemsPerPage * (this.currentPage - 1);
    return rowData.slice(start, this.currentPage * this.itemsPerPage);
  }

  render() {
    return (
      <div>
        <table cellspacing={0} class="table">
          <thead class="table-head">
            <tr>
              {getProp(this.headings).map(heading => (
                <th>
                  <span
                    onClick={() => {
                      if (this.sortOrder[heading.accessor] === 'desc') {
                        const newSortOrder = { ...this.sortOrder };
                        delete newSortOrder[heading.accessor];
                        this.sortOrder = { ...newSortOrder };
                      } else {
                        this.sortOrder = {
                          ...this.sortOrder,
                          [heading.accessor]: this.sortOrder[heading.accessor] === 'asc' ? 'desc' : 'asc',
                        };
                      }
                    }}
                    style={{ cursor: 'pointer' }}
                  >
                    {heading.label}
                  </span>
                  {this.sortOrder[heading.accessor] === 'asc' ? (
                    <svg xmlns="http://www.w3.org/2000/svg" class="icon" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                      <path stroke-linecap="round" stroke-linejoin="round" d="M8 7l4-4m0 0l4 4m-4-4v18" />
                    </svg>
                  ) : this.sortOrder[heading.accessor] === 'desc' ? (
                    <svg xmlns="http://www.w3.org/2000/svg" class="icon" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                      <path stroke-linecap="round" stroke-linejoin="round" d="M16 17l-4 4m0 0l-4-4m4 4V3" />
                    </svg>
                  ) : (
                    <span></span>
                  )}
                </th>
              ))}
            </tr>
          </thead>
          <tbody class={clsx('table-body', this.variant === 'striped' && 'table-striped')}>
            {this.rowData.map(row => (
              <tr innerHTML={renderRow(row, getProp(this.headings))}></tr>
            ))}
            {/* footer */}
            <tr>
              {Array.from({ length: getProp(this.headings).length }).map((val, index) => {
                // last cell
                if (index === getProp(this.headings).length - 1) {
                  return (
                    <td class="w-8 h-8">
                      <span class="page-indicator">
                        Page {this.currentPage}/{this.maxPages}
                      </span>
                      {/* Prev */}
                      <svg
                        onClick={() => {
                          this.currentPage = this.currentPage === 1 ? this.currentPage : this.currentPage - 1;
                        }}
                        xmlns="http://www.w3.org/2000/svg"
                        class="icon-btn"
                        fill="none"
                        viewBox="0 0 24 24"
                        stroke="currentColor"
                        stroke-width="2"
                      >
                        <path stroke-linecap="round" stroke-linejoin="round" d="M15 19l-7-7 7-7" />
                      </svg>
                      {/*  Next */}
                      <svg
                        onClick={() => {
                          this.currentPage = this.currentPage === this.maxPages ? this.maxPages : this.currentPage + 1;
                        }}
                        xmlns="http://www.w3.org/2000/svg"
                        class="icon-btn"
                        fill="none"
                        viewBox="0 0 24 24"
                        stroke="currentColor"
                        stroke-width="2"
                      >
                        <path stroke-linecap="round" stroke-linejoin="round" d="M9 5l7 7-7 7" />
                      </svg>
                    </td>
                  );
                }
                return <td>{val}</td>;
              })}
            </tr>
          </tbody>
        </table>
      </div>
    );
  }
}
