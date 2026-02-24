#!/usr/bin/env python3
"""
Library/Framework Extraction from Trajectory Code Snippets
===========================================================

Purpose:
    Auto-extract library and framework information from code found in trajectory
    data (ShareGPT-format SFT conversations). This replaces the deleted "Library"
    taxonomy dimension (339 tags, library.yaml.removed) with a runtime extraction
    approach that derives library signals directly from code.

Approach:
    Regex-based parsing of import/require/using statements across 7+ languages.
    We deliberately avoid AST-based parsing because:
    1. Trajectory data contains code snippets, not compilable source files.
    2. Snippets may be incomplete, have syntax errors, or be mixed with prose.
    3. Regex is fast enough for the ~3M records at annotation scale.
    4. Import statements have highly regular syntax within each language.

Supported Languages:
    - Python:      import X, from X import Y, from X.Y import Z
    - JavaScript/TypeScript: import ... from 'X', require('X'), import('X')
    - Go:          import "X", import ( "X" )
    - Rust:        use X::Y, extern crate X
    - Java:        import X.Y.Z
    - Ruby:        require 'X', gem 'X', require_relative 'X'
    - C#:          using X.Y

Normalization:
    Raw extracted names are mapped to canonical library names via:
    1. A hand-curated alias table (e.g., "np" -> "numpy", "pd" -> "pandas").
    2. Scope/prefix stripping (e.g., "@types/react" -> "react").
    3. Go module path reduction (e.g., "github.com/gin-gonic/gin" -> "gin").
    4. Java package root extraction (e.g., "org.springframework.boot" -> "spring-boot").

Output:
    JSON or YAML with per-snippet library detections:
    {
        "file": "<source>",
        "libraries": [
            {"name": "numpy", "raw": "np", "language": "python", "line": "import numpy as np"},
            ...
        ]
    }

Limitations:
    - Cannot detect libraries used without import statements (e.g., vendored code,
      monkey-patching, runtime reflection).
    - Alias table is manually maintained; novel aliases will pass through unnormalized.
    - Does not distinguish between standard library and third-party modules (e.g.,
      Python's "os" will be extracted the same as "numpy"). Downstream filtering
      against a known-stdlib list is recommended.
    - Dynamic imports constructed via string concatenation are not detected.
    - May produce false positives from commented-out imports (we strip single-line
      comments but not all multi-line comment forms).
    - Rust `use` can refer to internal modules, not just external crates.

Integration:
    Designed to feed into the annotation pipeline's feature vector preprocessing
    (see design.md Decision 1: "import_statements" feature). Output can be matched
    against the former Library tag IDs for backward compatibility.
"""

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple

try:
    import yaml
    HAS_YAML = True
except ImportError:
    HAS_YAML = False


# ---------------------------------------------------------------------------
# Normalization tables
# ---------------------------------------------------------------------------

