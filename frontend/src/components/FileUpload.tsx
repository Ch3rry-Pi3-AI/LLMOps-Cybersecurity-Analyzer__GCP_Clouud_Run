import { FileUploadProps } from '@/types/security';

/**
 * FileUpload Component
 *
 * Allows the user to:
 * - select a Python file from their machine
 * - display the uploaded file's name
 * - trigger backend security analysis
 *
 * This component acts as the first step in the workflow:
 * it collects raw code, validates availability, and enables
 * the "Analyze" action when appropriate.
 */
export default function FileUpload({
  fileName,
  onFileUpload,
  onAnalyzeCode,
  isAnalyzing,
  hasCode
}: FileUploadProps) {
  return (
    <div className="flex items-center gap-4">
      
      {/* Display the uploaded file name as a badge, if present */}
      {fileName && (
        <span className="text-sm text-accent bg-secondary/20 px-3 py-1 rounded-full">
          {fileName}
        </span>
      )}

      {/* Hidden file input – styled trigger handled by the label below */}
      <input
        type="file"
        accept=".py"
        onChange={onFileUpload}
        className="hidden"
        id="file-upload"
      />

      {/* Visible button-like label used to open the file dialog */}
      <label
        htmlFor="file-upload"
        className="bg-primary hover:bg-primary/90 text-white px-4 py-2 rounded-lg cursor-pointer transition-colors font-medium"
      >
        Open python file...
      </label>

      {/* Analysis trigger button */}
      <button
        onClick={onAnalyzeCode}
        disabled={!hasCode || isAnalyzing}
        className="bg-accent hover:bg-accent/90 disabled:bg-gray-400 disabled:cursor-not-allowed text-white px-6 py-2 rounded-lg transition-colors font-medium"
      >
        {isAnalyzing ? 'Analyzing...' : 'Analyze code'}
      </button>
    </div>
  );
}
