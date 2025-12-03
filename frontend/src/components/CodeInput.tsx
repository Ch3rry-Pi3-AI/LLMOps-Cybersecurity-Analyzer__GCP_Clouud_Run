import { CodeInputProps } from '@/types/security';
import FileUpload from './FileUpload';

/**
 * CodeInput Component
 *
 * Displays:
 * - the uploaded Python file’s content in a read-only editor
 * - a combined header section containing the label and a FileUpload component
 *
 * Responsibilities:
 * - Provide a visual container for code being analysed
 * - Pass file upload and analysis callbacks to the FileUpload button group
 * - Ensure the analysis button is only enabled when code is present
 *
 * This component acts as a bridge between the raw file upload
 * and the security analysis logic.
 */
export default function CodeInput({
  codeContent,
  fileName,
  onFileUpload,
  onAnalyzeCode,
  isAnalyzing
}: CodeInputProps) {
  return (
    <div className="bg-white rounded-lg border border-border shadow-sm p-6 flex flex-col">
      
      {/* Header row containing label + file upload controls */}
      <div className="flex items-center justify-between mb-4 flex-shrink-0">
        <label
          htmlFor="code-input"
          className="text-lg font-semibold text-foreground"
        >
          Code to analyze
        </label>

        {/* File upload + analyze button group */}
        <FileUpload
          fileName={fileName}
          onFileUpload={onFileUpload}
          onAnalyzeCode={onAnalyzeCode}
          isAnalyzing={isAnalyzing}
          hasCode={!!codeContent}   {/* enables the analysis button */}
        />
      </div>

      {/* Read-only code preview area */}
      <textarea
        id="code-input"
        value={codeContent}
        readOnly
        placeholder="Select a Python file to display its contents here..."
        className="flex-1 w-full resize-none border border-border rounded-lg p-4 font-mono text-sm bg-input-bg focus:outline-none focus:ring-2 focus:ring-primary/50"
      />
    </div>
  );
}
