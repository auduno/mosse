export default {
	entry: 'src/mosse.js',
	targets: [
		{
			format: 'umd',
			moduleName: 'mosseFilter',
			dest: 'build/mosse.js'
		},
		{
			format: 'es',
			dest: 'build/mosse.module.js'
		}
	]
};