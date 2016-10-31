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
#zz99
"

curl -X POST -F "text=$data" "127.0.0.1:8080/yacc"
