function checkboxChange()
{
    var checkAllPerms = function()
    {
        $('#id_edited_pages_0_parent input[type=checkbox]')
            .prop('checked', true)
            .prop('disabled', true);
    };
    var enableAllPerms = function()
    {
        $('#id_edited_pages_0_parent input[type=checkbox]')
            .prop('disabled', false);
    };
    
    if($('#id_groups_2').prop('checked'))
    {
        checkAllPerms();
        $('#id_groups_1').prop('checked', true).prop('disabled', true);
        $('#id_groups_0').prop('checked', true).prop('disabled', true);
    }
    else
    {
        $('#id_groups_1').prop('disabled', false);
        $('#id_groups_0').prop('disabled', false);
    }
    
    if($('#id_groups_0').prop('checked'))
    {
        checkAllPerms();
        $('#id_groups_1').prop('checked', true).prop('disabled', true);
    }
    else
    {
        $('#id_groups_1').prop('disabled', false);
    } 

    if($('#id_groups_1').prop('checked'))
    {
        checkAllPerms();
    }
    else
    {
        enableAllPerms();
    }
}
$(function(){
	checkboxChange();
	$('.modal').on('change', '#id_groups_0_parent input', checkboxChange);

	$('.remove').click(function(){
		$self = $(this);
		mconfirm('Confirm user removal', 'Are you sure you want to remove this user?', function(){
		    $self.closest('.remove-form').submit();
		});
		return false;
	});

    $('.modal').on('hidden.bs.modal', function(){
      $(this).data('bs.modal', null);
      $(this).html('');
    });
});

