import Navbar from "../../components/Navbar";
import Head from "next/head";
import { useRouter } from "next/router";
import { Parallax } from "react-parallax";
import PredictResult from "../../components/PredictResult";
import axios from "axios";
import { Button, Card, ConfigProvider, Result } from "antd";
import Link from "next/link";

export default function ResultById({ result, resultId }) {
  const imageUrl = result?.image_url || "/images/background_image_blur.jpg";
  const predictResult = result?.predict_result || [];
  // const { image_url: imageUrl, predict_result: predictResult } = result;
  const router = useRouter();

  return (
    <>
      <Head>
        <title>Result WhatKind? ThaiFood!</title>
      </Head>
      <ConfigProvider
        theme={{
          token: {
            colorTextBase: "#111",
          },
        }}
      >
        <Parallax
          bgImage={imageUrl}
          blur={8}
          bgImageAlt="Golden Spoon"
          strength={600}
          className="content"
          bgImageSize="cover"
        >
          <div className="bg-gradient-to-b from-black via-[#00000066] to-transparent">
            <Navbar />
          </div>

          {result ? (
            <div className="container mx-auto mt-12 px-4">
              <div className="my-12 transition-all duration-500 ease-in-out">
                <Card bordered={false}>
                  <PredictResult
                    imageUrl={imageUrl}
                    predictResult={predictResult}
                    resultId={resultId}
                    selfTry={true}
                    onReset={() => {
                      router.push("/predict");
                    }}
                  />
                </Card>
              </div>
            </div>
          ) : (
            <ConfigProvider
              theme={{
                token: {
                  colorTextBase: "#eee",
                },
              }}
            >
              <Result
                status="404"
                title="Not Found"
                subTitle="Sorry, this type of food is not even exist."
                extra={
                  <Link href="/">
                    <Button type="primary">Back to Home</Button>
                  </Link>
                }
              />
            </ConfigProvider>
          )}
        </Parallax>
      </ConfigProvider>
    </>
  );
}

export async function getServerSideProps(context) {
  const { resultId } = context.params;
  try {
    const { data: result } = await axios.get(`/result/${resultId}`, {
      baseURL: process.env.NEXT_PUBLIC_API_ENDPOINT,
    });

    return {
      props: {
        result,
        resultId,
      },
    };
  } catch {
    context.res.statusCode = 404;
    return {
      props: {
        result: null,
        resultId: null,
      },
    };
  }
}
