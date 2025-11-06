# Testing Strategy

## Overview

This project uses **PyTest exclusively** for unit testing. This document establishes comprehensive guidelines for writing maintainable, atomic tests.

## Core Testing Rules

### Structure & Organization
- Test packages mirror production code structure
- One test file covers a single testee (typically a Python class)
- Create new packages when structural conflicts arise
- Always include `__init__.py` files in new test packages

### Test Design Principles
- **Atomic tests**: Cover only one test case per test function
- **Branch coverage**: Write one test per code branch, avoiding overengineering
- **Naming convention**: Follow `test_[TESTEE]_[TEST_CASE]` pattern
- **Pattern**: Apply AAA (Arrange/Act/Assert) methodology
- **Simplicity**: Keep tests straightforward and comprehensible

### Exception Testing
Tests must assert the error message and not just the exception class. This applies universally—never test exceptions without validating the actual error message.

### Mocking Guidelines
- Minimize mocking for first-party code; happy-path tests are preferable
- Use `unittest.mock` consistently with `mock.patch` for standardized patching
- For higher-level methods, prioritize testing the happy path over mocking

### Coverage Best Practices
- At minimum, one test per function or method
- Ensure all code branches are covered
- Avoid testing framework features
- Test through public interfaces

### Code Quality
- Avoid loops and abstractions that obscure test intent
- Limit global test setup overhead
- Keep tests clear and explicit
