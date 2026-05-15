import { Button, ConfigProvider, Divider, Drawer, Image, notification, Tooltip } from "antd";
import { FacebookShareButton, TwitterShareButton, WhatsappShareButton } from "react-share";
import {
  FacebookFilled,
  LinkOutlined,
  TwitterSquareFilled,
  WhatsAppOutlined,
  CameraOutlined,
  ReloadOutlined,
  BarChartOutlined,
} from "@ant-design/icons";
import { useState } from "react";
import clsx from "clsx";
import { Bar } from "@ant-design/plots";
import Link from "next/link";

export default function PredictResult({
  resultId,
  predictResult,
  imageUrl,
  selfTry = false,
  onReset = null,
}) {
  const [viewResultEvenNotCorrect, setViewResultEvenNotCorrect] = useState(false);
  const [statisticsDrawerVisible, setStatisticsDrawerVisible] = useState(false);

  return (
    <>
      <ConfigProvider
        theme={{
          token: {
            colorTextBase: "#111",
          },
        }}
      >
        <div className="flex flex-col lg:flex-row gap-8 justify-center align-middle">
          <div className="w-full lg:w-1/3">
            <Image
              src={imageUrl}
              alt="Result Image."
              width={"100%"}
              height={"100%"}
              style={{ objectFit: "cover" }}
              className={clsx("mx-auto")}
            />
          </div>
          {(predictResult && predictResult[0] && predictResult[0].confident > 80) ||
          viewResultEvenNotCorrect ? (
            <div className="mx-4 my-auto text-center">
              <div className="text-2xl font-bold mb-4">We think this is...</div>
              <div className="text-7xl font-bold mb-4 font-nakarat">{predictResult[0].name}</div>
              <div className="text-2xl font-bold mb-4 font-kanit">
                {predictResult[0].name} ({predictResult[0].name_th})
              </div>

              {!selfTry && (
                <Button
                  size="large"
                  className="mt-8 mr-2"
                  onClick={() => {
                    if (onReset) {
                      onReset();
                    } else {
                      window.location.reload();
                    }
                  }}
                  icon={<ReloadOutlined />}
                >
                  Back to start
                </Button>
              )}
              <Button
                size="large"
                type="primary"
                className="mt-8"
                onClick={() => {
                  setStatisticsDrawerVisible(true);
                }}
                icon={<BarChartOutlined />}
              >
                View advance statistics
              </Button>
              <Drawer
                title="Advance statistics"
                placement="bottom"
                closable={true}
                open={statisticsDrawerVisible}
                onClose={() => {
                  setStatisticsDrawerVisible(false);
                }}
                height={"calc(100vh - 64px)"}
              >
                <ConfigProvider
                  theme={{
                    token: {
                      colorTextBase: "#111",
                    },
                  }}
                >
                  <div className="text-gray-800">
                    <div className="container mx-auto">
                      {/* Title */}
                      <div className="text-2xl font-bold mb-4">Top 5 Prediction Probability (%)</div>

                      {/* Bar Chart */}
                      <Bar
                        data={predictResult.map((item) => {
                          return {
                            name: item.name + "\n" + item.name_th,
                            percentage: Math.round((item.confident + Number.EPSILON) * 100) / 100,
                          };
                        })}
                        xField="percentage"
                        yField="name"
                        meta={{
                          percentage: {
                            alias: "%",
                            formatter: (v) => {
                              return `${v}%`;
                            },
                            maxLimit: 100,
                          },
                        }}
                        label={{
                          position: "middle",
                        }}
                        color={({ name }) => {
                          return name === predictResult[0].name + "\n" + predictResult[0].name_th
                            ? "#379861"
                            : "#987737";
                        }}
                      />
                    </div>
                  </div>
                </ConfigProvider>
              </Drawer>
              {selfTry === true ? (
                <>
                  <Divider>Or try this yourself</Divider>
                  <div className="text-center">
                    <Link href="/predict">
                      <Button
                        // type="primary"
                        size="large"
                        icon={<CameraOutlined />}
                        // style={{ fontSize: "1.5rem", height: "3.5rem" }}
                      >
                        Select image
                      </Button>
                    </Link>
                  </div>
                </>
              ) : (
                <>
                  <Divider>Or share with your friends</Divider>
                  <FacebookShareButton
                    url={`${process.env.NEXT_PUBLIC_PUBLIC_BASE_URL}/result/${resultId}`}
                    id="facebook-share-button"
                  />
                  <TwitterShareButton
                    url={`${process.env.NEXT_PUBLIC_PUBLIC_BASE_URL}/result/${resultId}`}
                    id="twitter-share-button"
                  />
                  <WhatsappShareButton
                    url={`${process.env.NEXT_PUBLIC_PUBLIC_BASE_URL}/result/${resultId}`}
                    id="whatsapp-share-button"
                  />
                  {/* <VKShareButton
                          url={`${process.env.NEXT_PUBLIC_PUBLIC_BASE_URL}/result/${resultId}`}
                        ></VKShareButton> */}
                  {/* <TelegramShareButton
                          url={`${process.env.NEXT_PUBLIC_PUBLIC_BASE_URL}/result/${resultId}`}
                          >
                          <Button
                          size="large"
                          icon={<WhatsAppOutlined />}
                          shape="circle"
                          />
                        </TelegramShareButton> */}
                  <div className="flex justify-center gap-2">
                    <Tooltip title={"Share on Facebook"} placement="top">
                      <Button
                        size="large"
                        icon={<FacebookFilled style={{ color: "#4267B2" }} />}
                        shape="circle"
                        onClick={() => {
                          document.getElementById("facebook-share-button").click();
                        }}
                      />
                    </Tooltip>
                    <Tooltip title={"Share on Twitter"} placement="top">
                      <Button
                        size="large"
                        shape="circle"
                        icon={<TwitterSquareFilled style={{ color: "#1DA1F2" }} />}
                        onClick={() => {
                          document.getElementById("twitter-share-button").click();
                        }}
                      />
                    </Tooltip>
                    <Tooltip title={"Share on WhatsApp"} placement="top">
                      <Button
                        size="large"
                        icon={<WhatsAppOutlined style={{ color: "#075e54" }} />}
                        shape="circle"
                        onClick={() => {
                          document.getElementById("whatsapp-share-button").click();
                        }}
                      />
                    </Tooltip>
                    <Tooltip title={"Copy shareable link"} placement="top">
                      <Button
                        size="large"
                        icon={<LinkOutlined style={{ color: "#987737" }} />}
                        shape="circle"
                        onClick={() => {
                          notification.success({
                            message: "Copied share link to clipboard",
                          });
                          navigator.clipboard.writeText(
                            `${process.env.NEXT_PUBLIC_PUBLIC_BASE_URL}/result/${resultId}`
                          );
                        }}
                      />
                    </Tooltip>
                  </div>
                </>
              )}
            </div>
          ) : (
            <div className="mx-4 my-auto text-center">
              <div className="text-2xl font-bold mb-4">
                Our AI don&apos;t think this is a Thai food
              </div>
              <div className="text-4xl font-bold mb-4">Please try again with another image.</div>
              {onReset && (
                <Button
                  size="large"
                  // type="primary"
                  className="m-2"
                  onClick={() => {
                    if (onReset) {
                      onReset();
                    }
                  }}
                >
                  Back to start
                </Button>
              )}
              <Button
                size="large"
                type="primary"
                onClick={() => {
                  setViewResultEvenNotCorrect(true);
                }}
              >
                View result anyway
              </Button>
            </div>
          )}
        </div>
      </ConfigProvider>
    </>
  );
}
