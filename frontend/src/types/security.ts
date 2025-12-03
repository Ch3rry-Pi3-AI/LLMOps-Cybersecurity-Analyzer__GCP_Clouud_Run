/**
 * Security-related TypeScript interfaces used by the frontend components.
 * 
 * These types define the shape of:
 * - a detected security issue
 * - the response returned by the backend analysis
 * - props passed to file upload, code input, and results display components
 *
 * The goal is to enforce type safety across all security analysis UI elements.
 */

/**
 * Represents a single security issue found in the analysed code.
 */
export interface SecurityIssue {
  /** 
   * Human-readable issue title (e.g. “SQL Injection”, “Insecure Deserialisation”). 
   */
  title: string;

  /**
   * Explanation of the issue: why it matters, how it can be exploited, and context.
   */
  description: string;

  /**
   * The exact snippet or relevant portion of code where the issue occurs.
   */
  code: string;

  /**
   * Suggested remediation or best-practice fix for the issue.
   */
  fix: string;

  /**
   * Numerical CVSS score (0.0 – 10.0), describing severity in industry-standard terms.
   */
  cvss_score: number;

  /**
   * Severity scale categorised for UI display and sorting within the app.
   */
  severity: 'critical' | 'high' | 'medium' | 'low';
}

/**
 * Represents the backend's full analysis output.
 */
export interface AnalysisResponse {
  /**
   * High-level summary description of the analysed file or snippet.
   */
  summary: string;

  /**
   * List of detected security vulnerabilities.
   */
  issues: SecurityIssue[];
}

/**
 * Props for the FileUpload component.
 * Handles selecting a file, displaying its name, and initiating code analysis.
 */
export interface FileUploadProps {
  /** Name of the uploaded file (for UI display). */
  fileName: string;

  /** Event handler triggered when a user selects a file. */
  onFileUpload: (event: React.ChangeEvent<HTMLInputElement>) => void;

  /** Callback fired when the user clicks the "Analyze" button. */
  onAnalyzeCode: () => void;

  /** Indicates whether analysis is currently running. */
  isAnalyzing: boolean;

  /** True if code has been uploaded or typed; enables analysis button. */
  hasCode: boolean;
}

/**
 * Props for the CodeInput component.
 * Handles raw code input, file uploads, and analysis triggers.
 */
export interface CodeInputProps {
  /** Raw code entered by the user into the textarea. */
  codeContent: string;

  /** File name (if a file was uploaded). */
  fileName: string;

  /** Handler for upload selection. */
  onFileUpload: (event: React.ChangeEvent<HTMLInputElement>) => void;

  /** Initiates security analysis. */
  onAnalyzeCode: () => void;

  /** Whether the backend is currently analysing code. */
  isAnalyzing: boolean;
}

/**
 * Props for the AnalysisResults component.
 * Controls output rendering: either results, a loading state, or error messaging.
 */
export interface AnalysisResultsProps {
  /** The analysis data returned from the backend, or null if not yet run. */
  analysisResults: AnalysisResponse | null;

  /** Whether the system is still processing the request. */
  isAnalyzing: boolean;

  /** Optional error message for failed analyses. */
  error: string | null;
}
