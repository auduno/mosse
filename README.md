mosse
=====

**mosse.js** is a javascript implementation of MOSSE correlation filters as described in [*Visual Object Tracking using Adaptive Correlation Filters*](http://www.cs.colostate.edu/~draper/papers/bolme_cvpr10.pdf) by David Bolme. The library provides three prebuilt MOSSE filters for tracking of left and right eye and face, as well as tools for building your own filters. These three filters were trained on faces from the MUCT image database.

[Video example (tracking of eyes)](https://auduno.github.io/mosse/examples/filtertest_video.html) - [Webcam example (tracking of eyes)](https://auduno.github.io/mosse/examples/filtertest_gum.html) - [Webcam example (tracking of face)](https://auduno.github.io/mosse/examples/filtertest_gum_face.html)

### Usage ###

To use with precreated filters, include `build/mosse.js` in your code:

```html
<script src="js/mosse.js"></script>
```

then run the mossefilter on a canvas element:

```JavaScript
var mfilter = new mosse.mosseFilter();
mfilter.load(mosse.filters.face_filter);
var mode = mfilter.track(element, left, top, width, height);
// returns mode of correlation filter output inside window, relative to midpoint of window
// where `element` is a canvas element, and `left`, `top`, `width` and `height` 
// define the window on the canvas element
```

You can also update filter during tracking, by setting final parameter to true:

```JavaScript
mfilter.track(element, left, top, width, height, true);
```