# Common import aliases -> canonical library name
IMPORT_ALIASES: Dict[str, str] = {
    # Python
    "np": "numpy",
    "pd": "pandas",
    "plt": "matplotlib",
    "sns": "seaborn",
    "tf": "tensorflow",
    "sk": "scikit-learn",
    "sklearn": "scikit-learn",
    "cv2": "opencv",
    "cv": "opencv",
    "PIL": "pillow",
    "bs4": "beautifulsoup4",
    "wx": "wxpython",
    "gi": "pygobject",
    "yaml": "pyyaml",
    "lxml": "lxml",
    "mpl": "matplotlib",
    "mpl_toolkits": "matplotlib",
    "scipy": "scipy",
    "sp": "scipy",
    "nx": "networkx",
    "xr": "xarray",
    "dask": "dask",
    "sympy": "sympy",
    "boto3": "boto3",
    "botocore": "boto3",
    # JavaScript / TypeScript
    "React": "react",
    "ReactDOM": "react-dom",
    "Vue": "vue",
    "Vuex": "vuex",
    "express": "express",
    "axios": "axios",
    "lodash": "lodash",
    "_": "lodash",
    "$": "jquery",
    "jQuery": "jquery",
    "moment": "moment",
    "dayjs": "dayjs",
    "d3": "d3",
    "THREE": "three",
    "Phaser": "phaser",
    "Rx": "rxjs",
    "rxjs": "rxjs",
    "ng": "angular",
    "Ember": "ember",
    # Go
    "fmt": "go-stdlib",
    "net": "go-stdlib",
    "os": "go-stdlib",
    "io": "go-stdlib",
    "gin": "gin",
    "echo": "echo",
    "mux": "gorilla-mux",
    "gorm": "gorm",
    "chi": "chi",
    "fiber": "fiber",
    "zap": "zap",
    "logrus": "logrus",
    "cobra": "cobra",
    "viper": "viper",
    "testify": "testify",
    # Rust
    "serde": "serde",
    "tokio": "tokio",
    "actix": "actix",
    "reqwest": "reqwest",
    "clap": "clap",
    "diesel": "diesel",
    "rocket": "rocket",
    "hyper": "hyper",
    "warp": "warp",
    "axum": "axum",
    "anyhow": "anyhow",
    "thiserror": "thiserror",
    "tracing": "tracing",
    "rayon": "rayon",
    # Ruby
    "rails": "rails",
    "sinatra": "sinatra",
    "rspec": "rspec",
    "nokogiri": "nokogiri",
    "devise": "devise",
    "sidekiq": "sidekiq",
    "puma": "puma",
    "capybara": "capybara",
    "faraday": "faraday",
    "httparty": "httparty",
    "activerecord": "activerecord",
    "active_record": "activerecord",
    # Java
    "springframework": "spring",
    "spring": "spring",
    "junit": "junit",
    "mockito": "mockito",
    "hibernate": "hibernate",
    "lombok": "lombok",
    "jackson": "jackson",
    "guava": "guava",
    "slf4j": "slf4j",
    "log4j": "log4j",
    "netty": "netty",
    "okhttp": "okhttp3",
    # C#
    "Newtonsoft": "newtonsoft-json",
    "NUnit": "nunit",
    "xUnit": "xunit",
    "Moq": "moq",
    "Dapper": "dapper",
    "Serilog": "serilog",
    "AutoMapper": "automapper",
    "MediatR": "mediatr",
    "FluentValidation": "fluentvalidation",
}

# JavaScript scoped package normalization: @scope/name -> canonical
JS_SCOPED_PACKAGE_MAP: Dict[str, str] = {
    "@types/react": "react",
    "@types/node": "node",
    "@types/jest": "jest",
    "@types/express": "express",
    "@types/lodash": "lodash",
    "@angular/core": "angular",
    "@angular/common": "angular",
    "@angular/router": "angular",
    "@angular/forms": "angular",
    "@angular/http": "angular",
    "@angular/material": "angular-material",
    "@vue/cli": "vue",
    "@vue/composition-api": "vue",
    "@nestjs/core": "nestjs",
    "@nestjs/common": "nestjs",
    "@nestjs/testing": "nestjs",
    "@emotion/react": "emotion",
    "@emotion/styled": "emotion",
    "@mui/material": "material-ui",
    "@mui/icons-material": "material-ui",
    "@reduxjs/toolkit": "redux-toolkit",
    "@testing-library/react": "testing-library",
    "@testing-library/jest-dom": "testing-library",
    "@testing-library/user-event": "testing-library",
    "@prisma/client": "prisma",
    "@trpc/server": "trpc",
    "@trpc/client": "trpc",
    "@tanstack/react-query": "react-query",
    "@tanstack/react-table": "tanstack-table",
    "@hookform/resolvers": "react-hook-form",
    "@storybook/react": "storybook",
    "@babel/core": "babel",
    "@babel/preset-env": "babel",
    "@babel/preset-react": "babel",
    "@babel/preset-typescript": "babel",
    "@rollup/plugin-node-resolve": "rollup",
    "@sveltejs/kit": "sveltekit",
    "@supabase/supabase-js": "supabase",
    "@aws-sdk/client-s3": "aws-sdk",
    "@aws-sdk/client-dynamodb": "aws-sdk",
    "@google-cloud/storage": "google-cloud",
    "@google-cloud/firestore": "google-cloud",
    "@azure/storage-blob": "azure-sdk",
}

