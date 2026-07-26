# Python Roadmap

> [!info] Framing
> A Java backend engineer's path to Python fluency — syntax shift → interview-grade idioms → backend stack. Topics map to Java/Spring equivalents wherever it helps the mental model.

---

### **Phase 0: Foundations & Mental Model**

> [!example] Start here — these reframe Java intuitions before touching syntax.

- **Java vs Python:** Philosophy, typing, performance, concurrency, ecosystem trade-offs → [[0. Foundations & Mental Model]]
- **Program Lifecycle & Runtime:** `.py` → bytecode → PVM, CPython interpreter, `.pyc`/`__pycache__`, reference counting + cyclic GC, GIL, module/import system → [[0. Foundations & Mental Model]]
- **JVM vs PVM:** Why CPython is "interpreted," JIT absence, startup-time differences

> [!note] Notes written: [[0. Foundations & Mental Model]] · [[1. The Java to Python Syntax Shift]]

### **Phase 1: The "Java to Python" Syntax Shift**

- **Basic Syntax & Indentation:** `if`, `else`, `elif`, loops (`for`, `while`), `range`, `break`/`continue`/`else` on loops
- **Dynamic Typing:** Variables, type inference, `None` (vs `null`); identity (`is`) vs value-equality (`a == b`)
- **Mutable vs Immutable Types:** Strings, Tuples, frozensets (Immutable) vs Lists, Dictionaries, Sets (Mutable)
- **Operators:** `//` (floor div), `**` (power), `and`/`or`/`not`, ternary `x if cond else y`, chained comparisons (`0 < x < 10`), walrus `:=`
- **Truthiness:** Falsy values (`0`, `""`, `[]`, `{}`, `None`), short-circuit evaluation
- **String Manipulation:** f-strings (interpolation + formatting `f"{x:.2f}"`), slicing `[start:end:step]`, common methods (`split`, `join`, `strip`, `replace`)
- **I/O Basics:** `print` (with `sep`/`end`), `input`

### **Phase 2: Core Data Structures (The Collections Framework)**

- **Lists:** Slicing, `append`/`extend`/`insert`/`pop`/`remove`, `sort` vs `sorted` (+ `key`, `reverse`), list comprehensions (crucial)
- **Dictionaries (`dict`):** HashMaps, key-value pairs, `get`/`setdefault`, `keys`/`values`/`items`, dict comprehensions, merge `{**a, **b}` / `|`
- **Tuples:** Unpacking/Destructuring, `*rest` unpacking, as dict keys
- **Sets:** Set operations (union `|`, intersection `&`, difference `-`), set comprehensions
- **Iteration Helpers:** `enumerate`, `zip`, `reversed`, `sorted`, `any`/`all`, `min`/`max` (with `key`)
- **Generator Expressions:** Lazy comprehensions `(x for x in ...)` (memory-efficient)

### **Phase 3: Functions & Functional Concepts**

- **Functions:** `def`, positional/keyword args, default args (⚠️ mutable default trap), `*args`, `**kwargs`, keyword-only args
- **Scope:** LEGB rule, `global`, `nonlocal`
- **First-Class Functions:** Passing functions as arguments, returning functions
- **Closures:** Capturing enclosing state (vs anonymous inner classes in Java)
- **Lambda Functions:** Anonymous functions
- **`map` / `filter` / `reduce`:** Functional pipeline (Stream API equivalent)
- **Decorators:** `@decorator_name`, `functools.wraps`, decorators with arguments (conceptually like Java Annotations but functional)
- **Generators & Iterators:** `yield`, iterator protocol (`__iter__`, `__next__`), `yield from`

### **Phase 4: Object-Oriented Python**

- **Classes & Objects:** `class`, `self` (explicit `this`), `__init__` (Constructor), class vs instance variables
- **Magic/Dunder Methods:** `__str__`/`__repr__`, `__eq__`/`__hash__`, `__len__`, `__lt__` (operator overloading, sortability)
- **Inheritance:** `super()`, multiple inheritance, MRO (Method Resolution Order)
- **Method Types:** Instance methods, `@classmethod` (factory), `@staticmethod`
- **Access Modifiers:** `_protected` vs `__private` (name mangling) conventions
- **Properties:** `@property`, getters/setters
- **Abstract Base Classes:** `abc.ABC`, `@abstractmethod` (interfaces)
- **Data-holding classes:** `@dataclass`, `namedtuple`, `Enum` (records / enums)
- **`__slots__`:** Memory optimization for many instances

### **Phase 5: Exceptions & Error Handling**

