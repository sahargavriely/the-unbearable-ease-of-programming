# What is a Good Design

This document outlines principles for designing and maintaining a well-structured, maintainable, and understandable codebase. It emphasizes clarity, simplicity, and effective problem-solving strategies.
    _"I know it when I see it."_ - Potter Stewart

## Aesthetics and Organization

* Readability: Prioritize clear, descriptive variable and function names. Avoid unnecessary complexity for the sake of aesthetics.
* Consistency: Maintain a consistent coding style throughout the project.
* Modular Design: Break down the codebase into well-defined modules with minimal dependencies. Avoid overly complex folder structures based solely on material types.

    _"A Foolish Consistency is the Hobgoblin of Little Minds"_ - Ralph Waldo Emerson

    __Remember, consistency is important, but it shouldn't hinder logical organization.__

## The Principle of Least Astonishment

* Intuitive Behavior: Functions and fields should behave predictably:
    * Functions and methods do something.
    * Field or property should be immediate.
* Arguments should appear in a logical order, with the most common options readily accessible.

## Simplicity

* Leverage Native Types: When possible, utilize the language's native data types instead of creating custom objects for every scenario.
* Focus on Core Functionality: Concentrate on solving the core problem with minimal extra features. Edge cases can be addressed later as needed.

    _"Make the easy jobs easy, and the hard jobs possible."_ - Larry Wall

    __Focus on making the core functionality clear and efficient.__

## Avoiding Overgeneralization

* Balance Specificity and Flexibility: Design your code to be adaptable without introducing unnecessary complexity.

    _"I'd spell creat with an e."_ - Ken Thompson

    __Consider the "Goldilocks zone" - not too specific, not too general.__

## Problem-Solving and Complexity Management

* Prioritization: Distinguish between essential and non-essential features. Address complexity by managing dependencies, state, and edge cases effectively.
* Progressive Disclosure: Introduce functionalities gradually to avoid overwhelming users with options. Organize and expose elements thoughtfully.
* Use abstractions to hide implementation details and improve maintainability.
* Design is about refining the abstraction so we can build on top of it, while engineering is about implementing the abstraction.

    __Recognaize patterns and define abstractions.__

### Dependencies

* Directed Acyclic Graph (DAG): Organize dependencies in a way that avoids circular references. Consider using dependency managers for complex scenarios.
* Dependencies are unavoidable, but how you handle them matters.
    * Hardcoded vs. Injected: Dependencies can be tightly coupled to the code (hardcoded) or passed in as parameters (injected).
    * Discovery as an Option: In some cases, frameworks can discover dependencies automatically.
* Dependency Injection: When possible, pass dependencies as input for better testability and reduced coupling.

#### Dependency Injection

* Separation of Concerns: An injector constructs the service and injects it into the client, which only uses it.
* Easy to Test: a mock dependency can be easily injected.
* Decoupled the dependency from whatever uses it, which leaves it as an abstraction.

##### Complex Dependency Injection Management

* Context: A local class instance that is being injected and provide all the dependencies. Similar to flask's route request argument. Created locally instead of globally and can hold many dependencies.
* Containers: Functions or classes responsible for orchestrating object creation, composition, and injection. Similar to pytest's fixture interface - "You define a function with some arguments, and I'll figure out how to invoke it".
    * Configuration-Driven: Containers can be configured explicitly (e.g., by schema) or implicitly (e.g., by signatures).

##### A Well-Injected Dependency

* A litmus test for when should a dependency be injected:
    * What assumptions are hardcoded in my code?
    * Can and should they be passed in as arguments?

#### The Clean Architecture, An Addition/Alternative Solution for Dependency Injection

* Decouple the procedure, by putting the I/O operation at the top level, and move the data to the bottom - creating a pure functions  at the bottom which are easy to test.
* The coupling between I/O and logic is isolated to small procedure, making the procedure and its pure functions cohesive.

    __eminently readable because it stays at the same level of abstraction.__

##### A Well-Decoupled Design

* Cohesion vs. Coupling:
    * Cohesion: How well-related functionalities are within a module (higher is better).
    * Coupling: How interconnected modules are (lower is better).
* A litmus test for well-decoupled design is:
    * Is it cohesive?
    * Is it easier to test?

    __Avoid over-generic code in pursuit of reusability. Focus on solving specific problems effectively.__

### Generalizing to State

* State management adds complexity. Use it judiciously and consider decoupling complex state logic when necessary.

    __Use it, but not lightly.__

### Edge Cases

* Focus on Common Scenarios: Prioritize clear and reliable behavior for typical use cases. Handle edge cases explicitly and separately later as required.
* Fail Fast: Design your code to identify and signal errors as quickly as possible.
* Simplicity and usability often trump completeness (and even correctness!)

    __Prioritize a clear and usable interface over absolute edge case coverage.__

### Cognitive Load

* Organize Options Intuitively: Group options in a natural hierarchy, placing frequently used elements prominently.
* Composition over Inheritance: Favor code composition to distribute functionality and reduce cognitive load for developers.

    __Focus on clear and well-defined interfaces for both users and developers.__

### Multipurposeness

* Modular vs. Monolithic Systems: Evaluate whether a modular or monolithic architecture is better suited for the project's needs. Consider the trade-off between simplicity of interfaces and separation of responsibilities (Single Responsibility Principle).

    __The "Goldilocks zone" applies here too - avoid overly generic or overly specific designs.__

### Simplicity

* The Unix Philosophy: Strive for a clear and concise interface like the Unix commands: open, close, read, write.

    _"Simplicity is the ultimate sophistication"_ - Steve Jobs

    _"Perfection is achieved, not when there is nothing more to add, but when there is nothing left to take away."_ - Antoine de Saint-Exupéry

    _"Everything should be made as simple as possible, but no simpler"_ — Albert Einstein

    __Strive for simplicity, but avoid oversimplification; complexity is not always bad.__


### Practice Stepping Back

* Motivation is More Important Than Value: It implies latent value.
* Re-Phrasing The Problem: Copernican refactoring - change your point of view.
* Maturity: The ability to wholeheartedly reconcile contradictory ideas.

# Closing Remark

It is not expected of you to remember it all nor you should memorize it. I, as well, do mistakes and do not design according to what I've written here. But it is important to go over it form time to time and talk about it.
    _"I cannot remember the books I've read any more than the meals I have eaten; even so, they have made me."_ — Ralph Waldo Emerson