# Go module path -> canonical library name
GO_MODULE_MAP: Dict[str, str] = {
    "github.com/gin-gonic/gin": "gin",
    "github.com/labstack/echo": "echo",
    "github.com/gorilla/mux": "gorilla-mux",
    "github.com/gorilla/websocket": "gorilla-websocket",
    "github.com/go-chi/chi": "chi",
    "github.com/gofiber/fiber": "fiber",
    "github.com/stretchr/testify": "testify",
    "github.com/sirupsen/logrus": "logrus",
    "go.uber.org/zap": "zap",
    "github.com/spf13/cobra": "cobra",
    "github.com/spf13/viper": "viper",
    "gorm.io/gorm": "gorm",
    "github.com/jmoiron/sqlx": "sqlx",
    "github.com/lib/pq": "lib-pq",
    "github.com/go-redis/redis": "go-redis",
    "github.com/go-sql-driver/mysql": "go-mysql",
    "google.golang.org/grpc": "grpc-go",
    "google.golang.org/protobuf": "protobuf-go",
    "github.com/dgrijalva/jwt-go": "jwt-go",
    "github.com/golang-jwt/jwt": "jwt-go",
    "github.com/prometheus/client_golang": "prometheus-go",
    "github.com/aws/aws-sdk-go": "aws-sdk-go",
    "k8s.io/client-go": "client-go",
    "github.com/hashicorp/terraform": "terraform",
    "github.com/docker/docker": "docker-go",
}

# Java package prefixes -> canonical library name
JAVA_PACKAGE_MAP: Dict[str, str] = {
    "org.springframework": "spring",
    "org.springframework.boot": "spring-boot",
    "org.springframework.data": "spring-data",
    "org.springframework.security": "spring-security",
    "org.springframework.web": "spring-web",
    "org.junit": "junit",
    "org.mockito": "mockito",
    "org.hibernate": "hibernate",
    "org.apache.commons": "apache-commons",
    "org.apache.kafka": "kafka",
    "org.apache.spark": "spark",
    "org.apache.flink": "flink",
    "org.apache.hadoop": "hadoop",
    "org.apache.logging.log4j": "log4j",
    "org.slf4j": "slf4j",
    "com.google.common": "guava",
    "com.google.gson": "gson",
    "com.google.protobuf": "protobuf",
    "com.fasterxml.jackson": "jackson",
    "com.squareup.okhttp3": "okhttp3",
    "com.squareup.retrofit2": "retrofit",
    "io.reactivex": "rxjava",
    "io.netty": "netty",
    "io.grpc": "grpc-java",
    "io.micronaut": "micronaut",
    "io.quarkus": "quarkus",
    "javax.persistence": "jpa",
    "jakarta.persistence": "jpa",
    "javax.servlet": "servlet-api",
    "jakarta.servlet": "servlet-api",
    "lombok": "lombok",
    "reactor": "project-reactor",
}

# Python well-known standard library modules (to optionally filter out)
PYTHON_STDLIB = frozenset({
    "abc", "aifc", "argparse", "array", "ast", "asynchat", "asyncio",
    "asyncore", "atexit", "audioop", "base64", "bdb", "binascii",
    "binhex", "bisect", "builtins", "bz2", "calendar", "cgi", "cgitb",
    "chunk", "cmath", "cmd", "code", "codecs", "codeop", "collections",
    "colorsys", "compileall", "concurrent", "configparser", "contextlib",
    "contextvars", "copy", "copyreg", "cProfile", "crypt", "csv",
    "ctypes", "curses", "dataclasses", "datetime", "dbm", "decimal",
    "difflib", "dis", "distutils", "doctest", "email", "encodings",
    "enum", "errno", "faulthandler", "fcntl", "filecmp", "fileinput",
    "fnmatch", "fractions", "ftplib", "functools", "gc", "getopt",
    "getpass", "gettext", "glob", "grp", "gzip", "hashlib", "heapq",
    "hmac", "html", "http", "idlelib", "imaplib", "imghdr", "imp",
    "importlib", "inspect", "io", "ipaddress", "itertools", "json",
    "keyword", "lib2to3", "linecache", "locale", "logging", "lzma",
    "mailbox", "mailcap", "marshal", "math", "mimetypes", "mmap",
    "modulefinder", "multiprocessing", "netrc", "nis", "nntplib",
    "numbers", "operator", "optparse", "os", "ossaudiodev",
    "parser", "pathlib", "pdb", "pickle", "pickletools", "pipes",
    "pkgutil", "platform", "plistlib", "poplib", "posix", "posixpath",
    "pprint", "profile", "pstats", "pty", "pwd", "py_compile",
    "pyclbr", "pydoc", "queue", "quopri", "random", "re",
    "readline", "reprlib", "resource", "rlcompleter", "runpy",
    "sched", "secrets", "select", "selectors", "shelve", "shlex",
    "shutil", "signal", "site", "smtpd", "smtplib", "sndhdr",
    "socket", "socketserver", "sqlite3", "ssl", "stat", "statistics",
    "string", "stringprep", "struct", "subprocess", "sunau",
    "symtable", "sys", "sysconfig", "syslog", "tabnanny", "tarfile",
    "telnetlib", "tempfile", "termios", "test", "textwrap", "threading",
    "time", "timeit", "tkinter", "token", "tokenize", "tomllib",
    "trace", "traceback", "tracemalloc", "tty", "turtle", "turtledemo",
    "types", "typing", "unicodedata", "unittest", "urllib", "uu",
    "uuid", "venv", "warnings", "wave", "weakref", "webbrowser",
    "winreg", "winsound", "wsgiref", "xdrlib", "xml", "xmlrpc",
    "zipapp", "zipfile", "zipimport", "zlib", "_thread",
})


