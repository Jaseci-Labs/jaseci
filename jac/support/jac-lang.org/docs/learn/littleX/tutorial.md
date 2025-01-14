# **Tutorial For Beginners**

## **Introduction to Graphs**

A **graph** is a mathematical structure used to model relationships between objects. It consists of two primary components:

- **Nodes (or Vertices)**: These are the individual entities or points in the graph. Each node represents an object, entity, or a piece of data.

- **Edges**: These are the connections or relationships between nodes. Edges can be directed (one-way) or undirected (two-way).

### **Key Characteristics of Graphs**

- **Directed vs. Undirected**:
      - A **directed graph** has edges with a direction, indicating a one-way relationship (e.g., "A points to B").
      - An **undirected graph** has edges with no direction, indicating a two-way relationship (e.g., "A is connected to B").

- **Weighted vs. Unweighted**:
      - A **weighted graph** assigns a weight or value to each edge (e.g., distance, cost, or capacity).
      - An **unweighted graph** treats all edges equally.

??? example "Graph"
      ![Image title](images\graph.png)
      Sample Graph image will be updated soon

??? example "Family Graph"
      Sample Family Graph image will be updated soon
---

## **Introduction to Data-spatial Programming**

**Data Spatial Programming** organizes data as interconnected nodes within a spatial or graph-like structure. It focuses on the **relationships** between data points, rather than processing them **step-by-step**. This approach is ideal for complex systems like social networks or AI models, where data entities influence each other dynamically.

| Aspect      | Conventional Programming  | Data Spatial Programming |
| :---------: | :-------------: | :-------------: |
| Data Representation       | Data is stored in linear structures like arrays, tables, or objects.  | Data is represented as entities (nodes) in a multidimensional space (graphs).  |
| Focus       | Focuses on procedural logic and algorithmic problem-solving. | Focuses on relationships and interactions between data points. |
| Execution Model    | Runs sequentially, following explicit instructions. | Operates through spatial relationships, with data interacting dynamically. |
| Use Cases    | System programming, desktop applications, database manipulation. | Real-time network analysis, AI, graph-based applications, simulations. |

---

# **LittleX Architecture and Its Explanation**

## **Overview of LittleX Architecture**

![Image title](images\Architecture.png)

### **Nodes**

#### **profile**
- Represents a user profile.
- **Attributes:**
      - `username`: Name of the user.
      - `count_tag`: Tracks hashtag usage as a dictionary.
      - `followees`: List of followed profiles.

- User Node
      ```jac
      node User {
            has username: str;
            has followers: list;
            has posts: list;
      }
      ```

#### **tweet**
- Represents a user's post/tweet.
- **Attributes:**
      - `content`: Tweet text.
      - `created_at`: Timestamp when the tweet was created.

#### **comment**
- Represents a comment on a tweet.
- **Attributes:**
      - `content`: Comment text.

---

### **Edges (Relationships)**

- **follow:** Connects one profile to another (followee).
- **like:** Represents a "like" relationship between a profile and a tweet.
- **post:** Represents a relationship where a profile posts a tweet.

- **Follow Edge**
      ```jac
      edge follow {}
      ```







