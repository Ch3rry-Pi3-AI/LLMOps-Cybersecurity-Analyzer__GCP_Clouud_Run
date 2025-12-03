# **Components Folder**

This directory contains the React components that make up the user interface for the security analysis workflow. Each component is responsible for a specific part of the user interaction flow, from uploading Python files to displaying analysis results.

## Key Components

* **`FileUpload.tsx`**
  Provides the file selection and analysis trigger controls. Handles user uploads and initiates backend security analysis.

* **`CodeInput.tsx`**
  Displays uploaded code in a read-only editor and integrates the file upload actions into the main input area.

* **`AnalysisResults.tsx`**
  Renders the results returned by the backend, including summaries, error states, and detailed tables of detected security issues.

## Purpose

These components collectively form the interactive frontend for code security analysis. They are fully typed, modular, and designed to be easily composed within pages or higher-level containers.

## Usage

Import and embed these components in your main analysis page or workflow to provide a complete code upload, inspection, and results experience.