# ---------------------------------------------------------------------------
# Language-specific import parsers
# ---------------------------------------------------------------------------

def _strip_comments(text: str) -> str:
    """Remove single-line comments to avoid matching commented-out imports.

    Handles //, #, and -- style comments. Does not handle multi-line
    block comments (/* ... */) to keep the regex simple and fast.
    """
    lines = []
    for line in text.splitlines():
        # Preserve the line but strip trailing comments
        # Be careful not to strip inside strings - but for import lines,
        # strings rarely contain // or #, so this heuristic is acceptable
        stripped = line
        # For Python-style # comments (but not #! shebang, #include)
        if "#" in stripped:
            # Don't strip if it looks like a require statement with #
            if not re.match(r'^\s*(require|gem|from|import)\b', stripped):
                idx = stripped.index("#")
                stripped = stripped[:idx]
        lines.append(stripped)
    return "\n".join(lines)


def _get_line(text: str, match: "re.Match") -> str:
    """Extract the full source line containing a regex match.

    Handles edge cases where the match is on the first or last line
    of the text (no preceding/trailing newline).
    """
    start = text.rfind("\n", 0, match.start()) + 1
    end = text.find("\n", match.end())
    if end == -1:
        end = len(text)
    return text[start:end].strip()


def extract_python(text: str) -> List[Dict[str, str]]:
    """Extract library names from Python import statements.

    Patterns:
        import foo
        import foo as bar
        import foo, bar, baz
        from foo import bar
        from foo.bar import baz
        from foo import (bar, baz)
    """
    results = []
    patterns = [
        # from X import ... (captures the root module)
        r'^[ \t]*from\s+([\w.]+)\s+import\b',
        # import X [as Y] [, Z [as W]] ...
        # Uses a negative lookahead at start-of-match to skip JS-style
        # "import X from 'Y'" or "import { X } from 'Y'" lines entirely
        r'^(?!.*\bfrom\s+[\'"])[ \t]*import\s+([\w.]+(?:\s+as\s+\w+)?(?:\s*,\s*[\w.]+(?:\s+as\s+\w+)?)*)',
    ]

    is_from_pattern = [True, False]

    for pattern, is_from in zip(patterns, is_from_pattern):
        for match in re.finditer(pattern, text, re.MULTILINE):
            line_stripped = _get_line(text, match)

            # Skip lines ending with semicolons (Java/C#/JS, not Python)
            if line_stripped.endswith(";"):
                continue

            if is_from:
                # "from X.Y.Z import ..." -> root module is X
                full_module = match.group(1)
                root = full_module.split(".")[0]
                results.append({
                    "raw": root,
                    "full_path": full_module,
                    "language": "python",
                    "line": line_stripped,
                })
            else:
                # "import X, Y as Z, W" -> extract each module
                imports_str = match.group(1)
                for part in imports_str.split(","):
                    part = part.strip()
                    mod = part.split()[0]  # remove "as alias"
                    root = mod.split(".")[0]
                    results.append({
                        "raw": root,
                        "full_path": mod,
                        "language": "python",
                        "line": line_stripped,
                    })

    return results


