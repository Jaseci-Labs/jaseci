
import { configuration } from '@codedoc/core';
import { mermaidPlugin } from 'codedoc-mermaid-plugin'
import { theme } from './theme';


export const config = /*#__PURE__*/configuration({
  theme,                                  // --> add the theme. modify `./theme.ts` for changing the theme.
  dest: {
    namespace: '/mtllm'                   // --> your github pages namespace. remove if you are using a custom domain.
  },
  page: {
    title: {
      base: 'MTLLM API Documentation'                       // --> the base title of your doc pages
    }
  },
  plugins: [
      mermaidPlugin()   // --> make sure you add this section
  ],
  misc: {
    github: {
      user: 'Jaseci-Labs',              // --> your github username (where your repo is hosted)
      repo: 'mtllm',                      // --> your github repo name
    }
  },
});
