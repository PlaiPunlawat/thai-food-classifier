# WhatKind? ThaiFood! 🍜

A web application that uses machine learning to identify different types of Thai food from images. Built to help tourists and foreigners discover and learn about Thai cuisine.

![Next.js](https://img.shields.io/badge/Next.js-13-black?logo=next.js)
![React](https://img.shields.io/badge/React-18-blue?logo=react)
![TailwindCSS](https://img.shields.io/badge/TailwindCSS-3-38bdf8?logo=tailwindcss)

## 🎓 Project Background

This project was developed as part of **PROJECT IN DATA SCIENCE AND BUSINESS ANALYTICS 2** (Course Code: 06026128) in the 1st semester of academic year 2022 at the School of Information Technology, King Mongkut's Institute of Technology Ladkrabang.

### Team Members
- **Punlawat Leecharoen** - Data Science and Business Analytics Student
- **Smith Cheablam** - Data Science and Business Analytics Student

### Advisor
- **Asst. Prof. Dr. Somkiat Wangsiripitak** - School of Information Technology, KMITL

## ✨ Features

- **Image Upload**: Drag-and-drop or paste images from clipboard
- **Multiple ML Models**: Choose between Xception (default) or MobileNet models
- **Image Cropping**: Crop images for better prediction accuracy
- **Real-time Progress**: Upload and processing progress indicators
- **Responsive Design**: Works seamlessly on mobile and desktop devices
- **Result Sharing**: Share prediction results via unique URLs

## 🛠️ Tech Stack

### Frontend
- **Framework**: Next.js 13 (React 18)
- **Styling**: Tailwind CSS, DaisyUI, Ant Design
- **UI Components**: Ant Design, Ant Design Charts
- **Image Processing**: antd-img-crop
- **HTTP Client**: Axios

### Machine Learning Models
- **Xception** - High accuracy model (default)
- **MobileNet** - Lightweight model for faster predictions

## 📋 Prerequisites

- Node.js 14+ or Yarn
- Backend API server running (see Environment Variables section)

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/thai-food-image-classification-web.git
cd thai-food-image-classification-web
```

### 2. Install dependencies

```bash
npm install
# or
yarn install
```

### 3. Configure environment variables

Create a `.env.local` file in the root directory:

```bash
cp .env.example .env.local
```

Edit `.env.local` and set the following variables:

```env
NEXT_PUBLIC_PUBLIC_BASE_URL=http://localhost:3000
NEXT_PUBLIC_API_ENDPOINT=http://localhost:5000/api
```

#### Environment Variables Explained

| Variable | Description | Example |
|----------|-------------|---------|
| `NEXT_PUBLIC_PUBLIC_BASE_URL` | Base URL of the web application | `http://localhost:3000` |
| `NEXT_PUBLIC_API_ENDPOINT` | Backend API endpoint for image classification | `http://localhost:5000/api` |

### 4. Run the development server

```bash
npm run dev
# or
yarn dev
```

Open [http://localhost:3000](http://localhost:3000) in your browser to see the application.

### 5. Build for production

```bash
npm run build
npm run start
# or
yarn build
yarn start
```

## 📁 Project Structure

```
thai-food-image-classification-web/
├── components/          # React components
│   ├── Navbar.jsx      # Navigation bar component
│   ├── PredictImage.jsx # Image upload and prediction component
│   └── PredictResult.jsx # Results display component
├── lib/                # Utility functions and helpers
│   ├── api.js         # API client and configuration
│   ├── constants.js   # Application constants
│   └── utils.js       # Helper functions
├── pages/             # Next.js pages (routes)
│   ├── _app.js       # App wrapper and global config
│   ├── index.js      # Home page
│   ├── predict.js    # Prediction page
│   ├── about.js      # About page
│   └── result/       # Dynamic result pages
│       └── [resultId].js
├── public/           # Static assets
│   ├── images/      # Image files
│   └── fonts/       # Custom fonts
├── styles/          # Global styles
│   ├── globals.less # Global LESS styles
│   └── tailwind.css # Tailwind CSS imports
└── next.config.js   # Next.js configuration
```

## 🎨 Usage

1. **Navigate to the Upload page** - Click "Get Started" or "Upload" in the navigation
2. **Upload an image** - Either drag & drop, click to browse, or paste from clipboard
3. **Select ML model** (optional) - Choose between Xception or MobileNet
4. **Wait for results** - The image will be processed by the AI model
5. **View predictions** - See the top predicted Thai food dishes with confidence scores
6. **Share results** - Use the unique URL to share your results

## 🔌 API Integration

This frontend application requires a backend API server. The API should provide the following endpoints:

### POST `/upload`
Upload an image for classification

**Request:**
- `Content-Type: multipart/form-data`
- `image`: Image file (PNG, JPG, JPEG, max 5MB)
- `model`: Model name (`xception` or `mobilenet`)

**Response:**
```json
{
  "resultId": "unique-id",
  "predict_result": [
    {
      "food_name": "Tom Yum Kung",
      "confidence": 0.95
    }
  ]
}
```

### GET `/result/:resultId`
Get prediction result by ID

**Response:**
```json
{
  "image_url": "https://...",
  "predict_result": [...]
}
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is part of an academic course project. Please contact the authors for usage permissions.

## 📧 Contact

For questions or feedback, please contact:
- Punlawat Leecharoen
- Smith Cheablam

## 🙏 Acknowledgments

- Asst. Prof. Dr. Somkiat Wangsiripitak for project guidance
- King Mongkut's Institute of Technology Ladkrabang
- School of Information Technology

---

Built with ❤️ for Thai food lovers around the world
