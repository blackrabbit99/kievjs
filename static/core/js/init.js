var settings = {

};

requirejs.config({
  locale: 'en_us',
  hbs: {
    disableI18n: true,
    templateExtension : 'html',
    helperPathCallback: function(name) {
      return 'lib/helpers/' + name;
    }
  },
  shim: {
    'jquery': { exports: '$' },
    'underscore': { exports: '_' },
    'backbone': {
      deps: ['underscore', 'jquery'],
      exports: 'Backbone'
    }
  },
  baseUrl: '/static/core/js/app',
  paths: {
    hbs: '../libs/hbs',
    underscore: '../libs/underscore-1.4.2',
    backbone: '../libs/backbone-0.9.2',
    handlebars: '../libs/Handlebars',
    i18nprecompile: '../libs/i18nprecompile',
    json2: '../libs/json2',
    chaplin: '../libs/chaplin-0.6.0-pre-5b33dca',
    tpl: '/templates'
  },
  urlArgs: "bust=" +  (new Date()).getTime()
});
// initializing application flow
require(['application', 'routes'], function(Application, routes) {
  var app = new Application();
  app.initialize(routes);
});
