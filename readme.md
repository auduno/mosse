mosse
=====

**mosse.js** is a javascript implementation of MOSSE correlation filters as described in [*Visual Object Tracking using Adaptive Correlation Filters*](http://www.cs.colostate.edu/~draper/papers/bolme_cvpr10.pdf) by David Bolme. The library provides three prebuilt MOSSE filters for tracking of left and right eye and face, as well as tools for building your own filters. These three filters were trained on faces from the MUCT image database.

[Video example (tracking of eyes)](https://auduno.github.io/mosse/examples/filtertest_video.html) - [Webcam example (tracking of eyes)](https://auduno.github.io/mosse/examples/filtertest_gum.html) - [Webcam example (tracking of face)](https://auduno.github.io/mosse/examples/filtertest_gum_face.html)

### Usage ###

To use with precreated filters:

```html
<script src="js/mosse.js"></script>
```

```html
var mosse = new mosseFilter();
mosse.load(filter);
// returns mode of correlation filter output inside window, relative to midpoint of window
mosse.track(element, left, top, width, height);
```

use with precreated filter, updating filter:

```html
var mosse = new mosseFilter();
mosse.load(filter);
// for each call, returns mode of correlation filter output inside window, relative to midpoint of window
// also learns by adding
mosse.track(element, left, top, width, height, true);
```