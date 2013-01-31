(function($) {
  'use strict';

var organizers = [
  {
    mail: 'julia.saviyk@gmail.com',
    phone: '+380504306225',
    skype: 'juliya_saviyk'
  },
  {
    mail: 'klymyshyn@gmail.com',
    phone: '+380987183482',
    skype: 'max.klymyshyn'
  }
];
var showInfo = function(el, org) {
    el.empty();
    el.append('<ul>\
                  <li>Email: <a href="mailto:' + org.mail+ '">' + org.mail + '</a></li>\
                  <li>Phone: ' + org.phone + '</li>\
                  <li>Skype: ' + org.skype + '</li>\
                </ul>');

};

var sections = $('section.content');
var navlinks = $('header nav a');
var showSection = function(section) {
  navlinks.removeClass('active-narrow active-wide active-regular')
    .filter('a[href="#' + section + '"]')
    .addClass(function() {
      return 'active-' + $(this).attr('class').replace('menu-item-', '');
    });
  sections.hide();
  $('#' + section).show();
};
$.router(/\w+/, function(section) {
  showSection(section);
});
if (!window.location.hash) {
  showSection('topics');
}
$('#organizers .span6 .people-info p').each(function(i, el) {
  showInfo($(el), organizers[i]);
});
$('#partners h4 .mailto').each(function() {
  var email = organizers[0].email;
  $(this).html(email).attr('href', 'mailto:' + email);
});
})(window.jQuery);
