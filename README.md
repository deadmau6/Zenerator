# Zenerator 

A simple and configurable code generation tool with user defined templates

### Goal:

> The goal of this project is to create a tool that can help developers code faster. The tool should be able to help developers by creating code with minimal commands. The code creation should be defined by the user with templates and settings. The templates can be any file type and be readable in their file format. The settings should be clear and reflect the code creation process.

### Features:

 - [x] Save settings and templates both locally and globally.
 - [ ] Create a ubiquitous local folder structure to save settings and templates to.
 - [ ] Allow arguments in the template to be filled by the user.
 - [ ] Allow user to define start and end tags for the individual template parsing.
 - [ ] Allow users to create templates that append code to existing files.

### Tasks:

 - [ ] Create a parsing module.
 - [x] Create a simple configuration module that determines the settings and rules.
 - [ ] Define a robust set of operations and rules that make up the settings.
 - [ ] Create a command line interface.
 - [ ] Create an install script.
 - [ ] Create a generator module that uses the settings and templates to create the end result.

### Test Strategy:

 * Running tests: `/Zenerator$ pytest` runs **all** tests. To run a _specific_ test you just need to specify its path, like so: `/Zenerator$ pytest test/unit/test_utils.py`.

 * **Print statements not showing up?** Try using the `-s` flag or you can use `--capture=method      per-test capturing method: one of fd|sys|no|tee-sys`.