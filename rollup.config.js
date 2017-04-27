export default {
	entry: 'src/mosse.js',
	targets: [
		{
			format: 'umd',
			moduleName: 'mosse',
			dest: 'build/mosse.js'
		},
		{
			format: 'es',
			dest: 'build/mosse.module.js'
		}
	]
};