# **Types Folder**

This directory contains the TypeScript type definitions used throughout the frontend. These types ensure consistent data structures, improve maintainability, and provide strong compile-time validation across components.

## Contents

* **`security.ts`**
  Defines all interfaces related to the security analysis workflow, including:

  * security issue representations
  * analysis response structure
  * component prop types for file upload, code input, and result display

## Purpose

Centralising shared types in this folder ensures that components rely on a single source of truth for data contracts. This improves clarity, reduces duplication, and strengthens overall code reliability.

## Usage

Import the relevant interfaces directly from this folder when typing component props or working with analysis-related data structures.
