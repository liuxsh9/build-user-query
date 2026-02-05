#!/usr/bin/env python3
"""
Tag Collection Script

Collects capability tags from various sources using LLM assistance.
Outputs collected tags to intermediate JSON format for review.
"""

import argparse
import json
import sys
from pathlib import Path
from typing import List, Dict, Any, Optional
import yaml


def load_taxonomy(taxonomy_path: Path) -> Dict[str, Any]:
    """Load taxonomy definition from YAML file."""
    with open(taxonomy_path, 'r') as f:
        return yaml.safe_load(f)


def collect_language_tags(llm_client: Optional[Any] = None) -> List[Dict[str, Any]]:
    """
    Collect programming language tags from TIOBE/GitHub stats.

    Returns list of tag dictionaries with fields:
    - name: Language name
    - category: "Language"
    - source: Source of the tag
    - aliases: List of alternative names
    """
    print("Collecting Language tags...")

    # Curated list of major programming languages
    # Sources: TIOBE Index, GitHub Language Stats, Stack Overflow Survey
    languages = [
        {"name": "Python", "aliases": ["py", "python3"], "source": "TIOBE"},
        {"name": "JavaScript", "aliases": ["js", "javascript"], "source": "TIOBE"},
        {"name": "TypeScript", "aliases": ["ts", "typescript"], "source": "GitHub"},
        {"name": "Java", "aliases": ["java"], "source": "TIOBE"},
        {"name": "C", "aliases": ["c"], "source": "TIOBE"},
        {"name": "C++", "aliases": ["cpp", "c++", "cxx"], "source": "TIOBE"},
        {"name": "C#", "aliases": ["csharp", "c-sharp"], "source": "TIOBE"},
        {"name": "Go", "aliases": ["golang", "go"], "source": "TIOBE"},
        {"name": "Rust", "aliases": ["rust", "rs"], "source": "GitHub"},
        {"name": "Ruby", "aliases": ["ruby", "rb"], "source": "TIOBE"},
        {"name": "PHP", "aliases": ["php"], "source": "TIOBE"},
        {"name": "Swift", "aliases": ["swift"], "source": "TIOBE"},
        {"name": "Kotlin", "aliases": ["kotlin", "kt"], "source": "TIOBE"},
        {"name": "R", "aliases": ["r", "r-lang"], "source": "TIOBE"},
        {"name": "MATLAB", "aliases": ["matlab"], "source": "TIOBE"},
        {"name": "Perl", "aliases": ["perl", "pl"], "source": "TIOBE"},
        {"name": "Scala", "aliases": ["scala"], "source": "TIOBE"},
        {"name": "Haskell", "aliases": ["haskell", "hs"], "source": "GitHub"},
        {"name": "Lua", "aliases": ["lua"], "source": "TIOBE"},
        {"name": "Dart", "aliases": ["dart"], "source": "GitHub"},
        {"name": "Elixir", "aliases": ["elixir", "ex"], "source": "GitHub"},
        {"name": "Clojure", "aliases": ["clojure", "clj"], "source": "GitHub"},
        {"name": "Erlang", "aliases": ["erlang", "erl"], "source": "TIOBE"},
        {"name": "F#", "aliases": ["fsharp", "f-sharp"], "source": "GitHub"},
        {"name": "OCaml", "aliases": ["ocaml", "ml"], "source": "GitHub"},
        {"name": "Groovy", "aliases": ["groovy"], "source": "TIOBE"},
        {"name": "Julia", "aliases": ["julia", "jl"], "source": "GitHub"},
        {"name": "Zig", "aliases": ["zig"], "source": "GitHub"},
        {"name": "Nim", "aliases": ["nim"], "source": "GitHub"},
        {"name": "Crystal", "aliases": ["crystal", "cr"], "source": "GitHub"},
        {"name": "Objective-C", "aliases": ["objc", "objective-c"], "source": "TIOBE"},
        {"name": "Shell", "aliases": ["bash", "sh", "shell"], "source": "GitHub"},
        {"name": "PowerShell", "aliases": ["powershell", "ps1"], "source": "GitHub"},
        {"name": "SQL", "aliases": ["sql"], "source": "TIOBE"},
        {"name": "HTML", "aliases": ["html"], "source": "GitHub"},
        {"name": "CSS", "aliases": ["css"], "source": "GitHub"},
        {"name": "Solidity", "aliases": ["solidity", "sol"], "source": "GitHub"},
        {"name": "Vyper", "aliases": ["vyper", "vy"], "source": "GitHub"},
        {"name": "COBOL", "aliases": ["cobol"], "source": "TIOBE"},
        {"name": "Fortran", "aliases": ["fortran"], "source": "TIOBE"},
        {"name": "Ada", "aliases": ["ada"], "source": "TIOBE"},
        {"name": "Assembly", "aliases": ["asm", "assembly"], "source": "TIOBE"},
        {"name": "Verilog", "aliases": ["verilog", "v"], "source": "GitHub"},
        {"name": "VHDL", "aliases": ["vhdl"], "source": "GitHub"},
        {"name": "Prolog", "aliases": ["prolog", "pl"], "source": "TIOBE"},
        {"name": "Lisp", "aliases": ["lisp", "common-lisp"], "source": "TIOBE"},
        {"name": "Scheme", "aliases": ["scheme", "scm"], "source": "GitHub"},
        {"name": "Racket", "aliases": ["racket", "rkt"], "source": "GitHub"},
        {"name": "Smalltalk", "aliases": ["smalltalk"], "source": "TIOBE"},
        {"name": "APL", "aliases": ["apl"], "source": "TIOBE"},
    ]

    tags = []
    for lang in languages:
        tags.append({
            "name": lang["name"],
            "category": "Language",
            "source": lang["source"],
            "aliases": lang["aliases"]
        })

    print(f"Collected {len(tags)} Language tags")
    return tags


