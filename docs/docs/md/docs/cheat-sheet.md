# Markdown Cheat Sheet

Checkout `docs/md/docs/cheat-sheet.md` to see the markdown behind this page. Note that this is only
a cheat-sheet, for a more complete list of specific markdown features of codedoc, check out the [official docs](https://codedoc.cc).

> :Buttons
> > :Button label=Official Docs, url=https://codedoc.cc

<br>

> ⚠️⚠️
> Do not forget to **REMOVE THIS PAGE** from your actual documentation!
> ⚠️⚠️

<hr>

## Buttons

You can add buttons to your documents like this:

```md | some-doc.md
> :Buttons
> > :Button label=Click Me!, url=https://www.google.com
>
> > :Button label=Click Me Too!, url=https://www.github.com
```

Which looks like this:

> :Buttons
> > :Button label=Click Me!, url=https://www.google.com
>
> > :Button label=Click Me Too!, url=https://www.github.com

<br>

You can create icon buttons as well. By default material icons are used:

```md | some-doc.md
> :Buttons
> > :Button icon=true, label=android, url=https://www.google.com
>
> > :Button icon=true, label=code, url=https://www.github.com
>
> > :Button label=GitHub, url=https://www.github.com
```

Which looks like this:

> :Buttons
> > :Button icon=true, label=android, url=https://www.google.com
>
> > :Button icon=true, label=code, url=https://www.github.com
>
> > :Button label=GitHub, url=https://www.github.com


<br>

You can add a copy button after a `code` element. This button would
copy the contents of the `code` element.

```md | some-doc.md
> :Buttons
> > :CopyButton
```
> :Buttons
> > :CopyButton

<hr>

## Tabs

You can add tabbed content like this:

```md | some-doc.md
> :Tabs
> > :Tab title=First Tab
> >
> > So this is the content of the first tab. Lets even have some code here:
> > ```tsx | index.tsx
> > import { Renderer } from '@connectv/html';
> >
> > const renderer = new Renderer();
> > renderer.render(<div>Hellow World!</div>).on(document.body);
> > ```
>
> > :Tab title=Second Tab
> >
> > Perhaps some other content here, maybe some more code?
> >
> > ```tsx | another.tsx
> > import { Renderer } from '@connectv/html';
> > import { timer } from 'rxjs';
> >
> > const renderer = new Renderer();
> > renderer.render(<div>You have been here for {timer(0, 1000)} second(s).</div>)
> > .on(document.body);
> > ```
```

<br>

> :Tabs
> > :Tab title=First Tab
> >
> > So this is the content of the first tab. Lets even have some code here:
> > ```tsx | index.tsx
> > import { Renderer } from '@connectv/html';
> >
> > const renderer = new Renderer();
> > renderer.render(<div>Hellow World!</div>).on(document.body);
> > ```
>
> > :Tab title=Second Tab
> >
> > Perhaps some other content here, maybe some more code?
> >
> > ```tsx | another.tsx
> > import { Renderer } from '@connectv/html';
> > import { timer } from 'rxjs';
> >
> > const renderer = new Renderer();
> > renderer.render(<div>You have been here for {timer(0, 1000)} second(s).</div>)
> > .on(document.body);
> > ```

<hr>

## Collapse

You can add collapsible sections like this:

```md | some-doc.md
> :Collapse label=Collapsible content (click to open)
>
> This content is collapsed by default. You can write _any_ markdown syntax you would
> like here as this is simply just an enhanced `block quote` element. You can even have lists:
> - with multiple
> - items and stuff
>
> > :Collapse label=Or nested collapsible content (click to open)
> >
> > > :Collapse label=Collapception
> > >
> > >  To any depth that your heart might desire.
>
> This component is particularly useful in the table of contents (the left-side menu, activatable by
> clicking on the hamburger menu in the footer), when you have got many documents and you would want to
> neatly categorize them.
```

<br>

> :Collapse label=Collapsible content (click to open)
>
> This content is collapsed by default. You can write _any_ markdown syntax you would
> like here as this is simply just an enhanced `block quote` element. You can even have lists:
> - with multiple
> - items and stuff
>
> > :Collapse label=Or nested collapsible content (click to open)
> >
> > > :Collapse label=Collapception (click to open)
> > >
> > >  To any depth that your heart might desire.
>
> This component is particularly useful in the table of contents (the left-side menu, activatable by
> clicking on the hamburger menu in the footer), when you have got many documents and you would want to
> neatly categorize them.

<hr>

## Dark/Light Content

If you have some content that differs in light mode vs in dark mode, you
can use `DarkLight` component:

```md | some-doc.md
> :DarkLight
> > :InDark
> >
> > We are SO DARK! This content is only shown in dark-mode. Switch to light-mode
> > by clicking on the dark/light toggle in the footer to see the light-mode specific content.
>
> > :InLight
> >
> > LIGHT bless you! This content is only shown in light-mode. Switch to dark-mode
> > by clicking on the dark/light toggle in the footer to see the dark-mode specific content
```

<br>

> :DarkLight
> > :InDark
> >
> > We are SO DARK! This content is only shown in dark-mode. Switch to light-mode
> > by clicking on the dark/light toggle in the footer to see the light-mode specific content.
>
> > :InLight
> >
> > LIGHT bless you! This content is only shown in light-mode. Switch to dark-mode
> > by clicking on the dark/light toggle in the footer to see the dark-mode specific content

> If you are wondering why someone would **EVER** need such a thing, well I did. Because I wanted
> to display different banner images based on dark-mode / light-mode:
>
> ```md
> > :DarkLight
> > > :InLight
> > >
> > > ![header](https://raw.githubusercontent.com/CONNECT-platform/codedoc/master/repo-banner.svg?sanitize=true)
> >
> > > :InDark
> > >
> > > ![header](https://raw.githubusercontent.com/CONNECT-platform/codedoc/master/repo-banner-dark.svg?sanitize=true)
> ```
>
> > :DarkLight
> > > :InLight
> > >
> > > ![header](https://raw.githubusercontent.com/CONNECT-platform/codedoc/master/repo-banner.svg?sanitize=true)
> >
> > > :InDark
> > >
> > > ![header](https://raw.githubusercontent.com/CONNECT-platform/codedoc/master/repo-banner-dark.svg?sanitize=true)
>
> Yeah I know the life of an idealist is never easy.

<hr>

## Navigation

You can add _previous_ and _next_ buttons to your pages like this:

```markdown
> :ToCPrevNext
```

Which would then look like this:

> :ToCPrevNext