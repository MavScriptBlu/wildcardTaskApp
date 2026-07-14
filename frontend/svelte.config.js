/** @format */

import adapterNode from "@sveltejs/adapter-node";
import adapterVercel from "@sveltejs/adapter-vercel";

/** @type {import('sveltejs/kit').Config} */
const config = {
	kit: {
		// adapter-node builds a small standalone node server for running
		// inside our container; on Vercel (which sets VERCEL at build time)
		// we need adapter-vercel's Build Output API format instead
		adapter: process.env.VERCEL ? adapterVercel() : adapterNode(),
	},
};

export default config;