- **`try` / `except` / `else` / `finally`:** Control flow (vs Java try/catch/finally)
- **Raising:** `raise`, re-raising, exception chaining (`raise ... from ...`)
- **Exception Hierarchy:** `BaseException` → `Exception`, catching specific vs broad
- **Custom Exceptions:** Subclassing `Exception`
- **EAFP vs LBYL:** "Easier to Ask Forgiveness than Permission" — the Pythonic idiom
- **Context Managers as cleanup:** `with` for guaranteed teardown (try-with-resources)

### **Phase 6: The Standard Library (Interview Power Tools)**

- **`collections`:** `defaultdict`, `Counter`, `deque` (O(1) ends), `OrderedDict`, `namedtuple`
- **`heapq`:** Min-heap / priority queue (top-K, Dijkstra)
- **`bisect`:** Binary search / sorted insertion
- **`itertools`:** `product`, `permutations`, `combinations`, `accumulate`, `groupby`, `chain`
- **`functools`:** `lru_cache` / `cache` (memoization), `reduce`, `partial`, `cmp_to_key`
- **`math` / `random`:** `inf`, `gcd`, `comb`, `isqrt`; `random`/`shuffle`/`sample`
- **`datetime`:** Dates, times, `timedelta`, timezones
- **`re`:** Regular expressions (`match`/`search`/`findall`/`sub`)
- **Serialization:** `json`, `csv`, `pickle`
- **System & Paths:** `os`, `sys`, `pathlib`
- **`logging`:** Structured logging (vs `print`)
- **`typing` / `dataclasses`:** (cross-ref with Phases 4 & 7)

### **Phase 7: Modern Python & Tooling**

- **Type Hinting:** `list[str]`, `Optional[int]` / `int | None`, `dict`, `Callable`, generics; `mypy` for static analysis
- **Pydantic:** Runtime validation + settings models
- **Structural Pattern Matching:** `match` / `case` (Python 3.10+)
- **Modules & Packages:** import system, `__name__ == "__main__"`, `__init__.py`, absolute vs relative imports
- **Virtual Environments:** `venv`, `poetry` (dependency management vs Maven/Gradle)
- **Package Management:** `pip`, `requirements.txt`, `pyproject.toml`
- **Linting/Formatting:** `black`, `ruff`, `isort`
- **Context Managers:** `with open(...)`, writing your own (`__enter__`/`__exit__`, `contextlib.contextmanager`)

### **Phase 8: Backend Development (Spring Boot Equivalents)**

- **Web Frameworks:**
    - **FastAPI:** Async, modern, type-safe (closest to modern Spring Boot) — routing, request/response models, dependency injection, middleware
    - **Django:** "Batteries included" (heavy, similar to legacy Spring + Hibernate)
    - **Flask:** Micro-framework
- **API Design:** REST, validation with Pydantic, status codes, auth (JWT/OAuth)
- **ORM:**
    - **SQLAlchemy:** Core & ORM (Hibernate equivalent), sessions, relationships
    - **Migrations:** Alembic (Flyway/Liquibase equivalent)
- **Background Work & Messaging:** Celery / task queues, Redis, Kafka/RabbitMQ
- **Caching:** Redis, `functools.lru_cache`
- **Testing:** `pytest` (JUnit equivalent), fixtures, mocking (`unittest.mock`), parametrization, coverage

### **Phase 9: Concurrency**

- **AsyncIO:** `async` / `await`, event loop, `asyncio.gather`, async generators
- **`concurrent.futures`:** `ThreadPoolExecutor`, `ProcessPoolExecutor` (ExecutorService equivalent)
- **Threading vs Multiprocessing:** GIL (Global Interpreter Lock) limitations; threads for I/O-bound, processes for CPU-bound
- **Synchronization:** `Lock`, `Queue`, `Event`, `Semaphore`
- **GIL Outlook:** Free-threaded / no-GIL CPython (3.13+ experimental)

> [!tip] See also
> [[Tech/Concurrency/_Roadmap|Concurrency Roadmap]] for the deeper concurrency theory.

---

## Study Priority (for SDE-2 interviews)

### Learn deeply
- Lists / dicts / sets + comprehensions
- `collections`, `heapq`, `bisect` (DSA bread-and-butter)
- Generators, iterators, decorators, closures
- Exception handling + EAFP
- OOP (dunder methods, dataclasses)

### Learn moderately
- `itertools`, `functools`, type hints, pattern matching
- FastAPI + SQLAlchemy basics
- AsyncIO and the GIL

### Just know the basics
- `__slots__`, metaclasses, descriptors
- Packaging internals, no-GIL CPython
