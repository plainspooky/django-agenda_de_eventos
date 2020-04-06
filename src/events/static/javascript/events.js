$(document).ready(function() {

    $('.edit-event').click(function(){
        /*  recupera o id do objeto que invocou esta rotina e popula os
            campos de 'id' (oculto), descrição e prioridade. A data é
            preenchida diretamente no gabarito. */
        let values = this.id.split('-');
        $('#editInputId').prop('value', values[1]);
        $('#editInputEvent').prop('value', this.text);
        $('#editInputPriority').prop('value', values[2]);

        $('#editEvent').modal('toggle');
    })// click()

})// function()
