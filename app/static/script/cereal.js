// Full list of configuration options available here:
// https://github.com/hakimel/reveal.js#configuration
Reveal.initialize({
controls: false,
progress: true,
history: false,
center: true,
//autoSlide: 5000,
keyboard: true,
//loop: true,

theme: Reveal.getQueryHash().theme || 'serif', // available themes are in /css/theme
transition: Reveal.getQueryHash().transition || 'linear', // default/cube/page/concave/zoom/linear/fade/none
});

// set keyboard shortcuts
KeyboardJS.on('l', function() { checkIfEndOfFeed() }, null)
KeyboardJS.on('e', function() { checkIfEndOfFeed(); favorites(Reveal.getCurrentSlide()) }, null)
KeyboardJS.on('w', function() { checkIfEndOfFeed(); retweet(Reveal.getCurrentSlide()) }, null)
KeyboardJS.on('q', function() { checkIfEndOfFeed(); interestedIn(Reveal.getCurrentSlide()) }, null)

// TODO: feedback
// TODO: keylog
// TODO: test queue functionality

// we open this queue after user is down browsing
function favorites(slide) {
	if ($(slide).attr('id')) {
		$.ajax({
			type: 'POST',
			url: '/favorites',
			contentType: 'application/json',
			dataType:'json',
			data: JSON.stringify({id: $(slide).attr('id') }) ,
				success: function(data) {
				}
		})

		// go to the next slide
		Reveal.right();
					
	}
}

function retweet(slide) {
	if ($(slide).attr('id')) {
		$.ajax({
			type: 'POST',
			url: '/retweet',
			contentType: 'application/json',
			dataType:'json',
			data: JSON.stringify({id: $(slide).attr('id') }) ,
				success: function(data) {
				}
		})

		// go to the next slide
		Reveal.right();
	} 
}

var read_queue = []

// when we first express interest, we go to article preview
// if we express interest from article preview, we queue and go to the next slide
function interestedIn(slide) {

	// check if we're done
	checkIfEndOfFeed()

	queue(slide);

}

function skip(slide) {

	// check if we're done
	checkIfEndOfFeed()

	var main_slide = $(slide)

	// deque the slide if the user was interested in it before
	if (hasInterestMarker(main_slide)) {

		// we keep post url in id of <section> tag
		var tweet_id = main_slide.attr('id') 

		// use tweet_id to lookup post
		for (var i=0;i<read_queue.length;i++) {
			if (read_queue[i]['tweet_id'] === tweet_id) {
				// remove the post from the queue
				remove(read_queue,read_queue[i])
			}
		}

		// remove interest marker from the main slide
		removeInterestMarker(main_slide)

		// wait 300ms, then go right
		setTimeout(function() { Reveal.right()}, 300);
	} else 
		Reveal.right()

}

// adds the URL for the given slide to our interest queue
function queue(slide) {

	// the main display slide has the url 
	var main_slide = $(slide)

	// we keep post url in id of <section> tag
	var tweet_id = main_slide.attr('id') 

	if (!hasInterestMarker(main_slide)) {

	  	// add url to queue as a json object
	  	read_queue.push({
	  		tweet_id:tweet_id,
	  	})

	  	// add visual feedback to the slide to mark interest
	  	addInterestMarker(main_slide)

	  	// wait then go right
	  	setTimeout(Reveal.right,300)

	// if it does have an interest marker, just go right
	} else 
		Reveal.right()
	
	

}

// takes a jquery object and puts an interest marker on it
// static/i.png is the interest marker
function addInterestMarker(slide) {
		slide.append("<div class='i'><img src='static/i.png'></div>")
}

function removeInterestMarker(slide) {
		slide.children('.i').remove()
}

// returns true if the slide has already been liked
function hasInterestMarker(slide) {
	if (slide.children('.i').html() == undefined)
		return false;
	return true
}

// if we are at end of list, open up all the urls
// NB: this is triggered when 'l' key is pressed AND whenever queue() is called
function checkIfEndOfFeed() {

	if (Reveal.isLastSlide()) {

		// post the json object to server
		$.ajax({
			type: 'POST',
			url: '/done',
			contentType: 'application/json',
			dataType:'json',
			data: JSON.stringify({posts: read_queue}),
			success: function(data) {
				document.body.innerHTML = data.html
			}
		})
	}

}



// remove an item from an array
function remove(arr, item) {
	for(var i = arr.length; i--;) {if(arr[i] === item) {arr.splice(i, 1); } } return arr } 