import dayjs from 'dayjs';
import advancedFormatter from 'dayjs/plugin/advancedFormat';
import { renderComponentTree } from './utils';

dayjs.extend(advancedFormatter);

export function formatRowContent({ value, formatter, format }: { value: string; formatter?: 'date' | 'native'; format?: string }) {
  if (formatter === 'date') {
    return dayjs(value).format(format);
  }

  if (formatter === 'native') {
    return format.replaceAll('{{value}}', value);
  }

  return value;
}

export function getRowValue(accessor: string, row: { context: Record<string, any>; jid: string; j_timestamp: string }): string {
  if (accessor === 'jid') return row.jid;
  if (accessor === 'j_timestamp') return row.j_timestamp;
  return row.context[accessor];
}

export function renderRow(row: [], headers: []) {
  return row
    .map((col, colIndex) => {
      // render component if a render prop was provided to the col's header
      if (headers[colIndex]['render']) {
        return `<td>${renderComponentTree(headers[colIndex]['render']).replaceAll('{{value}}', col)}</td>`;
      }
      return `<td>${col}</td>`;
    })
    .join('');
}
