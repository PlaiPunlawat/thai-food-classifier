import { Divider } from "antd";
import Head from "next/head";
import { Parallax } from "react-parallax";
import Navbar from "../components/Navbar";

export default function About() {
  return (
    <>
      <Head>
        <title>About WhatKind? ThaiFood!</title>
      </Head>
      <Parallax
        bgImage="/images/background_image_blur.jpg"
        bgImageAlt="Golden Spoon"
        bgImageSize="cover"
        strength={300}
      >
        <Navbar />
        <div className="py-48">
          <div className="flex flex-col items-center justify-center py-2">
            <main className="flex flex-col items-center justify-center w-full flex-1 px-20 text-center">
              <h1 className="text-6xl font-bold">
                About WhatKind? ThaiFood!
              </h1>
              <p className="mt-3 text-2xl">
                This is a project to predict kind of Thai food from images.
              </p>
              <div className="flex flex-wrap items-center justify-around max-w-4xl mt-6 sm:w-full">
                <a
                  href="#about"
                  className="p-6 mt-6 text-left border w-96 rounded-xl hover:scale-110 transition-all duration-500 ease-in-out"
                >
                  <h3 className="text-2xl font-bold">About &rarr;</h3>
                  <p className="mt-4 text-xl">About WhatKind? ThaiFood!</p>
                </a>
                <a
                  href="#developer"
                  className="p-6 mt-6 text-left border w-96 rounded-xl hover:scale-110 transition-all duration-500 ease-in-out"
                >
                  <h3 className="text-2xl font-bold">Developers &rarr;</h3>
                  <p className="mt-4 text-xl">
                    About developer
                  </p>
                </a>
              </div>
            </main>
          </div>
        </div>

        <div className="custom-shape-divider-bottom-1670007665">
          <svg
            data-name="Layer 1"
            xmlns="http://www.w3.org/2000/svg"
            viewBox="0 0 1200 120"
            preserveAspectRatio="none"
          >
            <path
              d="M1200 120L0 16.48 0 0 1200 0 1200 120z"
              class="shape-fill"
            ></path>
          </svg>
        </div>
      </Parallax>

      <div className="pt-24 pb-12" id="about">
        <div className="flex flex-col items-center justify-center py-2">
          <main className="flex flex-col items-center justify-center w-full flex-1 px-20 text-center">
            <h2 className="text-3xl font-bold">About WhatKind? ThaiFood!</h2>
            <p className="mt-3 text-xl">
            This website is part of (06026128) PROJECT IN DATA SCIENCE AND
              BUSINESS ANALYTICS 2 course, 1st semester, academic year 2022,
              School of Information Technology, King Mongkut&apos;s Institute of
              Technology Ladkrabang.
            </p>
            <p className="mt-3 text-2xl">
              For classifying Thai food from images using
              Xception and MobileNet trained models to support Thai food and
              Thai food business for tourists or foreigners.
            </p>
          </main>
        </div>
      </div>

      <div className="divider w-1/2 mx-auto"></div>

      <div className="py-12" id="developer">
        <div className="flex flex-col items-center justify-center py-2">
          <main className="flex flex-col items-center justify-center w-full flex-1 px-20 text-center">
            <h2 className="text-3xl font-bold mb-3">About Developers</h2>
            {/* <p className="mt-3 text-2xl">This project build with love by</p> */}
            <div className="flex flex-row flex-wrap gap-8 my-6">
              <div class="card w-full md:w-72 lg:w-96 bg-[#222] shadow-xl">
                <figure className="px-10 pt-10 avatar">
                  <div className="rounded-full">
                    {/* eslint-disable-next-line @next/next/no-img-element */}
                    <img
                      src="https://i.imgur.com/Hv3Dsh0.jpg"
                      alt="Punlawat Leecharoen"
                      className="rounded-xl"
                      draggable={false}
                    />
                  </div>
                </figure>
                <div className="card-body items-center text-center">
                  <h2 className="card-title">Punlawat Leecharoen</h2>
                  <p className="font-kanit">
                    Data Science and Business Analytics Program Student at
                    School of Information Technology King Mongkut&apos;s
                    Institute of Technology Ladkrabang
                  </p>
                </div>
              </div>
              <div class="card w-full md:w-72 lg:w-96 bg-[#222] shadow-xl">
                <figure className="px-10 pt-10 avatar">
                  <div className="rounded-full">
                    {/* eslint-disable-next-line @next/next/no-img-element */}
                    <img
                      src="https://i.imgur.com/ol6KCMC.png"
                      alt="Smith Cheablam"
                      className="rounded-xl"
                      draggable={false}
                    />
                  </div>
                </figure>
                <div className="card-body items-center text-center">
                  <h2 className="card-title">Smith Cheablam</h2>
                  <p className="font-kanit">
                    Data Science and Business Analytics Program Student at
                    School of Information Technology King Mongkut&apos;s
                    Institute of Technology Ladkrabang
                  </p>
                </div>
              </div>
            </div>

            <div className="divider w-1/2 lg:w-1/4 mx-auto my-8">Advisor</div>

            <div className="flex flex-row flex-wrap justify-center gap-8 my-6">
              <div class="card w-full lg:w-1/2 bg-[#222] shadow-xl">
                <figure className="px-10 pt-10 avatar">
                  <div className="rounded-full">
                    {/* eslint-disable-next-line @next/next/no-img-element */}
                    <img
                      src="https://www.it.kmitl.ac.th/wp-content/uploads/2017/12/Somkiat-300x300.jpg"
                      alt="Asst. Prof. Dr. Somkiat Wangsiripitak"
                      className="rounded-xl"
                      draggable={false}
                    />
                  </div>
                </figure>
                <div className="card-body items-center text-center">
                  <h2 className="card-title">
                    Asst. Prof. Dr. Somkiat Wangsiripitak
                  </h2>
                  <p className="font-kanit">
                    Advisor, Lecturer at at School of Information Technology
                    King Mongkut&apos;s Institute of Technology Ladkrabang
                  </p>
                </div>
              </div>
            </div>
          </main>
        </div>
      </div>
    </>
  );
}