def collect_library_tags(subcategory: str, llm_client: Optional[Any] = None) -> List[Dict[str, Any]]:
    """
    Collect library/framework tags from awesome-lists and package registries.

    Args:
        subcategory: Library subcategory (Web, Data, Infrastructure, Testing, Database)
        llm_client: Optional LLM client for assisted extraction

    Returns list of tag dictionaries.
    """
    print(f"Collecting Library tags for subcategory: {subcategory}...")

    # Curated library lists by subcategory
    libraries = {
        "Web": [
            {"name": "React", "aliases": ["react", "reactjs"], "language_scope": ["javascript", "typescript"]},
            {"name": "Vue", "aliases": ["vue", "vuejs"], "language_scope": ["javascript", "typescript"]},
            {"name": "Angular", "aliases": ["angular", "angularjs"], "language_scope": ["typescript"]},
            {"name": "Svelte", "aliases": ["svelte"], "language_scope": ["javascript", "typescript"]},
            {"name": "Next.js", "aliases": ["nextjs", "next"], "language_scope": ["javascript", "typescript"]},
            {"name": "Nuxt", "aliases": ["nuxt", "nuxtjs"], "language_scope": ["javascript", "typescript"]},
            {"name": "Express", "aliases": ["express", "expressjs"], "language_scope": ["javascript", "typescript"]},
            {"name": "FastAPI", "aliases": ["fastapi"], "language_scope": ["python"]},
            {"name": "Django", "aliases": ["django"], "language_scope": ["python"]},
            {"name": "Flask", "aliases": ["flask"], "language_scope": ["python"]},
            {"name": "Spring Boot", "aliases": ["spring-boot", "spring"], "language_scope": ["java"]},
            {"name": "Ruby on Rails", "aliases": ["rails", "ror"], "language_scope": ["ruby"]},
            {"name": "Laravel", "aliases": ["laravel"], "language_scope": ["php"]},
            {"name": "ASP.NET", "aliases": ["aspnet", "asp-net"], "language_scope": ["csharp"]},
            {"name": "Gin", "aliases": ["gin"], "language_scope": ["go"]},
            {"name": "Echo", "aliases": ["echo"], "language_scope": ["go"]},
            {"name": "Actix", "aliases": ["actix", "actix-web"], "language_scope": ["rust"]},
            {"name": "Axum", "aliases": ["axum"], "language_scope": ["rust"]},
            {"name": "Rocket", "aliases": ["rocket"], "language_scope": ["rust"]},
            {"name": "Phoenix", "aliases": ["phoenix"], "language_scope": ["elixir"]},
            {"name": "Tailwind CSS", "aliases": ["tailwind", "tailwindcss"], "language_scope": ["css"]},
            {"name": "Bootstrap", "aliases": ["bootstrap"], "language_scope": ["css"]},
            {"name": "Material-UI", "aliases": ["mui", "material-ui"], "language_scope": ["javascript", "typescript"]},
            {"name": "Ant Design", "aliases": ["antd", "ant-design"], "language_scope": ["javascript", "typescript"]},
        ],
        "Data": [
            {"name": "Pandas", "aliases": ["pandas", "pd"], "language_scope": ["python"]},
            {"name": "NumPy", "aliases": ["numpy", "np"], "language_scope": ["python"]},
            {"name": "PyTorch", "aliases": ["pytorch", "torch"], "language_scope": ["python"]},
            {"name": "TensorFlow", "aliases": ["tensorflow", "tf"], "language_scope": ["python"]},
            {"name": "Scikit-learn", "aliases": ["sklearn", "scikit-learn"], "language_scope": ["python"]},
            {"name": "Matplotlib", "aliases": ["matplotlib", "plt"], "language_scope": ["python"]},
            {"name": "Seaborn", "aliases": ["seaborn", "sns"], "language_scope": ["python"]},
            {"name": "Plotly", "aliases": ["plotly"], "language_scope": ["python", "javascript"]},
            {"name": "Polars", "aliases": ["polars"], "language_scope": ["python", "rust"]},
            {"name": "Dask", "aliases": ["dask"], "language_scope": ["python"]},
            {"name": "Ray", "aliases": ["ray"], "language_scope": ["python"]},
            {"name": "Apache Spark", "aliases": ["spark", "pyspark"], "language_scope": ["python", "scala", "java"]},
            {"name": "Hugging Face Transformers", "aliases": ["transformers", "huggingface"], "language_scope": ["python"]},
            {"name": "LangChain", "aliases": ["langchain"], "language_scope": ["python"]},
            {"name": "OpenCV", "aliases": ["opencv", "cv2"], "language_scope": ["python", "cpp"]},
            {"name": "NLTK", "aliases": ["nltk"], "language_scope": ["python"]},
            {"name": "spaCy", "aliases": ["spacy"], "language_scope": ["python"]},
        ],
        "Infrastructure": [
            {"name": "Docker", "aliases": ["docker"], "language_scope": []},
            {"name": "Kubernetes", "aliases": ["k8s", "kubernetes"], "language_scope": []},
            {"name": "Terraform", "aliases": ["terraform", "tf"], "language_scope": ["hcl"]},
            {"name": "Ansible", "aliases": ["ansible"], "language_scope": ["yaml"]},
            {"name": "Helm", "aliases": ["helm"], "language_scope": []},
            {"name": "AWS CDK", "aliases": ["cdk", "aws-cdk"], "language_scope": ["typescript", "python"]},
            {"name": "Pulumi", "aliases": ["pulumi"], "language_scope": ["typescript", "python", "go"]},
            {"name": "GitHub Actions", "aliases": ["github-actions", "gha"], "language_scope": ["yaml"]},
            {"name": "GitLab CI", "aliases": ["gitlab-ci"], "language_scope": ["yaml"]},
            {"name": "Jenkins", "aliases": ["jenkins"], "language_scope": []},
            {"name": "CircleCI", "aliases": ["circleci"], "language_scope": ["yaml"]},
            {"name": "Prometheus", "aliases": ["prometheus"], "language_scope": []},
            {"name": "Grafana", "aliases": ["grafana"], "language_scope": []},
            {"name": "Nginx", "aliases": ["nginx"], "language_scope": []},
            {"name": "Apache", "aliases": ["apache", "httpd"], "language_scope": []},
            {"name": "Redis", "aliases": ["redis"], "language_scope": []},
            {"name": "RabbitMQ", "aliases": ["rabbitmq"], "language_scope": []},
            {"name": "Kafka", "aliases": ["kafka"], "language_scope": []},
        ],
        "Testing": [
            {"name": "Pytest", "aliases": ["pytest"], "language_scope": ["python"]},
            {"name": "unittest", "aliases": ["unittest"], "language_scope": ["python"]},
            {"name": "Jest", "aliases": ["jest"], "language_scope": ["javascript", "typescript"]},
            {"name": "Vitest", "aliases": ["vitest"], "language_scope": ["javascript", "typescript"]},
            {"name": "Mocha", "aliases": ["mocha"], "language_scope": ["javascript"]},
            {"name": "Chai", "aliases": ["chai"], "language_scope": ["javascript"]},
            {"name": "Cypress", "aliases": ["cypress"], "language_scope": ["javascript", "typescript"]},
            {"name": "Playwright", "aliases": ["playwright"], "language_scope": ["javascript", "typescript", "python"]},
            {"name": "Selenium", "aliases": ["selenium"], "language_scope": ["python", "java", "javascript"]},
            {"name": "JUnit", "aliases": ["junit"], "language_scope": ["java"]},
            {"name": "TestNG", "aliases": ["testng"], "language_scope": ["java"]},
            {"name": "RSpec", "aliases": ["rspec"], "language_scope": ["ruby"]},
            {"name": "Mockito", "aliases": ["mockito"], "language_scope": ["java"]},
            {"name": "Mock", "aliases": ["mock", "unittest.mock"], "language_scope": ["python"]},
        ],
        "Database": [
            {"name": "SQLAlchemy", "aliases": ["sqlalchemy"], "language_scope": ["python"]},
            {"name": "Prisma", "aliases": ["prisma"], "language_scope": ["typescript", "javascript"]},
            {"name": "TypeORM", "aliases": ["typeorm"], "language_scope": ["typescript"]},
            {"name": "Sequelize", "aliases": ["sequelize"], "language_scope": ["javascript", "typescript"]},
            {"name": "Hibernate", "aliases": ["hibernate"], "language_scope": ["java"]},
            {"name": "Diesel", "aliases": ["diesel"], "language_scope": ["rust"]},
            {"name": "GORM", "aliases": ["gorm"], "language_scope": ["go"]},
            {"name": "Mongoose", "aliases": ["mongoose"], "language_scope": ["javascript", "typescript"]},
            {"name": "psycopg2", "aliases": ["psycopg2"], "language_scope": ["python"]},
            {"name": "PyMongo", "aliases": ["pymongo"], "language_scope": ["python"]},
            {"name": "Redis-py", "aliases": ["redis-py"], "language_scope": ["python"]},
            {"name": "Alembic", "aliases": ["alembic"], "language_scope": ["python"]},
        ]
    }

    if subcategory not in libraries:
        print(f"Warning: Unknown subcategory '{subcategory}'")
        return []

    tags = []
    for lib in libraries[subcategory]:
        tags.append({
            "name": lib["name"],
            "category": "Library",
            "subcategory": subcategory,
            "source": "curated-list",
            "aliases": lib["aliases"],
            "language_scope": lib.get("language_scope", [])
        })

    print(f"Collected {len(tags)} Library tags for {subcategory}")
    return tags


