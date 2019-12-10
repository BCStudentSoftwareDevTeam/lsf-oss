$(document).ready(function() {
  // CKEDITOR.replace( 'editor1' );
});

function populatePurpose(){
  // alert("Hello world")
  $("#purpose").val('default').selectpicker("refresh");
  $("#purpose").empty();
  $("#subject").val("Subject")
  CKEDITOR.instances["editor1"].setData('');
  var recipient = $("#recipient").val();
  console.log(recipient);
  $.ajax({
    url: "/admin/emailTemplates/getPurpose/" + recipient,
    dataType: "json",
    success: function(response){
      console.log(response)
      for (var key in response){
        var value = response[key]["Purpose"]
        $("#purpose").append('<option value="' + value + '">' + value + '</option>');
        $("#purpose").val('default').selectpicker("refresh");
      }
    }
  })
}

function getEmailTemplate(){
  $("#subject").val("Subject")
  CKEDITOR.instances["editor1"].setData('');
  var purpose = $("#purpose").val();
  console.log(purpose);
  $.ajax({
    url: "/admin/emailTemplates/getEmail/" + purpose,
    dataType: "json",
    success: function(response){
      // console.log(response)
      var body = response["emailBody"]
      var subject = response["emailSubject"]
      console.log(subject);
      // console.log(body);
      CKEDITOR.instances["editor1"].insertHtml(body);
      $("#subject").val(subject)
      // var content= CKEDITOR.instances.editor1.getData();
      // console.log(content);
      // for (var key in response){
      //   var value = response[key]["Purpose"]
      //   $("#purpose").append('<option value="' + value + '">' + value + '</option>');
      //   $("#purpose").val('default').selectpicker("refresh");
      // }
    }
  })
}

function postEmailTemplate(){
  var body = CKEDITOR.instances.editor1.getData();
  var purpose = $("#purpose").val();
  console.log(body);
  console.log(purpose);
  $.ajax({
    url: "/admin/emailTemplates/postEmail/",
    data: { 'body': body, 'purpose': purpose },
    dataType: 'json',
    type: 'POST',
    success: function(response){
      location.reload()
    }

  })
}

//
// CKEDITOR.replace( 'editor1', {
//     toolbarGroups: [
//         { name: 'mode' },
//         { name: 'basicstyles' },
//         { name: 'styles' }
//    ],
//     on: {
//         pluginsLoaded: function() {
//             var editor = this,
//                 config = editor.config;
//
//             // Helper function. Coverts color name into colorful <span>.
//             function colorfulSpan( color ) {
//                 return '<span style="color:' + color + '">' + color + '</span>';
//             }
//
//             // AllowedContent rule for the contents inserted by the combo.
//             // As this sample combo inserts <span> of certain style only, it's quite short.
//             // See: http://docs.ckeditor.com/#!/guide/dev_advanced_content_filter
//             var acfRules = 'span{color}';
//
//             // Let the party on!
//             editor.ui.addRichCombo( 'myCombo', {
//                 label: 'My combo\'s label',
//                 title: 'My combo',
//                 toolbar: 'styles',
//
//                 // Registers a certain type of contents in the editor.
//                 allowedContent: acfRules,
//
//                 // The minimal content that must be allowed in the editor for this combo to work.
//                 requiredContent: acfRules,
//
//                 // Combo iherits from the panel. Set up it first so all styles
//                 // of the contents are available in the panel.
//                 panel: {
//                     css: [ CKEDITOR.skin.getPath( 'editor' ) ].concat( config.contentsCss ),
//                     multiSelect: false
//                 },
//
//                 // Let's populate the list of available items.
//                 init: function() {
//                     this.startGroup( 'My custom panel group' );
//
//                     var items = [ 'red', 'orange', 'blue', 'green' ];
//
//                     for ( var i = 0; i < items.length; i++ ) {
//                         var item = items[ i ];
//
//                         // Add entry to the panel.
//                         this.add( item, colorfulSpan( item ), item );
//                     }
//                 },
//
//                 // This is what happens when the item is clicked.
//                 onClick: function( value ) {
//                     editor.focus();
//
//                     // Register undo snapshot.
//                     editor.fire( 'saveSnapshot' );
//
//                     // Insert a colorful <span>.
//                     editor.insertHtml( colorfulSpan( value ) );
//
//                     // Register another undo snapshot. The insertion becomes undoable.
//                     editor.fire( 'saveSnapshot' );
//                 },
//
//                 // The value of the combo may need to be updated, i.e. according to the selection.
//                 // This is where such listener is supposed to be created.
//                 onRender: function() {
//                     //editor.on( 'selectionChange', function( ev ) {
//                     //    var currentValue = this.getValue();
//                     //    ...
//                     //    this.setValue( value );
//                     //}, this );
//                 },
//
//                 // The contents of the combo may change, i.e. according to the selection.
//                 // This is where it supposed to be updated.
//                 onOpen: function() {
//                 },
//
//                 // Disable the combo if the current editor's filter does not allow
//                 // the type of contents that the combo delivers (i.e. widget's nested editable).
//                 // See: http://docs.ckeditor.com/#!/guide/dev_widgets.
//                 refresh: function() {
//                     if ( !editor.activeFilter.check( acfRules ) )
//                         this.setState( CKEDITOR.TRISTATE_DISABLED );
//                 }
//             } );
//         }
//     }
// } );
