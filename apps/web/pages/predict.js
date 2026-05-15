import { Parallax } from "react-parallax";
import Navbar from "../components/Navbar";
import PredictImage from "../components/PredictImage";
import Head from "next/head";
import { Card } from "antd";

export default function Predict() {
  return (
    <>
      <Head>
        <title>Predict WhatKind? ThaiFood!</title>
      </Head>

      <Parallax
        bgImage="/images/background_image_blur.jpg"
        bgImageAlt="Golden Spoon"
        strength={600}
        className="content"
        bgImageSize="cover"
      >
        <Navbar />
        <PredictImage />
      </Parallax>
    </>
  );
}
