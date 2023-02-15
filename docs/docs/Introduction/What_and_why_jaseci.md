# Simplifying the Development of Modern Production Applications with Jaseci

The development of modern production applications that encompass multiple services and programs, such as databases, memcache, logging, application logic, and AI models, requires technical expertise and a skilled developer team. This complexity in creating multi-service applications is in contrast to the earlier era of computing, where software products were single binaries developed by a single programmer.

To mitigate this complexity, we introduce a top-down rethinking of the system stack, from the programming language to the system architecture, to simplify the creation of sophisticated production software. Our design aims to allow the programmer to express solutions with high-level abstractions at the problem level, while the runtime system subsumes and hides the underlying sub-applications and inter-machine resources.

We present Jaseci, a production-grade system architecture, and Jac, a corresponding programming language, as an implementation of this new approach. Jac and Jaseci have been released as open source and have been successfully utilized by product teams to accelerate the development and deployment of sophisticated AI products and other applications at scale. Jac has been shown to reduce AI development timelines by approximately 10 times in commercial production environments, and the Jaseci runtime automates the decisions and optimizations typically requiring manual engineering roles.

# Motivations
## The Landscape of Software Development Has Evolved

In the past two decades, the way we build software has undergone a significant transformation. In the early days of computing, a single program was expected to run on a single machine. The underlying system software managed resources such as processor, memory, disk, and physically connected peripherals within the context of the machine. However, with the growth of the internet, the concept of software shifted towards applications that are served through a network of multiple services.

Today, a single application can be comprised of several individual sub-applications, such as databases, memcache, logging, application logic, and AI models, that interact with each other via APIs. This shift has resulted in complex and costly software development, as the underlying programming paradigms have not evolved at the same pace as the changes in the software landscape.

## Mitigating the Complexity of Diffuse Applications

To address the complexity of building diffuse applications, two key abstractions have emerged. The first is the widespread adoption of containerization service platforms, such as Kubernetes, which abstracts away the underlying hardware resources and introduces virtual machines called pods that can be virtually networked together.

The second abstraction is the concept of Serverless Computing, popularized by Amazon's Lambda functions. This Function as a Service (FaaS) abstraction allows developers to make function calls in their preferred language without having to be aware of the underlying containerized service ecosystem or the system-level resources that are allocated or managed.

## Chase for Change

The current landscape of serverless computing has improved the speed of software development, but significant challenges still exist, especially in the development of AI-based applications. The traditional software engineering model involves multiple siloed roles such as architects, data scientists, backend engineers, and DevOps engineers, each with their own responsibilities. However, this model leads to complexities and challenges, such as re-architecture and delays due to resource limitations.

Jaseci is a solution aimed at accelerating and democratizing the development and deployment of scalable AI applications. Jaseci presents a set of high-level abstractions for programming sophisticated software in a micro-service/serverless AI environment and a full-stack architecture and programming model that automates much of the complexity in building distributed applications on potentially thousands of compute nodes.

# Elevating the Abstraction Level

In the field of computer science, the goal of raising the abstraction level in computational models has mainly been to enhance programmer efficiency. This efficiency comes from enabling engineers to tackle problems at a higher level while hiding the underlying system complexity. The Jac language incorporates new abstractions guided by these principles, based on two crucial observations. Firstly, Jac acknowledges the growing need for programmers to deal with graph representations of data to solve problems. Secondly, Jac facilitates the need for algorithmic modularity and encapsulation in order to change and test production software instead of executing existing codebases.

Based on these observations, Jac introduces two new sets of abstractions. Jac's data-spatial scoping supports graph-based problem solving by replacing the traditional temporal notion of scope with a flattened, graph-structured scoping. This type of scoping allows for a deeper understanding of the data related to the problem being solved. Jac's agent-oriented programming can be taught of as "little robots" that carry their scope with them as they move and perform computations relevant to their position in the graph. These agent abstractions capture the need for algorithmic modality and encapsulation when introducing solutions to complex codebases. Jac can be used as a standalone language to build complete solutions, or as an interface between components built in other languages.

By utilizing these new language abstractions, HomeLendingPal was able to create a production-level conversational AI experience with just 300 lines of code, compared to the tens of thousands that would have been required using a traditional programming language.

# Revolutionary Cloud-Scale Technology

Jaseci introduces a new level of abstraction in software technology, offering a cloud-scale runtime engine that simplifies the optimization, orchestration, and configuration of program code, microservices, and the entire cloud compute stack. Automated tasks such as container formation, microservice scaling, scheduling, and optimization are handled by the runtime, allowing programmers to focus on their code without worrying about the underlying system.

Jaseci also introduces the concept of container-linked libraries, which seamlessly merge traditional statically and dynamically linked libraries with the running program. The runtime engine makes decisions about which functions should be part of the program's object scope and which should be remote microservices, without requiring any manual input from the programmer. This new level of abstraction allows the runtime to handle complex tasks such as autoscaling and provides full visibility and control over the application.

With the help of the Jaseci runtime, a single frontend engineer was able to implement the ZeroShotBot application, which uses multiple transformer neural networks, without having to write any backend code. This implementation currently supports tens of thousands of queries per day across 12 business customers with numerous individual end-users in a single production environment.

# Jaseci in Action: Powering the Next Generation of AI Products

The Jaseci platform is an open-source technology stack with a license from MIT. It consists of three packages: Jaseci Core, the core execution engine, Jaseci Serv, the diffuse runtime cloud-scale execution engine, and Jaseci Kit, a collection of AI engines provided by the Jaseci community. There is also an experimental toolkit in development called Jaseci Studio that provides visual programming and debugging tools for developers building with Jaseci.

There are several examples of Jaseci being used in production by various startups. These include myca.ai, a personal productivity platform that uses AI to understand personal behavior and help users prioritize tasks. It was launched within 3 months of development and is one of the fast-growing personal growth tools with positive feedback from users. ZeroShotBot is a B2B company that develops a cutting-edge conversational AI platform using Jaseci. The product development took 2 months and was done by front-end engineers, and has gained significant market traction. Truselph is a minority-founded startup that creates an avatar with conversational intelligence and is in partnership with Lenovo to co-develop powered kiosks. Home Lending Pal is an AI-powered mortgage advisor and helps under-served minority populations navigate the mortgage and home purchase process. It adopted Jaseci to provide personalized mortgage advice and an AI-powered chatbot to answer questions about the process and give users a plan to improve their finances.

# Jaseci: The Future of AI Development

Jaseci introduces a revolutionary computational model designed to streamline the development of AI applications. With its unique data-spacial programming model and diffuse execution environment, Jaseci has achieved significant results, including a 10x reduction in development time and nearly complete elimination of typical backend code. Open-sourced in 2021, Jaseci is already in production with four commercial products, such as Myca, HomeLendingPal, ZeroShotBot, and TrueSelph, leading the way in AI innovation.

