#!/bin/bash
# In The Name Of God
# ========================================
# [] File Name : lex.sh
#
# [] Creation Date : 26-10-2016
#
# [] Created By : Parham Alvani (parham.alvani@gmail.com)
# =======================================
data="
int #zz99
//It's a fucking comment :)
#zz99 = 1 + 2
#ps77 = '\\n' + 'c' + '\\c'
"

curl -X POST -F "text=$data" "127.0.0.1:8080/lex"
