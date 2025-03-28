// React Application File Indexer (ES Modules)
// Save this as 'collect-files.js' in your project root

import fs from 'fs';
import path from 'path';
import crypto from 'crypto';
import { fileURLToPath } from 'url';

// Get the directory name in ESM
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// Configuration
const CONFIG = {
  // Directories to scan (relative to script location)
  targetDirs: ['src', 'public'],
  
  // File extensions to include
  includeExtensions: [
    // React/JS files
    '.js', '.jsx', '.ts', '.tsx', 
    // Styles
    '.css', '.scss', '.sass', '.less',
    // Config files
    '.json', '.env',
    // Assets
    '.svg', '.png', '.jpg', '.jpeg', '.gif',
    // Other
    '.html', '.md'
  ],
  
  // Directories to exclude
  excludeDirs: [
    'node_modules',
    'build',
    'dist',
    '.git',
    'coverage'
  ],
  
  // Max file size to include (in bytes, default 1MB)
  maxFileSize: 1024 * 1024,
  
  // Output file name
  outputFileName: 'react-app-index.json'
};

// Hash function to create file identifiers
function createFileHash(filePath, fileSize) {
  return crypto
    .createHash('md5')
    .update(`${filePath}:${fileSize}`)
    .digest('hex')
    .substring(0, 8);
}

// Function to check if file should be included based on extension
function shouldIncludeFile(filePath) {
  const ext = path.extname(filePath).toLowerCase();
  return CONFIG.includeExtensions.includes(ext);
}

// Function to check if directory should be excluded
function shouldExcludeDir(dirPath) {
  const dirName = path.basename(dirPath);
  return CONFIG.excludeDirs.includes(dirName);
}

// Function to scan directory recursively
function scanDirectory(dir, baseDir, result = []) {
  try {
    const entries = fs.readdirSync(dir, { withFileTypes: true });
    
    for (const entry of entries) {
      const fullPath = path.join(dir, entry.name);
      const relativePath = path.relative(baseDir, fullPath);
      
      if (entry.isDirectory()) {
        if (!shouldExcludeDir(fullPath)) {
          scanDirectory(fullPath, baseDir, result);
        }
      } else if (entry.isFile()) {
        if (shouldIncludeFile(fullPath)) {
          try {
            const stats = fs.statSync(fullPath);
            
            if (stats.size <= CONFIG.maxFileSize) {
              const fileContent = fs.readFileSync(fullPath, 'utf8');
              const fileId = createFileHash(relativePath, stats.size);
              
              result.push({
                id: fileId,
                path: relativePath,
                size: stats.size,
                lastModified: stats.mtime,
                content: fileContent
              });
            } else {
              console.log(`Skipping large file: ${relativePath} (${Math.round(stats.size / 1024)}KB)`);
              
              // Still include metadata without content for large files
              const fileId = createFileHash(relativePath, stats.size);
              result.push({
                id: fileId,
                path: relativePath,
                size: stats.size,
                lastModified: stats.mtime,
                content: '[FILE TOO LARGE - CONTENT OMITTED]'
              });
            }
          } catch (err) {
            console.error(`Error reading file ${fullPath}: ${err.message}`);
          }
        }
      }
    }
  } catch (err) {
    console.error(`Error scanning directory ${dir}: ${err.message}`);
  }
  
  return result;
}

// Main function to index React application
function indexReactApplication() {
  const startTime = Date.now();
  console.log('Starting React application indexing...');
  
  // Get the base directory (where this script is run from)
  const baseDir = process.cwd();
  console.log(`Base directory: ${baseDir}`);
  
  let allFiles = [];
  
  // Scan each target directory
  for (const targetDir of CONFIG.targetDirs) {
    const dirPath = path.join(baseDir, targetDir);
    
    try {
      if (fs.existsSync(dirPath)) {
        console.log(`Scanning directory: ${targetDir}`);
        const files = scanDirectory(dirPath, baseDir);
        allFiles = allFiles.concat(files);
        console.log(`Found ${files.length} files in ${targetDir}`);
      } else {
        console.warn(`Directory not found: ${targetDir}`);
      }
    } catch (err) {
      console.error(`Error processing directory ${targetDir}: ${err.message}`);
    }
  }
  
  // Create index object
  const index = {
    metadata: {
      generatedAt: new Date().toISOString(),
      fileCount: allFiles.length,
      baseDirectory: baseDir,
      targetDirectories: CONFIG.targetDirs,
      includedExtensions: CONFIG.includeExtensions,
      excludedDirectories: CONFIG.excludeDirs
    },
    files: allFiles
  };
  
  // Write output file
  try {
    fs.writeFileSync(
      path.join(baseDir, CONFIG.outputFileName),
      JSON.stringify(index, null, 2)
    );
    console.log(`Index successfully written to ${CONFIG.outputFileName}`);
  } catch (err) {
    console.error(`Error writing index file: ${err.message}`);
  }
  
  const endTime = Date.now();
  console.log(`Indexing completed in ${(endTime - startTime) / 1000} seconds`);
  console.log(`Total files indexed: ${allFiles.length}`);
}

// Run the indexer
indexReactApplication();