def collect_concept_tags(subcategory: str, llm_client: Optional[Any] = None) -> List[Dict[str, Any]]:
    """
    Collect programming concept tags from educational sources.

    Args:
        subcategory: Concept subcategory (Fundamentals, Advanced, Engineering)
        llm_client: Optional LLM client for assisted extraction

    Returns list of tag dictionaries.
    """
    print(f"Collecting Concept tags for subcategory: {subcategory}...")

    concepts = {
        "Fundamentals": [
            {"name": "Variables", "difficulty": "basic"},
            {"name": "Data Types", "difficulty": "basic"},
            {"name": "Control Flow", "difficulty": "basic"},
            {"name": "Loops", "difficulty": "basic"},
            {"name": "Functions", "difficulty": "basic"},
            {"name": "Arrays", "difficulty": "basic"},
            {"name": "Strings", "difficulty": "basic"},
            {"name": "Conditionals", "difficulty": "basic"},
            {"name": "Input/Output", "difficulty": "basic"},
            {"name": "Comments", "difficulty": "basic"},
            {"name": "Operators", "difficulty": "basic"},
            {"name": "Scope", "difficulty": "basic"},
            {"name": "Recursion", "difficulty": "intermediate"},
            {"name": "Object-Oriented Programming", "difficulty": "intermediate", "aliases": ["oop"]},
            {"name": "Classes", "difficulty": "intermediate"},
            {"name": "Inheritance", "difficulty": "intermediate"},
            {"name": "Polymorphism", "difficulty": "intermediate"},
            {"name": "Encapsulation", "difficulty": "intermediate"},
            {"name": "Functional Programming", "difficulty": "intermediate", "aliases": ["fp"]},
            {"name": "Lambda Functions", "difficulty": "intermediate"},
            {"name": "Higher-Order Functions", "difficulty": "intermediate"},
            {"name": "Closures", "difficulty": "intermediate"},
        ],
        "Advanced": [
            {"name": "Concurrency", "difficulty": "advanced"},
            {"name": "Parallelism", "difficulty": "advanced"},
            {"name": "Async/Await", "difficulty": "advanced", "aliases": ["asynchronous"]},
            {"name": "Threads", "difficulty": "advanced"},
            {"name": "Processes", "difficulty": "advanced"},
            {"name": "Coroutines", "difficulty": "advanced"},
            {"name": "Memory Management", "difficulty": "advanced"},
            {"name": "Garbage Collection", "difficulty": "advanced"},
            {"name": "Pointers", "difficulty": "advanced", "language_scope": ["c", "cpp"]},
            {"name": "References", "difficulty": "advanced"},
            {"name": "Borrow Checker", "difficulty": "advanced", "language_scope": ["rust"]},
            {"name": "Lifetimes", "difficulty": "advanced", "language_scope": ["rust"]},
            {"name": "Ownership", "difficulty": "advanced", "language_scope": ["rust"]},
            {"name": "Type System", "difficulty": "advanced"},
            {"name": "Generics", "difficulty": "advanced"},
            {"name": "Type Inference", "difficulty": "advanced"},
            {"name": "Traits", "difficulty": "advanced", "language_scope": ["rust"]},
            {"name": "Interfaces", "difficulty": "advanced"},
            {"name": "Abstract Classes", "difficulty": "advanced"},
            {"name": "Metaprogramming", "difficulty": "advanced"},
            {"name": "Macros", "difficulty": "advanced"},
            {"name": "Reflection", "difficulty": "advanced"},
            {"name": "Decorators", "difficulty": "advanced", "language_scope": ["python"]},
            {"name": "Generators", "difficulty": "advanced"},
            {"name": "Iterators", "difficulty": "advanced"},
            {"name": "Streams", "difficulty": "advanced"},
            {"name": "Error Handling", "difficulty": "intermediate"},
            {"name": "Exception Handling", "difficulty": "intermediate"},
            {"name": "Result Types", "difficulty": "intermediate"},
            {"name": "Option Types", "difficulty": "intermediate"},
        ],
        "Engineering": [
            {"name": "Design Patterns", "difficulty": "advanced"},
            {"name": "Singleton Pattern", "difficulty": "intermediate"},
            {"name": "Factory Pattern", "difficulty": "intermediate"},
            {"name": "Observer Pattern", "difficulty": "intermediate"},
            {"name": "Strategy Pattern", "difficulty": "intermediate"},
            {"name": "Dependency Injection", "difficulty": "advanced"},
            {"name": "SOLID Principles", "difficulty": "advanced"},
            {"name": "Testing", "difficulty": "intermediate"},
            {"name": "Unit Testing", "difficulty": "intermediate"},
            {"name": "Integration Testing", "difficulty": "intermediate"},
            {"name": "Test-Driven Development", "difficulty": "advanced", "aliases": ["tdd"]},
            {"name": "Mocking", "difficulty": "intermediate"},
            {"name": "Code Coverage", "difficulty": "intermediate"},
            {"name": "Refactoring", "difficulty": "intermediate"},
            {"name": "Code Review", "difficulty": "intermediate"},
            {"name": "Version Control", "difficulty": "basic"},
            {"name": "Git", "difficulty": "intermediate"},
            {"name": "Branching Strategies", "difficulty": "intermediate"},
            {"name": "CI/CD", "difficulty": "advanced"},
            {"name": "Documentation", "difficulty": "basic"},
            {"name": "API Design", "difficulty": "advanced"},
            {"name": "REST API", "difficulty": "intermediate"},
            {"name": "GraphQL", "difficulty": "advanced"},
            {"name": "Microservices", "difficulty": "advanced"},
            {"name": "Monolithic Architecture", "difficulty": "intermediate"},
            {"name": "Event-Driven Architecture", "difficulty": "advanced"},
            {"name": "CQRS", "difficulty": "advanced"},
            {"name": "Database Design", "difficulty": "intermediate"},
            {"name": "Normalization", "difficulty": "intermediate"},
            {"name": "Indexing", "difficulty": "intermediate"},
            {"name": "Transactions", "difficulty": "intermediate"},
            {"name": "ACID Properties", "difficulty": "intermediate"},
            {"name": "CAP Theorem", "difficulty": "advanced"},
            {"name": "Security", "difficulty": "advanced"},
            {"name": "Authentication", "difficulty": "intermediate"},
            {"name": "Authorization", "difficulty": "intermediate"},
            {"name": "Encryption", "difficulty": "intermediate"},
            {"name": "SQL Injection", "difficulty": "intermediate"},
            {"name": "XSS", "difficulty": "intermediate"},
            {"name": "CSRF", "difficulty": "intermediate"},
            {"name": "Performance Optimization", "difficulty": "advanced"},
            {"name": "Caching", "difficulty": "intermediate"},
            {"name": "Load Balancing", "difficulty": "advanced"},
            {"name": "Profiling", "difficulty": "intermediate"},
        ]
    }

    if subcategory not in concepts:
        print(f"Warning: Unknown subcategory '{subcategory}'")
        return []

    tags = []
    for concept in concepts[subcategory]:
        tag = {
            "name": concept["name"],
            "category": "Concept",
            "subcategory": subcategory,
            "source": "educational-sources",
            "difficulty": concept["difficulty"]
        }
        if "aliases" in concept:
            tag["aliases"] = concept["aliases"]
        if "language_scope" in concept:
            tag["language_scope"] = concept["language_scope"]
        tags.append(tag)

    print(f"Collected {len(tags)} Concept tags for {subcategory}")
    return tags


