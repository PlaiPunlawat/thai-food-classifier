import Navbar from "../components/Navbar";
// import Image from "next/image";
import { Button } from "antd";
import { Parallax } from "react-parallax";
import Head from "next/head";
import Link from "next/link";

export default function Home() {
  return (
    <>
      <Head>
        <title>WhatKind? ThaiFood!</title>
      </Head>

      <Parallax
        bgImage="/images/background_image_blur.jpg"
        bgImageAlt="Golden Spoon"
        strength={600}
        bgImageSize="cover"
      >
        <Navbar />
        <div className="hero flex text-white">
          <div className="container mx-auto">
            <div className="hero-content block">
              <div>
                <h1 className="text-6xl font-bold">WhatKind?</h1>
                <h1 className="text-7xl font-bold">ThaiFood!</h1>
                <span className="text-lg block my-2">
                  What&apos;s that Thai food called? Let us help you!
                </span>
                <Link
                  href="/predict"
                  className="btn btn-primary mt-2 text-2xl bg-[#987737] text-white normal-case font-thin"
                >
                  Get Started!
                </Link>
              </div>
            </div>
          </div>
        </div>
      </Parallax>
    </>
  );
}
