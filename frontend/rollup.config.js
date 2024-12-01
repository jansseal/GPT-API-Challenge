import { spawn } from 'child_process';
import svelte from 'rollup-plugin-svelte';
import commonjs from '@rollup/plugin-commonjs';
import terser from '@rollup/plugin-terser';
import resolve from '@rollup/plugin-node-resolve';
import livereload from 'rollup-plugin-livereload';
import css from 'rollup-plugin-css-only';
import dotenv from 'rollup-plugin-dotenv';
import replace from '@rollup/plugin-replace';

const production = !process.env.ROLLUP_WATCH;

function serve() {
	let server;

	function toExit() {
		if (server) server.kill(0);
	}

	return {
		writeBundle() {
			if (server) return;
			server = spawn('npm', ['run', 'start', '--', '--dev'], {
				stdio: ['ignore', 'inherit', 'inherit'],
				shell: true
			});

			process.on('SIGTERM', toExit);
			process.on('exit', toExit);
		}
	};
}

export default {
	input: 'src/main.js',
	output: {
		sourcemap: true,
		format: 'iife',
		name: 'app',
		file: 'public/build/bundle.js'
	},
	plugins: [
		svelte({
			compilerOptions: {
				// Enable run-time checks when not in production
				dev: !production
			}
		}),
		// Extract CSS into a separate file for better performance
		css({ output: 'bundle.css' }),

		// Resolve Node modules and deduplicate Svelte imports
		resolve({
			browser: true,
			dedupe: ['svelte', 'svelte/transition', 'svelte/internal', 'svelte/store', 'svelte-routing'],
			exportConditions: ['svelte']
		}),
		commonjs(),

		// Serve during development
		!production && serve(),

		// Enable live reloading in development
		!production && livereload('public'),

		// If we're building for production (npm run build
		// instead of npm run dev), minify
		production && terser(),
		dotenv(),
		replace({
			preventAssignment: true,
			'process.env': production ? '"production"' : '"dev"',
		}),
	],
	watch: {
		clearScreen: false
	}
};