def collect_domain_tags(llm_client: Optional[Any] = None) -> List[Dict[str, Any]]:
    """Collect application domain tags."""
    print("Collecting Domain tags...")

    domains = [
        {"name": "Web Backend", "aliases": ["backend", "server-side"]},
        {"name": "Web Frontend", "aliases": ["frontend", "client-side"]},
        {"name": "Full Stack", "aliases": ["fullstack"]},
        {"name": "Mobile Development", "aliases": ["mobile", "mobile-dev"]},
        {"name": "Desktop Application", "aliases": ["desktop", "desktop-app"]},
        {"name": "CLI Tool", "aliases": ["cli", "command-line"]},
        {"name": "Data Science", "aliases": ["data-science", "ds"]},
        {"name": "Machine Learning", "aliases": ["ml", "machine-learning"]},
        {"name": "Deep Learning", "aliases": ["dl", "deep-learning"]},
        {"name": "DevOps", "aliases": ["devops"]},
        {"name": "Cloud Computing", "aliases": ["cloud"]},
        {"name": "Embedded Systems", "aliases": ["embedded"]},
        {"name": "IoT", "aliases": ["iot", "internet-of-things"]},
        {"name": "Game Development", "aliases": ["gamedev", "game-dev"]},
        {"name": "Blockchain", "aliases": ["blockchain", "web3"]},
        {"name": "Smart Contracts", "aliases": ["smart-contracts"]},
        {"name": "Cybersecurity", "aliases": ["security", "infosec"]},
        {"name": "Network Programming", "aliases": ["networking"]},
        {"name": "Systems Programming", "aliases": ["systems"]},
        {"name": "Compiler Development", "aliases": ["compilers"]},
        {"name": "Operating Systems", "aliases": ["os"]},
        {"name": "Database Administration", "aliases": ["dba"]},
        {"name": "ETL", "aliases": ["etl", "data-pipeline"]},
        {"name": "API Development", "aliases": ["api"]},
        {"name": "Automation", "aliases": ["automation", "scripting"]},
        {"name": "Scientific Computing", "aliases": ["scientific"]},
        {"name": "Computer Vision", "aliases": ["cv", "computer-vision"]},
        {"name": "Natural Language Processing", "aliases": ["nlp"]},
        {"name": "Robotics", "aliases": ["robotics"]},
        {"name": "Financial Technology", "aliases": ["fintech"]},
        {"name": "Healthcare Technology", "aliases": ["healthtech"]},
        {"name": "E-commerce", "aliases": ["ecommerce"]},
    ]

    tags = []
    for domain in domains:
        tags.append({
            "name": domain["name"],
            "category": "Domain",
            "source": "curated-list",
            "aliases": domain["aliases"]
        })

    print(f"Collected {len(tags)} Domain tags")
    return tags


