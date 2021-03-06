# Voice-vim-editor

## Requirements
* libclang-vim: https://github.com/libclang-vim/libclang-vim
* vim with python3 package

## Usage
Type the following command in vim command(line) mode. Commands are non-case-sensitive
```
:call VoiceCommand("...")
```

## Commands to Implement
* **Mode switch command**
  - [x] **Switch to insert mode** [vim command: i] user can type by keyboard in insert mode.
  ```
  VoiceCommand("switch insert")
  ```
  - [x] **Switch to normal mode** [vim command: \<esc\>]
  ```
  VoiceCommand("switch normal")
  ```
* **Char level commands** (Insert mode)
  - [x] **Insert text** [vim command: a]
  
    Insert text in current cursor position.
    ```
    VoiceCommand("add [text]")
    ```
  - [x] **Delete text** [vim command: dnl / dnh / ndd /ndl / dnw / dnb]
  
    Delete text around current cursor position. Text can be delete in unit of char, word or line. You can specific number of units to delete. 
    
    You can also define the delete direction (forward/backward). If the direction is not specified, it is forward by default.
    ```
    VoiceCommand("delete n [char/word/line] [forward/backward]")
    ```
  - [x] **Move cursor** [vim command: <count> gg / hjkl]
    - Move cursor to certain line
      ``` 
      VoiceCommand("move line n")
      ```
    - Move cursor in unit of char, word or line. 
      ```
      VoiceCommand("move n [char/word/line] [forward/right/down/backward/left/up]")
      ```
  
  - [x] **Search text** [vim command: \ / next / *]
    Unimplement: Highlight for search result.
    - Search word the cursor currently on
      ```
      VoiceCommand("search current word")
      ```
    - Search [text]
      ```
      VoiceCommand("search [text]")
      ```
    - Show next search result
      ```
      VoiceCommand("next")
      ```
    
  
* **Node level commands**
  - [x] **Select current node** (the most inner node the cursor currently at)
    ```
    VoiceCommand("select current node")
    ```
    If there is no node at current cursor position, it will warning error. Otherwise highlight the most inner node in visual mode.
  
  - [x] **Select parent node of current node**
    ```
    VoiceCommand("select parent node")
    ```
    If there is no node selected or no parent node, shows error message. Otherwise select parent of current selected node in visual mode. 
  
  - [x] **Select first child node of current node**
    ```
    VoiceCommand("select child node")
    ```
    If there is no node selected or no child node, shows error message. Otherwise select the first child of current selected node in visual mode.
  
  - [x] **Select previous sibling of current node**
    ```
    VoiceCommand("select previous sibling node")
    ```
    If there is no node selected or no previous sibling node, shows error message. Otherwise select the first child of current selected node in visual mode.
  
  - [x] **Select next sibling of current node**
    ```
    VoiceCommand("select next sibling node")
    ```
    If there is no node selected or no next sibling, shows error message. Otherwise select the next sibling node in visual mode.
  
  - [x] **Search a function name / variable name**
    ```
    VoiceCommand("search node [function / variable] [name]")
    ```
    Show the first occurrence after current cursor position.
    
    ```
    VoiceCommand("next result")
    ```
    Show next result in order.
  
  - [x] **Search a declaration of a function / variable**
    ```
    VoiceCommand("search node declaration [name]")
    ```
    Show the declaration of the function or declaration.
    
  - [x] **Search if / switch / for / while blocks with conditions**
    ```
    VoiceCommand("search node [if / switch / for / while] [conditions]")
    ```
    Currently a searchable condition can only be variable name. Need to modify libclang-vim to enable primitive value search.
    A condition can be name of a variable, a integer / float / double / char / string literal.
  
    Not support 1: do while; 2: in-line if expression yet; 3: nested search
    
  - [x] **Search line contains keywords**
    ```
    VoiceCommand("search node [conditions]")
    ```
    Search a line contains all specified keywords. The entire line will be highlighted instead of a node.
    A keyword can be name of a variable, a integer / float / double / char / string literal.
   
* **Other commands**

