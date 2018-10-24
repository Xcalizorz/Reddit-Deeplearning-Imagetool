# Contributing

When contributing to this repository, please first describe the change you wish to make via an issue and discuss it. \
If there is an interesting issue you would like to work on, discuss it first and assign it to yourself, if possible.

## Pull Request Process

1. Ensure you have installed all the requirements and adhered our [coding guideline](#coding-guideline)
2. Update the Changelog.md with useful information on the changes you've made
3. Your pull request will be merged, if at least two other developers accepted it.

## Coding Guideline

This will be a short list of important things you need to consider.
Please adhere to them, because your merge request will not be accepted, if you provide code not adhering to these important rules:

- Use PEP8 and Pylint in parallel
  - PEP8 is the standard linter for PyCharm
    - Ignore: E203
    - Ignore: E501 (80 chars per line), we accept **90-95 chars per line**
  - Pylint can easily be added
    - Ignore: W0511
- Try to write clean code from the beginning
  - [SOLID](https://en.wikipedia.org/wiki/SOLID)
  - Investing more time in the beginning, means less time to invest at the end
- If possible, add unit-testing to the features or bugfixes etc. you provide