def collect_task_tags(llm_client: Optional[Any] = None) -> List[Dict[str, Any]]:
    """Collect task type tags."""
    print("Collecting Task tags...")

    tasks = [
        {"name": "Code Generation", "aliases": ["generation", "code-gen"]},
        {"name": "Code Completion", "aliases": ["completion", "autocomplete"]},
        {"name": "Code Translation", "aliases": ["translation", "transpilation"]},
        {"name": "Code Refactoring", "aliases": ["refactoring", "refactor"]},
        {"name": "Debugging", "aliases": ["debug", "bug-fix"]},
        {"name": "Code Review", "aliases": ["review"]},
        {"name": "Test Generation", "aliases": ["test-gen", "testing"]},
        {"name": "Documentation", "aliases": ["docs", "documentation"]},
        {"name": "Code Explanation", "aliases": ["explanation", "explain"]},
        {"name": "Code Optimization", "aliases": ["optimization", "optimize"]},
        {"name": "Migration", "aliases": ["migration", "upgrade"]},
        {"name": "API Design", "aliases": ["api-design"]},
        {"name": "Schema Design", "aliases": ["schema-design", "data-modeling"]},
        {"name": "Configuration", "aliases": ["config", "configuration"]},
        {"name": "Deployment", "aliases": ["deploy", "deployment"]},
        {"name": "Monitoring", "aliases": ["monitoring", "observability"]},
        {"name": "Performance Analysis", "aliases": ["profiling", "performance"]},
        {"name": "Security Audit", "aliases": ["security-audit", "vulnerability-scan"]},
        {"name": "Code Search", "aliases": ["search", "code-search"]},
        {"name": "Dependency Management", "aliases": ["dependencies"]},
    ]

    tags = []
    for task in tasks:
        tags.append({
            "name": task["name"],
            "category": "Task",
            "source": "curated-list",
            "aliases": task["aliases"]
        })

    print(f"Collected {len(tags)} Task tags")
    return tags


