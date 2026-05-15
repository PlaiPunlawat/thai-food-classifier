import { ConfigProvider, theme } from "antd";
import Head from "next/head";
import "../styles/globals.less";
import "../styles/tailwind.css";
// import "antd/dist/reset.css";
import { StyleProvider } from "@ant-design/cssinjs";

import NextNProgress from "nextjs-progressbar";
import { configureApi } from "../lib/api";
import { COLORS } from "../lib/constants";

function MyApp({ Component, pageProps }) {
  // Configure API client
  configureApi();

  return (
    <>
      <Head>
        <link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon.png" />
        <link rel="icon" type="image/png" sizes="32x32" href="/favicon-32x32.png" />
        <link rel="icon" type="image/png" sizes="16x16" href="/favicon-16x16.png" />
        <link rel="manifest" href="/site.webmanifest" />
      </Head>
      <NextNProgress color={COLORS.primary} />
      <StyleProvider hashPriority="high">
        <ConfigProvider
          theme={{
            token: {
              algorithm: theme.darkAlgorithm,
              colorPrimary: COLORS.primary,
              colorTextBase: "white",
              // colorBgBase: "#343434",
              // colorPrimaryText: "#ffffff",
              fontFamily: "'Inter', sans-serif",
            },
          }}
        >
          <div data-theme="black">
            <Component {...pageProps} />
          </div>
        </ConfigProvider>
      </StyleProvider>
    </>
  );
}

export default MyApp;
