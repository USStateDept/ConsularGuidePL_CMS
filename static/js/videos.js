$(function(){
   	$(".video-edit-modal, #video-add-modal").on('change', 'select', function(){
       if(this.value == 'YT'){
           $('#id_video_original_parent').hide('200');
           $('#id_url_parent').show('200');
       }
       else {
           $('#id_video_original_parent').show('200');
           $('#id_url_parent').hide('200');
       }
   	});

    $('#video-table').on('click', '.video-remove', function(){
        $self = $(this);
        mconfirm(
            'Confirm video removal', 
            'Are you sure you want to remove this video?', 
            function(){
                $self.parent().submit();
            }
        );
        return false;
    });

    $('.video-edit-modal').on('hidden.bs.modal', function(){
      $(this).data('bs.modal', null);
    });

    var backup = $('#video-add-modal').clone();
    $('#video-add-modal').on('hidden.bs.modal', function(){
      $(this).html('');
      $(this).html(backup.html());
    });
});
