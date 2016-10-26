/*
 * +===============================================
 * | Author:        Parham Alvani (parham.alvani@gmail.com)
 * | Author:        Iman Tabrizian (tabrizian@outlook.com)
 * |
 * | Creation Date: 09-09-2016
 * |
 * | File Name:     index.js
 * +===============================================
 */

/* global Vue : Vue.js */
/* global $   : JQuery */

var lexer = new Vue({
  el: '#lexer',
  data: {
    tokens: []
  },
  methods: {
    tokenize: function () {
      var form = $("#source").serialize()
      console.log(form)
      $.post('lex', form, function (data, status) {
        lexer.tokens = JSON.parse(data)
      })
    }
  }
})

$('document').ready(function () {
})
