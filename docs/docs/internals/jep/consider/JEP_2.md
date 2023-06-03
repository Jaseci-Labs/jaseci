---
sidebar_position: 2
title: JEP 2 - Co-design and Interoperability With Netron
---

### JEP 2 - Co-design and Interoperability With Netron
---
#### Details
| Author      | Type | Quick Description | 
| ----------- | ------ | ------ |
| Jason Mars | Technical | Jaseci Graph Adherence to Netron's Standard |

#### Description

Jaseci, with its unique combination of compute elements and graph representations, should be designed to be interoperable with the Netron open-source project. Netron serves as a versatile viewer for neural networks and supports a wide spectrum of representations, making it inherently generalizable to compute intersecting graph structures. By adhering to the Netron project, Jaseci can leverage the existing visualization codebase and benefit from the flexibility and compatibility it offers.

Jaseci's computation abstractions surpass the capabilities of a typical neural network flow, encompassing a broader range of graph-based computations. While achieving a comprehensive mapping of Jaseci graphs to a subsetted representation compatible with Netron may be challenging, it is worth attempting for general graphs. However, at the very least, Jaseci's new model abstraction should ensure full interoperability with Netron.

Aligning the design of Jaseci's graph compute structures to Netron provides several significant advantages for the developer and user community:

1. **Generalizability**: By integrating with Netron, Jaseci gains the ability to handle a wide variety of graph representations, expanding its scope beyond traditional neural networks. This enhances Jaseci's applicability to different domains and use cases, promoting generalizability.

2. **Portability**: The alignment with Netron ensures that Jaseci models and graph computations can be seamlessly transported and shared across platforms and frameworks supported by Netron. This portability empowers developers to leverage Jaseci's capabilities in diverse environments.

3. **Understandability**: Netron's visualization codebase is widely recognized and understood by the developer and user community. By piggybacking on Netron's existing codebase, Jaseci benefits from a familiar and user-friendly interface, facilitating comprehension and adoption among users.