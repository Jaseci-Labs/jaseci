# Installation

To install MTLLM run,

```bash
pip install mtllm
```

By default, MTLLM will not install any llm integrations, to install the available integrations, include the extra(s) below:

> :Tabs
> > :Tab title=OpenAI
> >
> > ```bash
> > pip install mtllm[openai]
> > ```
>
> > :Tab title=Anthropic
> >
> > ```bash
> > pip install mtllm[anthropic]
> > ```
>
> > :Tab title=Together
> >
> > ```bash
> > pip install mtllm[together]
> > ```
>
> > :Tab title=Ollama
> >
> > ```bash
> > pip install mtllm[ollama]
> > ```
>
> > :Tab title=Huggingface
> >
> > ```bash
> > pip install mtllm[huggingface]
> > ```
>
> > :Tab title=Groq
> >
> > ```bash
> > pip install mtllm[groq]
> > ```

MTLLM Supports MultiModal LLMs. To Support Images and Videos, you need to install the following extra(s):

> :Tabs
> > :Tab title=Image Support
> >
> > ```bash
> > pip install mtllm[image]
> > ```
>
> > :Tab title=Video Support
> >
> > ```bash
> > pip install mtllm[video]
> > ```
> >

Currently, only multimodal LLMs from OpenAI and Anthropic are supported. In the future, we plan to support multimodal LLMs from other providers as well