def extract_javascript(text: str) -> List[Dict[str, str]]:
    """Extract library names from JavaScript/TypeScript import/require statements.

    Patterns:
        import X from 'Y'
        import { X } from 'Y'
        import * as X from 'Y'
        import 'Y'
        const X = require('Y')
        require('Y')
        import('Y')  (dynamic import)
    """
    results = []

    # Static imports: import ... from 'module' or import 'module'
    # Handles single and double quotes
    import_from = re.finditer(
        r'''^\s*import\s+(?:(?:[\w{},\s*]+)\s+from\s+)?['"]([^'"]+)['"]''',
        text, re.MULTILINE,
    )
    for match in import_from:
        module = match.group(1)
        line = _get_line(text, match)
        results.append({
            "raw": module,
            "language": "javascript",
            "line": line,
        })

    # require('module') or require("module")
    require_calls = re.finditer(
        r'''\brequire\s*\(\s*['"]([^'"]+)['"]\s*\)''',
        text,
    )
    for match in require_calls:
        module = match.group(1)
        line = _get_line(text, match)
        results.append({
            "raw": module,
            "language": "javascript",
            "line": line,
        })

    # Dynamic import: import('module')
    dynamic_imports = re.finditer(
        r'''\bimport\s*\(\s*['"]([^'"]+)['"]\s*\)''',
        text,
    )
    for match in dynamic_imports:
        module = match.group(1)
        line = _get_line(text, match)
        results.append({
            "raw": module,
            "language": "javascript",
            "line": line,
        })

    return results


def extract_go(text: str) -> List[Dict[str, str]]:
    """Extract library names from Go import statements.

    Patterns:
        import "fmt"
        import (
            "fmt"
            "net/http"
            "github.com/gin-gonic/gin"
        )
    """
    results = []

    # Single import
    single = re.finditer(
        r'^\s*import\s+"([^"]+)"',
        text, re.MULTILINE,
    )
    for match in single:
        module = match.group(1)
        line = _get_line(text, match)
        results.append({
            "raw": module,
            "language": "go",
            "line": line,
        })

    # Grouped imports
    grouped = re.finditer(
        r'^\s*import\s*\((.*?)\)',
        text, re.MULTILINE | re.DOTALL,
    )
    for match in grouped:
        block = match.group(1)
        for imp in re.finditer(r'"([^"]+)"', block):
            module = imp.group(1)
            results.append({
                "raw": module,
                "language": "go",
                "line": f'import "{module}"',
            })

    return results


def extract_rust(text: str) -> List[Dict[str, str]]:
    """Extract library names from Rust use/extern crate statements.

    Patterns:
        use serde::Deserialize;
        use std::collections::HashMap;
        extern crate serde;
        use tokio::{task, time};
    """
    results = []

    # use X::Y
    use_stmts = re.finditer(
        r'^\s*use\s+([\w]+)(?:::|;)',
        text, re.MULTILINE,
    )
    for match in use_stmts:
        crate = match.group(1)
        line = _get_line(text, match)
        results.append({
            "raw": crate,
            "language": "rust",
            "line": line,
        })

    # extern crate X
    extern_crates = re.finditer(
        r'^\s*extern\s+crate\s+(\w+)',
        text, re.MULTILINE,
    )
    for match in extern_crates:
        crate = match.group(1)
        line = _get_line(text, match)
        results.append({
            "raw": crate,
            "language": "rust",
            "line": line,
        })

    return results


def extract_java(text: str) -> List[Dict[str, str]]:
    """Extract library names from Java import statements.

    Patterns:
        import org.springframework.boot.SpringApplication;
        import static org.junit.Assert.*;
        import java.util.List;
    """
    results = []

    imports = re.finditer(
        r'^\s*import\s+(?:static\s+)?([\w.]+(?:\.\*)?)\s*;',
        text, re.MULTILINE,
    )
    for match in imports:
        package = match.group(1)
        line = _get_line(text, match)
        results.append({
            "raw": package,
            "language": "java",
            "line": line,
        })

    return results


def extract_ruby(text: str) -> List[Dict[str, str]]:
    """Extract library names from Ruby require/gem statements.

    Patterns:
        require 'json'
        require "nokogiri"
        require_relative 'lib/foo'
        gem 'rails', '~> 7.0'
    """
    results = []

    # require / require_relative
    requires = re.finditer(
        r'''^\s*(?:require|require_relative)\s+['"]([^'"]+)['"]''',
        text, re.MULTILINE,
    )
    for match in requires:
        module = match.group(1)
        line = _get_line(text, match)
        results.append({
            "raw": module,
            "language": "ruby",
            "line": line,
        })

    # gem 'X'
    gems = re.finditer(
        r'''^\s*gem\s+['"]([^'"]+)['"]''',
        text, re.MULTILINE,
    )
    for match in gems:
        module = match.group(1)
        line = _get_line(text, match)
        results.append({
            "raw": module,
            "language": "ruby",
            "line": line,
        })

    return results


