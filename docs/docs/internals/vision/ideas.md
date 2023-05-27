---
sidebar_position: 3
description: Ideas being considered for Jaseci 2.0
title: Ideas (JSEPs)
---

# Idea's for Jaseci 2.0

This document represents our Jaseci Enhancement Proposals system (JSEP). 
## Accepted 


### JSEP 1 - JSEP Purpose and Guidelines
---
#### Details
| Author      | Type | Quick Description | 
| ----------- | ------ | ------ |
| Jason Mars  | Process | Specifying the Jaseci enhancement proposal process and guidelines |

#### Description
This process is inspired by python's pep system but much simplified. 

There are three categories of JSEPs that will be merged into this document, JSEPs accepted for inclusion in the language design and specification, idea's worth deep consideration, and idea's considered but rejected for now. 

All JSEPs will start in the deep consideration category and moved to either accepted, or rejected categories for long term archival. 


The process is as follows: 

* To submit an idea simply make a pull request including the idea to this document in the to be considered section using the same format (and linear number scheme) of other ideas in this document. 
* If the idea is merged into into main, it has made it through the first filter, if not, it will not be not enter the consideration phase.
* After necessary discussion / iteration the JSEP will move either into accepted or rejected categories. 
* Rarely, rejected JSEPs that was deeply consider may be resurrected in the future if circumstance provide. 

The types of JSEPs include: 

* Process - Proposal for implementation, improvements, or modifications to any processes associated to how Jaseci is maintained. 
* Technical - Proposals around, features, designs, or any technical aspects around Jaseci
* Informational - Any best practices, code style guidelines, or other official guidelines around how Jaseci should be used by the broader community. 

JSEPs can be iterated on at any time and evolve over time regardless of the category they are in wether accepted, under consideration, or rejected via further PRs. 

Feel free to use any/all features of markdown to clearly articulate your ideas in the body of your JSEPs such as code snippets etc! 

## Under Consideration 
### JSEP 2 - Co-design and Interoperability With Netron
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

## Considered but Rejected


## Template

### JSEP X - Title...
---
#### Details
| Author      | Type | Quick Description | 
| ----------- | ------ | ------ |
|  |  |  |

#### Description

Description goes here...