# Code Features

This is a quick overview of codedoc specific features at your disposal in markdown
`code` elements. For a complete list, please checkout the [official documentation](https://codedoc.cc).
You can also take a look at `docs/md/docs/code-features.md` to see the markdown behind this page.

> :Buttons
> > :Button label=Official Docs, url=https://codedoc.cc

<br>

> ⚠️⚠️
> Do not forget to **REMOVE THIS PAGE** from your actual documentation!
> ⚠️⚠️

<hr>

## Hints

A comment with the following format will cause a hint to be displayed on-hover:

> `// --> some hint here`

```tsx | index.tsx
import { Renderer } from '@connectv/html';                       // --> there is a hint on this line

const MyComp = ({ name }, renderer) => <div>Hellow {name}!</div> // --> there is also a hint on this line

const renderer = new Renderer();
renderer.render(
  <fragment>
    <MyComp name='World'/>
    <MyComp name='Fellas'/>                                      {/* --> also this is a hint */}
  </fragment>
)
.on(document.body);
```

<br>

The following syntax styles are supported:


```go
"// --> standard one-liner" // --> standard one-liner
```

```java
"/* --> standard multi-liner */" /* --> standard multi-liner */
```

```py
"# --> python/bash comments" # --> python/bash comments
```

```md
<‌!--> html comments --> <!--> html comments -->
```


<hr>

## References

Add a comment with following format in the code will show a link on-hover over the line:

> `// @see https://www.google.com`

```tsx
import { Renderer } from '@connectv/html';                       // @see https://github.com/CONNECT-platform/connective-html
```

You can also use the markdown link format to give your links a title:

````md | --no-wmbar
```
import { Renderer } from '@connectv/html'; // @see [CONNECTIVE HTML Docs](https://github.com/CONNECT-platform/connective-html)
```
````
```tsx
import { Renderer } from '@connectv/html';                       // @see [CONNECTIVE HTML Docs](https://github.com/CONNECT-platform/connective-html)
```

You can also use these references to refer to another tab in a tab-component:

```md | some-doc.md
> :Tabs
> > :Tab title=First Tab
> >
> > ```tsx
> > import { func } from './other'; // @see tab:Second Tab
> >
> > func(); // --> good stuff will happen now
> > ```
>
> > :Tab title=Second Tab
> >
> > ```tsx
> > export function func() {
> >   console.log('Good Stuff!');
> > }
> > ```
```
<br>

> :Tabs
> > :Tab title=First Tab
> >
> > ```tsx
> > import { func } from './other'; // @see tab:Second Tab
> >
> > func(); // --> good stuff will happen now
> > ```
>
> > :Tab title=Second Tab
> >
> > ```tsx
> > export function func() {
> >   console.log('Good Stuff!');
> > }
> > ```

Similar syntax styles to hints are supported for references as well:


```js
"// @‌see [random stuff](https://www.randomlists.com/things)" // @see [random stuff](https://www.randomlists.com/things)
```

```go
"/* @‌see https://google.com */" /* @see https://google.com */
```

```python
"#@see https://github.com" #@see https://github.com
```

```html
<!-- @‌see [the first page](/) --> <!-- @see [the first page](/) -->
```


> :ToCPrevNext