def extract_csharp(text: str) -> List[Dict[str, str]]:
    """Extract library names from C# using statements.

    Patterns:
        using System.Linq;
        using Newtonsoft.Json;
        using static System.Math;
        using X = Some.Namespace;
    """
    results = []

    usings = re.finditer(
        r'^\s*using\s+(?:static\s+)?(?:\w+\s*=\s*)?([\w.]+)\s*;',
        text, re.MULTILINE,
    )
    for match in usings:
        namespace = match.group(1)
        line = _get_line(text, match)
        results.append({
            "raw": namespace,
            "language": "csharp",
            "line": line,
        })

    return results


# ---------------------------------------------------------------------------
# Normalization
# ---------------------------------------------------------------------------

def normalize_js_module(raw: str) -> str:
    """Normalize a JavaScript/TypeScript module name to a canonical form.

    - Scoped packages: check the scoped map, else use @scope/name -> name
    - Relative imports (./foo, ../bar): return as-is (local module)
    - Subpath imports (lodash/fp): use the root package
    """
    # Skip relative imports
    if raw.startswith("."):
        return raw

    # Check scoped package map first (exact match)
    if raw in JS_SCOPED_PACKAGE_MAP:
        return JS_SCOPED_PACKAGE_MAP[raw]

    # For scoped packages not in the map: @scope/name -> name
    if raw.startswith("@"):
        parts = raw.split("/")
        if len(parts) >= 2:
            # Check if @scope/name is in the map
            base = f"{parts[0]}/{parts[1]}"
            if base in JS_SCOPED_PACKAGE_MAP:
                return JS_SCOPED_PACKAGE_MAP[base]
            return parts[1]
        return raw

    # Subpath: lodash/fp -> lodash
    if "/" in raw:
        return raw.split("/")[0]

    return raw


def normalize_go_module(raw: str) -> str:
    """Normalize a Go import path to a canonical library name.

    - Standard library (no dots): return as-is
    - Known module paths: use the map
    - github.com/org/name/... -> name
    - Other paths: use the last meaningful segment
    """
    # Standard library (no dots in path)
    if "." not in raw:
        return raw

    # Check exact match in module map
    if raw in GO_MODULE_MAP:
        return GO_MODULE_MAP[raw]

    # Check prefix match (handles versioned paths like .../v2)
    for prefix, canonical in GO_MODULE_MAP.items():
        if raw.startswith(prefix + "/") or raw == prefix:
            return canonical

    # github.com/org/name -> name
    parts = raw.split("/")
    if len(parts) >= 3 and "." in parts[0]:
        # Skip version suffixes like v2, v3
        name = parts[2]
        for part in parts[3:]:
            if re.match(r'^v\d+$', part):
                continue
            break
        return name

    # Fallback: last segment
    return parts[-1]


def normalize_java_package(raw: str) -> str:
    """Normalize a Java package path to a canonical library name.

    - Check known package prefixes (longest match first)
    - java.* / javax.* / jakarta.* -> 'java-stdlib'
    - Other: use first two meaningful segments
    """
    # Skip wildcards
    clean = raw.rstrip(".*").rstrip(".")

    # Check known package map (longest prefix match)
    best_match = ""
    best_canonical = ""
    for prefix, canonical in JAVA_PACKAGE_MAP.items():
        if clean.startswith(prefix) and len(prefix) > len(best_match):
            best_match = prefix
            best_canonical = canonical
    if best_canonical:
        return best_canonical

    # Standard library
    if clean.startswith("java.") or clean.startswith("javax.") or clean.startswith("jakarta."):
        return "java-stdlib"

    # Fallback: use the first two segments after the TLD
    parts = clean.split(".")
    if len(parts) >= 3:
        # org.foo.bar -> foo (skip org/com/io/net)
        if parts[0] in ("org", "com", "io", "net", "de", "uk", "fr"):
            return parts[1]
    if len(parts) >= 2:
        return parts[1]

    return clean


def normalize_csharp_namespace(raw: str) -> str:
    """Normalize a C# namespace to a canonical library name.

    - System.* -> 'dotnet-stdlib'
    - Microsoft.* -> extract the product name
    - Known third-party roots
    """
    parts = raw.split(".")

    if parts[0] == "System":
        return "dotnet-stdlib"

    if parts[0] == "Microsoft":
        if len(parts) >= 3:
            # Microsoft.AspNetCore.Mvc -> aspnetcore
            # Microsoft.EntityFrameworkCore -> entityframeworkcore
            return parts[1].lower()
        if len(parts) == 2:
            return parts[1].lower()
        return "microsoft"

    # Check alias table for root namespace
    root = parts[0]
    if root in IMPORT_ALIASES:
        return IMPORT_ALIASES[root]

    return root.lower()


