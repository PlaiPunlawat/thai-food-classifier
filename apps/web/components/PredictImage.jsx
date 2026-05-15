import { UploadOutlined, LoadingOutlined } from "@ant-design/icons";
import {
  Button,
  Card,
  ConfigProvider,
  Divider,
  Dropdown,
  Image,
  notification,
  Progress,
  Steps,
  Upload,
} from "antd";
// import AntdImgCrop from "antd-img-crop";
import { useState } from "react";
import dynamic from "next/dynamic";
import clsx from "clsx";
import axios from "axios";
import PredictResult from "./PredictResult";

const AntdImgCrop = dynamic(() => import("antd-img-crop"), { ssr: false });

export default function PredictImage() {
  const [currentStep, setCurrentStep] = useState(0);

  const [processing, setProcessing] = useState(false);

  const [processingPercentage, setProcessingPercentage] = useState(0);

  const [uploadingFile, setUploadingFile] = useState(null);
  const [uploadingFilePreview, setUploadingFilePreview] = useState(null);

  const [resultId, setResultId] = useState(null);
  const [predictResult, setPredictResult] = useState(null);

  const resetStates = () => {
    setCurrentStep(0);
    // reset all state
    setUploadingFile(null);
    setUploadingFilePreview(null);
    setProcessing(false);
    setProcessingPercentage(0);
    setResultId(null);
    setPredictResult(null);
  };

  const handlePaste = (e) => {
    const items = e.clipboardData.items;
    for (let i = 0; i < items.length; i++) {
      if (items[i].type.indexOf("image") !== -1) {
        const blob = items[i].getAsFile();
        const reader = new FileReader();
        reader.onload = (event) => {
          setUploadingFile(blob);
          setUploadingFilePreview(event.target.result);
          setCurrentStep(1);
        };
        reader.readAsDataURL(blob);
      }
    }
  };

  const handleUpload = async (model = "xception") => {
    setProcessing(true);
    setCurrentStep(2);

    // console.log(uploadingFile.size / 1024 / 1024);

    if (uploadingFile.size > 1024 * 1024 * 5) {
      notification.error({
        message: "File size is too large",
        description: "Please upload file less than 5MB",
      });
      setCurrentStep(1);
      setProcessing(false);
      return;
    }

    const formData = new FormData();
    formData.append("image", uploadingFile);
    formData.append("model", model);
    axios
      .post("/upload", formData, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
        onUploadProgress: (progressEvent) => {
          // console.log((progressEvent.loaded / progressEvent.total) * 100);
          setProcessingPercentage(Math.floor((progressEvent.loaded / progressEvent.total) * 100));
        },
      })
      .then((res) => {
        setProcessingPercentage(100);
        setResultId(res.data.resultId);
        setPredictResult(res.data.predict_result);
        setTimeout(() => {
          setProcessing(false);
          setCurrentStep(3);
        }, 1234);
      })
      .catch((err) => {
        if (err.response?.status === 413) {
          notification.error({
            message: "File too large",
            description: "Please upload a smaller file",
          });
        } else if (err.response?.status === 429) {
          notification.error({
            message: "Too many requests",
            description:
              "You have exceeded the maximum number of requests per minute. Please try again in few minutes.",
          });
        } else {
          notification.error({
            message: "Error",
            description: "Error while uploading file, please try again later.",
          });
        }
        setProcessing(false);
        setCurrentStep(1);
      });
  };

  return (
    <>
      <div className="container mx-auto mt-12 px-4" onPaste={handlePaste}>
        <Steps
          className="text-white"
          current={currentStep}
          items={[
            {
              title: "Select Image",
              description: "Select an image of a Thai food.",
              onClick: () => {
                if (currentStep !== 0 && currentStep !== 2) {
                  resetStates();
                }
              },
            },
            {
              title: "Upload Image",
              description: "Upload selected image",
            },
            {
              title: "Processing",
              description: "Image being processed by our AI",
            },
            {
              title: "Result",
              description: "What kind is this food ?",
            },
          ]}
        />
        {/* <Steps.Step title="Select Image" description="Select an image of a Thai food." />
          <Steps.Step title="Upload Image" description="Upload selected image" />
          <Steps.Step title="Processing" description="Image being processed by our Super AI" />
          <Steps.Step title="Result" description="What kind of that food ?" /> */}
        {/* </Steps> */}

        <ConfigProvider
          theme={{
            token: {
              colorTextBase: "#111",
            },
          }}
        >
          <div className="my-12 transition-all duration-500 ease-in-out">
            <Card bordered={false}>
              {currentStep === 0 && (
                <>
                  <AntdImgCrop quality={0.8} modalTitle="Crop Image for only Food or Plate">
                    <Upload.Dragger
                      showUploadList={false}
                      accept={".png,.jpg,.jpeg"}
                      customRequest={(options) => {
                        const { onSuccess, onError, file } = options;

                        const reader = new FileReader();
                        reader.readAsDataURL(file);
                        reader.onload = () => {
                          setUploadingFile(file);
                          setUploadingFilePreview(reader.result);
                          onSuccess("ok");
                          setCurrentStep(1);
                        };
                        reader.onerror = (error) => {
                          notification.error({
                            message: "Error",
                            description: "Error while reading file, please try again later.",
                          });
                          onError(error);
                        };
                      }}
                    >
                      <p className="ant-upload-drag-icon">
                        <UploadOutlined />
                      </p>
                      <p className="ant-upload-text">Click or drag image to this area to upload</p>
                      <p className="ant-upload-hint">
                        Support only JPG and PNG file. Max file size is 5MB.
                      </p>
                    </Upload.Dragger>
                  </AntdImgCrop>
                  <Divider>Or</Divider>
                  <div className="text-center">
                    <h3 className="text-xl">Paste Image from clipboard here</h3>
                  </div>
                </>
              )}
              {currentStep !== 0 && currentStep !== 3 && (
                <div className={clsx("flex justify-center relative")}>
                  <div
                    className={clsx(
                      "transition-all duration-500 ease-in-out",
                      currentStep === 2 && "w-full md:w-2/3 lg:w-1/2",
                      currentStep === 3 && "w-1/2 md:w-1/3 lg:w-1/4",
                      currentStep !== 2 && "w-full md:w-1/2 lg:w-1/3"
                    )}
                  >
                    <Image
                      src={uploadingFilePreview}
                      alt="Selected Image."
                      className={clsx("mx-auto", currentStep === 2 && "opacity-30")}
                      preview={currentStep !== 2}
                      width={"100%"}
                    />
                    {currentStep === 2 ? (
                      <div className="absolute w-full h-full top-1/3 left-0">
                        {processingPercentage < 95 ? (
                          <>
                            <div className="text-center">
                              <div className="text-xl mb-4 font-bold">Uploading</div>
                              <Progress
                                type="circle"
                                percent={processingPercentage}
                                format={(percent) => `${percent}%`}
                                strokeColor={"#987737"}
                              />
                            </div>
                          </>
                        ) : (
                          <>
                            <div className="text-center">
                              <div className="text-xl mb-4 font-bold">Processing</div>
                              <LoadingOutlined
                                spin
                                style={{ fontSize: "6rem", color: "#987737" }}
                              />
                            </div>
                          </>
                        )}
                      </div>
                    ) : undefined}
                  </div>
                </div>
              )}
              {currentStep === 1 && (
                <>
                  <div className="flex flex-col md:flex-row md:justify-between mt-8">
                    <div>
                      <Button
                        size="large"
                        loading={processing}
                        onClick={() => {
                          setCurrentStep(0);
                          setUploadingFile(null);
                          setUploadingFilePreview(null);
                        }}
                        className="my-2"
                      >
                        Reselect image
                      </Button>
                    </div>
                    <div>
                      {/* <Button
                      size="large"
                      type="primary"
                      loading={processing}
                      onClick={() => {}}
                      className="my-2"
                    >
                      Upload this image
                    </Button> */}
                      <Dropdown.Button
                        size="large"
                        type="primary"
                        loading={processing}
                        onClick={() => {
                          handleUpload();
                        }}
                        menu={{
                          items: [
                            {
                              key: "xception",
                              label: "Upload and predict using Xception (default)",
                            },
                            {
                              key: "mobilenet",
                              label: "Upload and predict using   MobileNet",
                            },
                          ],
                          onClick: ({ key }) => {
                            handleUpload(key);
                          },
                        }}
                      >
                        Upload and predict this image
                      </Dropdown.Button>
                    </div>
                  </div>
                </>
              )}
              {currentStep === 3 && (
                <PredictResult
                  resultId={resultId}
                  predictResult={predictResult}
                  imageUrl={uploadingFilePreview}
                  onReset={resetStates}
                />
              )}
            </Card>
          </div>
        </ConfigProvider>
      </div>
    </>
  );
}
