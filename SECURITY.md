# Security Policy

## Reporting Security Issues

**Please do not report security vulnerabilities through public GitHub issues.**

If you believe you have found a security vulnerability in sdd-cli, please open a [GitHub Security Advisory](https://github.com/mikecubed/spec-kit/security/advisories/new) to report it privately.

Please include as much of the following as possible:

- A description of the vulnerability and its potential impact
- Steps to reproduce the issue
- Any relevant source file paths, tags, branches, or commit SHAs
- Proof-of-concept code (if applicable)

## Scope

sdd-cli is a local CLI tool that writes files to disk. It makes no network calls and has no authentication surface. Security issues most likely to apply:

- Path traversal vulnerabilities in file-writing logic
- Dependency vulnerabilities in `click` or the Python stdlib

## Policy

We will acknowledge reports within 7 days and aim to resolve confirmed vulnerabilities before public disclosure.