def normalize_ruby_module(raw: str) -> str:
    """Normalize a Ruby require path.

    - require_relative paths: return as-is (local)
    - Subpaths: 'active_support/core_ext' -> 'active_support'
    - Known aliases
    """
    # Take the root segment
    root = raw.split("/")[0]

    if root in IMPORT_ALIASES:
        return IMPORT_ALIASES[root]

    return root


def normalize_rust_crate(raw: str) -> str:
    """Normalize a Rust crate name.

    - 'std' -> 'rust-stdlib'
    - 'core' -> 'rust-stdlib'
    - 'alloc' -> 'rust-stdlib'
    - Known aliases
    """
    if raw in ("std", "core", "alloc"):
        return "rust-stdlib"

    if raw in IMPORT_ALIASES:
        return IMPORT_ALIASES[raw]

    # Rust crate names use underscores; normalize to hyphens for consistency
    return raw.replace("_", "-")


def normalize_library(entry: Dict[str, str]) -> str:
    """Normalize a single extracted library entry to a canonical name."""
    raw = entry["raw"]
    lang = entry["language"]

    # Dispatch to language-specific normalizer first, which handles
    # both language-specific aliases and structural normalization.
    # The global IMPORT_ALIASES table is checked within each normalizer
    # where appropriate.
    if lang == "python":
        root = raw.split(".")[0]
        if root in IMPORT_ALIASES:
            canonical = IMPORT_ALIASES[root]
            # Guard: don't apply Go/Rust/C# stdlib mappings to Python
            if canonical not in ("go-stdlib", "rust-stdlib", "dotnet-stdlib"):
                return canonical
        return root.lower()

    if lang == "javascript":
        return normalize_js_module(raw)

    if lang == "go":
        return normalize_go_module(raw)

    if lang == "rust":
        return normalize_rust_crate(raw)

    if lang == "java":
        return normalize_java_package(raw)

    if lang == "ruby":
        return normalize_ruby_module(raw)

    if lang == "csharp":
        return normalize_csharp_namespace(raw)

    return raw.lower()


# ---------------------------------------------------------------------------
# Top-level extraction
# ---------------------------------------------------------------------------

def extract_libraries(
    text: str,
    *,
    include_stdlib: bool = False,
    languages: Optional[List[str]] = None,
) -> List[Dict[str, str]]:
    """Extract and normalize library references from code text.

    Args:
        text: Source code text (may contain multiple languages, markdown fences, etc.)
        include_stdlib: If False, filter out standard library imports.
        languages: If specified, only run extractors for these languages.
            Valid values: python, javascript, go, rust, java, ruby, csharp.
            If None, run all extractors.

    Returns:
        List of dicts with keys: name, raw, language, line.
        Deduplicated by (name, language).
    """
    cleaned = _strip_comments(text)

    extractors = {
        "python": extract_python,
        "javascript": extract_javascript,
        "go": extract_go,
        "rust": extract_rust,
        "java": extract_java,
        "ruby": extract_ruby,
        "csharp": extract_csharp,
    }

    if languages:
        extractors = {k: v for k, v in extractors.items() if k in languages}

    raw_results = []
    for extractor in extractors.values():
        raw_results.extend(extractor(cleaned))

    # Normalize and deduplicate
    seen = set()
    results = []
    for entry in raw_results:
        name = normalize_library(entry)

        # Filter stdlib if requested
        if not include_stdlib:
            if entry["language"] == "python" and entry["raw"] in PYTHON_STDLIB:
                continue
            if name in ("go-stdlib", "java-stdlib", "rust-stdlib", "dotnet-stdlib"):
                continue

        key = (name, entry["language"])
        if key in seen:
            continue
        seen.add(key)

        results.append({
            "name": name,
            "raw": entry["raw"],
            "language": entry["language"],
            "line": entry["line"],
        })

    # Sort by language, then name for stable output
    results.sort(key=lambda r: (r["language"], r["name"]))
    return results


