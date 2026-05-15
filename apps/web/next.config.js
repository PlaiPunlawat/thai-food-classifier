/** @type {import('next').NextConfig} */

const withLess = require("next-with-less");
const removeImports = require("next-remove-imports")();
const withTM = require("next-transpile-modules")(["antd-img-crop"]);

const nextConfig = {
  reactStrictMode: true,
  compiler: {
    styledComponents: true,
  },
  experimental: {
    esmExternals: "loose",
  },
};

// Compose plugins
module.exports = (_phase, { defaultConfig }) => {
  const plugins = [withLess, removeImports, withTM];
  return plugins.reduce((acc, plugin) => plugin(acc), { ...nextConfig });
};
