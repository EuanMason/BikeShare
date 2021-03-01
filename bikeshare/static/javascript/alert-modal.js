
/**
 * Creates and manage a popup modal
 * 
 * @param {string} - title: The title of the modal
 * @param {string} - message: The message of the modal
 * @param {function} - callback: The function to be called when clossed (optional)
*/
function callModalAlert(title, message, callback){
    // String representing the modal
    /**
     * Layout took from the official documention.
     *  Bootstrap team. Vertically centered. On https://getbootstrap.com/docs/4.0/components/modal/
     *  Accessed on: 28/02/2021
     */
    let stringModal = ""
    stringModal += '<div class="modal fade" id="alert-modal" tabindex="-1" role="dialog" aria-labelledby="exampleModalCenterTitle" aria-hidden="true"> '
    stringModal += '  <div class="modal-dialog modal-dialog-centered" role="document"> '
    stringModal += '    <div class="modal-content"> '
    stringModal += '      <div class="modal-header"> '
    stringModal += '        <h5 class="modal-title" id="exampleModalLongTitle">'+title+'</h5> '
    stringModal += '        <button type="button" class="close" data-dismiss="modal" aria-label="Close"> '
    stringModal += '          <span aria-hidden="true">&times;</span> '
    stringModal += '        </button> '
    stringModal += '      </div> '
    stringModal += '      <div class="modal-body"> '
    stringModal += '       '+message+' '
    stringModal += '      </div> '
    stringModal += '      <div class="modal-footer"> '
    stringModal += '        <button type="button" class="btn btn-primary" data-dismiss="modal" >OK</button> '
    stringModal += '      </div> '
    stringModal += '    </div> '
    stringModal += '  </div> '
    stringModal += '</div> '

    // Add the modal to html
    $("#modal-area").html(stringModal)

    // Call the modal
    $('#alert-modal').modal('toggle');

    // If there a callback then call it on close
    if(callback) {
        $('#alert-modal').on('hidden.bs.modal', function () {
            callback()
        });
    } 
    
}