def extract_from_trajectory(
    trajectory: Dict,
    *,
    include_stdlib: bool = False,
) -> Dict:
    """Extract libraries from a ShareGPT-format trajectory record.

    Looks for code in:
    - conversation turns (user/assistant messages)
    - tool_call arguments
    - tool outputs

    Returns a dict with the trajectory ID and detected libraries.
    """
    code_blocks = []

    conversations = trajectory.get("conversations", [])
    for turn in conversations:
        content = turn.get("value", "") or turn.get("content", "")
        if content:
            # Extract fenced code blocks
            fenced = re.finditer(
                r'```(?:\w+)?\s*\n(.*?)```',
                content, re.DOTALL,
            )
            for block in fenced:
                code_blocks.append(block.group(1))

            # Also try the raw content (might be plain code)
            code_blocks.append(content)

        # Check tool_calls
        tool_calls = turn.get("tool_calls", [])
        if isinstance(tool_calls, list):
            for tc in tool_calls:
                args = tc.get("arguments", tc.get("args", ""))
                if isinstance(args, str):
                    code_blocks.append(args)
                elif isinstance(args, dict):
                    for v in args.values():
                        if isinstance(v, str):
                            code_blocks.append(v)

    combined_text = "\n".join(code_blocks)
    libraries = extract_libraries(combined_text, include_stdlib=include_stdlib)

    result = {
        "id": trajectory.get("id", trajectory.get("conversation_id", "unknown")),
        "libraries": libraries,
        "library_count": len(libraries),
    }

    # Build a summary of unique library names
    result["library_names"] = sorted(set(lib["name"] for lib in libraries))

    return result


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Extract library/framework references from code snippets.",
        epilog=(
            "Examples:\n"
            "  cat code.py | python extract_libraries.py\n"
            "  python extract_libraries.py -f snippet.py\n"
            "  python extract_libraries.py -f trajectory.json --trajectory\n"
            "  python extract_libraries.py -f data.jsonl --trajectory --format yaml\n"
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "-f", "--file",
        type=str,
        help="Input file path. If not provided, reads from stdin.",
    )
    parser.add_argument(
        "--trajectory",
        action="store_true",
        help="Parse input as trajectory data (JSON/JSONL with ShareGPT format).",
    )
    parser.add_argument(
        "--format",
        choices=["json", "yaml"],
        default="json",
        help="Output format (default: json).",
    )
    parser.add_argument(
        "--include-stdlib",
        action="store_true",
        help="Include standard library imports in output.",
    )
    parser.add_argument(
        "--languages",
        type=str,
        nargs="+",
        choices=["python", "javascript", "go", "rust", "java", "ruby", "csharp"],
        help="Only extract from these languages (default: all).",
    )
    parser.add_argument(
        "--compact",
        action="store_true",
        help="Output only unique library names (no metadata).",
    )

    args = parser.parse_args()

    # Read input
    if args.file:
        input_path = Path(args.file)
        if not input_path.exists():
            print(f"Error: file not found: {args.file}", file=sys.stderr)
            sys.exit(1)
        text = input_path.read_text(encoding="utf-8")
    else:
        text = sys.stdin.read()

    if not text.strip():
        print("Error: empty input", file=sys.stderr)
        sys.exit(1)

    # Process
    if args.trajectory:
        # Parse as JSON or JSONL
        results = []
        try:
            data = json.loads(text)
            if isinstance(data, list):
                records = data
            else:
                records = [data]
        except json.JSONDecodeError:
            # Try JSONL
            records = []
            for line_num, line in enumerate(text.splitlines(), 1):
                line = line.strip()
                if not line:
                    continue
                try:
                    records.append(json.loads(line))
                except json.JSONDecodeError:
                    print(
                        f"Warning: skipping invalid JSON at line {line_num}",
                        file=sys.stderr,
                    )

        for record in records:
            result = extract_from_trajectory(
                record, include_stdlib=args.include_stdlib,
            )
            results.append(result)

        output = {
            "source": args.file or "<stdin>",
            "record_count": len(results),
            "results": results,
        }
    else:
        # Plain code input
        libraries = extract_libraries(
            text,
            include_stdlib=args.include_stdlib,
            languages=args.languages,
        )

        if args.compact:
            output = sorted(set(lib["name"] for lib in libraries))
        else:
            output = {
                "source": args.file or "<stdin>",
                "libraries": libraries,
                "library_count": len(libraries),
                "library_names": sorted(set(lib["name"] for lib in libraries)),
            }

    # Output
    if args.format == "yaml":
        if not HAS_YAML:
            print(
                "Error: pyyaml is required for YAML output. "
                "Install with: pip install pyyaml",
                file=sys.stderr,
            )
            sys.exit(1)
        yaml.dump(output, sys.stdout, default_flow_style=False, sort_keys=False)
    else:
        json.dump(output, sys.stdout, indent=2, ensure_ascii=False)
        sys.stdout.write("\n")


if __name__ == "__main__":
    main()
