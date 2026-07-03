/** @type {import('next').NextConfig} */

const withLess = require("next-with-less");
const removeImports = require("next-remove-imports")();
const withTM = require("next-transpile-modules")([
  "antd-img-crop",
  "@ant-design/charts",
  "@ant-design/plots",
  "@antv/g2plot",
  "@antv/g2",
  "@antv/g-base",
  "@antv/path-util",
  "d3-interpolate",
  "lodash-es",
]);

const nextConfig = {
  reactStrictMode: true,
  experimental: {
    esmExternals: "loose",
  },
  compiler: {
    styledComponents: true,
  },
};

// Compose plugins
module.exports = (_phase, { defaultConfig }) => {
  const plugins = [withLess, removeImports, withTM];
  return plugins.reduce((acc, plugin) => plugin(acc), { ...nextConfig });
};