def collect_constraint_tags(llm_client: Optional[Any] = None) -> List[Dict[str, Any]]:
    """Collect constraint tags."""
    print("Collecting Constraint tags...")

    constraints = [
        {"name": "High Performance", "aliases": ["performance", "fast"]},
        {"name": "Low Latency", "aliases": ["low-latency", "real-time"]},
        {"name": "Memory Efficient", "aliases": ["memory-efficient", "low-memory"]},
        {"name": "Thread Safe", "aliases": ["thread-safe", "concurrency-safe"]},
        {"name": "Type Safe", "aliases": ["type-safe", "strongly-typed"]},
        {"name": "Secure", "aliases": ["security", "secure"]},
        {"name": "HIPAA Compliant", "aliases": ["hipaa"]},
        {"name": "GDPR Compliant", "aliases": ["gdpr"]},
        {"name": "PCI-DSS Compliant", "aliases": ["pci-dss"]},
        {"name": "MISRA C Compliant", "aliases": ["misra-c"]},
        {"name": "Readable", "aliases": ["readability", "clean-code"]},
        {"name": "Maintainable", "aliases": ["maintainability"]},
        {"name": "Testable", "aliases": ["testability"]},
        {"name": "Scalable", "aliases": ["scalability"]},
        {"name": "Portable", "aliases": ["portability", "cross-platform"]},
        {"name": "Backward Compatible", "aliases": ["backward-compatibility"]},
        {"name": "No External Dependencies", "aliases": ["no-deps", "zero-dependencies"]},
        {"name": "No Dynamic Allocation", "aliases": ["no-malloc", "static-memory"]},
        {"name": "No Recursion", "aliases": ["no-recursion"]},
        {"name": "Gas Optimized", "aliases": ["gas-optimization"], "language_scope": ["solidity"]},
        {"name": "Deterministic", "aliases": ["deterministic"]},
        {"name": "Idempotent", "aliases": ["idempotent"]},
        {"name": "Fault Tolerant", "aliases": ["fault-tolerance"]},
        {"name": "Accessible", "aliases": ["accessibility", "a11y"]},
        {"name": "Internationalized", "aliases": ["i18n", "internationalization"]},
    ]

    tags = []
    for constraint in constraints:
        tag = {
            "name": constraint["name"],
            "category": "Constraint",
            "source": "curated-list",
            "aliases": constraint["aliases"]
        }
        if "language_scope" in constraint:
            tag["language_scope"] = constraint["language_scope"]
        tags.append(tag)

    print(f"Collected {len(tags)} Constraint tags")
    return tags


