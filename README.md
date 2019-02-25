# Voice-vim-editor

# Usage
Type the following command in vim command(line) mode
```
:call VoiceCommand("...")
```

# Commands to Implement
* **Mode switch command**
  - [x] **Switch to insert mode** [vim command: i]
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
  - [ ] **Move cursor** [vim command: hjkl]
  
  - [ ] **Search text** [vim command: \\]
  
* **Node level commands**
  - [ ] **Select current node** (the smallest node cursor current in)
  
  - [ ] **Select parent node of current node**
  
  - [ ] **Select child node of current node**
  
  - [ ] **Search a node**
  
  - [ ] **Add text** ??????
  
  - [ ] **Delete node**
  
   
* **Other commands**

