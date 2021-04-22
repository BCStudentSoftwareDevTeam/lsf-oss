$(document).ready(function(){
  $('#pendingDescriptions').DataTable();
});

function manage(versionID) {
  window.location.href = '/positionDescriptionEdit/' + versionID
}
