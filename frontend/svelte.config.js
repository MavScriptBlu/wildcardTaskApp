/** @format */

import adapter from "@sveltejs/adapter-node";

/** @type {import('sveltejs/kit').Config} */
const config = {
	kit: {
		// adapter-node builds a small standalone node server, which is
		// exactly what we want for running this inside a container
		adapter: adapter(),
	},
};

export default config;
