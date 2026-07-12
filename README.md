# Script2Story — AI Storyboard Generator

Convert any screenplay into a cinematic storyboard PDF using Generative AI.

## What it does

Upload a screenplay (.txt file) → AI analyses each scene → Generates cinematic images → Downloads as a professional storyboard PDF.

## Features

- Automatic scene parsing from standard screenplay format
- AI-powered cinematic prompt engineering per scene
- Shot type detection — wide shots, close-ups, tracking shots, medium shots
- Real AI image generation using Flux image model
- Retry logic and graceful degradation for reliable output
- Clean web interface built with Flask

## Tech Stack

- Python, Flask
- Replicate API (Flux image generation model)
- Pillow for image processing and PDF generation
- Prompt engineering for cinematic output

## Setup

1. Clone the repo
2. Install dependencies: