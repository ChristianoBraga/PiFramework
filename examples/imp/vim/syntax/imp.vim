" Vim syntax file
" Language: IMP
" Maintainer: Christiano Braga
" Latest Revision: March 2018

if exists("b:current_syntax")
  finish
endif

syn match impIdentifiers '\<\h\w*' 
syn keyword impMachine module end   
syn keyword impClauses var const init proc
syn keyword impCommands add=impConditional,impRepeat,impBlock,impComp
syn keyword impConditional if else  
syn keyword impLoop while do           
syn keyword impBlock { } 
syn keyword impComp | ;
syn match  impOperators display "[-+\*/=,\~\<\>\[\]\->]"
syn keyword impSystemCmd exec mc and view eof
syn keyword impBoolean true false
syn match impNumber '\d\+'  
syn match impNumber '[-+]\d\+'
syn match impComment "---.*$" 
syn match impComment "\*\*\*.*$"

let b:current_syntax = "imp"

hi def link impIdentifiers Identifiers
hi def link impBoolean     Boolean
hi def link impTodo        Todo
hi def link impComment     Comment
hi def link impMachine     Statement    
hi def link impClauses     Statement
hi def link impLoop        Repeat
hi def link impConditional Conditional
hi def link impBlock       Statement
hi def link impComp        Statement
hi def link impNumber      Constant
hi def link impOperators   Operator
hi def link impSystemCmd   Special
