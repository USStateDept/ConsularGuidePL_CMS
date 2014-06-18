$(function(){
   	$('#feedback-table').on('click', '.feedback-remove', function(){
        $self = $(this);
        mconfirm(
            'Confirm opinion removal',
            'Are you sure you want to remove this opinion?',
            function(){
                $.post('/feedback/deactivate/', { f_id: $self.attr('f_id') }, function(data) {
                    $self.parent().parent().hide();
                });
            }
        );
        return false;
    });
});
