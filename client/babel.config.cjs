module.exports = {
  presets: [
    ['@babel/preset-env', { targets: { node: 'current' } }],
    ['@babel/preset-react', { runtime: 'automatic' }],
  ],
  plugins: [
    // Jest runs tests in Node, which doesn't understand Vite's
    // `import.meta.env.DEV` syntax (used for the dev-only preview role
    // switcher). This plugin rewrites it to `process.env.DEV` before
    // Jest ever sees it, since Node's plain CommonJS transform can't
    // parse `import.meta` at all otherwise.
    'babel-plugin-transform-vite-meta-env',
  ],
};
