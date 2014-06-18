$(function(){
    $('#file-table').on('click', '.file-remove', function(){
        $self = $(this);
        mconfirm(
            'Confirm file removal', 
            'Are you sure you want to remove this file?', 
            function(){
                $self.parent().submit();
            }
        );
        return false;
    });
});