def collect_agentic_tags(llm_client: Optional[Any] = None) -> List[Dict[str, Any]]:
    """Collect agentic capability tags."""
    print("Collecting Agentic tags...")

    agentic = [
        {"name": "Bash Execution", "aliases": ["bash", "shell", "command-execution"]},
        {"name": "File Read", "aliases": ["read-file", "file-reading"]},
        {"name": "File Write", "aliases": ["write-file", "file-writing"]},
        {"name": "File Edit", "aliases": ["edit-file", "file-editing"]},
        {"name": "Code Search", "aliases": ["search-code", "grep"]},
        {"name": "File Navigation", "aliases": ["navigate", "file-tree"]},
        {"name": "Multi-step Reasoning", "aliases": ["reasoning", "planning"]},
        {"name": "Tool Selection", "aliases": ["tool-use", "tool-calling"]},
        {"name": "Error Recovery", "aliases": ["error-handling", "retry"]},
        {"name": "Context Management", "aliases": ["context", "memory"]},
        {"name": "Web Search", "aliases": ["search", "web-search"]},
        {"name": "API Calling", "aliases": ["api-call", "http-request"]},
        {"name": "Database Query", "aliases": ["db-query", "sql-execution"]},
        {"name": "Code Execution", "aliases": ["execute-code", "run-code"]},
        {"name": "Test Running", "aliases": ["run-tests", "test-execution"]},
        {"name": "Build Execution", "aliases": ["build", "compile"]},
        {"name": "Dependency Installation", "aliases": ["install-deps", "package-install"]},
        {"name": "Git Operations", "aliases": ["git", "version-control"]},
        {"name": "Multi-file Coordination", "aliases": ["multi-file", "cross-file"]},
        {"name": "Iterative Refinement", "aliases": ["iteration", "refinement"]},
    ]

    tags = []
    for agent in agentic:
        tags.append({
            "name": agent["name"],
            "category": "Agentic",
            "source": "curated-list",
            "aliases": agent["aliases"]
        })

    print(f"Collected {len(tags)} Agentic tags")
    return tags


