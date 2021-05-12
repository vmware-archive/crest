<!-- Copyright 2020-2021 VMware, Inc.
SPDX-License-Identifier: MIT -->
Contributing to Crest
=======================

Project Structure
-----------------
All of the source code for Crest itself is written in `src/`. Inside of that folder, 
contributions are grouped by feature or general area, where the deepest folders correspond to a 
specific component. When writing a component, you should respect the following structure:
```text
src/crest
        └──
            <feature folder>/ (depending on where your feature fits in Crest)
                ├── <feature>.py
        └── utils
            ├── <script_name>.py
```
Let's check out each of these files and what they should contain.

##### `<feature>.py`
This file should contain the implementation of a feature/functionality.

##### `<script_name>.py`
This file should run independently and contribute to one of the existing functionalities.


Commit message format
---------------------
Your commit message should respect the following format:
```
[<bucket>] <title>

<detailed commit message>

Bug number: <bug number if available>
Reviewed by: <reviewers' usernames>
Approved by: <reviewers' usernames>
Review URL: <reviewboard URL>
```
Note that the blank lines after the title and before the references are part of the format and 
should be respected.