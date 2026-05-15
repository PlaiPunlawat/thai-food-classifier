/** @type {import('next').NextConfig} */

const withLess = require("next-with-less");
const removeImports = require("next-remove-imports")();
const withTM = require("next-transpile-modules")(["antd-img-crop"]);

const nextConfig = {
  reactStrictMode: true,
  compiler: {
    // Enables the styled-components SWC transform
    styledComponents: true,
  },
};

// Compose plugins
module.exports = (_phase, { defaultConfig }) => {
  const plugins = [withLess, removeImports, withTM];
  return plugins.reduce((acc, plugin) => plugin(acc), { ...nextConfig });
};