def collect_context_tags(llm_client: Optional[Any] = None) -> List[Dict[str, Any]]:
    """Collect context complexity tags."""
    print("Collecting Context tags...")

    contexts = [
        {"name": "Single Function", "aliases": ["function", "single-function"]},
        {"name": "Single File", "aliases": ["file", "single-file"]},
        {"name": "Multi-file", "aliases": ["multiple-files", "cross-file"]},
        {"name": "Module", "aliases": ["module", "package"]},
        {"name": "Repository", "aliases": ["repo", "repository-level", "codebase"]},
        {"name": "Monorepo", "aliases": ["monorepo", "multi-project"]},
        {"name": "With Dependencies", "aliases": ["with-deps", "external-deps"]},
        {"name": "Legacy Code", "aliases": ["legacy", "brownfield"]},
        {"name": "Greenfield", "aliases": ["greenfield", "new-project"]},
    ]

    tags = []
    for context in contexts:
        tags.append({
            "name": context["name"],
            "category": "Context",
            "source": "curated-list",
            "aliases": context["aliases"]
        })

    print(f"Collected {len(tags)} Context tags")
    return tags


def save_collected_tags(tags: List[Dict[str, Any]], output_path: Path):
    """Save collected tags to JSON file."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, 'w') as f:
        json.dump(tags, f, indent=2, ensure_ascii=False)
    print(f"Saved {len(tags)} tags to {output_path}")


def main():
    parser = argparse.ArgumentParser(
        description="Collect capability tags from various sources"
    )
    parser.add_argument(
        '--category',
        required=True,
        choices=['Language', 'Library', 'Domain', 'Concept', 'Task', 'Constraint', 'Agentic', 'Context'],
        help='Category to collect tags for'
    )
    parser.add_argument(
        '--subcategory',
        help='Subcategory (for Library and Concept categories)'
    )
    parser.add_argument(
        '--output',
        type=Path,
        default=Path('collected_tags.json'),
        help='Output JSON file path'
    )
    parser.add_argument(
        '--taxonomy',
        type=Path,
        default=Path('taxonomy.yaml'),
        help='Path to taxonomy.yaml'
    )
    parser.add_argument(
        '--use-llm',
        action='store_true',
        help='Use LLM for assisted extraction'
    )

    args = parser.parse_args()

    # Load taxonomy
    taxonomy = load_taxonomy(args.taxonomy)

    # Initialize LLM client if requested
    llm_client = None
    if args.use_llm:
        # TODO: Initialize LLM client
        print("LLM-assisted extraction not yet implemented")

    # Collect tags based on category
    collected_tags = []

    if args.category == 'Language':
        collected_tags = collect_language_tags(llm_client)
    elif args.category == 'Library':
        if not args.subcategory:
            print("Error: --subcategory required for Library category")
            sys.exit(1)
        collected_tags = collect_library_tags(args.subcategory, llm_client)
    elif args.category == 'Concept':
        if not args.subcategory:
            print("Error: --subcategory required for Concept category")
            sys.exit(1)
        collected_tags = collect_concept_tags(args.subcategory, llm_client)
    elif args.category == 'Domain':
        collected_tags = collect_domain_tags(llm_client)
    elif args.category == 'Task':
        collected_tags = collect_task_tags(llm_client)
    elif args.category == 'Constraint':
        collected_tags = collect_constraint_tags(llm_client)
    elif args.category == 'Agentic':
        collected_tags = collect_agentic_tags(llm_client)
    elif args.category == 'Context':
        collected_tags = collect_context_tags(llm_client)

    # Save collected tags
    save_collected_tags(collected_tags, args.output)

    print(f"\nCollection complete. Review tags in {args.output}")
    print("Next step: Run normalize_tags.py to process collected tags")


if __name__ == '__main__':
    main()
