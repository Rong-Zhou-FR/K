Plan the implementation of the following project in this repository:

```
[Project name] K

[Project description]

- Python library for 3D classical physics simulation, calculation and visualization
  - covers all major branchs of classical physics

[project scope]

- user can:
  - simulate
    - create 2D,3D space
    - choose what areas to include
      - e.g., simulate only mechanics, but not thermodynamics
    - add elements:
      - objects
        - e.g., blocks, rods, etc.
      - abstract physical influences
        - e.g., forces, torques, light source, heat source, etc. into spaces created
  - calculate
    - properties of objects
      - motion
      - temperature
      - ...
    - property of subsystems (a group of objects)
  - visualise
    - visualise the created space in 2D/3D static image/videos
    - export diagrams
      - e.g., force diagram, optical geometry diagram

[project requirements]

- 100% FOSS: zero proprietary dependency
- modularity
  - each function does one small thing and one small thing only
  - functions that can be potentially reused must be 
  - each module fulfills one purpose
- lightweight and minimalist
  - when existing FOSS libraries fulfill already a function, import it instead of rewriting from scratch
- extensible
  - user can easily extend functionality by writing a custom layer over base functions
```

## Delivrables

You must create `./dev/plans/0-init-plan.md` and in it:

- Propose at least one project architecture and illustrate it in a tree diagram
- Propose at least one tech stack and illustrate it in a markdown table
- Outline main dependencies in a multi-level markdown list for each proposed stack


## Requirements

- When there are multiple comparable alternatives, you must include both, compare them and make clear which one(s) is/are best according to your opinion and why
- You must write clearly and concisely


