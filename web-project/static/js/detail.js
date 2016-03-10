$('.login').on('click',function(){
	$('.nav').show();
	$('.login').addClass('active');
})
$('.container').on('click',function(e){
	target=$(e.target).attr('class')
	console.log(target);
	if (target != 'open')
	{
		$('.nav').hide();
		$('.login').removeClass('active');
	}

})
