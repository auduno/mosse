MOSSE - fast javascript correlation filters for tracking objects in video

MOSSE.js is a javascript implementation of MOSSE correlation filters as described in "Visual Object Tracking using Adaptive Correlation Filters" by David Bolme. The library also provides three prebuilt MOSSE filters for tracking of left and right eye and face, as well as tools for building your own filters. These three filters were trained on faces from the MUCT image database.

Video example (tracking of eyes) - Webcam example (tracking of eyes) - Webcam example (tracking of face)

Some more information will be available in an upcoming blogpost.

To use with precreated filters:

var mosse = new mosseFilter();
mosse.load(filter);
// returns mode of correlation filter output inside window, relative to midpoint of window
mosse.track(element, left, top, width, height);

use with precreated filter, updating filter:

var mosse = new mosseFilter();
mosse.load(filter);
// for each call, returns mode of correlation filter output inside window, relative to midpoint of window
// also learns by adding
mosse.track(element, left, top, width, height, true);